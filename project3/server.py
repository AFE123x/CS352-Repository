import socket
import signal
import sys
import random

passwords_list = {}
secrets_list = {}
session_tokens = {}

# Populate the lists with the contents of passwords.txt and secrets.txt
def populate_passwords():
    global passwords_list
    global secrets_list
    # Read from passwords.txt
    with open("passwords.txt", "r") as pw_file:
        for line in pw_file:
            user, password = line.strip().split()
            passwords_list[user] = password

    # Read from secrets.txt
    with open("secrets.txt", "r") as sec_file:
        for line in sec_file:
            user, secret = line.strip().split()
            secrets_list[user] = secret
    
    print(passwords_list)
    print(secrets_list)



# Read a command line argument for the port where the server
# must run.
port = 8080
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    print("Using default port 8080")
hostname = "localhost"
populate_passwords()
# Start a listening server socket on the port
sock = socket.socket()
sock.bind(('', port))
sock.listen(2)

### Contents of pages we will serve.
# Login form
login_form = """
   <form action = "http://%s" method = "post">
   Name: <input type = "text" name = "username">  <br/>
   Password: <input type = "text" name = "password" /> <br/>
   <input type = "submit" value = "Submit" />
   </form>
"""
# Default: Login page.
login_page = "<h1>Please login</h1>" + login_form
# Error page for bad credentials
bad_creds_page = "<h1>Bad user/pass! Try again</h1>" + login_form
# Successful logout
logout_page = "<h1>Logged out successfully</h1>" + login_form
# A part of the page that will be displayed after successful
# login or the presentation of a valid cookie
success_page = """
   <h1>Welcome!</h1>
   <form action="http://%s" method = "post">
   <input type = "hidden" name = "action" value = "logout" />
   <input type = "submit" value = "Click here to logout" />
   </form>
   <br/><br/>
   <h1>Your secret data is here:</h1>
"""

#### Helper functions
# Printing.
def print_value(tag, value):
    print("Here is the", tag)
    print("\"\"\"")
    print(value)
    print("\"\"\"")
    print()

# Signal handler for graceful exit
def sigint_handler(sig, frame):
    print('Finishing up by closing listening socket...')
    sock.close()
    sys.exit(0)
# Register the signal handler
signal.signal(signal.SIGINT, sigint_handler)


# TODO: put your application logic here!
# Read login credentials for all the users
# Read secret data of all the users

'''
handlepostrequest(entity)
this function will parse the entity body,
and handle the page depending on what the
client wants.
'''
def handlepostrequest(entity, cookie=""):
    params = {}
    pairs = entity.split('&')

    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            params[key] = value

    # Check if this is a logout request
    if params.get('action') == 'logout':
        print("Logout requested!")
        # Set expired cookie header
        expired_cookie_header = 'Set-Cookie: token=; expires=Thu, 01 Jan 1970 00:00:00 GMT\r\n'
        return logout_page % (hostname + ":" + str(port)), expired_cookie_header

    username = params.get('username', '')
    password = params.get('password', '')

    # Make sure both are provided
    if not username or not password:
        print("Missing username or password!")
        return bad_creds_page, ''

    # Check if user exists and password matches
    if username in passwords_list and passwords_list[username] == password:
        # Generate random 64-bit token
        rand_val = random.getrandbits(64)
        rand_val_str = str(rand_val)

        # Store token in session_tokens
        session_tokens[rand_val_str] = username
        print(f"Saved cookie: token={rand_val_str} for user {username}")

        # Prepare Set-Cookie header to send
        headers_to_send = f'Set-Cookie: token={rand_val_str}\r\n'

        # Prepare success page
        if username in secrets_list:
            return (success_page + secrets_list[username]), headers_to_send
        else:
            return success_page, ''
    else:
        return bad_creds_page, ''


### Loop to accept incoming HTTP connections and respond.
while True:
    client, addr = sock.accept()
    req = client.recv(1024)

    header_body = req.decode().split('\r\r\n\r\n') if '\r\r\n\r\n' in req.decode() else req.decode().split('\r\n\r\n')
    headers = header_body[0]
    body = '' if len(header_body) == 1 else header_body[1]

    print_value('headers', headers)
    print_value('entity body', body)

    request_type = headers.split('\r\n')[0].split(' ')
    submit_hostport = "%s:%d" % (hostname, port)

    headers_to_send = ''
    html_content_to_send = ''

    cookie_val = ''
    found_cookie = False

    # Check if the request has a cookie
    for header_line in headers.split('\r\n'):
        if header_line.startswith('Cookie:'):
            cookie = header_line.split('Cookie: ')[1]
            token_parts = cookie.split('=')
            if len(token_parts) == 2 and token_parts[0] == 'token':
                cookie_val = token_parts[1]
                found_cookie = True
                break

    # --- First: check if it's a logout request
    if request_type[0] == "POST":
        params = {}
        pairs = body.split('&')
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key] = value
        if params.get('action') == 'logout':
            print("Logout requested!")
            expired_cookie_header = 'Set-Cookie: token=; expires=Thu, 01 Jan 1970 00:00:00 GMT\r\n'
            html_content_to_send = logout_page % submit_hostport
            headers_to_send = expired_cookie_header
        else:
            # Handle login normally
            html_content_to_send, headers_to_send = handlepostrequest(body, cookie_val)
            if '%s' in html_content_to_send:
                html_content_to_send = html_content_to_send % submit_hostport

    # --- Second: if cookie is present and valid
    elif found_cookie:
        username = session_tokens.get(cookie_val, '')
        if username:
            # Valid cookie → Auto-login!
            secret = secrets_list.get(username, '')
            html_content_to_send = (success_page % submit_hostport) + secret
        else:
            # Invalid cookie
            html_content_to_send = bad_creds_page % submit_hostport

    # --- Third: no cookie and not POST, show login page
    else:
        html_content_to_send = login_page % submit_hostport

    response  = 'HTTP/1.1 200 OK\r\n'
    response += headers_to_send
    response += 'Content-Type: text/html\r\n\r\n'
    response += html_content_to_send
    print_value('response', response)
    client.send(response.encode())
    client.close()

    print("Served one request/connection!\n")
