TECH USED
Streamlit

For building the interactive b UI where the user can type natural commands (like "create ticket").

Lets us display input fields, buttons, JSON responses, and cURL commands neatly.

Python requests library

Handles real HTTP calls to the Freshservice API based on the mapped endpoint and method.

Sends authentication and JSON request bodies.

Freshservice REST API

The backend service ’re talking to.

Supports various endpoints like /api/v2/tickets, /api/v2/requesters, etc.

Accepts Basic Auth with API_KEY:X and JSON request format.

Base64 encoding (base64 library)

Used to encode the API Key with :X into the proper Basic Auth header format.

Required by Freshservice API authentication.

JSON (json library)

Used to format the request body as text for both:

Sending in the API call (requests needs it as JSON).

Displaying inside the generated cURL.

LOGIC USED
1. Static API Key & Domain
Instead of asking the user for the API Key & domain each time,  hardcode them into the script (API_KEY and DOMAIN variables).

This keeps the UI simple.

2. Natural Language  Predefined Command Mapping
 created a command_map dictionary where  list:

A human-friendly trigger phrase ("create ticket", "list tickets", "get ticket")

The HTTP method (GET, POST, PUT, DELETE)

The endpoint path (like /api/v2/tickets or /api/v2/tickets/{id})

A sample request body if needed (mostly for POST and PUT)

3. Matching User Input
When the user types something, :

Convert to lorcase.

Check if the text starts with one of our predefined keys in command_map.

If the endpoint has {id},  try to extract the ticket ID from what the user typed.

e.g. "get ticket 101" → endpoint becomes /api/v2/tickets/101.

4. Calling the Real Freshservice API
Once  have the method, endpoint, and optional JSON body:

 build the full URL:

text
https://{DOMAIN}{endpoint}
Add authentication and headers.

Use requests.request() to make the call.

Get the real API response back.

5. Generating the Matching cURL Command
Using the exact same:

Method

URL

Request body

 build a real equivalent cURL string so that the user can directly run it in a terminal if they want.

The cURL will always match the actual request just sent.

6. Displaying Results
In the Streamlit UI, show:

The cURL command used.

The HTTP status code.

The API response JSON from Freshservice.

Flow Summary
User Command  Match to Mapping  Build endpoint & body  Call Freshservice API  Get response  Generate matching cURL  Show in streamlitUI.
