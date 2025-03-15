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
def handle_it(socket,domain_name):
    global iteration
    domain_name = f"0 {domain_name} {iteration} it"
    iteration += 1
    socket.sendall(domain_name.encode())
    response = socket.recv(1024)
    print(f"{response.decode()}")


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