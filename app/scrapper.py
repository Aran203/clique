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
    
def process_problem_set(soup: BeautifulSoup, filename):
    '''returns a dict mapping each student to (number of problems solved, which problems they solved) for a problem set'''

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

    
    return student_info
    
def process_lab(soup: BeautifulSoup, filename):
    '''returns a dict mapping each student to (number of problems solved, which problems they solved) for lab'''

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
            
            # col 1 is name; col 2 is num solved, col 4 -> end are problems
            if counter == 1:
                name = td.text.strip()
            elif counter == 2:
                num_solved = int(td.text.strip())
            elif counter >= 4:
                status = td.get("class", None)

                if status and status[0].strip() == "solved":
                    problems_solved.append(chr(counter + 61))
            counter += 1
    

        if name and name in student_info:
            student_info[name] = (num_solved, problems_solved)

    
    return student_info
    



