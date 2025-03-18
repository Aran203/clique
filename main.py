from app import *
import pandas as pd

# root url to scrap; change to fit semester in which course is taught
BASE_URL = "https://tamu.kattis.com/courses/CSCE430/2025Spring/assignments"


def fetch_results(code, filename):
    URL = f'{BASE_URL}/{code}/standings'

    soup = scrape_kattis_submissions(URL)

    if not soup:
        raise ValueError(f"HTML content could not be obtained.\n\nCode provided is {code}\nURL scraped is {URL}")
    
    results = process_solve_period(soup, filename)

    return results


def main():
    print("Enter assignment code: ", end = "")
    code = input()

    print("Enter file containing student names to process: ", end = "")
    filename = input()

    print("Enter assignment period (upsolve/solve): ", end = "")
    type = input()

    if (type.lower() != "solve"):
        print("Enter code for corresponding solve period: ", end = "")
        solve_code = input()

        upsolve_raw = fetch_results(code, filename)
        solve_results = fetch_results(solve_code, filename)
        results = {}

        for student in solve_results:
            upsolved_raw = set(upsolve_raw[student][1])
            solved = set(solve_results[student][1])

            all = upsolved_raw.union(solved)
            upsolved = all - solved
            results[student] = (len(upsolved), list(upsolved))
    else:
        results = fetch_results(code, filename)


    data = pd.DataFrame(parse_results(results))
    data.to_csv(f'{code}_results.csv', index = False)

    print(f"\nProcessing complete\n")
    


if __name__ == "__main__":
    main()