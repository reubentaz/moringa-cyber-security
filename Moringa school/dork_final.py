import time
import requests
from bs4 import BeautifulSoup

# Global constants required for Google Search requests
GOOGLE_SEARCH_URL = "https://www.google.com/search?q="
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}


def generate_dork_queries():
    """Generate Google dorking queries for security research."""
    queries = [
        "inurl:login",  # Find login pages
        "filetype:pdf OR filetype:doc",  # Find exposed documents
        "intitle:index.of mysql"  # Find open databases
    ]
    return queries


def send_search_request(query):
    """Send a request to Google Search with error handling."""
    try:
        search_url = GOOGLE_SEARCH_URL + query
        response = requests.get(search_url, headers=HEADERS)
        
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: Unable to fetch results for {query}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def parse_search_results(html):
    """Extract search result URLs from Google's search response."""
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and "http" in href:
            results.append(href)

    return results


def perform_dorking():
    """Perform Google dorking using predefined queries."""
    queries = generate_dork_queries()
    all_results = {}

    for query in queries:
        print(f"Searching: {query}")
        html = send_search_request(query)
        
        if html:
            results = parse_search_results(html)
            all_results[query] = results
            time.sleep(2)  # Prevent rapid requests to Google

    return all_results


def save_results(results):
    """Save search results to a text file."""
    with open("dorking_results.txt", "w") as file:
        for query, urls in results.items():
            file.write(f"Results for: {query}\n")
            for url in urls:
                file.write(f"{url}\n")
            file.write("\n")

    print("Results saved to dorking_results.txt")


def main():
    """Main execution entry point."""
    dork_results = perform_dorking()
    save_results(dork_results)


if __name__ == "__main__":
    main()