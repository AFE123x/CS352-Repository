import socket
import sys

domain_map = {}
def write_response_to_file(response):
    with open('ts2response.txt', 'a') as file:
        file.write(response + "\n")
    

def main():
    with open('ts2response.txt', 'w') as file:
        pass  # This will create or clear the file
    global domain_app
    args = sys.argv
    print(len(args))
    if len(args) < 2:
        print("python3 ts2.py <port_num>")
        exit(1)

    # initialize the data structure to search for goods!
    with open('ts2database.txt', 'r') as file:
        # Now iterate through the rest of the lines
        for line in file:
            line = line.strip().split()
            if len(line) < 2:
                print("Failed to read line properly")
                continue
            domain_map[line[0]] = line[1]
            
    # initialize socket
    host_name = socket.gethostname() # get's the current host computer!
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create the TCP/IP Socket
    server_socket.bind((host_name,int(args[1]))) # Bind the host_name and port number
    
    # Keep the server running to accept connections continuously
    server_socket.listen(5)  # Allow up to 5 queued connections
    
    print(f"TS2 server started on {host_name}:{args[1]}")
    
    try:
        while True:
            # Accept a new connection
            connection, client_address = server_socket.accept()
            print(f"New connection from {client_address}")
            
            try:
                # Handle the connection
                while True:
                    data = connection.recv(1024)
                    if not data:
                        break
                    
                    str = data.decode().strip().split()
                    print(f"Received query: {str}")
                    
                    if str[1] in domain_map:
                        print(f" code is {str[3]}")
                        response = f"1 {str[1]} {domain_map[str[1]]} {str[2]} aa"
                        write_response_to_file(response)
                        connection.sendall(response.encode())
                    else:
                        response = f"1 {str[1]} 0.0.0.0 {str[2]} nx"
                        write_response_to_file(response)
                        connection.sendall(response.encode())
                        
            except Exception as e:
                print(f"Error handling connection: {e}")
            finally:
                # Close the connection but keep the server running
                print(f"Connection closed with {client_address}")
                connection.close()
                
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()

# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣩⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢩⣿⢫⣿⣿⣿⣿⣿⣏⢏⢿⣿⣿⡌⠻⣿⣿⣯⣹⣿⣿⣿⣿⣿⣯⡹⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⡿⢫⣤⣤⡐⢶⣮⣭⢛⣵⣿⣿⣿⣿⣿⣿⢹⣿⣿⣿⠿⠿⢿⣛⣛⣛⣛⣛⣃⣛⡋⠼⢿⣿⣿⣿⣿⣿⡌⡎⢿⣿⣿⡌⢎⠻⣿⣿⣯⡻⣿⣿⣿⣿⣷⡜⣿⣿⣿⣿
# ⣿⣿⣿⣿⡟⣴⣿⣿⠿⠿⡌⠟⣱⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣭⣙⠻⣿⣷⢸⡜⣿⣿⣿⡜⣷⡙⣿⣿⣿⣮⡻⣿⣿⣿⣿⡜⢿⣿⣿
# ⣿⣿⣿⡟⠼⣋⣵⣶⡿⢋⢄⡆⣧⣝⡻⠿⠿⣋⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣝⠎⣷⢸⣿⣿⣷⠸⣿⡈⢿⣿⣿⣷⣌⢿⣿⣿⣿⡌⢿⣿
# ⣿⣿⡿⣰⣾⣿⣿⡟⣱⢏⣾⣧⢻⣿⠟⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⠂⣿⣿⣿⡇⣿⡇⢊⢿⣿⣿⣿⣧⡹⣿⣿⣿⡜⣿
# ⣿⣿⢣⣿⣿⣿⡟⣰⡏⢸⣿⣿⡮⣣⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣻⣭⣭⣭⣭⣽⣛⡻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣝⢿⣿⣷⢹⡇⡸⡎⢿⣿⣿⣿⣷⡙⣿⣿⣷⣿
# ⣿⡟⣼⣿⣿⣿⢡⣿⠀⣾⣿⡟⣱⣿⣿⣿⣿⣿⣿⣿⡿⢻⣿⣿⣿⣿⣿⣿⣻⣿⣿⣛⣛⠿⢷⣮⣝⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡻⣿⢸⡇⡇⣿⡘⣿⣿⣿⣿⣷⡘⠿⣋⣵
# ⣿⣷⣿⣿⣿⡇⣾⡇⡇⣿⠏⣼⣿⣿⣿⣿⣿⣿⢋⣴⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣝⡻⣮⡻⣿⣿⣿⡙⣿⣿⣿⣿⣿⣿⣿⡌⢳⣿⢸⣿⡈⢟⣵⣾⣿⠟⢫⢰⢣
# ⣿⣿⣿⣿⣿⢸⣿⢱⡇⡟⣼⣿⣿⣿⣿⣿⡿⢡⣿⡟⣩⣾⣿⡛⢿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡹⣿⢸⡇⡇⣿⡘⣿⣿⣿⣿⣷⡘⠿⣋⣵
# ⣿⣿⣿⣿⡇⣿⣿⢸⡇⢱⣿⣿⣿⣿⣿⡿⢱⣿⢋⣾⣿⣿⣿⣿⡆⡙⢷⣙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡻⣿⢸⡇⡇⣿⡘⣿⣿⣿⣿⣷⡘⠿⣋⣵
# ⣿⣿⣿⣿⢸⣿⣿⢸⢇⣿⣿⣿⣿⣿⣿⢡⣿⢣⣾⣿⣿⣿⣿⣿⡇⢹⣤⣙⢷⣝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⢳⣿⢸⣿⡈⢟⣵⣾⣿⠟⢫⢰⢣
# ⣿⣿⣿⣿⡇⣿⣿⢸⢇⣿⣿⣿⣿⣿⣿⢡⣿⢣⣾⣿⣿⣿⣿⣿⡇⢹⣤⣙⢷⣝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⢳⣿⢸⣿⡈⢟⣵⣾⣿⠟⢫⢰⢣
# ⣿⣿⣿⣿⡇⣿⣿⢸⢇⣿⣿⣿⣿⣿⣿⢡⣿⢣⣾⣿⣿⣿⣿⣿⡇⢹⣤⣙⢷⣝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⢳⣿⢸⣿⡈⢟⣵⣾⣿⠟⢫⢰⢣
# ⣿⣿⣿⣿⡇⣿⣿⢸⢇⣿⣿⣿⣿⣿⣿⢡⣿⢣⣾⣿⣿⣿⣿⣿⡇⢹⣤⣙⢷⣝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⢳⣿⢸⣿⡈⢟⣵⣾⣿⠟⢫⢰⢣
# ⣿⣿⣿⣿⡇⣿⣿⢸⢇⣿⣿⣿⣿⣿⣿⢡⣿⢣⣾⣿⣿⣿⣿⣿⡇⢹⣤⣙⢷⣝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⢳⣿⢸⣿⡈⢟⣵⣾⣿⠟⢫⢰⢣
# ⣿⣿⣿⣿⡇⣿⣿⢸⢇⣿⣿⣿⣿⣿⣿⢡⣿⢣⣾⣿⣿⣿⣿⣿⡇⢹⣤⣙⢷⣝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⢳⣿⢸⣿⡈⢟⣵⣾⣿⠟⢫⢰⢣
# ⣿⣿⣿⣿⡇⣿⣿⢸⢇⣿⣿⣿⣿⣿⣿⢡⣿⢣⣾⣿⣿⣿⣿⣿⡇⢹⣤⣙⢷⣝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⢳⣿⢸⣿⡈⢟⣵⣾⣿⠟⢫⢰⢣
# ⣿⣿⣿⣿⡇⣿⣿⢸⢇⣿⣿⣿⣿⣿⣿⢡⣿⢣⣾⣿⣿⣿⣿⣿⡇⢹⣤⣙⢷⣝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⢳⣿⢸⣿⡈⢟⣵⣾⣿⠟⢫⢰⢣
# ⣿⣿⣿⣿⡇⣿⣿⢸⢇⣿⣿⣿⣿⣿⣿⢡⣿⢣⣾⣿⣿⣿⣿⣿⡇⢹⣤⣙⢷⣝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⢳⣿⢸⣿⡈⢟⣵⣾⣿⠟⢫⢰⢣
# ⣿⣿⣿⣿⡇⣿⣿⢸⢇⣿⣿⣿⣿⣿⣿⢡⣿⢣⣾⣿⣿⣿⣿⣿⡇⢹⣤⣙⢷⣝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⢳⣿⢸⣿⡈⢟⣵⣾⣿⠟⢫⢰⢣
# ⣿⣿⣿⣿⡇⣿⣿⢸⢇⣿⣿⣿⣿⣿⣿⢡⣿⢣⣾⣿⣿⣿⣿⣿