from scraper import scrape_url


def main():
    url = input("Enter URL to research: ").strip()

    print("\nScraping...")

    result = scrape_url(url)

    print("\n" + "=" * 70)
    print("RESEARCH RESULT")
    print("=" * 70)

    data = result.get("data", {})

    print(data)


if __name__ == "__main__":
    main()