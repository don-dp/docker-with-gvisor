import os

def execute_string_as_code():
    input_code = os.getenv('input_code')
    if not input_code:
        print("Error: No code provided.")
        return
    try:
        exec(input_code)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    execute_string_as_code()