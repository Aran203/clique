
def parse_results(results: dict):
    dat = []

    for student, info in results.items():
        num_solved = info[0]
        # problems = info[1]

        # if problems:
        #     problems = ";".join(problems)
        # else:
        #     problems = None

        dat.append({"Name": student, "Number Solved": num_solved})
        
    return dat