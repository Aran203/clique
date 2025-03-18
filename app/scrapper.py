import requests
from bs4 import BeautifulSoup

def scrape_kattis_submissions(url):

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    
def process_solve_period(soup: BeautifulSoup, filename):

    student_info = {}

    with open(filename) as f:
        for row in f.readlines():
            student_info[row.strip()] = None 


    table = soup.find("table")
    rows = table.find_all("tr")


    for row in rows:
        counter = 0
        name = num_solved = None
        problems_solved = []

        for td in row.find_all("td"):
            # counter can be thought of similar to 0-indexed column number
            # col 0 is name; col 1 is num solved
            if counter == 0:
                name = td.text.strip()
            elif counter == 1:
                num_solved = int(td.text.strip())
            else:
                status = td.get("class", None)

                if status and status[0].strip() == "solved":
                    problems_solved.append(chr(counter + 63))
            counter += 1
    

        if name and name in student_info:
            student_info[name] = (num_solved, problems_solved)


    for name in student_info:
        print(f'{name}: {student_info[name]}')
    



