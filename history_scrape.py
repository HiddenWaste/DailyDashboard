import requests
from bs4 import BeautifulSoup

KEYWORDS = {
    'physicist': 5,
    'academic': 8,
    'composer': 7,
    'politician': 4,
    'pianist': 11,
    'author': 7,
    'poet': 4,
    'emporer': 7,
    'emperor': 7,
    'empress': 7,
    'king': 7,
    'queen': 7,
    'prince': 7,
    'princess': 7,
    'actor': 4,
    'actress': 4,
    'nobel': 6,
}

def event_sort(soup):
    # Grab the Events Section on the Page
    events_section = soup.find(id="Events")
    events_list = events_section.find_next('ul').find_all('li')

    # Events specific keywords and weights
    keywords = {
        # Some General Words
        'independence': 10,
        'revolution': 8,
        'diplomacy': 4,
        'treaty': 7,

        # Country Specific
        'Roman' : 5,
        'Japan': 8,
        'United States': 10,
        'Mexico': 6,

        # War Specific
        'World War II': 5,
        'Cold War': 5,
        'Vietnam War': 6,
        'Civil War': 6,
        
        # Title Specific
        'King':7,
        'Queen':7,
        'Emporer':7,
        'Empress':7,
        'President':9,

        # Person Specific
        'Nixon': 3,
        'Kennedy': 5,
        'Reagan': 6,
        'Carter': 4
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

    all_birth_entries = []  # Initialize list to store all birth entries

    # Loop to capture the `li` elements from the next three `ul` lists
    for _ in range(3):
        if birth_section:
            birth_section = birth_section.find_next('ul')  # Move to the next `ul` list
            if birth_section:
                all_birth_entries.extend(birth_section.find_all('li'))  # Extract all `li` elements

    # Filtering and scoring BIRTHS
    filtered_births = []
    for birth in all_birth_entries:
        birth_text = birth.get_text().lower()  # Normalize for matching
        # print("Birth text:", birth_text)  # Debug print
        score = sum(weight for keyword, weight in KEYWORDS.items() if keyword in birth_text)
        if score > 6:  # Threshold for relevance
            filtered_births.append((score, birth_text))
    
    # Sort by relevance score
    filtered_births.sort(reverse=True, key=lambda x: x[0])

    # # Final Debug print
    # print("Total number of birth entries found:", len(all_birth_entries))
    # print("Number of filtered births:", len(filtered_births))
    
    return filtered_births

def death_sort(soup):
    death_section = soup.find(id="Deaths")                          # Go to Births Section

    all_death_entries = []  # Initialize list to store all death entries

    # Loop to capture the `li` elements from the next three `ul` lists
    for _ in range(3):
        if death_section:
            death_section = death_section.find_next('ul')  # Move to the next `ul` list
            if death_section:
                all_death_entries.extend(death_section.find_all('li'))  # Extract all `li` elements
    
    # Filter Keywords
    keywords = KEYWORDS

    # Filtering and scoring BIRTHS
    filtered_deaths = []
    for death in death_section:
        death_text = death.get_text()
        score = sum(weight for keyword, weight in keywords.items() if keyword in death_text)
        if score > 5:  # Arbitrary threshold
            filtered_deaths.append((score, death_text))
    
    # Sort by relevance score
    filtered_deaths.sort(reverse=True, key=lambda x: x[0])

    # # Debug print to check the number of entries found
    # print("Total number of death entries found:", len(all_death_entries))
    # print("Number of filtered deaths:", len(filtered_deaths))
    
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

def create_history_content(events, births, deaths):
    markdown_content = f"# Today In History!!\n\n"

    markdown_content += "## Events\n\n"
    for score, event in events:
        markdown_content += f"**{score}** - {event}\n\n"

    markdown_content += "## Births\n\n"
    for score, birth in births:
        markdown_content += f"**{score}** - {birth}\n\n"

    markdown_content += "## Deaths\n\n"
    for score, death in deaths:
        markdown_content += f"**{score}** - {death}\n\n"

    return markdown_content