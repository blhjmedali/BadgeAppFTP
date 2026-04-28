# BadgeAppFTP
**PhD Research Project | University of Djelfa** **Module:** File Transfer Protocol (FTP) / Network Protocols

---

## 1. Project Overview
`BadgeAppFTP` is a specialized research application developed to bridge badge management systems with robust file transfer mechanisms. The project investigates the automation, reliability, and security of synchronizing badge-related data—including user credentials, access logs, and profile assets—across distributed network nodes using the FTP framework.

This work is conducted as part of the doctoral curriculum at the **University of Ziane Achour (Djelfa)** to analyze protocol efficiency in academic and professional infrastructure.

---

## 2. Key Features
* **Automated Synchronization:** Streamlined uploading of badge data to a centralized FTP server.
* **Protocol Flexibility:** Support for standard FTP and secure variants (FTPS/SFTP) to ensure data confidentiality.
* **Audit Logging:** Generation of detailed transfer logs for monitoring system integrity and access history.
* **Scalable Architecture:** Designed to handle batch processing of badge records and associated media files.

---

## 3. Technical Implementation
The application utilizes a client-server architecture where the **BadgeApp** functions as the primary client, pushing updates to remote nodes within the university's lab environment or cloud storage.

### Prerequisites
* **Environment:** Python 3.10+ (or relevant runtime)
* **Protocols:** FTP, FTPS, or SFTP
* **Key Dependencies:** `ftplib`, `python-dotenv`

---

## 4. Installation & Setup

### Clone the Repository
```bash
git clone [https://github.com/blhjmedali/BadgeAppFTP.git](https://github.com/blhjmedali/BadgeAppFTP.git)
cd BadgeAppFTP
