
import csv
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

OUTPUT_DIR = Path("results")
OUTPUT_DIR.mkdir(exist_ok=True)

PLATFORMS = {
    "GitHub": "https://github.com/",
    "Reddit": "https://www.reddit.com/user/",
    "Pinterest": "https://www.pinterest.com/",
    "YouTube": "https://www.youtube.com/@",

}



def check_public_page(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "PublicProfileFinder/1.0"}
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status, response.geturl(), (
                "Page reachable; account not confirmed"
            )

    except urllib.error.HTTPError as error:
        if error.code == 404:
            note = "Page not found at this URL; account unconfirmed"
        elif error.code in (401, 403, 429):
            note = "Access restricted or rate limited; inconclusive"
        else:
            note = "HTTP response received; account status inconclusive"

        return error.code, error.geturl(), note

    except Exception as error:
        return None, url, (
            f"Could not verify page: {type(error).__name__}"
        )


def find_profiles(email, username):
    results = []

    if username:
        for platform, base_url in PLATFORMS.items():
            url = base_url + quote(username, safe="")
            print(f"\nChecking {platform}...")

            status, final_url, note = check_public_page(url)

            item = {
                "input_type": "username",
                "input": username,
                "platform": platform,
                "profile_url": url,
                "http_status": status,
                "final_url": final_url,
                "result": note,
            }
            results.append(item)

            print(f"URL: {url}")
            print(f"HTTP status: {status or 'Unavailable'}")
            print(f"Result: {note}")

    if email:
        results.append({
            "input_type": "email",
            "input": email,
            "platform": "Email",
            "profile_url": "",
            "http_status": None,
            "final_url": "",
            "result": (
                "Email-to-profile association not checked; "
                "email alone cannot confirm social accounts"
            ),
        })

    return results


def save_results(results):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    json_path = OUTPUT_DIR / f"results_{timestamp}.json"
    csv_path = OUTPUT_DIR / f"results_{timestamp}.csv"

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    fields = [
        "input_type", "input", "platform", "profile_url",
        "http_status", "final_url", "result"
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nJSON saved: {json_path}")
    print(f"CSV saved:  {csv_path}")


def main():
    print("=== Public Profile Finder ===")
    email = input("Email (optional): ").strip()
    username = input("Username (optional): ").strip().lstrip("@")

    if not email and not username:
        print("Please enter an email or username.")
        return

    results = find_profiles(email, username)
    save_results(results)


if __name__ == "__main__":
    main()
