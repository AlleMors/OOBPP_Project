from pulp import *

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
                print("Line with weights:", repr(next_line))  # Debug print

                a = list(map(int, next_line.split('\t'))) if next_line else []

                break
    except Exception as e:
        print(f"Error while reading the file: {e}")
        N, b, a = None, None, []

    return N, b, a


if __name__ == '__main__':
    read_instance("../Instances/Instance10.txt")
    print("Number of elements (N):", N)
    print("Bin capacity (b):", b)
    print("Element weights (a_j):", a)

    ii = range(N)
    jj = range(N)

    model = LpProblem("OOEBP_Problem", LpMinimize)

    # y_i indicates if item i is the overflow item in its bin
    y = LpVariable.dicts("y", ii, cat="Binary")
    # x_ij indicates whether item i is assigned to the bin where the overflow item is j
    x = LpVariable.dicts("x", ((i, j) for i in ii for j in jj if j > i), cat="Binary")

    model += lpSum([y[i] for i in ii]), "Objective"

    for i in ii:
        model += y[i] + lpSum(x[i, j] for j in jj if j > i) == 1, f"OverflowItemConstraint_{i}"

    for j in jj:
        model += lpSum(a[i] * x[i, j] for i in ii if j > i) <= (b - 1) * y[j], f"AssignToOverflowBinConstraint_{j}"

    model.writeLP("OOBPP_Problem.lp")

    model.solve()
    print("Status:", LpStatus[model.status])

    # Dopo aver risolto il problema
    if LpStatus[model.status] == "Optimal":
        bin_contents = {}
        for i in ii:
            for j in range(i + 1, N):
                if value(x[i, j]) == 1:
                    if j not in bin_contents:
                        bin_contents[j] = []
                    bin_contents[j].append((i, a[i]))  # Aggiungi il valore dell'elemento al bin

        for bin_number, items in bin_contents.items():
            total_value = sum(item[1] for item in items)  # Calcola il valore totale del bin
            print(f"Bin {bin_number}: {items}, Valore Totale: {total_value}")
    else:
        print("Il problema non ha una soluzione ottimale.")
