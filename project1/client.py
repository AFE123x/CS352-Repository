import socket

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)
    with open("in-proj.txt","r") as file:
        for line in file:
            cs.send(line.encode('utf-8'))
            data_from_server=cs.recv(2000)
            print(f"[C]: Data received from server: {data_from_server.strip().decode('utf-8')}")
    # Receive data from the server

    # close the client socket
    cs.close()
    exit()

if __name__ == "__main__":
    client()
