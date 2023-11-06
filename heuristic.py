import time


class Bin:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add(self, weight):
        self.capacity -= weight
        self.items.append(weight)


def read_input_from_file(filename):
    with open(filename, 'r') as file:
        def get_next_valid_line():
            line = file.readline().strip()
            while not line or line.startswith('#'):
                line = file.readline().strip()
            return line

        # Leggi N
        N = int(get_next_valid_line())

        # Leggi b
        b = int(get_next_valid_line())

        # Leggi i pesi a_j
        a = list(map(int, get_next_valid_line().split()))

    return N, b, a


def first_fit(N, b, a):
    print(a)
    print(b)
    print(N)
    bins = [Bin(b)]
    i = 0

    for item in a:
        if bins[i].capacity > 0:
            bins[i].add(item)
        else:
            bins.append(Bin(b))
            i += 1
            bins[i].add(item)

    return bins


def main():
    instance = "../Instances/Instance200.txt"
    N, bin_capacity, item_weights = read_input_from_file(instance)
    start_time = time.perf_counter()
    bins = first_fit(N, bin_capacity, item_weights)
    end_time = time.perf_counter()
    print(f"Time: {end_time - start_time}")
    print(f'Number of bins used: {len(bins)}')

    with open("output.txt", "w") as output_file:
        output_file.write(f"Instance Path: {instance}\n")
        output_file.write(f"Status: Heuristic Solution\n")
        output_file.write(f"Objective Value: {len(bins)}\n")
        for bin in bins:
            output_file.write(f"Items in Bin: {bin.items}\n")
        output_file.write(f"Solving Time: {end_time-start_time}")


if __name__ == "__main__":
    main()
