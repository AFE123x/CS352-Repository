import threading
import time
import random
import subprocess
import socket

import socket
import time

import socket
import time
def is_port_in_use(port_num):
    """
    Check if a port is in use by attempting to bind to it.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port_num))
            return False  # Port is not in use
        except OSError:
            return True  # Port is in use

def wait_for_port(port_num, timeout=30, interval=1):
    """
    Wait until a port is no longer in use.
    
    :param port_num: The port number to check.
    :param timeout: Maximum time to wait (in seconds).
    :param interval: Time to wait between checks (in seconds).
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if not is_port_in_use(port_num):
            return True
        print(f"Port {port_num} is still in use. Waiting...")
        time.sleep(interval)
    print(f"Timeout: Port {port_num} is still in use after {timeout} seconds.")
    return False

def server():
    wait_for_port(50007)
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))
    with open("out-proj.txt","w") as output:
        while True:
            data_from_client = csockid.recv(2000)
            if not data_from_client:
                break
            string_to_rev = data_from_client.decode('utf-8')
            string_to_rev = string_to_rev.strip('\n')
            string_to_rev = string_to_rev[::-1]
            string_to_rev = string_to_rev.swapcase()
            output.write(f"{string_to_rev}\n") 
            csockid.send(string_to_rev.encode('utf-8'))

    msg = "Welcome to CS 352!"

    # Close the server socket
    ss.close()
    exit()



def client(input_file,output_file):
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)
    with open(input_file,"r") as file:
        with open(output_file,"w") as output:
            for line in file:
                cs.send(line.encode('utf-8'))
                line = line.strip('\n')
                data_from_server=cs.recv(2000)
                print(f"[C]: Data received from server: {data_from_server.strip().decode('utf-8')}")
                output.write(f"{data_from_server.decode('utf-8').strip()}\n")
    cs.close()
    exit()

def test_server(test_num,input_file, output_file, expected_file):
    t1 = threading.Thread(name='server', target=server)
    t2 = threading.Thread(name='client', target=client, args=(input_file,output_file))

    t1.start()
    time.sleep(1)
    t2.start()

    t1.join()
    t2.join()

    diff = subprocess.run(['diff', output_file, expected_file], capture_output=True)
    if diff.returncode != 0:
        print(f"Test {test_num} failed: {output_file} differs from {expected_file}")
        print(diff.stdout.decode())  # Print diff output
    else:
        print(f"Test {test_num} passed: {output_file} matches {expected_file}")

if __name__ == "__main__":
    test_server(1,"test1.txt", "test1o.txt", "test1.out")
    test_server(2,"in-proj.txt", "out-proj.txt", "out-proj.out")
    test_server(3,"test2.txt", "out-test2.txt", "test2.out")
