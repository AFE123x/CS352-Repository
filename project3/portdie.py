import socket
import time
import psutil
import sys

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_process_using_port(port):
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == port:
                    return proc
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
    return None

def wait_and_kill(port, check_interval=1):
    print(f"Waiting for port {port} to become active...")
    while not is_port_in_use(port):
        time.sleep(check_interval)

    print(f"Port {port} is now in use. Locating process...")
    proc = find_process_using_port(port)

    if proc:
        print(f"Killing process {proc.pid} ({proc.name()}) using port {port}...")
        proc.kill()
        print("Process killed.")
    else:
        print("No process found using the port (race condition?).")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python wait_and_kill_port.py <port>")
        sys.exit(1)

    port_number = int(sys.argv[1])
    wait_and_kill(port_number)
