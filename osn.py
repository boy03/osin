import argparse
import requests
from bs4 import BeautifulSoup
import os

def search_google(name):
    """Scrape hasil pencarian Google."""
    print("[1] Searching Google...")
    search_url = f"https://www.google.com/search?q={name.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("h3")
            print(f"  - Top results from Google:")
            for result in results[:5]:  # Ambil 5 hasil teratas
                print(f"    • {result.get_text()}")
        else:
            print("  - Failed to fetch Google results.")
    except Exception as e:
        print(f"  - Error during Google search: {e}")

def search_twitter(name):
    """Cari nama di Twitter."""
    print("[2] Searching Twitter...")
    query = f"https://twitter.com/search?q={name.replace(' ', '%20')}&src=typed_query"
    print(f"  - Twitter Search Link: {query}")

def search_linkedin(name):
    """Cari nama di LinkedIn."""
    print("[3] Searching LinkedIn...")
    query = f"https://www.linkedin.com/search/results/all/?keywords={name.replace(' ', '%20')}"
    print(f"  - LinkedIn Search Link: {query}")

def search_instagram(name):
    """Cari nama di Instagram."""
    print("[4] Searching Instagram...")
    query = f"https://www.instagram.com/explore/tags/{name.replace(' ', '')}/"
    print(f"  - Instagram Search Link: {query}")

def search_email(name):
    """Gunakan API Hunter.io untuk mencari email."""
    print("[5] Searching Email Finder...")
    api_key = os.getenv("HUNTER_API_KEY", "your_hunter_api_key")
    domain = name.split()[-1] + ".com"
    api_url = f"https://api.hunter.io/v2/email-finder?domain={domain}&api_key={api_key}"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            email = data.get("data", {}).get("email")
            print(f"  - Found email: {email}" if email else "  - No email found.")
        else:
            print("  - Hunter.io API failed.")
    except Exception as e:
        print(f"  - Error with Hunter.io API: {e}")

def check_breached_data(email):
    """Cek data bocor menggunakan Have I Been Pwned."""
    print("[6] Checking Breached Data...")
    api_key = os.getenv("HIBP_API_KEY", "your_hibp_api_key")
    api_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {"hibp-api-key": api_key, "User-Agent": "OSINT-Tool"}
    
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            breaches = response.json()
            print(f"  - {email} ditemukan dalam {len(breaches)} kebocoran data:")
            for breach in breaches:
                print(f"    • {breach['Name']}: {breach['Description']}")
        elif response.status_code == 404:
            print(f"  - No breaches found for {email}.")
        else:
            print(f"  - Error: {response.status_code}")
    except Exception as e:
        print(f"  - Failed to check breached data: {e}")

def show_banner():
    """Tampilkan banner."""
    print("""
   ___   ____  ____  _   _ _______ 
  / _ \ |  _ \|  _ \| \ | | ____\ \ 
 | | | || | | | | | |  \| |  _|  \ \ 
 | |_| || |_| | |_| | |\  | |___  | |
  \___/ |____/|____/|_| \_|_____| |_|
    """)
    print("       Advanced OSINT Tool\n")

def main():
    parser = argparse.ArgumentParser(
        description="Tool OSINT otomatis untuk mengumpulkan informasi seseorang."
    )
    parser.add_argument("name", help="Nama individu target (contoh: John Doe)")
    parser.add_argument("-e", "--email", help="Email target untuk mengecek data bocor (opsional)")
    args = parser.parse_args()

    name = args.name.strip()
    email = args.email.strip() if args.email else None

    show_banner()
    print(f"Target: {name}\n")
    
    search_google(name)
    search_twitter(name)
    search_linkedin(name)
    search_instagram(name)
    search_email(name)

    if email:
        check_breached_data(email)

    print("\nOSINT process completed.")

if __name__ == "__main__":
    main()

