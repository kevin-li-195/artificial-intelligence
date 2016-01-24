from collections import deque
import json

class NoNodeFoundError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return(repr(self.value))

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

        for neighbour in tree[last_node]:
            if neighbour not in used:
                new_path = list(path)
                new_path.append(neighbour)
                used.append(neighbour)
                if neighbour == end_node:
                    return(new_path)
                q.append(new_path)
    return(False)
    
def recursive_dfs(next_node, end_node, used=[]):
    new_used = list(used)
    new_used.append(next_node)
    if next_node == end_node:
        return([end_node])
    elif all(p in new_used for p in tree[next_node]):
        raise NoNodeFoundError(next_node)
    else:
        for p in tree[next_node]:
            if p not in new_used:
                try:
                    return([next_node] + dfs(p, end_node, used=new_used))
                except NoNodeFoundError as e:
                    print("No more neighbours at: " + str(e))
                    continue
                except TypeError:
                    continue

def iterative_dfs(next_node, end_node):
    used = []
    used.append(next_node)
    stack = deque([[next_node]])
    while len(stack) > 0:
        path = stack.pop()
        last_elem = path[-1]
        for new_node in reversed(tree[last_elem]):
            if new_node in used:
                continue
            new_path = list(path)
            used.append(new_node)
            new_path.append(new_node)
            if new_node == end_node:
                return(new_path)
            stack.append(new_path)

def ids(next_node, end_node):
    for a in range(0,900):
        b = dfs(next_node, end_node)
        print("IDS Result: " + str(b))
    #if a:
    #    return(a)
    #else:
    #    return(ids(next_node, end_node, max_depth=max_depth+1))

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
            if n["name"] not in tree[station["name"]]:
                tree[station["name"]].append(n["name"])

    start_node = "Gare du Nord"
    end_node = "Roi Baudouin"

    # Now we apply our functions.
    bfs_result = bfs(start_node, end_node)
    dfs_result = iterative_dfs(start_node, end_node)
    #ids_result = ids(start_node, end_node)
    print("BFS: " + ", ".join(bfs_result))
    print("UCS: " + ", ".join(bfs_result))
    print("DFS: " + ", ".join(dfs_result))
    #print("Result: " + str(ids_result))
