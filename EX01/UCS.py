from collections import deque
import heapq

def ucs_path(self, start, goal):
        if start not in self.adj_list or goal not in self.adj_list:
            print("Goal or start not found")
            return

        # frontier stores: (cost, current_node, path_list)
        frontier = [(0, start, [start])]
        explored_set = set()
        explored_order = []
        itr = 1

        print("\nIter | Frontier (Cost, Node, Path) | Explored")
        print("-" * 70)

        while frontier:

            print(f"{itr:>4} | {sorted(frontier)} | {explored_order}")
            itr += 1

            cost, node, path = heapq.heappop(frontier)

            if node == goal:
                explored_order.append(node) # Add goal to explored before finishing
                print(f"\nExplored Order: {explored_order}")
                print(f"Optimal UCS Path: {' -> '.join(path)} | Total Cost: {cost}")
                return

            if node not in explored_set:
                explored_set.add(node)
                explored_order.append(node) # This is the correct moment of exploration

                for neighbor, weight in self.adj_list[node]:
                    if neighbor not in explored_set:
                        new_cost = cost + weight
                        new_path = path + [neighbor]

                        found_in_frontier = False
                        for i, (f_cost, f_node, f_path) in enumerate(frontier):
                            if f_node == neighbor:
                                found_in_frontier = True
                                if new_cost < f_cost:
                                    frontier[i] = (new_cost, neighbor, list(new_path))
                                    heapq.heapify(frontier)
                                break

                        if not found_in_frontier:
                            heapq.heappush(frontier, (new_cost, neighbor, new_path))

        print("Error: Goal not reachable")

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
