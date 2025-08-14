import streamlit as st
import json
import requests
import base64

# ===== STATIC SETTINGS =====
API_KEY = "6raY-7tF5YgEt2r_bGyz"   # <-- replace with your API key
DOMAIN = "adiiii.freshservice.com"  # <-- replace with your Freshservice domain

# ===== COMMAND MAPPING =====
command_map = {
    "create ticket": {
        "method": "POST",
        "endpoint": "/api/v2/tickets",
        "body": {
            "ticket": {
                "subject": "Support Needed",
                "description": "Details about the issue...",
                "email": "user@example.com",
                "priority": 1,
                "status": 2
            }
        }
    },
    "list tickets": {
        "method": "GET",
        "endpoint": "/api/v2/tickets",
        "body": None
    },
    "get ticket": {
        "method": "GET",
        "endpoint": "/api/v2/tickets/{id}",
        "body": None
    }
}

# ===== Helper: Generate cURL =====
def generate_curl(method, endpoint, body=None):
    url = f"https://{DOMAIN}{endpoint}"
    if body:
        body_str = json.dumps(body)
        curl_cmd = f'''curl -v -u {API_KEY}:X -H "Content-Type: application/json" -X {method} -d '{body_str}' "{url}"'''
    else:
        curl_cmd = f'''curl -v -u {API_KEY}:X -H "Content-Type: application/json" -X {method} "{url}"'''
    return curl_cmd

# ===== Helper: Call the API =====
def call_freshservice_api(method, endpoint, body=None):
    url = f"https://{DOMAIN}{endpoint}"
    auth_header = base64.b64encode(f"{API_KEY}:X".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/json"
    }
    resp = requests.request(method, url, headers=headers, json=body if body else None)
    try:
        resp_json = resp.json()
    except ValueError:
        resp_json = {"raw_response": resp.text}
    return resp.status_code, resp_json

# ===== Streamlit UI =====
st.title("Freshservice Command → API Call & cURL")

user_cmd = st.text_input("Enter your command (e.g., 'create ticket', 'list tickets', 'get ticket 101')")

if st.button("Run Command"):
    cmd_lower = user_cmd.lower().strip()
    matched_key = None

    for key in command_map.keys():
        if cmd_lower.startswith(key):
            matched_key = key
            break

    if not matched_key:
        st.error("Command not recognized.")
    else:
        action = command_map[matched_key]
        endpoint = action["endpoint"]

        # Handle {id} in endpoint
        if "{id}" in endpoint:
            words = cmd_lower.split()
            ticket_id = next((w for w in words if w.isdigit()), None)
            if not ticket_id:
                ticket_id = "1234"  # fallback if no ID provided
            endpoint = endpoint.replace("{id}", ticket_id)

        method = action["method"]
        body = action["body"]

        # ===== Call the actual API =====
        status_code, resp_json = call_freshservice_api(method, endpoint, body)

        # ===== Generate matching cURL =====
        curl_cmd = generate_curl(method, endpoint, body)

        # ===== Output =====
        st.subheader("cURL Command Used")
        st.code(curl_cmd, language="bash")
        st.subheader("API Response")
        st.write(f"Status Code: {status_code}")
        st.json(resp_json)
