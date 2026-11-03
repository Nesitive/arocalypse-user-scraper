import requests
from bs4 import BeautifulSoup

headers = {
    "Host": "www.arocalypse.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:159.0) Gecko/20100101 Firefox/159.0",
    "Accept": "text/html",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Cookie": "ips4_forum_list_view=snippet; ips4_ipsTimezone=Atlantic/Reykjavik; ips4_hasJS=true",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}

url = str(input("""
Paste the URL for your profile page.
This can be done via right-click on Windows and Ctrl+Shift+V everywhere else.

The URL should be similar to this:
    https://www.arocalypse.com/profile/12345-username/

> """)) + "/content"

def get_page(url, headers, max_retry_attempts = 5):
    for i in range(max_retry_attempts):
        print(f"==> Getting profile page (attempt {i + 1} of {max_retry_attempts})...")
        response = requests.get(url, headers = headers)

        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        else:
            print("[ERROR] Arocalypse returned error code:", response.status_code)
            print("Retrying...")

page = get_page(url, headers)
if not page:
    print("Failed to get page:", url)
    exit

for link in page.find_all("a"):
    if "page" in str(link):
        print(link.get("href"))
