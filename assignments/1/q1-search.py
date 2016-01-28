from collections import deque
import json
import Queue

# Returns solution path
# from start_node to end_node in list form.
# Returns false if no path exists.
def bfs(next_node, end_node):
    used = []
    used.append(next_node)

    q = deque([[next_node]])

    while len(q) > 0:
        path = q.popleft()
        last_node = path[-1]

        for neighbour, line in tree[last_node]:
            if neighbour not in used:
                new_path = list(path)
                new_path.append(neighbour)
                used.append(neighbour)
                if neighbour == end_node:
                    return(new_path)
                q.append(new_path)
    return(False)
    
# Check if this actually works
# Right now check if the nodes getting put in
# are strings or node tuples.
def ucs(next_node, end_node):
    used = []
    used.append(next_node)
    
    q = Queue.Queue()
    q = Queue.PriorityQueue(q)

    for neighbour, cost in tree[next_node]:
        if (neighbour, cost) not in used:
            q.put((cost, ([next_node], neighbour)))

    while not q.empty():
        b  = q.get()
        succ_cost = b[0]
        prev_path, succ_node = b[1]
        used.append((succ_node, succ_cost))

        if succ_node == end_node:
            return(prev_path + [end_node])

        for (neighbour, cost) in tree[succ_node]:
            if (neighbour, cost) not in used:
                q.put((cost, (prev_path+[succ_node], neighbour)))

    return(False)

def iterative_dfs(next_node, end_node):
    used = []
    used.append(next_node)
    stack = deque([[next_node]])
    while len(stack) > 0:
        path = stack.pop()
        last_elem = path[-1]
        for new_node, line in reversed(tree[last_elem]):
            if new_node in used:
                continue
            new_path = list(path)
            used.append(new_node)
            new_path.append(new_node)
            if new_node == end_node:
                return(new_path)
            stack.append(new_path)
    return([])

def dls(next_node, end_node, max_depth):
    used = []
    used.append(next_node)
    stack = deque([[next_node]])
    while len(stack) > 0:
        path = stack.pop()
        last_elem = path[-1]
        if len(path) <= max_depth+1:
            for new_node, line in reversed(tree[last_elem]):
                if new_node in used:
                    continue
                new_path = list(path)
                used.append(new_node)
                new_path.append(new_node)
                if new_node == end_node:
                    return(new_path)
                stack.append(new_path)
    return([])

def ids(next_node, end_node, depth=1):
    a = dls(next_node, end_node, depth)
    if a:
        return(a)
    else:
        return(ids(next_node, end_node, depth=depth+1))

if __name__ == "__main__":
    # First we construct the tree, implemented with a Python dictionary.
    # Keys are nodes, and the values associated with the keys are lists of
    # 
    tree = {}
    f = open("brussels_metro.json","r")
    j = json.load(f)
    f.close()
    stations = j["stations"]
    for station in stations:
        tree[station["name"]] = []
        for n in station["neighbours"]:
            if any(c == n["line"] for c in [1, 2, 3]):
                cost = 2
            else:
                cost = 1
            tree[station["name"]].append((n["name"],cost))

    start_node = "Gare du Nord"
    end_node = "Roi Baudouin"

    # Now we apply our functions.
    bfs_result = bfs(start_node, end_node)
    ucs_result = ucs(start_node, end_node)
    dfs_result = iterative_dfs(start_node, end_node)
    ids_result = ids(start_node, end_node)
    print("BFS: " + ", ".join(bfs_result) + "\n")
    print("UCS: " + ", ".join(ucs_result) + "\n")
    print("DFS: " + ", ".join(dfs_result) + "\n")
    print("IDS: " + ", ".join(ids_result) + "\n")
