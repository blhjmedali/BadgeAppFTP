BadgeAppFTP
PhD Research Project | University of Djelfa
Module: File Transfer Protocol (FTP) / Network Protocols

1. Project Overview
BadgeAppFTP is a specialized application designed to integrate badge management systems with secure file transfer mechanisms. This project explores the efficiency, security, and automation of syncing badge-related data (user credentials, access logs, and profile images) across distributed servers using the FTP framework.

Developed as part of the doctoral curriculum at the University of Ziane Achour (Djelfa), this tool aims to bridge the gap between physical access control systems and networked data storage.

2. Key Features
Automated Synchronization: Real-time uploading of badge data to a centralized FTP server.

Secure Authentication: Implementation of FTPS (FTP over SSL/TLS) to ensure data integrity.

Log Management: Automated generation of transfer logs for audit purposes in an academic environment.

Multi-format Support: Handles .json, .csv, and image files related to badge issuance.

3. System Architecture
The application follows a client-server model where the BadgeApp acts as the client, pushing updates to a remote FTP node configured at the University's lab environment.

4. Getting Started
Prerequisites
Python 3.10+ (or preferred language)

Access to an FTP/SFTP server

Dependencies: pip install -r requirements.txt

Installation
Clone the repository:

Bash
git clone https://github.com/blhjmedali/BadgeAppFTP.git
cd BadgeAppFTP
Configure Environment:
Create a .env file with your server credentials:

Code snippet
FTP_HOST=ftp.univ-djelfa.dz
FTP_USER=your_username
FTP_PASS=your_password
Run the Application:

Bash
python main.py
5. Research Context
This project serves as a practical implementation for the FTP Module. It evaluates:

Latency: The time delay in badge data propagation.

Reliability: Packet loss handling during high-frequency badge scans.

Protocol Efficiency: Comparing standard FTP vs. SFTP in high-security university settings.

6. Author
[Your Name/Med Ali]
PhD Student, University of Djelfa
Contact: [Your Email]
