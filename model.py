from pulp import *
import time

N = None  # Number of elements
b = None  # Bin capacity
a = []  # List to store element weights


# Function to read the input instance from a file
def read_instance(file_path):
    global N, b, a

    try:
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()

        line_iterator = iter(lines)

        for line in line_iterator:
            if line.startswith("#N"):
                N = int(next(line_iterator))
            elif line.startswith("#b"):
                b = int(next(line_iterator))
            elif line.startswith("#a_j"):
                next_line = next(line_iterator)

                a = list(map(int, next_line.split('\t'))) if next_line else []
                print(len(a))

                break
    except Exception as e:
        print(f"Error while reading the file: {e}")
        N, b, a = None, None, []

    return N, b, a


if __name__ == '__main__':
    instance = "../Instances/Instance50.txt"
    read_instance(instance)
    print("Number of elements (N):", N)
    print("Bin capacity (b):", b)
    print("Element weights (a_j):", a)

    ii = range(N)
    jj = range(N)

    model = LpProblem("OOEBP_Problem", LpMinimize)

    time_limit = 300

    model.solver = PULP_CBC_CMD(timeLimit=time_limit)

    # y_i indicates if item i is the overflow item in its bin
    y = LpVariable.dicts("y", ii, cat="Binary")
    # x_ij indicates whether item i is assigned to the bin where the overflow item is j
    x = LpVariable.dicts("x", ((i, j) for i in ii for j in jj if j > i), cat="Binary")

    model += lpSum([y[i] for i in ii]), "Objective"

    for i in ii:
        model += y[i] + lpSum([x[i, j] for j in jj if j > i]) == 1, f"OverflowItemConstraint_{i}"

    for j in jj:
        model += lpSum([a[i] * x[i, j] for i in ii if j > i]) <= (b - 1) * y[j], f"AssignToOverflowBinConstraint_{j}"

    model.writeLP("OOBPP_Problem.lp")
    start_time = time.perf_counter()
    model.solve()
    stop_time = time.perf_counter()

    solve_time = stop_time - start_time

    print("Status:", LpStatus[model.status])

    with open("model_output.txt", "w") as output_file:
        output_file.write(f"Instance Path: {instance}\n")
        output_file.write(f"Status: {LpStatus[model.status]}\n")
        output_file.write(f"Objective Value: {value(model.objective)}\n")

        bin_contents = {}

        for i in ii:
            in_overflow = False
            for j in range(i + 1, N):
                if value(x[i, j]) == 1:
                    if j not in bin_contents:
                        bin_contents[j] = []
                    bin_contents[j].append((i, a[i]))
                    in_overflow = True

            if not in_overflow:
                if i not in bin_contents:
                    bin_contents[i] = [(i, a[i])]
                else:
                    bin_contents[i].append((i, a[i]))

        for bin_number, items in bin_contents.items():
            output_file.write(f"Bin {bin_number}: {items}\n")

        output_file.write(f"Solving time: {solve_time}")
