def cricket_connections(n, nx):
    number_line = list(range(1, n + 1))
    print(number_line)

    cricket_in_number_line = number_line.index(nx)

    connections = n - (cricket_in_number_line + 1)
    return connections


print(cricket_connections(5, 3))