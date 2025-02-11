import socket

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('Socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = socket.gethostbyname(host)
    print("[S]: Server IP address is {}".format(localhost_ip))

    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at {}".format(addr))

    # Receive data from the client
    data = csockid.recv(4096)  # Receive up to 4096 bytes
    msg = data.decode('utf-8')  # Decode to string

    # Reverse each line and inverse the case, then write to a file
    with open("out-proj.txt", "w", encoding="utf-8") as file:
        for line in msg.splitlines():
            reversed_line = line[::-1]  # Reverse the string
            reversed_and_case_inverted = reversed_line.swapcase()  # Inverse the case
            file.write(reversed_and_case_inverted + "\n")  # Write to output file
            print("[S]: Processed Line:", reversed_and_case_inverted)  # Print for verification

    print("[S]: Reversed and case-inverted content saved to 'out-proj.txt'")

    # Close the server socket
    csockid.close()
    ss.close()

if __name__ == "__main__":
    server()
