import os
from dotenv import load_dotenv
from composio import Composio

load_dotenv()

composio = Composio(
    api_key=os.getenv("COMPOSIO_API_KEY")
)

USER_ID = "research-agent"
AUTH_CONFIG_ID = "ac_IZAoFTlqVkr5"

connection = composio.connected_accounts.link(
    USER_ID,
    AUTH_CONFIG_ID,
)

print("Connection request created.")
print("ID:", connection.id)
print("Open this URL:")
print(connection.redirect_url)