# NOTES

- We'll be implement a DNS, where we have a:
    - Root DNS Server (RS)
    - Top level domain server:
        - TS1
        - TS2

## RU-DNS Message format

### Request Format
- We'll be using the following format:

```txt
0 Domainname identification flags
```
- 0 is the protocol request message
- domain_name is the name of the domani we want to resolve.
- identification is an int incremented by the requesting client.
- flags tells us the desired way to handle the response.
    - rd specifies recursive.
    - it specifies iterative.

### Response Format

```
1 DomainName IPAddress identification flags
```
- 1 specifies it's a response.
- domain name is the name of the domain
- ip address is the address it's correlated to.
- identification is the same from the request.
- Flags indicates the condition of the response.
    - aa, indicates the response is directly from an authoritative name server.
        - AKA, when one of the servers responds to a client in it's own local database, it's consider authoritative.
    - ra tels us that the response was constructed through a recursive solution.
    - ns indicates the DNS response didn't resolve the domain name, and the client needs to contact another DNS server. it's not "fully solved"
    - NX means the domain doesn't exist.

## Flow of stuff

