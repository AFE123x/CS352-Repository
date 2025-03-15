import socket
import sys
import os

def parse_rsdatabase(filename):
    """Parse the root server database file."""
    tld_to_ts = {}
    domain_to_ip = {}
    
    try:
        with open(filename, 'r') as file:
            # First two lines contain TLD mappings
            tld_com = file.readline().strip().split()
            tld_edu = file.readline().strip().split()
            
            if len(tld_com) >= 2:
                tld_to_ts[tld_com[0]] = tld_com[1]  # Map 'com' to TS1 hostname
            
            if len(tld_edu) >= 2:
                tld_to_ts[tld_edu[0]] = tld_edu[1]  # Map 'edu' to TS2 hostname
            
            # Remaining lines contain domain to IP mappings
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 2:
                    domain_to_ip[parts[0].lower()] = (parts[0], parts[1])  # Store original case and IP
    except FileNotFoundError:
        print(f"Error: Database file {filename} not found.")
        sys.exit(1)
    
    return tld_to_ts, domain_to_ip

def get_tld(domain):
    """Extract the top-level domain from a domain name."""
    parts = domain.lower().split('.')
    if len(parts) >= 2:
        return parts[-1]  # Return the last part as TLD
    return None

def process_request(request, tld_to_ts, domain_to_ip):
    """Process an RU-DNS request and generate a response."""
    parts = request.strip().split()
    
    # Validate request format
    if len(parts) != 4 or parts[0] != '0':
        return None
    
    req_type, domain, ident, flag = parts
    domain_lower = domain.lower()
    tld = get_tld(domain)
    
    # Case 3 & 4: Check if domain is in RS database
    if domain_lower in domain_to_ip:
        original_domain, ip = domain_to_ip[domain_lower]
        return f"1 {original_domain} {ip} {ident} aa"
    
    # Case 1 & 2: Check if domain is under one of the managed TLDs
    if tld in tld_to_ts:
        ts_hostname = tld_to_ts[tld]
        
        if flag == 'it':  # Iterative query
            # Case 1: Return the TS hostname to client
            return f"1 {domain} {ts_hostname} {ident} ns"
        
        elif flag == 'rd':  # Recursive query
            # Case 2: Forward query to appropriate TS
            try:
                # Create a socket to connect to the TS
                ts_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ts_sock.connect((ts_hostname, ts_port))
                
                # Forward the query to TS
                ts_sock.sendall(request.encode())
                
                # Receive response from TS
                ts_response = ts_sock.recv(1024).decode()
                ts_sock.close()
                
                # Parse TS response and modify flags if necessary
                ts_parts = ts_response.strip().split()
                if len(ts_parts) == 5 and ts_parts[0] == '1':
                    if ts_parts[4] == 'aa':
                        # Change authoritative (aa) to recursion available (ra)
                        return f"1 {ts_parts[1]} {ts_parts[2]} {ts_parts[3]} ra"
                    else:
                        # For nx flag, relay response as is
                        return ts_response
            except Exception as e:
                print(f"Error forwarding request to TS: {e}")
                return None
    
    # Case 4: Domain not in RS database and not under managed TLDs
    return f"1 {domain} 0.0.0.0 {ident} nx"

if __name__ == '__main__':
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python3 rs.py rudns_port")
        sys.exit(1)
    
    # Parse command line arguments
    try:
        rs_port = int(sys.argv[1])
        ts_port = rs_port  # TS servers use the same port
    except ValueError:
        print("Error: Port must be an integer")
        sys.exit(1)
    
    # Parse RS database
    tld_to_ts, domain_to_ip = parse_rsdatabase('rsdatabase.txt')
    
    # Create socket
    try:
        rs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rs_sock.bind(('', rs_port))
        rs_sock.listen(10)
        print(f"RS server is listening on port {rs_port}")
    except Exception as e:
        print(f"Error creating socket: {e}")
        sys.exit(1)
    
    # Create/open log file
    log_file = open('rsresponses.txt', 'w')
    
    try:
        while True:
            # Accept client connections
            conn, addr = rs_sock.accept()
            print(f"Connection from {addr}")
            
            try:
                # Receive data
                data = conn.recv(1024).decode()
                if not data:
                    continue
                
                print(f"Received: {data}")
                
                # Process request
                response = process_request(data, tld_to_ts, domain_to_ip)
                
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
        rs_sock.close()
        log_file.close()