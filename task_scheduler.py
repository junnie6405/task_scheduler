import fileinput
from collections import defaultdict
from collections import deque

# Read tasks data that has priorities ranked as int, and return a graph.

def read_graph():
    dic, cntr = defaultdict(list), defaultdict(int)
    vertices = set()
    # Process each line in standard input.
    for line in fileinput.input():
        # Split the current line into tokens, and remove the trailing newline.
        tokens = line.rstrip().split(',')
        if tokens[0] == tokens[-1]:
            vertices.add(tokens[0])
        else:
            dic[tokens[1]].append(tokens[0])
            cntr[tokens[0]] += 1
    return dic, cntr, vertices


#if there is a cycle, a task can never be completed. 
def dfs(cycle, cur_node, dic, visited):
    for edge in dic[cur_node]:
        if edge in cycle:
            return cycle
        if edge not in visited:
            visited.add(cur_node)
            cycle.add(edge)
            cycle_set = dfs(cycle, edge, dic, visited)
            if cycle_set:
                return cycle_set
            cycle.remove(edge)
    return {}

def topological_sort(dic, cntr, vertices):
    deq = deque()
    visited = set()
    topological_order = []
    if not vertices:
        return {}
    for vertex in vertices:
        if vertex not in cntr:
            deq.append(vertex)
    # check point - if there is nothing in the deque to begin with, we are done.

    if not deque:
        print("there is nothing to begin with. Prob cycle ")
        # or it could be a cycle in the graph.
        return {}

    while deq:
        cur_vertex = deq.popleft()
        topological_order.append(cur_vertex)
        visited.add(cur_vertex)
        for edge in dic[cur_vertex]:
            cntr[edge] -= 1
            if edge not in visited and cntr[edge] == 0:
                deq.append(edge)

    if len(topological_order) == len(vertices):
        return topological_order

    else:  # there must be a cycle
        for v in vertices:
            if v not in visited:  # let's see if this node has a cycle.v
                visited.add(v)
                cycle_set = dfs({v}, v, dic, visited)
                if cycle_set:
                    print("Task schedule:")
                    return cycle_set

def main():
    dic, cntr, vertices = read_graph()
    solution = topological_sort(dic, cntr, vertices)
    print(solution)
    for file in solution:
        print(file)

main()