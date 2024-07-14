
GETINFO is a Python script that retrieves information about a specified domain including its IP address, DNS records, open ports, server details, and SSL certificate information.

## Features

- **Get IP Address:** Retrieves the IP address associated with the domain.
- **DNS Records:** Fetches the DNS records (A records) for the domain.
- **Scan Open Ports:** Uses nmap to scan for open ports on the domain.
- **Server Details:** Retrieves the server information, including the server type.
- **SSL Certificate Information:** Retrieves details about the SSL certificate, including issuer and subject.

## Prerequisites

- Python 3.x installed on your system.
- Required Python packages:
  - `dns.resolver` (install using `pip install dnspython`)
  - `requests` (install using `pip install requests`)
  - `nmap` command-line tool installed and available in your PATH.

## Usage

1. **Clone the repository:**
   ```bash
   git clone +GITHUB LINK+
   cd GETINFO
