# Proof of Concept (PoC) for Automated Login Script

---

## 1. Proof of Concept (PoC)
**Objective**: Validate that the login process can be automated successfully.

### Key Goals:
- Programmatically interact with the target server.
- Correctly handle hidden fields like `__VIEWSTATE` and `__EVENTVALIDATION`.
- Establish a working session for further testing.

---

## 2. Reconnaissance and Preparation
### Initial Observations:
- The successful login confirms that:
  - The **username** and **password** fields are functioning as expected.
  - The server properly responds to **POST** requests.
- Verifies the endpoint and form structure, reducing errors during brute-forcing or advanced automation.

---

## 3. Foundation for Brute-Forcing
### Advantages of the Initial Script:
- Serves as the groundwork for:
  - Automating password testing with wordlists.
  - Refining logic to identify valid credentials based on response content.
- **Why It Matters**:
  - Without understanding and handling the underlying mechanisms, brute-forcing or further automation would fail.

---

## 4. Debugging and Validation
### By Successfully Logging In with a Known Password:
- You confirm:
  - Proper handling of cookies, session data, and form fields.
  - Absence of server-side defenses like **CAPTCHA** or account lockouts.
- Eliminates potential issues such as:
  - Incorrect field names.
  - Incomplete **POST** requests.
  - CSRF validation errors.

---

This process ensures a robust and reliable foundation for automating further tasks like credential testing or advanced interaction with the target system.

## login_script.py

```
#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)

# Target URL (login page) %2f is the url-encoded representation of the forwared slash
url = "http://10.10.51.155/Account/login.aspx?ReturnURL=%2fadmin" 

# Create a session to persist cookies
session = requests.Session()

# Send a GET request to fetch the login page
logging.info("Fetching the login page...")
response = session.get(url)

# Parse the page content using BeautifulSoup 
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the hidden input fields (__VIEWSTATE, __EVENTVALIDATION) => below we set viewstate and eventvalidation
viewstate = soup.find("input", {"id": "__EVENTVALIDATION"})
eventvalidation = soup.find("input", {"id": "__EVENTVALIDATION"})

if viewstate and eventvalidation:
		viewstate = viewstate['value']
		eventvalidation = eventvalidation['value']
else:
	logging.error("Hidden fields not found. Exiting...")
	exit()

# Log the extracted values
logging.info(f"__VIEWSTATE: {viewstate}")
logging.info(f"__EVENTVALIDATION: {eventvalidation}")

# Dynamically detect form fields
username_field = soup.find("input", {"name": lambda x: "UserName" in x})
password_field = soup.find("input", {"name": lambda x: "Password" in x})
login_button_field = soup.find("input", {"name": lambda x: "LoginButton" in x})

if not username_field or not password_field or not login_button_field:
	logging.error("Required form fields not found. Exiting...")
	exit()

# Credential management (replace 'admin' and 'password' with secure inputs or environment variables)
username = os.getenv('USERNAME', 'admin') 		# Default to 'admin'
password = os.getenv('PASSWORD', 'password') 	# Default to 'password'

# Prepare POST data
payload = {
	"__VIEWSTATE": viewstate,
	"__EVENTVALIDATION": eventvalidation,
	username_field['name']: username,
	password_field['name']: password,
	login_button_field['name']: login_button_field.get('value', 'Log in')
}

# Send a POST request with the form data
logging.info("Attempting to log in...")
login_response = session.post(url, data=payload)

# Check if login was successful by analyzing the response 
if "Invalid login" in login_response.text:
	logging.info("Login failed. Check credential or form structure.")
else:
	logging.info("Login successful!")

# Print the response content for debugging (optional)
# print(login_response.text)

```



