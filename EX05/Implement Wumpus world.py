import random

class WumpusWorld:
    def __init__(self, size=4, pit_prob=0.2, wumpus_count=1):
        self.size = size
        self.pit_prob = pit_prob
        self.wumpus_count = wumpus_count
        self.agent_pos = (0, 0)
        self.agent_dir = (0, 1)  # East
        self.pits = set()
        self.wumpus_alive = set()
        self.arrow = True
        self.scream_heard = False
        self.generate_pits()
        self.generate_wumpus()
        self.gold = self.random_empty_cell()

    def generate_pits(self):
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) not in [(0, 0), (0, 1), (1, 0)]:
                    if random.random() < self.pit_prob:
                        self.pits.add((i, j))

    def generate_wumpus(self):
        while len(self.wumpus_alive) < self.wumpus_count:
            cell = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            if cell not in [(0, 0), (0, 1), (1, 0)] and cell not in self.pits:
                self.wumpus_alive.add(cell)

    def random_empty_cell(self):
        while True:
            cell = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            if cell not in [(0, 0), (0, 1), (1, 0)] and cell not in self.pits and cell not in self.wumpus_alive:
                return cell

    def neighbors(self, pos):
        x, y = pos
        moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return [(i, j) for i, j in moves if 0 <= i < self.size and 0 <= j < self.size]

    def get_sensors(self, bump_occurred):
        sensors = {"stench": False, "breeze": False, "glitter": False,
                   "bump": bump_occurred, "scream": self.scream_heard}
        self.scream_heard = False
        for n in self.neighbors(self.agent_pos):
            if n in self.wumpus_alive: sensors["stench"] = True
            if n in self.pits: sensors["breeze"] = True
        if self.agent_pos == self.gold: sensors["glitter"] = True
        return sensors

    def display_grid(self):
        dir_map = {(0, 1): ">", (0, -1): "<", (1, 0): "v", (-1, 0): "^"}
        print("-" * (self.size * 4 + 1))
        for i in range(self.size):
            row_str = "|"
            for j in range(self.size):
                cell = (i, j)
                if cell == self.agent_pos: char = dir_map[self.agent_dir]
                elif cell == self.gold: char = "G"
                elif cell in self.wumpus_alive: char = "W"
                elif cell in self.pits: char = "P"
                else: char = "."
                row_str += f" {char} |"
            print(row_str)
        print("-" * (self.size * 4 + 1))

class Agent:
    def __init__(self, world, initial_points=1000):
        self.world = world
        self.points = initial_points
        self.kb = {(i, j): {"safe": False, "visited": False} for i in range(world.size) for j in range(world.size)}
        self.history = []
        self.first_move = True
        self.bump_flag = False
        self.wumpus_dead = False

    def execute_move(self, target):
        x1, y1 = self.world.agent_pos
        x2, y2 = target
        desired_dir = (x2 - x1, y2 - y1)
        while self.world.agent_dir != desired_dir:
            dx, dy = self.world.agent_dir
            self.world.agent_dir = (dy, -dx)
            self.points -= 1
            print(f"Action: Turned Right | Points: {self.points}")
            if self.points <= 0: return False
        if 0 <= x2 < self.world.size and 0 <= y2 < self.world.size:
            self.world.agent_pos = target
            self.points -= 1
            self.bump_flag = False
            print(f"Action: Moved Forward to {target} | Points: {self.points}")
        else:
            self.points -= 1
            self.bump_flag = True
            print(f"Action: Attempted Move to {target} - BUMP Detected! | Points: {self.points}")
        return self.points > 0

    def shoot_arrow(self, target_cell):
        if self.world.arrow:
            self.world.arrow = False
            self.points -= 10
            x1, y1 = self.world.agent_pos
            x2, y2 = target_cell
            desired_dir = (x2 - x1, y2 - y1)
            while self.world.agent_dir != desired_dir:
                dx, dy = self.world.agent_dir
                self.world.agent_dir = (dy, -dx)
                self.points -= 1
            print(f"Action: Shot Arrow toward {target_cell} (-10 pts) | Points: {self.points}")
            if target_cell in self.world.wumpus_alive:
                self.world.wumpus_alive.remove(target_cell)
                self.world.scream_heard = True
                self.wumpus_dead = True
                return True
        return False

    def run(self):
        while self.points > 0:
            curr = self.world.agent_pos
            self.kb[curr]["visited"] = True
            self.kb[curr]["safe"] = True
            self.world.display_grid()
            sensors = self.world.get_sensors(self.bump_flag)
            print(f"Position: {curr} | Points: {self.points} | Sensors: {sensors}")

            if sensors["scream"]:
                print("Strategy: Scream heard! The Wumpus in this direction is dead.")

                for n in self.world.neighbors(curr):
                    if not sensors["breeze"]: self.kb[n]["safe"] = True

            if sensors["glitter"]:
                self.points += 1000
                print(f"SUCCESS: Gold Found! Final Points: {self.points}")
                break

            if curr in self.world.pits or curr in self.world.wumpus_alive:
                self.points -= 1000
                print(f"DEATH: Final Points: {self.points}")
                break

            if not sensors["breeze"] and (not sensors["stench"] or self.wumpus_dead):
                for n in self.world.neighbors(curr):
                    self.kb[n]["safe"] = True

            target = None
            if self.first_move:
                target = (0, 1)
                self.first_move = False
                print("Strategy: Mandatory first move.")
            else:
                active_disturbances = [k for k, v in sensors.items() if v and k in ["stench", "breeze", "bump"]]
                if active_disturbances:
                    print(f"Strategy: Disturbance detected ({', '.join(active_disturbances)}).")
                else:
                    dx, dy = self.world.agent_dir
                    ahead = (curr[0] + dx, curr[1] + dy)
                    if (0 <= ahead[0] < self.world.size and 0 <= ahead[1] < self.world.size and not self.kb[ahead]["visited"]):
                        target = ahead

                if not target:
                    target = next((n for n in self.world.neighbors(curr) if self.kb[n]["safe"] and not self.kb[n]["visited"]), None)

                if not target and sensors["stench"] and self.world.arrow:
                    for n in self.world.neighbors(curr):
                        if not self.kb[n]["visited"]:
                            print(f"Strategy: Path blocked by Stench. Shooting arrow at {n} to clear path...")
                            if self.shoot_arrow(n):
                                self.kb[n]["safe"] = True
                                target = n
                                break
                            else:
                                print("Strategy: No scream. Wumpus is not in this cell. Checking next...")

            if target:
                self.history.append(curr)
                if not self.execute_move(target): break
            elif self.history:
                back_target = self.history.pop()
                print(f"Strategy: Backtracking to {back_target}...")
                if not self.execute_move(back_target): break
            else:
                print("FAILURE: No safe options left.")
                break
        if self.points <= 0: print("GAME OVER: Out of points.")

try:
    Agent(WumpusWorld(size=int(input("Size: "))), initial_points=int(input("Points: "))).run()
except ValueError: print("Invalid input.")