from app import *

# root url to scrap; change to fit semester in which course is taught
BASE_URL = "https://tamu.kattis.com/courses/CSCE430/2025Spring/assignments"


def main():
    print("Enter assignment code: ", end = "")
    code = input()

    print("Enter file containing student names to process: ", end = "")
    filename = input()

    print("Enter assignment period (upsolve/solve): ", end = "")
    type = input()

    URL = f'{BASE_URL}/{code}/standings'

    soup = scrape_kattis_submissions(URL)
    process_solve_period(soup, filename)

    


if __name__ == "__main__":
    main()