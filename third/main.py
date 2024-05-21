import requests
import os
import concurrent.futures
# Complete the 'getNumDraws' function below.
#
# The function is expected to return an INTEGER.
# The function accepts INTEGER year as parameter.
#
def fetch_page(session, url):
    try:
        response = session.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def getNumDraws(year):
    draws = 0
    base_url = f"https://jsonmock.hackerrank.com/api/football_matches?year={year}&page="
    
    with requests.Session() as session:
        # Fetch the first page to determine the total number of pages
        initial_response = fetch_page(session, base_url + "1")
        if not initial_response:
            return 0
        
        total_pages = initial_response["total_pages"]
        
        # Use ThreadPoolExecutor to make concurrent requests
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Create list of futures for all pages
            futures = [executor.submit(fetch_page, session, base_url + str(page)) for page in range(1, total_pages + 1)]
            
            for future in concurrent.futures.as_completed(futures):
                per_page_data = future.result()
                if per_page_data:
                    for match in per_page_data["data"]:
                        if match["team1goals"] == match["team2goals"]:
                            draws += 1
    
    return draws
if __name__ == '__main__':
    year = input("enter year")
    getNumDraws(year)