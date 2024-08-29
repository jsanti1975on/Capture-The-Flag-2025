### 3-Minute Talk: Overview of the CTF Challenge

---

**Introduction:**  
In this Capture the Flag (CTF) challenge, we were presented with a vulnerable binary named `vuln`, and our objective was to exploit it to uncover a hidden flag. The challenge fell under the category of **binary exploitation**, specifically focusing on **buffer overflows**. Our mission was to craft an input that would overflow a buffer, manipulate the program's execution flow, and trigger a specific function named `win`, which would ultimately reveal the flag.

---

**Understanding the Vulnerability:**  
The binary was a **32-bit executable** with several security mitigations either disabled or only partially enabled. Crucially, it lacked a **stack canary**, a protective measure that usually prevents buffer overflow attacks. Through disassembly, we discovered that the `vuln` function employed the unsafe `gets()` function, notorious for not performing bounds checking on input. This made the program susceptible to buffer overflow, allowing us to overwrite the return address on the stack.

---

**Exploitation Strategy:**  
Our exploitation strategy was to overwrite the return address with the address of the `win` function. The `win` function was designed to reveal the flag, but only if it received two specific arguments: `0xCAFEF00D` and `0xF00DF00D`. We determined that **112 bytes** were needed to overflow the buffer and reach the return address. With this knowledge, we constructed a payload that not only redirected execution to the `win` function but also passed the correct arguments to it.

---

**Executing the Exploit:**  
We carefully crafted the payload and verified its functionality in a local environment before attacking the remote server. Using a Python script named `remote.py`, which utilized the `pwntools` library, we sent the payload over the network to the target. The payload successfully caused the program to execute the `win` function and pass the required arguments, leading to the flag being displayed.

---

**Conclusion:**  
This CTF challenge was an excellent exercise in buffer overflow exploitation, requiring meticulous binary analysis, precise stack manipulation, and strategic use of debugging tools. The successful extraction of the flag—`picoCTF{argum3nt5_4_d4yZ_59cd5643}`—highlighted our technical skills and methodical approach to binary exploitation.
