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
def bfs(start_node, end_node):
    used = []
    used.append(start_node)

    q = deque([[start_node]])

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
    
def dfs(start_node, end_node, used=[]):
    new_used = list(used)
    new_used.append(start_node)
    if all(p in new_used for p in tree[start_node]) and start_node == end_node:
        return([end_node])
    elif all(p in new_used for p in tree[start_node]):
        raise NoNodeFoundError(start_node)
    else:
        for p in tree[start_node]:
            if p not in new_used:
                try:
                    return([start_node] + dfs(p, end_node, new_used))
                except NoNodeFoundError as e:
                    print("No more neighbours at: " + str(e))
                    continue
                except TypeError:
                    continue

def ids(node, end_node):
    pass

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

    # Now we apply our functions.
    bfs_result = bfs("Gare du Nord", "Roi Baudouin")
    dfs_result = dfs("Gare du Nord", "Roi Baudouin")
    print("BFS: " + ", ".join(bfs_result))
    print("UCS: " + ", ".join(bfs_result))
    print("DFS: " + ", ".join(dfs_result))
