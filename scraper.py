import os
from composio import Composio
from dotenv import load_dotenv

load_dotenv()

composio = Composio(
    api_key=os.getenv("COMPOSIO_API_KEY"),
    toolkit_versions={
        "apify": "20260707_00"
    }
)

USER_ID = "research-agent"
CONNECTED_ACCOUNT_ID = "ca_LaDPL7VQZ5DK"


def scrape_url(url: str):
    result = composio.tools.execute(
        "APIFY_RUN_ACTOR_SYNC_GET_DATASET_ITEMS",
        arguments={
            "actorId": "apify/rag-web-browser",
            "input": {
                "query": url,
                "maxResults": 1,
                "outputFormats": ["markdown"]
            },
            "waitForFinish": 30,
            "limit": 1,
            "format": "json"
        },
        connected_account_id=CONNECTED_ACCOUNT_ID,
        user_id=USER_ID,
        version="20260707_00"
    )

    if not result.get("successful"):
        raise RuntimeError(str(result))

    print("\nRAW APIFY RESPONSE:")
    print(result)

    return result