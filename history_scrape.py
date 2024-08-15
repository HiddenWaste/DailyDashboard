import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Get today's date
today = datetime.today()
MONTH = today.strftime('%B')
DAY = today.strftime('%d')

def event_sort(soup):
    # Grab the Events Section on the Page
    events_section = soup.find(id="Events")
    events_list = events_section.find_next('ul').find_all('li')

    # Keyword filters (simplified example)
    keywords = {
        'Roman' : 5,
        'Japan': 8,
        'World War II': 10,
        'Cold War': 8,
        'diplomacy': 4,
        'treaty': 7,
        'King':7,
        'Queen':7,
        'Emporer':7,
        'Empress':7
    }
    
    # Filtering and scoring events
    filtered_events = []
    for event in events_list:
        event_text = event.get_text()
        score = sum(weight for keyword, weight in keywords.items() if keyword in event_text)
        if score > 0:  # Arbitrary threshold
            filtered_events.append((score, event_text))
    
    # Sort by relevance score
    filtered_events.sort(reverse=True, key=lambda x: x[0])
    
    return filtered_events

def birth_sort(soup):
    birth_section = soup.find(id="Births")  # Go to Births Section

    # Initialize list to store all birth entries
    all_birth_entries = []

    # Iterate through all sub-sections (e.g., "Pre-1600", "1600-1901", "1901-present")
    for sibling in birth_section.find_next_siblings():
        # Check if it's a subheading related to the time periods (e.g., h3 tags)
        if sibling.name == "h3" or sibling.name == "h4":  # Adjust if needed based on the HTML structure
            period_heading = sibling
            # Continue to find the list (ul) of births associated with this period
            for period_sibling in period_heading.find_next_siblings():
                if period_sibling.name == "ul":
                    all_birth_entries.extend(period_sibling.find_all('li'))
                elif period_sibling.name in {"h2", "h3"}:
                    break  # Stop if we reach the next major section or another subheading

    print("Number of birth entries found:", len(all_birth_entries))  # Debug print

    # Filter Keywords
    keywords = {
        'physicist': 5,
        'academic': 8,
        'composer': 10,
        'politician': 8,
    }

    # Filtering and scoring BIRTHS
    filtered_births = []
    for birth in all_birth_entries:
        birth_text = birth.get_text().lower()  # Normalize for matching
        print("Birth text:", birth_text)  # Debug print
        score = sum(weight for keyword, weight in keywords.items() if keyword in birth_text)
        if score > 0:  # Arbitrary threshold
            filtered_births.append((score, birth_text))
    
    # Sort by relevance score
    filtered_births.sort(reverse=True, key=lambda x: x[0])

    print("Number of filtered births:", len(filtered_births))  # Debug print
    
    return filtered_births

def death_sort(soup):
    death_section = soup.find(id="Deaths")                          # Go to Births Section
    death_section = death_section.find_next('ul').find_all('li')    # Find Each individual point

    # Filter Keywords
    keywords = {
        'physicist' : 5,
        'academic': 8,
        'composer': 10,
        'pianist': 11,
        'politician': 8,
    }

    # Filtering and scoring BIRTHS
    filtered_deaths = []
    for death in death_section:
        death_text = death.get_text()
        score = sum(weight for keyword, weight in keywords.items() if keyword in death_text)
        if score > 0:  # Arbitrary threshold
            filtered_deaths.append((score, death_text))
    
    # Sort by relevance score
    filtered_deaths.sort(reverse=True, key=lambda x: x[0])
    
    return filtered_deaths


def scrape_wikipedia_today(month, day):
    url = f"https://en.wikipedia.org/wiki/{month}_{day}"
    response = requests.get(url)

    # Soup to Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Sort and Section The Data
    event_list = event_sort(soup)
    birth_list = birth_sort(soup)
    death_list = death_sort(soup)

    return event_list, birth_list, death_list

def main():

    events, births, deaths = scrape_wikipedia_today(MONTH, DAY)

    print("Events")
    for score, event in events:
        print(f"Score: {score} | Event: {event}")

    print("\nBirths")
    for score, birth in births:
        print(f"Score: {score} | Birth: {birth}")

    print("\nDeaths")
    for score, death, in deaths:
        print(f"Score: {score} | Death: {death}")

if __name__ == "__main__":
    main()