import socket
import dns.resolver
import subprocess
import requests
import ssl

# ASCII art logo for GETINFO project
GETINFO = """
|||||   |||||  ||||||| ||||||||  ||     |  ||||||| ||||||||
|       |         |       |      | ||   |  |       |      |
|       ||||      |       |      |  ||  |  |       |      |
| ||||  |         |       |      |   || |  |||||   |      |
|    |  |         |       |      |    |||  |       |      |
||||||  |||||     |    ||||||||  |     ||  |       ||||||||
"""

def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None

def get_dns_records(domain):
    try:
        dns_records = dns.resolver.resolve(domain, 'A')
        return [str(record) for record in dns_records]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return []

def scan_open_ports(domain):
    try:
        command = f"nmap -F {domain}"
        output = subprocess.check_output(command, shell=True).decode('utf-8')
        open_ports = [line.split('/')[0] for line in output.splitlines() if '/tcp' in line]
        return open_ports
    except subprocess.CalledProcessError:
        return []

def get_server_details(domain):
    try:
        url = f"http://{domain}"
        response = requests.head(url, allow_redirects=True)
        
        server = response.headers.get('Server')
        if not server:
            server = "Not Available"
        
        # SSL Certificate details
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as ssock:
            ssock.connect((domain, 443))
            ssl_info = ssock.getpeercert()
        
        if isinstance(ssl_info, tuple):
            issuer = ssl_info[0][1][4][1]
            cert_subject = ssl_info[0][1][5][1]
        else:
            issuer = "Not Available"
            cert_subject = "Not Available"
        
        return server, issuer, cert_subject
    except requests.RequestException:
        return "Not Available", "Not Available", "Not Available"
    except ssl.SSLError:
        return "Not Available", "Not Available", "Not Available"

if __name__ == "__main__":
    # Print the ASCII art logo with the name "GETINFO"
    print(GETINFO)
    
    domain = input("Enter the domain name: ").strip()
    
    ip_address = get_ip_address(domain)
    if ip_address:
        print(f"IP Address: {ip_address}")
    else:
        print("IP Address not found.")
    
    dns_records = get_dns_records(domain)
    if dns_records:
        print("DNS Records (A):")
        for record in dns_records:
            print(f"- {record}")
    else:
        print("No DNS Records found.")
    
    open_ports = scan_open_ports(domain)
    if open_ports:
        print("Open Ports:")
        for port in open_ports:
            print(f"- {port}")
    else:
        print("No open ports found.")
    
    server, issuer, cert_subject = get_server_details(domain)
    print(f"Server: {server}")
    print(f"Issuer: {issuer}")
    print(f"SSL Certificate Subject: {cert_subject}")
