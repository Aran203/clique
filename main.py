from app import *
import pandas as pd


def fetch_results(soup, filename, is_problem_set, solve, code = None):

    if not soup:
        inf = scrape_kattis_submissions(code)

        if not inf:
            raise ValueError(f"HTML content could not be obtained.\n\nCode provided is {code}")
        
        soup = inf[0]
    
    # If problem set or upsolve period, format of table remains same
    if (is_problem_set or not solve):
        results = process_submissions(soup, filename, 0, 1, 2)
    else:
        results = process_submissions(soup, filename, 1, 2, 4)
        

    return results


def main():

    print("Enter assignment code: ", end = "")
    code = input()

    info = scrape_kattis_submissions(code)
    if info:
        soup, is_solve, is_problem_set, OUT_FILENAME = info
    else:
        raise ValueError(f"HTML content could not be obtained.\n\nCode provided is {code}\n")

    
    # print("Enter file containing student names to process: ", end = "")
    # filename = input()
    filename = "data/roster/spring_25.txt"

    # Processing Upsolve Period
    if (not is_solve):
        print("Enter code for corresponding SOLVE period: ", end = "")
        solve_code = input()
        solve_results = fetch_results(None, filename, is_problem_set, True, code = solve_code)

        upsolve_raw = fetch_results(soup, filename, is_problem_set, False)
        results = {}

        for student in solve_results:
            upsolved_raw = set(upsolve_raw[student][1])
            solved = set(solve_results[student][1])

            all = upsolved_raw.union(solved)
            upsolved = all - solved

            # if upsolved != upsolved_raw:
            #     print(f'{student} {upsolved} {upsolve_raw}')
            
            results[student] = (len(upsolved), list(upsolved))
    else:
        results = fetch_results(soup, filename, is_problem_set, is_solve)


    # convert results to csv
    data = pd.DataFrame(parse_results(results))
    data.to_csv(f'{OUT_FILENAME}.csv', index = False)

    print(f"\nProcessing complete\n")
    


if __name__ == "__main__":
    main()