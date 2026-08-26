import os
import json

from dotenv import load_dotenv
from composio import Composio


load_dotenv()

API_KEY = os.getenv("COMPOSIO_API_KEY")

if not API_KEY:
    raise RuntimeError("COMPOSIO_API_KEY is missing from .env")


USER_ID = "research-agent"

TOOL = "ANCHOR_BROWSER_GET_WEBPAGE_CONTENT"

URL = "https://developer.salesforce.com/docs/"


composio = Composio(
    api_key=API_KEY,
    toolkit_versions={
        "anchor_browser": "20260707_00"
    }
)


def main():

    print("Testing Composio → Anchor Browser")
    print("=" * 70)
    print(f"User: {USER_ID}")
    print(f"Tool: {TOOL}")
    print(f"URL:  {URL}")
    print("=" * 70)

    try:

        result = composio.tools.execute(
            TOOL,

            arguments={
                "url": URL,
                "format": "markdown",
                "wait": 2000,
                "return_partial_on_timeout": True,
            },

            user_id=USER_ID,

            dangerously_skip_version_check=True,
        )

        print("\nSUCCESS")
        print("=" * 70)

        print(json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
            default=str
        ))

    except Exception as e:

        print("\nFAILED")
        print("=" * 70)
        print(type(e).__name__)
        print(str(e))


if __name__ == "__main__":
    main()