import socket

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('Socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # Connect to the server on the local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    # Read entire file into memory and send it
    with open("in-proj.txt", "rb") as file:  # Read as bytes (binary mode)
        file_data = file.read()  # Read the whole file into a buffer
        cs.sendall(file_data)  # Send the entire buffer at once

    # Receive response from server
    data_from_server = cs.recv(1024)
    print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

    # Close the client socket
    cs.close()

if __name__ == "__main__":
    client()
