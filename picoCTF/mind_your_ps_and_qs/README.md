# PicoCTF: Mind Your Ps and Qs

**Challenge Description:**
- A capture the flag challange based on RSA Encryption.

**Solution:**

```python
# Example Python3 code for the challenge
c = 421345306292040663864066688931456845278496274597031632020995583473619804626233684
n = 631371953793368771804570727896887140714495090919073481680274581226742748040342637
e = 65537
p = 1461849912200000206276283741896701133693
q = 431899300006243611356963607089521499045809

# Calculate totient
t = (p - 1) * (q - 1)
print(f"Totient (φ(n)): {t}")

# Calculate d
d = pow(e, -1, t)
print(f"Private exponent (d): {d}")

# Decrypt ciphertext
plaintext = pow(c, d, n)
print(f"Decrypted plaintext (numeric): {plaintext}")

# Print the plaintext in hexadecimal and ASCII
hex_plaintext = hex(plaintext)[2:]
ascii_plaintext = bytearray.fromhex(hex_plaintext).decode('ascii', errors='ignore')

print("Hexadecimal Representation:", hex_plaintext)
print("ASCII Representation:", ascii_plaintext)

