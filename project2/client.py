'''
client.py: Resolves domain names listed in an input file.

rs.py: Root DNS server that manages the overall resolution process.

ts1.py: Top-level domain server 1.

ts2.py: Top-level domain server 2.
'''

import socket
import sys
import os

def read_hostnames(filename):
    """Read domain names and query types from the input file."""
    hostnames = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 2:
                    domain = parts[0]
                    flag = parts[1]
                    hostnames.append((domain, flag))
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        sys.exit(1)
    
    return hostnames

def send_query(hostname, port, domain, ident, flag):
    """Send a DNS query to the specified server and return the response."""
    try:
        # Create socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((hostname, port))
        
        # Create and send query
        query = f"0 {domain} {ident} {flag}"
        client_socket.sendall(query.encode())
        
        # Receive response
        response = client_socket.recv(1024).decode()
        
        # Close connection
        client_socket.close()
        
        return response
    except Exception as e:
        print(f"Error sending query to {hostname}: {e}")
        return None

def process_domain(rs_hostname, rs_port, domain, flag, ident, log_file):
    """Process a domain resolution request."""
    # Initial query to root server
    rs_response = send_query(rs_hostname, rs_port, domain, ident, flag)
    
    if not rs_response:
        print(f"Failed to get response from root server for {domain}")
        return ident
    
    # Log response
    log_file.write(f"{rs_response}\n")
    log_file.flush()
    
    # Parse response
    parts = rs_response.strip().split()
    if len(parts) != 5 or parts[0] != '1':
        print(f"Invalid response format from root server: {rs_response}")
        return ident
    
    # Handle response based on flags
    response_flag = parts[4]
    
    # For iterative query that needs to contact a TS server
    if flag == 'it' and response_flag == 'ns':
        ts_hostname = parts[2]  # TS hostname from RS response
        
        # Increment identification for new query
        ident += 1
        
        # Send query to TS server
        ts_response = send_query(ts_hostname, rs_port, domain, ident, flag)
        
        if ts_response:
            # Log TS response
            log_file.write(f"{ts_response}\n")
            log_file.flush()
    
    return ident

if __name__ == '__main__':
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 client.py rs_hostname rudns_port")
        sys.exit(1)
    
    # Parse command line arguments
    rs_hostname = sys.argv[1]
    try:
        rs_port = int(sys.argv[2])
    except ValueError:
        print("Error: Port must be an integer")
        sys.exit(1)
    
    # Read hostnames from input file
    hostnames = read_hostnames('hostnames.txt')
    
    # Create log file
    log_file = open('resolved.txt', 'w')
    
    try:
        # Process each domain name
        ident = 1  # Start identification from 1
        
        for domain, flag in hostnames:
            ident = process_domain(rs_hostname, rs_port, domain, flag, ident, log_file)
            ident += 1  # Increment identification for next query
    
    except KeyboardInterrupt:
        print("Client shutting down")
    finally:
        # Clean up
        log_file.close()