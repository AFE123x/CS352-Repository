import socket
import sys
import os

def parse_ts_database(filename):
    """Parse the TLD server database file."""
    domain_to_ip = {}
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 2:
                    domain = parts[0]
                    ip = parts[1]
                    domain_to_ip[domain.lower()] = (domain, ip)  # Store original case and IP
    except FileNotFoundError:
        print(f"Error: Database file {filename} not found.")
        sys.exit(1)
    
    return domain_to_ip

def process_request(request, domain_to_ip):
    """Process an RU-DNS request and generate a response."""
    parts = request.strip().split()
    
    # Validate request format
    if len(parts) != 4 or parts[0] != '0':
        return None
    
    req_type, domain, ident, flag = parts
    domain_lower = domain.lower()
    
    # Check if domain exists in the database
    if domain_lower in domain_to_ip:
        original_domain, ip = domain_to_ip[domain_lower]
        return f"1 {original_domain} {ip} {ident} aa"
    else:
        # Domain not found in database
        return f"1 {domain} 0.0.0.0 {ident} nx"

if __name__ == '__main__':
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python3 ts2.py rudns_port")
        sys.exit(1)
    
    # Parse command line arguments
    try:
        ts_port = int(sys.argv[1])
    except ValueError:
        print("Error: Port must be an integer")
        sys.exit(1)
    
    # Parse TS2 database
    domain_to_ip = parse_ts_database('ts2database.txt')
    
    # Create socket
    try:
        ts_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ts_sock.bind(('', ts_port))
        ts_sock.listen(10)
        print(f"TS2 server is listening on port {ts_port}")
    except Exception as e:
        print(f"Error creating socket: {e}")
        sys.exit(1)
    
    # Create/open log file
    log_file = open('ts2responses.txt', 'w')
    
    try:
        while True:
            # Accept client connections
            conn, addr = ts_sock.accept()
            print(f"Connection from {addr}")
            
            try:
                # Receive data
                data = conn.recv(1024).decode()
                if not data:
                    continue
                
                print(f"Received: {data}")
                
                # Process request
                response = process_request(data, domain_to_ip)
                
                if response:
                    # Send response
                    conn.sendall(response.encode())
                    print(f"Sent: {response}")
                    
                    # Log response
                    log_file.write(f"{response}\n")
                    log_file.flush()
            except Exception as e:
                print(f"Error handling request: {e}")
            finally:
                # Close connection
                conn.close()
    except KeyboardInterrupt:
        print("Server shutting down")
    finally:
        # Clean up
        ts_sock.close()
        log_file.close()