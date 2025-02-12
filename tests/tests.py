import threading
import time
import random
import subprocess
import socket

import socket
import time

def wait_for_port(port, host='localhost', check_interval=1):
    """Wait for a port to become available."""
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((host, port)) != 0:
                return
        time.sleep(check_interval)

def server(output_file, port=50007):
    wait_for_port(port)

    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of port
        print("[S]: Server socket created")
    except socket.error as err:
        print(f"Socket open error: {err}\n")
        exit()

    while True:  # Retry binding until it succeeds
        try:
            ss.bind(('', port))
            break  # If binding succeeds, exit the loop
        except socket.error as err:
            print(f"[S]: Port {port} is in use, retrying in 1 second...")
            time.sleep(1)

    ss.listen(1)
    print(f"[S]: Server listening on port {port}")

    csockid, addr = ss.accept()
    print(f"[S]: Got a connection request from a client at {addr}")

    # Receive data from the client
    data = csockid.recv(4096)
    msg = data.decode('utf-8')

    # Reverse each line and invert the case, then write to a file
    with open(output_file, "w", encoding="utf-8") as file:
        for line in msg.splitlines():
            reversed_line = line[::-1]
            reversed_and_case_inverted = reversed_line.swapcase()
            file.write(reversed_and_case_inverted + "\n")
            print("[S]: Processed Line:", reversed_and_case_inverted)

    print(f"[S]: Processed content saved to {output_file}")

    # Send acknowledgment to client
    csockid.sendall(b"Received file data successfully")

    csockid.close()
    ss.close()



def client(input_file):
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('Socket open error: {} \n'.format(err))
        exit()
        
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # Retry connection until the server is ready
    while True:
        try:
            cs.connect((localhost_addr, port))
            break
        except ConnectionRefusedError:
            print("[C]: Connection refused, retrying...")
            time.sleep(0.5)

    # Read and send file
    with open(input_file, "rb") as file:
        file_data = file.read()
        cs.sendall(file_data)

    # Receive server confirmation
    data_from_server = cs.recv(1024)
    print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

    cs.close()

def test_server(test_num,input_file, output_file, expected_file):
    t1 = threading.Thread(name='server', target=server, args=(output_file,))
    t2 = threading.Thread(name='client', target=client, args=(input_file,))

    t1.start()
    time.sleep(1)  # Allow server to start
    t2.start()

    t1.join()
    t2.join()

    # Compare output with expected file
    diff = subprocess.run(['diff', output_file, expected_file], capture_output=True)
    if diff.returncode != 0:
        print(f"Test {test_num} failed: {output_file} differs from {expected_file}")
        print(diff.stdout.decode())  # Print diff output
    else:
        print(f"Test {test_num} passed: {output_file} matches {expected_file}")

if __name__ == "__main__":
    test_server(1,"test1.txt", "test1o.txt", "test1.out")
    test_server(2,"in-proj.txt", "out-proj.txt", "out-proj.out")
