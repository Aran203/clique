import requests
from bs4 import BeautifulSoup

# root url to scrape; change to fit semester in which course is taught
BASE_URL = "https://tamu.kattis.com/courses/CSCE430/2025Spring/assignments"

def scrape_kattis_submissions(code):
    try:
        url = f'{BASE_URL}/{code}/standings'
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        name = soup.find("h1").text.split("-")[1].strip()
        components = [el.lower() for el in name.split()]
        is_solve = is_problem_set = True

        if "upsolve" in components:
            is_solve = False 

        if "lab" in components:
            is_problem_set = False 

        out_filename = "_".join(components)

        return (soup, is_solve, is_problem_set, out_filename)

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    
    
def process_submissions(soup: BeautifulSoup, students, name_col, num_solved_col, problem_start_col, honors_problem = None):
    '''
        Args:
            soup: HTML content of kattis submissions
            students: dict of student names to process
            name_col: 0-based column number for the NAME in results table
            num_solved_col: 0-based column number for the NUMBER PROBLEMS SOLVED in results table
            problem_start_col: 0-based column number for the PROBLEM A in results table
    '''

    
    table = soup.find("table")
    rows = table.find_all("tr")

    for row in rows:
        counter = 0
        num_solved = None
        names = problems_solved = []

        for td in row.find_all("td"):
            # counter can be thought of similar to 0-indexed column number
            if counter == name_col:
                names = td.text.strip()
                names = [i.strip() for i in names.split(',')]

            elif counter == num_solved_col:
                num_solved = int(td.text.strip())
            elif counter >= problem_start_col:
                status = td.get("class", None)

                if status and status[0].strip() == "solved":
                    problems_solved.append(chr(counter + 65 - problem_start_col))
            counter += 1
    
        
        for name in names:
            if name in students:
                students[name] = (num_solved, problems_solved)

    return students

    
