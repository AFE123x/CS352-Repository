## 1. Group Members: Bhavya Patel (bsp75) & Arun Felix (NETID)

2. 

3. After removing the sleep statements the program throws an error after rerunning twice. The error is thrown because without the sleep statements the server is closed before the client can connect to it. The client thread attempts to connect to the server before the server has finished setting up and started listening for connections.

