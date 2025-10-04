# Baby Steps - CTF Writeup

## Challenge Overview
This is a beginner-level web exploitation challenge that involves analyzing source code and decoding encoded data.

## Solution Process

### Step 1: Initial Analysis
First, I examined the web application by viewing the source code (see `source_code.png`). This revealed important information about the application structure and potential vulnerabilities.

### Step 2: Application Analysis
The application appears to be built with JavaScript (see `appjs.png`). By analyzing the app.js file, I was able to identify key components and understand how the application processes requests.

### Step 3: Finding the Encoded Data
Through source code analysis, I discovered a base64-encoded string that appeared to contain important information. The encoded string was:
```
ZmxhZ18xMzM3LnR4dA==
```

### Step 4: Decoding the Information
I decoded the base64 string using the following command:
```bash
echo "ZmxhZ18xMzM3LnR4dA==" | base64 -d
```

This revealed the decoded content (see `decoding_findings.png`), which provided the next step in solving the challenge.

### Step 5: Obtaining the Flag
The base64 decoding revealed the filename `flag_1337.txt`. To get the actual flag, I visited:
```
http://68.219.177.187:8006/flag_1337.txt
```

This provided the flag for the challenge.

## Key Learning Points
- Always check the source code of web applications for hidden information
- Base64 encoding is commonly used to obfuscate data in CTF challenges
- Simple encoding doesn't provide security - it's just obscurity
- Decoded information often points to specific files or endpoints

## Tools Used
- Web browser developer tools
- Base64 decoder (command line)
- Source code analysis

## Flag
`SecurinetsENIT{B4BY_ST3PS!}`

---

