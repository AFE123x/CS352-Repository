import sys  # for argument vector
import socket # for our lovely sockets

iteration = 1

def handle_rd(socket,domain_name):
    global iteration
    domain_name = f"0 {domain_name} {iteration} rd"
    iteration += 1
    socket.sendall(domain_name.encode())
    response = socket.recv(1024)
    print(f"{response.decode()}")

# # handle iterative responses
def handle_it(client_socket, domain_name):
    global iteration

    # Step 1: Send query to RS
    query = f"0 {domain_name} {iteration} it"
    iteration += 1
    client_socket.sendall(query.encode())

    # Step 2: Receive response from RS
    response = client_socket.recv(1024).decode().strip()
    print(response)
    response_data = response.split()

    # Step 3: If RS redirects to a TLD server (ns flag), follow the referral
    while response_data[-1] == "ns":
        next_server = response_data[2]  # Extract TLD server hostname

        # Create a new socket for the TLD server connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tld_socket:
            try:
                # Connect to the TLD server
                tld_socket.connect((next_server, int(sys.argv[2])))

                # Send the same query to the TLD server
                tld_socket.sendall(query.encode())

                # Receive the final response
                response = tld_socket.recv(1024).decode().strip()
                print(response)
                response_data = response.split()
            
            except Exception as e:
                print(f"Error connecting to {next_server}: {e}")
                return


# defines the main function
def main():
    if len(sys.argv) < 3:  # handle invalid arguments
        print("Usage: python3 client <host_name> <port_num>")
        exit(1)

    # Extract hostname and port number from command line arguments
    host_name = sys.argv[1]
    port_num = int(sys.argv[2])
    # Creates our sockets
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((host_name,port_num))
    try:
        with open('hostnames.txt', 'r') as file:
            for line in file:
                args = line.strip().split()
                if len(args) < 2:
                    print("Failed to read line (expected domain_name and type).")
                    continue
                domain_name = args[0]
                response_type = args[1]
                if response_type == "rd":
                    handle_rd(client_socket,domain_name)
                elif response_type == "it":
                    handle_it(client_socket,domain_name)
                else:
                    print(f"Unknown type '{response_type}' in line: {line.strip()}")
    finally:
        client_socket.close() # close our socket after going through all files

if __name__ == "__main__":
    main()

