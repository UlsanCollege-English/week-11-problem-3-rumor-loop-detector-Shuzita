"""
HW03 — Rumor Loop Detector (Cycle in Undirected Graph)

Implement:
- has_cycle(graph)
- find_cycle(graph)
"""


def has_cycle(graph):
    """Return True if the undirected graph has any cycle; else False."""
    visited = set()

    for start in graph:
        if start not in visited:
            if _dfs_has_cycle(graph, start, visited, parent=None):
                return True
    return False


def _dfs_has_cycle(graph, u, visited, parent):
    """Helper DFS for has_cycle."""
    visited.add(u)

    for v in graph[u]:
        # Self-loop
        if v == u:
            return True

        if v not in visited:
            if _dfs_has_cycle(graph, v, visited, u):
                return True
        elif v != parent:
            # Found a back-edge in undirected graph
            return True

    return False


def find_cycle(graph):
    """Return a list of nodes forming a simple cycle with first == last.
    If no cycle, return None.
    Self-loop: return [u, u].
    """

    visited = set()

    for start in graph:
        if start not in visited:
            parent = {start: None}
            cycle = _dfs_find_cycle(graph, start, visited, parent)
            if cycle is not None:
                return cycle

    return None


def _dfs_find_cycle(graph, u, visited, parent):
    """Helper DFS that returns cycle list if found."""
    visited.add(u)

    for v in graph[u]:

        # Self-loop
        if v == u:
            return [u, u]

        if v not in visited:
            parent[v] = u
            cycle = _dfs_find_cycle(graph, v, visited, parent)
            if cycle is not None:
                return cycle

        elif parent[u] != v:
            # Found a cycle: reconstruct path u -> ... -> v
            return _reconstruct_cycle(parent, u, v)

    return None


def _reconstruct_cycle(parent, u, v):
    """
    Return cycle: path from u up to root, and path from v up to root,
    merging at LCA; final list ends with the starting node.
    """
    # Build ancestor chain for u
    path_u = []
    x = u
    while x is not None:
        path_u.append(x)
        x = parent[x]

    # Build ancestor chain for v
    path_v = []
    y = v
    while y is not None:
        path_v.append(y)
        y = parent[y]

    # Convert to sets for LCA search
    set_u = set(path_u)

    # Find first ancestor of v that appears in u's chain
    lca = None
    for node in path_v:
        if node in set_u:
            lca = node
            break

    # Build cycle: u → ... → lca → ... → v → u
    # Get part from u down to lca
    cycle_u = []
    for node in path_u:
        cycle_u.append(node)
        if node == lca:
            break

    # Get part from v down to lca (reverse it)
    cycle_v = []
    for node in path_v:
        cycle_v.append(node)
        if node == lca:
            break
    cycle_v.reverse()

    cycle = cycle_u + cycle_v[1:]  # skip duplicate LCA
    cycle.append(cycle[0])  # close the loop

    return cycle
