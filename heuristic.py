class Bin:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add(self, weight):
        self.capacity -= weight
        self.items.append(weight)


def read_input_from_file(filename):
    with open(filename, 'r') as file:
        # Funzione helper per leggere la prossima riga non commentata e non vuota
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
    a_sorted = sorted(a, reverse=True)
    bins = [Bin(b)]
    i = 0

    for item in a_sorted:
        if bins[i].capacity > 0:
            bins[i].add(item)
        else:
            bins.append(Bin(b))
            i += 1

    return bins


def main():
    N, bin_capacity, item_weights = read_input_from_file("Instances/Instance200.txt")
    bins = first_fit(N, bin_capacity, item_weights)
    print(f'Number of bins used: {len(bins)}')

    for bin in bins:
        print("Bin Capacity:", bin.capacity)
        print(f"Items in Bin:", bin.items)


# Ora, chiama le funzioni:
if __name__ == "__main__":
    main()
