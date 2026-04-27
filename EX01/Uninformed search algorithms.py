from collections import deque
import heapq

class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = []
            print(f"Node '{node}' added.")
        else:
            print(f"Node '{node}' already exists.")

    def add_edge(self, node1, node2, weight=1):
        if node1 not in self.adj_list or node2 not in self.adj_list:
            print("One or both nodes do not exist. Add them first.")
            return
        # Check if edge already exists
        if any(neighbor == node2 for neighbor, w in self.adj_list[node1]):
            print(f"Edge between '{node1}' and '{node2}' already exists.")
            return
        self.adj_list[node1].append((node2, int(weight)))
        self.adj_list[node2].append((node1, int(weight)))
        print(f"Edge between '{node1}' and '{node2}' with weight {weight} added.")

    def delete_node(self, node):
        if node in self.adj_list:
            # Remove the node from all other nodes' adjacency lists
            for n in self.adj_list:
                self.adj_list[n] = [item for item in self.adj_list[n] if item[0] != node]
            del self.adj_list[node]
            print(f"Node '{node}' deleted.")
        else:
            print(f"Node '{node}' not found.")

    def delete_edge(self, node1, node2):
        if node1 in self.adj_list and node2 in self.adj_list:
            original_len = len(self.adj_list[node1])
            self.adj_list[node1] = [item for item in self.adj_list[node1] if item[0] != node2]
            self.adj_list[node2] = [item for item in self.adj_list[node2] if item[0] != node1]
            if len(self.adj_list[node1]) < original_len:
                print(f"Edge between '{node1}' and '{node2}' deleted.")
            else:
                print("Edge does not exist.")
        else:
            print("One or both nodes do not exist.")

    def delete_graph(self):
        self.adj_list = {}
        print("Graph has been cleared/deleted.")


    def display(self):
        print("\nGraph Structure:")
        if not self.adj_list:
            print("Graph is empty.")
        for node, neighbors in self.adj_list.items():
            print(f"{node} -> {neighbors}")

    def display_node_adjacency(self):
        node = input("Enter the node to display its adjacency: ")
        if node not in self.adj_list:
            print(f"Node '{node}' does not exist.")
            return
        print(f"Neighbors of node '{node}': {self.adj_list[node]}")

    def create_graph_explicitly(self):
        print("Enter nodes separated by spaces (e.g. A B C):")
        nodes = input().split()
        for node in nodes:
            self.add_node(node)
        print("Enter edges as 'node1 node2 weight', separated by commas (e.g. A B 5, B C 10):")
        edges_input = input()
        if edges_input.strip():
            edges = [e.strip().split() for e in edges_input.split(",")]
            for edge in edges:
                if len(edge) == 3:
                    self.add_edge(edge[0], edge[1], edge[2])
                elif len(edge) == 2:
                    self.add_edge(edge[0], edge[1], 1)

    def bfs_path(self, start, goal, direction="1"):
        if start not in self.adj_list or goal not in self.adj_list: return
        frontier = deque([start])
        explored, parent = [], {start: None}
        print("\nIter | Fringe | Explored\n" + "-"*40)
        while frontier:
            print(f"{len(explored)+1:>4} | {list(frontier)} | {explored}")
            node = frontier.popleft()
            if node not in explored:
                explored.append(node)
                if node == goal: return self._print_res(parent, goal, explored, "BFS")

                # "1" = Left to Right (Ascending), "2" = Right to Left (Descending)
                rev = True if direction == "2" else False
                neighbors = sorted([n for n, w in self.adj_list[node]], reverse=rev)

                for neighbor in neighbors:
                    if neighbor not in parent and neighbor not in explored:
                        parent[neighbor] = node
                        frontier.append(neighbor)


    def dfs_path(self, start, goal, direction="1"):
        if start not in self.adj_list or goal not in self.adj_list: return
        stack = [start]
        explored, parent = [], {start: None}
        print("\nIter | Stack | Explored\n" + "-"*40)
        while stack:
            print(f"{len(explored)+1:>4} | {stack} | {explored}")
            node = stack.pop()
            if node not in explored:
                explored.append(node)
                if node == goal: return self._print_res(parent, goal, explored, "DFS")

                # For L->R: Push Right first so Left is on top (Reverse=True)
                # For R->L: Push Left first so Right is on top (Reverse=False)
                rev = False if direction == "2" else True
                neighbors = sorted([n for n, w in self.adj_list[node]], reverse=rev)

                for neighbor in neighbors:
                    if neighbor not in explored:
                        parent[neighbor] = node
                        stack.append(neighbor)

    def _print_res(self, parent, goal, explored, alg, cost=None):
        path, temp = [], goal
        while temp is not None:
            path.append(temp)
            temp = parent[temp]
        print(f"\nExplored Order: {explored}")
        print(f"Correct {alg} Path: {' -> '.join(path[::-1])}" + (f" | Total Cost: {cost}" if cost is not None else ""))

def menu():
    graph = Graph()
    while True:
        print("\nMenu:")
        print("1. Add Node\n2. Add Edge\n3. Delete Node\n4. Delete Edge\n5. Display Graph")
        print("6. Create Graph Explicitly\n7. Display Node Adjacency\n8. BFS Traversal\n9. DFS Traversal\n10. UCS Traversal\n11. Delete Graph\n0. Exit")
        choice = input("Enter your choice: ")
        if choice == '1': graph.add_node(input("Node: "))
        elif choice == '2': graph.add_edge(input("N1: "), input("N2: "), input("Weight: "))
        elif choice == '3': graph.delete_node(input("Node: "))
        elif choice == '4': graph.delete_edge(input("N1: "), input("N2: "))
        elif choice == '5': graph.display()
        elif choice == '6': graph.create_graph_explicitly()
        elif choice == '7': graph.display_node_adjacency()
        elif choice in ['8', '9', '10']:
            s, g = input("Start: "), input("Goal: ")
            if choice == '8': graph.bfs_path(s, g, input("1) L-R 2) R-L: "))
            elif choice == '9': graph.dfs_path(s, g, input("1) L-R 2) R-L: "))
            elif choice == '10': graph.ucs_path(s, g)
        elif choice == '11': graph.delete_graph()
        elif choice == '0': break

if __name__ == "__main__":
    menu()