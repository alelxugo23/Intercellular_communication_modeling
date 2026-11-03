import matplotlib.pyplot as plt
import networkx as nx


# Your running-total function (parameter renamed to avoid clashing with "nx").
def cricket_connections(n, nx_position):
    cricket_total_so_far = 0
    for position in range(nx_position, 0, -1):
        connections = n - position
        cricket_total_so_far = cricket_total_so_far + connections
    return cricket_total_so_far


def build_staircase(n):
    graph = nx.DiGraph()
    layout = {}

    for talker in range(1, n + 1):
        # Cricket node: a plain number, placed in the top row.
        graph.add_node(talker, kind="cricket")
        layout[talker] = (talker, 0)

        previous = talker  # the arrow chain starts at the cricket itself
        for listener in range(talker + 1, n + 1):
            square = (talker, listener)  # tuple name: (who talks, who listens)
            graph.add_node(square, kind="connection")

            # Column = talker. Depth = distance between the two crickets.
            layout[square] = (talker, -(listener - talker))

            graph.add_edge(previous, square)  # arrow from the square above
            previous = square

    return graph, layout


def draw_staircase(n, highlight=None):
    graph, layout = build_staircase(n)

    crickets = []
    squares = []
    for node, data in graph.nodes(data=True):
        if data["kind"] == "cricket":
            crickets.append(node)
        else:
            squares.append(node)

    # Yellow squares, or orange if they belong to the highlighted cricket.
    square_colors = []
    for talker, listener in squares:
        if talker == highlight:
            square_colors.append("darkorange")
        else:
            square_colors.append("gold")

    fig, ax = plt.subplots(figsize=(1.6 * n, 1.4 * n))

    # Plain lines between neighboring crickets in the top row (no arrowheads).
    for talker in range(1, n):
        ax.plot([talker, talker + 1], [0, 0], color="black", zorder=0)

    nx.draw_networkx_edges(graph, layout, ax=ax, arrowstyle="-|>",
                           node_shape="s", node_size=1400)
    nx.draw_networkx_nodes(graph, layout, nodelist=crickets, ax=ax,
                           node_shape="s", node_size=1400,
                           node_color="mediumvioletred", edgecolors="black")
    nx.draw_networkx_nodes(graph, layout, nodelist=squares, ax=ax,
                           node_shape="s", node_size=1400,
                           node_color=square_colors, edgecolors="black")

    # Labels: crickets show their number; squares show who they talk to.
    labels = {}
    for cricket in crickets:
        labels[cricket] = str(cricket)
    for talker, listener in squares:
        labels[(talker, listener)] = f"→{listener}"
    nx.draw_networkx_labels(graph, layout, labels=labels, ax=ax,
                            font_color="black", font_weight="bold")

    title = f"N = {n}: {len(squares)} connections  [n(n-1)/2 = {n * (n - 1) // 2}]"
    if highlight is not None:
        title += (f"\ncricket {highlight} makes {n - highlight} | "
                  f"total so far (1-{highlight}) = {cricket_connections(n, highlight)}")
    ax.set_title(title)
    ax.axis("off")
    plt.tight_layout()
    plt.show()


draw_staircase(5, highlight=2)
