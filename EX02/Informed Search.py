def get_heuristic(self, goal):
        heuristic = {}
        print(f"\nEnter heuristic values h(n) for goal '{goal}':")
        for node in self.adj_list:
            if node == goal:
                heuristic[node] = 0
            else:
                h = int(input(f"h({node}) = "))
                heuristic[node] = h
        return heuristic

    def astar_path(self, start, goal):
        if start not in self.adj_list or goal not in self.adj_list:
            print("Start or goal not in graph")
            return

        heuristic = self.get_heuristic(goal)

        # fringe stores: (f, g, current_node, path)
        fringe = [(heuristic[start], 0, start, [start])]
        explored_set = set()
        explored_order = []
        itr = 1

        print("\nItr | Fringe(f, g, node, path) | Explored Order")
        print("-" * 75)

        while fringe:
            print(f"{itr:>3} | {sorted(fringe)} | {explored_order}")
            itr += 1

            f, g, node, path = heapq.heappop(fringe)

            if node not in explored_set:
                explored_order.append(node)
                explored_set.add(node)

                if node == goal:
                    print(f"\nExplored Order: {explored_order}")
                    print(f"A* Path: {' -> '.join(path)}")
                    print(f"Total Cost (g): {g}")
                    return

                for child, cost in self.adj_list[node]:
                    if child not in explored_set:
                        new_g = g + cost
                        new_f = new_g + heuristic[child]
                        new_path = path + [child]

                        # Handle updating fringe if better path is found
                        better_path_exists = False
                        for i, (of, og, on, op) in enumerate(fringe):
                            if on == child:
                                if og <= new_g:
                                    better_path_exists = True
                                else:
                                    fringe[i] = (new_f, new_g, child, new_path)
                                    heapq.heapify(fringe)
                                    better_path_exists = True
                                break

                        if not better_path_exists:
                            heapq.heappush(fringe, (new_f, new_g, child, new_path))

        print("Goal not reachable")

def main():
    g = Graph()
    while True:
        print("\n--- A* Graph Menu ---")
        print("1. Add Node")
        print("2. Add Edge")
        print("3. Delete Node")
        print("4. Display Graph")
        print("5. Create Graph Explicitly")
        print("6. Run A* Search")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            node = input("Enter node name: ")
            g.add_node(node)
        elif choice == '2':
            data = input("Enter 'node1 node2 weight': ").split()
            if len(data) == 3:
                g.add_edge(data[0], data[1], data[2])
            else:
                print("Invalid input.")
        elif choice == '3':
            node = input("Enter node to delete: ")
            g.delete_node(node)
        elif choice == '4':
            g.display()
        elif choice == '5':
            g.create_graph_explicitly()
        elif choice == '6':
            start = input("Enter start node: ")
            goal = input("Enter goal node: ")
            g.astar_path(start, goal)
        elif choice == '7':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
