# Docker with gVisor

This project is a Flask-based web service for executing Docker-contained tasks, secured with session IDs and tokens and offering both synchronous and asynchronous operations. It employs Celery with Redis for task queue management and Docker integrated with gVisor for enhanced isolation in task execution, ensuring both resource and network control. Results are efficiently communicated in real-time through WebSockets. The configuration is tailored for secure, scalable execution, particularly aimed at facilitating function calls for locally running Language Learning Models (LLMs) with gVisor providing an additional layer of security through isolation.

The cloud-init script automates the setup of a new Ubuntu server with Docker and gVisor installed, configured for enhanced security with user namespaces and optional network isolation. It also prepares the system with essential packages, configures firewall rules for SSH, and adds a user with sudo privileges and Docker group membership for immediate deployment readiness.

Run the cloud-init script and reboot the server.

To check the cloud-init logs:

`sudo cat /var/log/cloud-init-output.log`

`sudo cat /var/log/cloud-init.log`

## Setup

`git clone https://github.com/don-dp/docker-with-gvisor.git`

`cd docker-with-gvisor/`

Update `test1.mydomain.com` in the Caddyfile with your actual domain.

`sudo ufw allow from [your-ip-address] to any port 80`

`sudo ufw allow from [your-ip-address] to any port 443`

Set up an A record in your DNS provider's dashboard for your domain, and allow some time for the DNS changes to propagate

`docker compose up -d`

Visit the `/hello` endpoint to verify that the deployment was successful.

Build the demo docker image `fetch_web_page` by changing directory into the folder of the same name and then running the following command:

`docker build -t fetch_web_page .`

The purpose of the demo function: fetches and prints the plain text content of a webpage specified by the url passed in, ensuring the URL is valid and the content size does not exceed 1 MB.

Sample `curl` command:

`curl -X POST \
-H "Content-Type: application/json" \
-H "Authorization: your_random_token_here" \
-d '{"docker_image":"fetch_web_page", "arguments":{"url":"https://example.com"}, "network": true}' \
https://test1.mydomain.com/runfunction_sync/37`

Output:

`{"output":"Example Domain Example Domain This domain is for use in illustrative examples in documents. You may use this\n    domain in literature without prior coordination or asking for permission. More information..."}`

This framework enables secure execution of untrusted code submissions for coding platforms or the safe processing of potentially malicious files within isolated environments, ensuring the integrity of the host system while facilitating diverse language learning model applications.
