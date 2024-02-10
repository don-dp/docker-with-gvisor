import websocket
import json
import docker
from docker.types import Ulimit

def is_docker_image_available(images, image_name, tag='latest'):
    for image in images:
        for t in image.tags:
            if "{}:{}".format(image_name, tag) in t:
                return True
    return False

def send_message(json_message, session_id, token):
    #print(f"JSON Message: {str(json_message)}\nSession ID: {session_id}\nToken: {token}")
    ws = websocket.WebSocket()
    try:
        ws.connect(f"wss://apiforllm.com/wsapi/sendresult/{session_id}?token={token}")
        ws.send(json.dumps(json_message))
    except Exception as e:
        print("Websocket error occurred.")
    finally:
        ws.close()

def run_container_logic(data):
    container = None
    response = {}

    try:
        docker_image = data.get('docker_image')
        client = docker.from_env()
        if not is_docker_image_available(client.images.list(), docker_image):
            raise Exception("Docker image not available")
        
        arguments = data.get('arguments')
        runtime = "runsc" if data.get('network', False) else "runsc-no-network"

        ulimits = [
            Ulimit(name='nofile', soft=90, hard=100),
            Ulimit(name='nproc', soft=90, hard=100)
        ]

        MAX_OUTPUT_SIZE = 10000

        container = client.containers.run(
            docker_image,
            environment=arguments,
            remove=True,
            runtime=runtime,
            mem_limit='300m',
            ulimits=ulimits,
            cap_drop=["MKNOD", "NET_RAW", "NET_BIND_SERVICE"],
            cpu_period=100000,
            cpu_quota=50000,
            detach=True,
        )
        output = ''
        for chunk in container.logs(stream=True):
            output += chunk.decode('utf-8')
            if len(output) > MAX_OUTPUT_SIZE:
                break
        if container:
            container.stop()
        response =  {'output': output.strip()}
    except Exception as e:
        if container:
            container.stop()
        response = {'error': "Function call failed."}
    
    return response