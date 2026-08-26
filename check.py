import os

from composio import Composio
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("COMPOSIO_API_KEY")

if not API_KEY:
    raise RuntimeError("COMPOSIO_API_KEY is missing from .env")

composio = Composio(api_key=API_KEY)

USER_ID = "research-agent"


def main():
    print(f"Checking connected accounts for: {USER_ID}\n")

    accounts = composio.connected_accounts.list(
        user_ids=[USER_ID]
    )

    print("=" * 70)
    print("OBJECT TYPE")
    print("=" * 70)
    print(type(accounts))

    print("\n" + "=" * 70)
    print("OBJECT")
    print("=" * 70)
    print(accounts)

    print("\n" + "=" * 70)
    print("AVAILABLE ATTRIBUTES")
    print("=" * 70)

    print(dir(accounts))

    print("\n" + "=" * 70)
    print("INTERNAL DICTIONARY")
    print("=" * 70)

    if hasattr(accounts, "__dict__"):
        print(accounts.__dict__)
    else:
        print("No __dict__ available.")


if __name__ == "__main__":
    main()