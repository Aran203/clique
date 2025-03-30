from app import *
import pandas as pd

# root url to scrape; change to fit semester in which course is taught
BASE_URL = "https://tamu.kattis.com/courses/CSCE430/2025Spring/assignments"


def fetch_results(code, filename, is_problem_set, solve):
    URL = f'{BASE_URL}/{code}/standings'

    soup = scrape_kattis_submissions(URL)

    if not soup:
        raise ValueError(f"HTML content could not be obtained.\n\nCode provided is {code}\nURL scraped is {URL}")
    
    if (is_problem_set):
        results = process_submissions(soup, filename, 0, 1, 2)
    else:
        if (solve):
            results = process_submissions(soup, filename, 1, 2, 4)
        else:
            results = process_submissions(soup, filename, 0, 1, 2)

    return results


def main():
    print("Is assignment being processed a problem set? (yes/no) ", end = "")
    is_problem_set = input().lower() 

    if ("yes" in is_problem_set or "y" in is_problem_set):
        is_problem_set = True
    else:
        is_problem_set = False

    print("Enter assignment code: ", end = "")
    code = input()

    print("Enter file containing student names to process: ", end = "")
    filename = input()

    print("Is assignment being processed for SOLVE period? (yes/no) ", end = "")
    is_solve = input().lower()

    if ("yes" in is_solve or "y" in is_solve):
        is_solve = True
    else:
        is_solve = False



    # Processing Upsolve Period
    if (not is_solve):
        print("Enter code for corresponding SOLVE period: ", end = "")
        solve_code = input()

        upsolve_raw = fetch_results(code, filename, is_problem_set, False)
        solve_results = fetch_results(solve_code, filename, is_problem_set, True)
        results = {}

        for student in solve_results:
            upsolved_raw = set(upsolve_raw[student][1])
            solved = set(solve_results[student][1])

            all = upsolved_raw.union(solved)
            upsolved = all - solved
            results[student] = (len(upsolved), list(upsolved))
    else:
        results = fetch_results(code, filename, is_problem_set, is_solve)


    # convert results to csv
    data = pd.DataFrame(parse_results(results))
    data.to_csv(f'{code}_results.csv', index = False)

    print(f"\nProcessing complete\n")
    


if __name__ == "__main__":
    main()