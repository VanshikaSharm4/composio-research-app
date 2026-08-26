import os
from dotenv import load_dotenv
from composio import Composio


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("COMPOSIO_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "COMPOSIO_API_KEY is missing. Check your .env file."
    )

composio = Composio(api_key=API_KEY)

USER_ID = "research-agent"

CONNECTED_ACCOUNT_ID = "ca_LaDPL7VQZ5DK"

FETCH_TOOL = "APIFY_MCP_APIFY_SLASH_RAG_WEB_BROWSER"

URL = "https://developer.salesforce.com/docs/"


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("Testing Composio + Apify...")
    print(f"User: {USER_ID}")
    print(f"Connected Account: {CONNECTED_ACCOUNT_ID}")
    print(f"Tool: {FETCH_TOOL}")
    print(f"URL:  {URL}")
    print()

    try:

        result = composio.tools.execute(
            FETCH_TOOL,

            arguments={
                "query": URL,
                "maxResults": 3,
                "outputFormats": ["markdown"],
            },

            user_id=USER_ID,

            connected_account_id=CONNECTED_ACCOUNT_ID,

            # The installed Composio SDK requires a toolkit
            # version for manual execution. We don't have a
            # specific version, so explicitly skip that check.
            dangerously_skip_version_check=True,
        )

        print("SUCCESS")
        print("=" * 70)
        print(result)

    except Exception as e:

        print("FAILED")
        print("=" * 70)
        print(type(e).__name__)
        print(str(e))


if __name__ == "__main__":
    main()