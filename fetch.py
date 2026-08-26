import json
import os
import time
from pathlib import Path

from composio import Composio
from dotenv import load_dotenv


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("COMPOSIO_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "COMPOSIO_API_KEY is missing. Add it to your .env file."
    )


# Composio client
composio = Composio(
    api_key=API_KEY
)


INPUT_FILE = Path("data/apps_input.json")
OUTPUT_DIR = Path("data/raw_fetched")

USER_ID = "research-agent"

# Public web retrieval tool.
# This uses Apify's RAG Web Browser through Composio.
FETCH_TOOL = "APIFY_MCP_APIFY_SLASH_RAG_WEB_BROWSER"


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def load_apps():
    """Load the 100 applications from apps_input.json."""

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_page(url):
    """
    Fetch a public webpage using Apify's RAG Web Browser
    through Composio.
    """

    result = composio.tools.execute(
        FETCH_TOOL,
        arguments={
            "query": url,
            "maxResults": 1,
            "outputFormats": [
                "markdown"
            ],
        },
        user_id=USER_ID,
        dangerously_skip_version_check=True,
    )

    return result


def output_filename(app):
    """
    Create a stable filename such as:

        001_salesforce.json
        002_hubspot.json
    """

    safe_name = (
        app["name"]
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace("(", "")
        .replace(")", "")
        .replace(".", "")
        .replace(":", "")
    )

    return f"{app['id']:03d}_{safe_name}.json"


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    apps = load_apps()

    print(f"Found {len(apps)} apps.")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    successful = 0
    failed = 0
    skipped = 0

    for index, app in enumerate(apps[:1], start=1):

        app_id = app["id"]
        app_name = app["name"]

        # Prefer developer documentation.
        # Fall back to the company's main website.
        url = app.get("docs_hint") or app.get("website")

        if not url:

            print(
                f"[{index}/{len(apps)}] "
                f"{app_name}: NO URL"
            )

            failed += 1
            continue

        output_file = OUTPUT_DIR / output_filename(app)

        # -------------------------------------------------
        # Cache check
        # -------------------------------------------------

        if output_file.exists():

            print(
                f"[{index}/{len(apps)}] "
                f"{app_name}: already cached → "
                f"{output_file}"
            )

            skipped += 1
            continue

        print(
            f"\n[{index}/{len(apps)}] Fetching {app_name}"
        )

        print(
            f"           {url}"
        )

        try:

            result = fetch_page(url)

            cached_data = {
                "id": app_id,
                "name": app_name,
                "category": app["category"],
                "website": app.get("website"),
                "docs_hint": app.get("docs_hint"),
                "fetched_url": url,
                "fetch_tool": FETCH_TOOL,
                "fetched_at": time.strftime(
                    "%Y-%m-%dT%H:%M:%SZ",
                    time.gmtime()
                ),
                "result": result,
            }

            with open(
                output_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    cached_data,
                    f,
                    indent=2,
                    ensure_ascii=False,
                    default=str,
                )

            print(
                f"           ✓ Saved → {output_file}"
            )

            successful += 1

        except Exception as e:

            print(
                f"           ✗ ERROR: "
                f"{type(e).__name__}: {e}"
            )

            error_data = {
                "id": app_id,
                "name": app_name,
                "category": app["category"],
                "website": app.get("website"),
                "docs_hint": app.get("docs_hint"),
                "fetched_url": url,
                "fetch_tool": FETCH_TOOL,
                "error": type(e).__name__,
                "error_message": str(e),
                "fetched_at": time.strftime(
                    "%Y-%m-%dT%H:%M:%SZ",
                    time.gmtime()
                ),
            }

            with open(
                output_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    error_data,
                    f,
                    indent=2,
                    ensure_ascii=False,
                )

            failed += 1

        # Small delay between requests.
        time.sleep(0.5)

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("FETCH STAGE COMPLETE")
    print("=" * 60)

    print(f"Total apps:  {len(apps)}")
    print(f"Successful:  {successful}")
    print(f"Failed:      {failed}")
    print(f"Skipped:     {skipped}")
    print(f"Output dir:  {OUTPUT_DIR}")
    print("=" * 60)


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()