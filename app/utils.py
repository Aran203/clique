
def parse_results(results: dict):
    dat = []

    for student, info in results.items():
        if info:
            num_solved = info[0]
        else:
            num_solved = 0
        # problems = info[1]

        # if problems:
        #     problems = ";".join(problems)
        # else:
        #     problems = None

        dat.append({"Name": student, "Number Solved": num_solved})
        
    return dat