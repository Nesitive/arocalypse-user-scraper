import requests
from bs4 import BeautifulSoup

# Headers for HTTP requests
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

# User enters profile page URL
url = str(input("""
Paste the URL for your profile page.
This can be done via right-click on Windows and Ctrl+Shift+V everywhere else.

The URL should be similar to this:
    https://www.arocalypse.com/profile/12345-username/

> """)) + "/content"

def get_page(url, headers, max_retry_attempts = 5):
    # Get page with <max_retry_attempts> retries
    for i in range(max_retry_attempts):
        print(f"==> Getting {url} (attempt {i + 1} of {max_retry_attempts})...")
        response = requests.get(url, headers = headers)

        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        else:
            print("[ERROR] Arocalypse returned error code:", response.status_code)
            print("Retrying...")

# Send initial HTTP request
page = get_page(url, headers)
if not page:
    print("Failed to get page:", url)
    exit

# Extract all links on "All Activity" page
activity_page_urls = []
for link in page.find_all("a"):
    if "page" in str(link):
        activity_page_urls += [link.get("href")]

# Extract highest page number
last_page_num = int(activity_page_urls[-1].split("/")[7])

# Get all post IDs of user's posts
post_urls = []
for page in range(3):
        soup = get_page(f"https://www.arocalypse.com/profile/11354-nesitive/content/page/{page + 1}/?all_activity=1", headers = headers)
        for link in soup.select("h2>span>a")[1:]:
            post_urls += [link.get("href")]

# Get posts
def get_post_from_id(page, post_id):
    for post in page.select("article.cPost"):
        print(int(post.get("id").split("_")[-1]), post_id)
        if post.get("id").split("_")[-1] == post_id:
            return post
    
while len(post_urls) > 0:
    current_page = get_page(post_urls[0], headers = headers)
    print(get_post_from_id(current_page, post_urls[0].split("=")[-1]))
    break
