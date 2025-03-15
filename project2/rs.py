import socket
import sys

domain_map = {}

ts1_server = []
ts2_server = []


def handle_rd(connection,str):
    # connection.sendall(response.encode())
    global domain_map
    global ts1_server
    global ts2_server

    # read the domain, and check if it's in the dictionary
    if str[1] not in domain_map:
        tld = str[1].split('.')[-1]
        if tld == ts1_server[0]:
            response = f"1 {str[1]} {ts1_server[1]} {str[2]} ns"
            connection.sendall(response.encode())
        elif tld == ts2_server[0]:
            response = f"1 {str[1]} {ts2_server[1]} {str[2]} ns"
            connection.sendall(response.encode())
        else:
            response = f"1 {str[1]} 0.0.0.0 {str[2]} nx"
            connection.sendall(response.encode())
    else:
        response = f"1 {str[1]} {domain_map[str[1]]} {str[2]} aa"
        connection.sendall(response.encode())

def handle_it(connection,str):
    # connection.sendall(response.encode())
    global domain_map
    global ts1_server
    global ts2_server

    # read the domain, and check if it's in the dictionary
    if str[1] not in domain_map:
        tld = str[1].split('.')[-1]
        if tld == ts1_server[0]:
            response = f"1 {str[1]} {ts1_server[1]} {str[2]} ns"
            print("it's com")
            connection.sendall(response.encode())
        elif tld == ts2_server[0]:
            print("it's edu")
            # 0 www.google.com 5 rd
            # 1 njit.edu cheese.cs.rutgers.edu 16 ns
            response = f"1 {str[1]} {ts2_server[1]} {str[2]} ns"
            connection.sendall(response.encode())
        else:
            response = f"1 {str[1]} 0.0.0.0 {str[2]} nx"
            connection.sendall(response.encode())
    else:
        # 0 www.google.com 5 rd
        # 1 DomainName IPAddress identification flags
        response = f"1 {str[1]} {domain_map[str[1]]} {str[2]} aa"
        connection.sendall(response.encode())
def main():
    global ts1_server
    global ts2_server
    global domain_app
    args = sys.argv
    print(len(args))
    if len(args) < 2:
        print("python3 rs.py <port_num>")
        exit(1)


    # initialize the data structure to search for goods!
    with open('rsdatabase.txt', 'r') as file:
        # Read the first two lines separately
        ts1_server = file.readline().strip().split() # server and top heirchachy thing for ts1 server
        ts2_server = file.readline().strip().split() # server and top heirchachy thing for ts2 server
        print(ts1_server)
        print(ts2_server)
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
    server_socket.listen(1) # we want to wait for one connection
    connection, client_address = server_socket.accept() # Wait for the connection

    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            str = data.decode()
            # We can parse the data, and find it in a cool data structure
            # 0 www.google.com 5 rd

            str = str.strip().split() # sprlit our string into an array
            if str[3] == "rd":
                handle_rd(connection,str)
            elif str[3] == "it":
                handle_it(connection,str)
            else:
                response = f"error occured!"
                connection.sendall(response.encode())
                continue
            # aoeu = "aoeu"
            # connection.sendall(aoeu.encode())
    finally:
        connection.close()

if __name__ == "__main__":
    main()

# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣩⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢩⣿⢫⣿⣿⣿⣿⣿⣏⢏⢿⣿⣿⡌⠻⣿⣿⣯⣹⣿⣿⣿⣿⣿⣯⡹⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⡿⢫⣤⣤⡐⢶⣮⣭⢛⣵⣿⣿⣿⣿⣿⣿⢹⣿⣿⣿⠿⠿⢿⣛⣛⣛⣛⣛⣃⣛⡋⠼⢿⣿⣿⣿⣿⣿⡌⡎⢿⣿⣿⡌⢎⠻⣿⣿⣯⡻⣿⣿⣿⣿⣷⡜⣿⣿⣿⣿
# ⣿⣿⣿⣿⡟⣴⣿⣿⠿⠿⡌⠟⣱⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣭⣙⠻⣿⣷⢸⡜⣿⣿⣿⡜⣷⡙⣿⣿⣿⣮⡻⣿⣿⣿⣿⡜⢿⣿⣿
# ⣿⣿⣿⡟⠼⣋⣵⣶⡿⢋⢄⡆⣧⣝⡻⠿⠿⣋⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣝⠎⣷⢸⣿⣿⣷⠸⣿⡈⢿⣿⣿⣷⣌⢿⣿⣿⣿⡌⢿⣿
# ⣿⣿⡿⣰⣾⣿⣿⡟⣱⢏⣾⣧⢻⣿⠟⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⠂⣿⣿⣿⡇⣿⡇⢊⢿⣿⣿⣿⣧⡹⣿⣿⣿⡜⣿
# ⣿⣿⢣⣿⣿⣿⡟⣰⡏⢸⣿⣿⡮⣣⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣻⣭⣭⣭⣭⣽⣛⡻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣝⢿⣿⣷⢹⡇⡸⡎⢿⣿⣿⣿⣷⡙⣿⣿⣷⣿
# ⣿⡟⣼⣿⣿⣿⢡⣿⠀⣾⣿⡟⣱⣿⣿⣿⣿⣿⣿⡿⢻⣿⣿⣿⣿⣿⣿⣻⣿⣿⣛⣛⠿⢷⣮⣝⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡻⣿⢸⡇⡇⣿⡘⣿⣿⣿⣿⣷⡘⠿⣋⣵
# ⣿⣷⣿⣿⣿⡇⣾⡇⡇⣿⠏⣼⣿⣿⣿⣿⣿⣿⢋⣴⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣝⡻⣮⡻⣿⣿⣿⡙⣿⣿⣿⣿⣿⣿⣷⡙⢸⡇⣧⢻⣧⢹⣿⣿⠿⣋⣵⣾⡿⢏
# ⣿⣿⣿⣿⣿⢸⣿⢱⡇⡟⣼⣿⣿⣿⣿⣿⡿⢡⣿⡟⣩⣾⣿⡛⢿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣝⠊⠻⣿⣿⣌⢿⣿⣿⣿⣿⣿⣿⡌⢳⣿⢸⣿⡈⢟⣵⣾⣿⠟⢫⢰⢣
# ⣿⣿⣿⣿⡇⣿⣿⢸⡇⢱⣿⣿⣿⣿⣿⡿⢱⣿⢋⣾⣿⣿⣿⣿⡆⡙⢷⣙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡘⠻⣿⣆⢻⣿⣿⣿⣿⣿⣿⡄⠟⠼⢋⣴⣿⠟⣫⣵⣿⢸⡖⣡
# ⣿⣿⣿⣿⢰⣿⣿⢸⢇⣿⣿⣿⣿⣿⣿⢡⣿⢣⣾⣿⣿⣿⣿⣿⡇⢹⣤⣙⢷⣝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡹⣿⣧⢻⣿⣿⣿⣿⣿⣿⡄⢵⣿⠟⣵⣾⣿⣿⢣⡏⢸⣿
# ⣿⣿⣿⡟⣼⣿⣿⠸⣸⣿⣿⣿⣿⣿⡏⣾⢇⣾⣿⣿⣿⣿⣿⣿⡇⣾⣿⣿⣷⣬⣓⢮⣛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡜⣿⣆⢿⣿⣿⣿⣿⡟⢿⡜⢣⣾⣿⣿⣿⡏⡎⣼⡇⣿
# ⣿⣿⣿⡇⣿⣿⣿⡆⡟⣿⣿⣿⣿⣿⡇⡟⣼⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣷⣮⣍⣒⠍⢋⡩⠭⢹⣿⣿⣿⣿⣿⡘⣿⡌⣿⣿⣿⣿⣿⡘⣷⢹⣿⣿⣿⡟⡸⣸⣿⣇⣿
# ⣿⣿⣿⢱⣿⣿⣿⢱⡇⣿⣿⣿⣿⣿⡀⢣⣿⣿⣿⣿⣿⣿⢿⣿⢡⣿⣿⣿⣿⣿⣿⣿⣿⣿⢣⣿⡶⢞⣡⣤⡒⠒⠚⣛⣛⣥⢹⣷⠙⣹⣿⣿⣿⣇⣿⡌⣿⣿⣿⢡⢡⣿⣿⣿⣿
# ⣿⣿⣿⢸⣿⣿⡏⢸⡇⣿⣿⣿⣿⣿⡇⣸⣿⣿⣿⣿⣿⡟⢰⠇⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣴⣶⣶⠟⣩⣴⣾⡿⠛⠛⠙⠫⠌⢁⡌⣿⣿⣿⣿⣿⢸⡇⠿⢟⣵⠃⡇⣿⣿⣿⣿
# ⣿⣿⣿⢸⣿⣿⡇⢸⡇⣿⣿⣿⣿⣿⣇⢿⣿⣿⣿⣿⡿⢑⠊⣬⡟⢛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢢⡿⠋⠐⠀⢀⠤⠀⠀⠄⢻⡇⣿⣿⣿⣿⡿⢸⣇⣜⠻⢣⣾⡇⣿⣿⣿⣿
# ⣿⣿⣿⢸⣿⣿⢸⣸⡇⣿⣿⣿⣿⣿⣿⠸⣿⣿⣿⡋⠎⠈⠾⡛⠵⠿⢿⣦⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⠗⢀⣾⡀⠻⢀⣠⠇⢤⢸⢱⣿⣿⣿⣿⡇⠊⡯⠋⣴⣿⣿⣷⣿⣿⣿⣿
# ⣐⠶⣿⣬⣭⣭⣼⡃⣇⢻⣿⣿⣿⣿⣿⣇⢿⣿⡿⠃⣰⢟⣡⣾⣿⣷⣦⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣼⣿⣿⣯⠍⢁⣰⣿⠘⡜⣿⣿⣿⣿⢱⠀⠃⡇⢹⣿⣿⣿⣿⣿⣿⣿
# ⣜⡳⢄⠲⠎⣭⢟⡃⣿⢸⣿⣿⣿⣿⣿⣿⡘⢟⣥⣾⣧⡾⠛⠉⠉⠉⠉⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢠⡇⣿⣿⣿⡏⡆⢣⠀⠀⡜⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣶⡍⠻⢿⡜⢷⢸⡆⣿⣿⣿⣿⣿⡝⣧⢻⡻⠿⠟⠁⣠⡆⠰⢷⠀⢀⠀⣍⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⣿⡇⣿⣿⡟⡼⢰⢸⢀⠆⡇⢿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⡇⠞⣶⢉⠲⡌⣿⠸⣿⣿⣿⣿⣷⠹⣄⠻⣿⣶⣦⡙⠿⣶⣆⣘⠛⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣾⣿⡇⣿⠟⣼⢡⢸⢸⣿⢠⢡⣾⣿⣿⣿⣿⡿⣿
# ⣿⣿⣿⣿⢀⣿⢸⣿⣆⢻⡇⢻⣿⣿⣿⣿⣧⢻⡜⣌⠻⣿⣿⣿⣴⣥⣦⣶⣾⣿⣿⣿⣿⠟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⡇⢏⣾⢣⣾⢨⡇⣿⡆⣼⣿⣼⣿⣿⣿⣇⣿
# ⣿⣿⣿⣿⡘⢸⣼⣿⣿⡌⣷⢀⢿⣿⣿⣿⣿⣧⠹⡌⢳⠝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡐⠃⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣣⡾⢡⣿⡏⣼⠃⣿⡇⣿⣿⣿⣿⣿⣿⢸⣿
# ⣿⣿⣿⣿⡇⡞⣿⣿⣿⣷⡘⡎⡎⢿⣿⣿⣿⣿⡆⡔⠔⢾⣮⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣼⣿⣿⣿⣿⣿⡿⢁⣾⣿⢣⡟⡄⣿⡇⣿⣟⣿⣿⣿⡟⣼⣿
# ⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣷⠱⡀⣦⠻⣿⣿⣿⣷⠀⡐⣌⠻⣷⣌⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣯⣵⣾⣿⣿⣿⣿⣿⣿⢏⣴⣿⣿⠃⡚⣰⢇⣿⢱⢻⣿⣿⣿⣿⢇⣿⣿
# ⣿⣿⣿⣿⣿⡌⣿⣿⣿⣿⣿⡇⡡⠡⢡⡌⢿⣇⢻⣤⢳⠙⣰⣈⣻⣿⣮⣛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣡⣿⣿⠟⢁⢀⣴⡿⢸⡿⡘⣼⣿⣿⣿⣿⢸⣿⣿
# ⣿⣿⣿⣿⣿⣇⢻⣿⣿⣿⣿⡇⡇⠀⠙⠡⣰⣝⠎⡿⡘⡆⣿⣿⣿⣿⣿⣿⣷⣶⣭⣭⣟⣛⣛⡿⠿⠿⠿⣿⣿⣿⡿⢟⣡⣾⡿⠟⠁⠀⡁⢿⣿⣧⣿⡇⢣⣿⣿⣿⣿⣧⣿⢇⣿
# ⣿⣿⣿⣿⣿⣿⡸⣿⣿⣿⣿⡇⡇⣀⢔⣴⣿⣿⣷⢠⣷⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡀⠀⡀⠀⣐⣚⣛⣭⠱⢀⡀⢀⣌⢿⣮⠻⣿⣿⠰⣼⣿⣿⣿⣿⣿⡟⣼⣿
# ⣿⣿⣿⣿⣿⣿⡇⢿⣿⣿⣿⡇⢷⣶⣿⣿⣿⣿⣿⣸⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡆⣲⡆⣶⡆⣿⣿⡿⠌⢻⣦⡻⣷⡝⠏⢄⣿⣿⣿⣿⣿⣿⢡⣿⣿
# ⣿⣿⣿⣿⣿⣿⣧⠸⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣌⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⡇⣿⠇⣱⣶⣬⣝⡣⠹⣷⡜⢿⡆⣸⣿⣿⣿⣿⣿⡟⣼⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⢀⢻⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣷⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢼⡇⢋⡄⣿⠿⠟⠛⠉⠁⠘⢿⣮⢃⣿⣿⣿⣿⣿⣿⢇⣿⣿⣿
# ⣿⣿⢹⣿⣿⣿⣿⡇⡜⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠘⣠⢸⡇⠠⡀⢀⣀⣀⣀⣤⠈⠻⢸⣿⣿⣿⣿⣿⣿⢸⣿⢋⣿
# ⣿⣿⡎⣿⣿⣿⣿⣷⢱⢹⣿⣿⢈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⢸⡇⢸⣿⣿⠿⢟⣛⣩⣤⣥⢸⣿⡟⣿⣿⣿⡟⣼⡏⣼⣿