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
    while True:
        data_from_client = csockid.recv(200)
        if not data_from_client:
            break
        string_to_rev = data_from_client.decode('utf-8')
        string_to_rev = string_to_rev[::-1]
        string_to_rev = string_to_rev.swapcase()
        csockid.send(string_to_rev.encode('utf-8'))

    msg = "Welcome to CS 352!"

    # Close the server socket
    ss.close()
    exit()

if __name__ == "__main__":
    server()