# ⣿⣿⣿⣿⣿⣿⡿⣡⢏⣾⣿⢃⣿⣿⣿⠏⣸⠇⢸⣿⣿⣿⣿⣿⣿⣿⡇⣾⣿⣿⣿⣿⢻⠽⣿⡡⢛⢻⣿⠘⣿⣟⢻⣿⣿⣧⢡⣀⣆⠡⡑⣄⢢⡙⣿⣿⣿⣿⣿⣿
# ⣿⡛⠿⠃⠾⠿⢡⢇⣾⣿⡏⣼⣿⣿⣿⣤⡿⣠⣾⣿⣿⡇⢸⣿⣿⣿⠇⣿⣿⣿⣿⡇⡇⣄⣿⣷⣼⢸⣿⡇⣿⣿⡘⣿⣿⣿⡆⢿⣿⣾⣿⡜⢆⢳⣌⢿⣿⣿⣿⣿
# ⣡⣶⣿⠯⣹⣷⣮⣜⢻⣿⢡⣿⣿⣿⣿⣿⠇⣿⣿⣿⣿⠇⣿⣿⣿⣿⢸⣿⣿⣿⣿⡇⣗⣿⣿⣿⣿⡌⣿⡇⢹⣿⡇⣿⣿⣿⣿⢸⣿⣿⣿⣿⡎⢆⢻⣦⠺⣿⣿⣿
# ⣿⣿⣷⣿⣿⣿⣷⣽⢸⡏⣼⣿⣿⣿⣿⣿⢰⣿⣿⣿⡟⠀⣿⣿⣿⡏⢸⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⡇⣿⡇⡘⣿⣧⢸⣿⣿⣿⡇⣿⣿⡙⣿⣿⡜⡎⣿⣦⢹⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⢘⢁⣿⣿⣿⣿⣿⣿⢸⣿⣏⡛⠇⢸⣿⣿⣿⢁⡌⣿⣿⣿⣿⣧⢹⣿⣿⣿⣿⡇⣿⡇⡇⣿⣿⠀⠟⣻⣿⡇⣿⣿⡇⣿⣿⢳⢱⠸⢾⣆⢻⣿
# ⣿⣿⣿⣿⣿⣿⣿⡟⣼⢸⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⢸⢰⣬⣍⡛⠸⠇⢿⣿⣿⣿⣿⢸⣿⣿⣿⣿⢃⠿⠁⠃⢩⣴⢰⢸⣿⣿⡇⣿⣿⣷⢸⣿⡆⠆⡇⡜⣿⡌⣿
# ⠄⣨⣍⡉⠭⢭⣍⢰⡆⣾⣿⣿⣿⣿⣿⣿⠸⣿⣿⡏⣼⡆⣿⣛⡃⣬⣤⠐⣲⣼⣿⣿⡄⢹⣿⣯⢁⢠⡄⣨⣥⢸⡟⣸⡆⣿⣿⡇⣿⣿⣿⠈⣿⡇⢰⢱⠠⣿⣷⣼
# ⣿⣟⣥⣾⣿⣷⢸⡎⠃⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⡇⠟⠃⠭⣁⡂⠭⢍⡃⢻⣿⣿⣿⣇⢸⣿⣿⠇⢊⠡⢒⣓⠐⠅⣛⣧⢻⣿⡇⣿⣿⡿⡆⣿⡇⡇⣸⢸⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣾⡇⢂⣿⣿⣿⣿⣿⣿⣿⢠⢹⠟⡀⠴⡒⠈⣩⡁⠙⠢⠈⣂⢻⣿⣿⣿⠸⣿⡿⠀⠀⠊⠉⢉⢈⠁⢦⡹⢸⣿⠀⢸⣿⡇⡇⣿⠇⣧⢻⠀⣿⣿⣿
# ⣿⣿⣿⣿⡿⠟⣹⡇⢸⣿⣿⣿⣿⣿⣿⣿⢸⠆⠜⡁⡎⠴⠁⠻⠇⣷⠘⣦⣽⣆⢻⣿⣿⡇⢻⣧⢀⡎⠜⠁⠀⠀⡆⢦⠱⠈⡏⢸⠸⣿⢃⢡⡿⢰⣿⠀⢸⣿⣿⣿
# ⣛⠿⠷⠿⢛⣋⣭⣾⢸⣿⣿⣿⣿⣿⣿⣿⢸⠸⠀⠇⠡⠖⠀⠈⠀⡒⠆⣿⣿⣿⣦⡙⣿⣿⡘⢡⣾⠁⠒⠀⠀⢐⠂⣸⡇⠁⢁⣿⡇⡟⣸⣾⢃⣿⣿⢠⢸⣿⣿⣿
# ⣿⣿⣿⡿⢸⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⡿⢸⣆⣹⣄⡆⢼⣦⣄⡠⣿⢀⣿⣿⣿⣿⡟⡨⠻⢷⠸⣿⡆⠿⣦⣐⢻⢀⣿⣧⡇⢸⣿⡇⢱⡿⠃⢸⣿⣿⣿⣷⣿⣿⣿
# ⣿⣿⣿⡇⣾⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⡇⣸⣿⣿⣿⣿⣦⣥⣿⣧⣥⣾⣿⣿⣿⡟⣀⣴⣿⣦⣅⣹⣿⣦⣭⣭⣵⣿⣿⣿⠃⣿⣿⡇⣿⣷⠀⢸⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣷⡅⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢸⠏⣹⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⠏⡀⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⢏⣼⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣶⡇⣿⣿⣿⡟⢸⣿⣿⣿⣿⣿⣿⡇⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣾⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⢃⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⡇⢸⢈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣟⣩⣙⣛⣛⣿⣛⣟⣿⣿⣿⣿⣿⣿⣿⡿⣣⡆⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⢸⣿⣿⣿⡇⡘⣿⡏⣿⣿⣿⣿⣿⠸⢸⡗⣨⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣡⢸⣿⡇⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⢿⢸⣿⣿⣿⢰⡇⣿⡏⣿⣿⣿⣿⣿⠀⠾⢃⣛⣩⡄⣝⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣥⢠⣿⣿⢸⣿⡇⣿⣿⣿⣿⣿⡿⡆⢸⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⡼⣸⣿⣿⡿⢸⡇⣿⣥⢹⣿⣿⣿⣿⠀⣆⢿⣿⣿⡇⣿⣿⣶⣬⣙⠻⢿⣿⣿⣿⣿⠿⢋⣥⣶⣶⠌⡘⢿⣿⢸⣿⡇⣿⣿⣿⣿⣿⡇⡇⢸⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⡃⣿⣿⣿⡇⣿⣷⢹⡇⠸⣿⣿⣿⣿⠈⣿⣷⣬⣝⣃⠻⠿⠿⣿⣿⣷⣦⣄⡉⠉⠀⡀⠞⣛⣩⣵⣾⡇⣼⣿⢸⣿⡇⣿⣿⣿⣿⢸⠇⡇⢸⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⠇⣿⣿⣿⢡⣿⣿⢸⣷⠀⢿⣿⣿⣿⠀⢹⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣭⣝⡻⠿⢋⣴⣿⣿⣿⣿⣿⢁⣿⣿⡄⣿⡇⣿⣿⣿⡇⣾⢸⡇⢸⣿⣿⣿⣿⣿⣿⣿
# ⣿⣷⢸⣿⣿⡏⣼⠿⠿⠌⣿⠘⠸⣿⣿⣿⡆⡂⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣿⣿⣿⣿⣿⣿⡏⠴⢶⣌⠃⠛⠃⣿⣿⣿⠃⡟⢸⡇⢸⣿⣿⣿⣿⣿⣿⣿
# ⣿⡟⣼⠟⢉⣠⣤⡶⠶⠆⢻⡄⠧⢹⣿⣿⡇⣿⣷⣍⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⡿⢰⣾⣦⡙⠿⠿⠇⣿⣿⡟⢠⡇⣦⣄⠺⣿⣿⣿⣿⣿⣿⣿
# ⣿⠇⢁⣴⡿⣫⣴⣾⣿⣿⠸⡇⣿⣇⢻⣿⡇⢿⣿⣧⡑⢦⣝⡻⢿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⠟⡹⢻⣿⣿⣿⣿⣿⢸⣿⡿⢰⢸⢰⣮⡙⢷⡈⢿⣿⢿⣿⣿⣿
# ⡟⢀⣾⢋⣼⣿⣿⣿⣿⣿⡇⠃⣿⣿⣆⢻⣧⢸⣿⣿⣿⣦⣝⠻⣷⣦⣍⣛⣻⣿⣿⡖⣿⣿⠟⣡⢊⢄⣼⣿⣿⣿⣿⣿⢸⡟⣱⣿⠈⣾⣿⣿⣦⡙⣄⢿⣿⣿⣿⣿
# ⢀⣾⢃⣾⣿⣿⣿⢹⣿⣿⣿⣄⣿⣿⣿⣆⠻⢸⣿⣿⣿⣿⣿⣷⣬⡛⢿⣿⣿⣿⣿⣷⢸⣶⣿⡃⣣⣾⣿⣿⣿⣿⣿⡇⢊⣴⣿⣇⣰⣿⣿⣿⡟⢳⡜⡌⢸⣿⣿⣿
# ⣾⢃⣾⣿⣿⣿⣿⡌⣿⣿⣿⣿⣿⣿⣿⣿⣧⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⡛⢿⣿⡇⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⡏⣿⣿⣿⡇⣿⣿⡜⡘⣿⣿⣿
# ⣯⣼⣿⢿⣿⣿⣿⣧⢹⣿⣿⡿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢹⣿⣿⡇⣿⣿⣷⡀⢹⣿⣿
# ⣿⣿⣿⡄⣿⣿⣿⣿⡈⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⡇⣿⣿⡿⣧⠀⢿⣿
# ⣿⣿⣿⣷⠸⣿⣿⣿⡇⢿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⢰⣿⡿⢰⣿⡆⠸⣿