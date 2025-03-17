import socket
import sys

domain_map = {}

ts1_server = []
ts2_server = []

# Function to handle the writing of the response to the file
def write_response_to_file(response):
    with open('rsresponse.txt', 'a') as file:
        file.write(response + "\n")

def recursive_connection(host_name, port_num, client_socket, str):
    # 0 DomainName identification flags
    # ['0', 'www.google.com', '1', 'rd']
    recursive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recursive_socket.connect((host_name, port_num))
    try:
        inquiry = f"{str[0]} {str[1]} {str[2]} {str[3]}"
        recursive_socket.sendall(inquiry.encode())
        data = recursive_socket.recv(1024)
        response = data.decode()
        array = response.split()
        print(array)
        if array[4] == "aa":
            data = f"{array[0]} {array[1]} {array[2]} {array[3]} ra"
            write_response_to_file(data)
            client_socket.sendall(data.encode())
        else:
            data = f"{array[0]} {array[1]} {array[2]} {array[3]} nx"
            write_response_to_file(data)
            client_socket.sendall(data.encode())
        # Write response to the file
        # write_response_to_file(response)
        
        # # Send the response to the client
        # client_socket.sendall(data)
    finally:
        recursive_socket.close()

def handle_rd(connection, str, port):
    global domain_map
    global ts1_server
    global ts2_server

    # Read the domain, and check if it's in the dictionary
    if str[1] not in domain_map:
        tld = str[1].split('.')[-1]
        if tld == ts1_server[0]:
            recursive_connection(ts1_server[1], port, connection, str)
        elif tld == ts2_server[0]:
            recursive_connection(ts2_server[1], port, connection, str)
        else:
            response = f"1 {str[1]} 0.0.0.0 {str[2]} nx"
            # Write response to the file
            write_response_to_file(response)
            connection.sendall(response.encode())
    else:
        response = f"1 {str[1]} {domain_map[str[1]]} {str[2]} aa"
        # Write response to the file
        write_response_to_file(response)
        connection.sendall(response.encode())

def handle_it(connection, str):
    global domain_map
    global ts1_server
    global ts2_server

    # Read the domain, and check if it's in the dictionary
    if str[1] not in domain_map:
        tld = str[1].split('.')[-1]
        if tld == ts1_server[0]:
            response = f"1 {str[1]} {ts1_server[1]} {str[2]} ns"
            # Write response to the file
            write_response_to_file(response)
            connection.sendall(response.encode())
        elif tld == ts2_server[0]:
            response = f"1 {str[1]} {ts2_server[1]} {str[2]} ns"
            # Write response to the file
            write_response_to_file(response)
            connection.sendall(response.encode())
        else:
            response = f"1 {str[1]} 0.0.0.0 {str[2]} nx"
            # Write response to the file
            write_response_to_file(response)
            connection.sendall(response.encode())
    else:
        response = f"1 {str[1]} {domain_map[str[1]]} {str[2]} aa"
        # Write response to the file
        write_response_to_file(response)
        connection.sendall(response.encode())

def main():
    with open('rsresponse.txt', 'w') as file:
        pass  # This will create or clear the file
    global ts1_server
    global ts2_server
    global domain_map
    args = sys.argv
    if len(args) < 2:
        print("python3 rs.py <port_num>")
        exit(1)

    # Initialize the data structure to search for goods!
    with open('rsdatabase.txt', 'r') as file:
        # Read the first two lines separately
        ts1_server = file.readline().strip().split()  # server and top hierarchy thing for ts1 server
        ts2_server = file.readline().strip().split()  # server and top hierarchy thing for ts2 server
        # Now iterate through the rest of the lines
        for line in file:
            line = line.strip().split()
            if len(line) < 2:
                print("Failed to read line properly")
                continue
            domain_map[line[0]] = line[1]

    # Initialize socket
    host_name = socket.gethostname()  # Get the current host computer!
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create the TCP/IP Socket
    server_socket.bind((host_name, int(args[1])))  # Bind the host_name and port number
    server_socket.listen(1)  # We want to wait for one connection
    connection, client_address = server_socket.accept()  # Wait for the connection

    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            str = data.decode()
            str = str.strip().split()  # Split our string into an array
            
            if str[3] == "rd":
                handle_rd(connection, str, int(args[1]))
            elif str[3] == "it":
                handle_it(connection, str)
            else:
                response = "error occurred!"
                # Write response to the file
                write_response_to_file(response)
                connection.sendall(response.encode())
                continue
    finally:
        connection.close()

if __name__ == "__main__":
    main()
