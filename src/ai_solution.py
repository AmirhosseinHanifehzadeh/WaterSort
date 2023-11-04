from copy import deepcopy 
from queue import PriorityQueue

class GameSolution:
    """
        A class for solving the Water Sort game and finding solutions(normal, optimal).

        Attributes:
            ws_game (Game): An instance of the Water Sort game which implemented in game.py file.
            moves (List[Tuple[int, int]]): A list of tuples representing moves between source and destination tubes.
            solution_found (bool): True if a solution is found, False otherwise.

        Methods:
            solve(self, current_state):
                Find a solution to the Water Sort game from the current state.
                After finding solution, please set (self.solution_found) to True and fill (self.moves) list.

            optimal_solve(self, current_state):
                Find an optimal solution to the Water Sort game from the current state.
                After finding solution, please set (self.solution_found) to True and fill (self.moves) list.
    """
    def __init__(self, game):
        """
            Initialize a GameSolution instance.
            Args:
                game (Game): An instance of the Water Sort game.
        """
        self.ws_game = game  # An instance of the Water Sort game.
        self.moves = []  # A list of tuples representing moves between source and destination tubes.
        self.tube_numbers = game.NEmptyTubes + game.NColor  # Number of tubes in the game.
        self.solution_found = False  # True if a solution is found, False otherwise.
        self.visited_tubes = list()  # A set of visited tubes.
        self.tube_capacity = game.NColorInTube

    def solve(self, current_state):
        if (self.ws_game.check_victory(current_state)):
            self.solution_found = True 
            return 
        
        for (child, move) in self.find_children_move(current_state):
            if child not in self.visited_tubes: 
                self.moves.append(move)
                self.visited_tubes.append(child)
                self.solve(child)

                if (not(self.solution_found)):
                    self.moves.pop()
        
                else: 
                    return

    def find_children_move(self, state): 
        children = []
        l = len(state)
        for source in range(l): 
            if not(len(state[source])):
                continue
            color = state[source][-1]
            for dest in range(l): 
                if dest != source and (not(len(state[dest])) or (len(state[dest]) < self.tube_capacity and color == state[dest][-1])):
                    child = deepcopy(state)
                    while (len(child[source]) and child[source][-1] == color and len(child[dest]) < self.tube_capacity):
                        child[source].pop()
                        child[dest].append(color)

                    children.append((child, (source, dest)))

        return children

    def optimal_solve(self, current_state):
        """
            Find an optimal solution to the Water Sort game from the current state.

            Args:
                current_state (List[List[int]]): A list of lists representing the colors in each tube.

            This method attempts to find an optimal solution to the Water Sort game by minimizing
            the number of moves required to complete the game, starting from the current state.
        """

        pq = PriorityQueue()
        h = {}
        g = {} 
        
        root = str(current_state)
        g[root] = 0
        h[root] = 0
        pq.put((g[root] + h[root], current_state, []))

        while not(pq.empty()):
            fn, state, moves = pq.get()
            if (self.check_vecotry(state)):
                self.solution_found = True
                self.moves = moves

                return
            
            for (child, move) in self.find_children_move(state):
                child_key = str(child)
                h[child_key] = self.heurisitc(child)
                g[child_key] = g[str(state)] + 1
                pq.put((g[child_key] + h[child_key], child, moves + [move]))


    @staticmethod
    def heurisitc(current_state):
        h = 0
        for tube in current_state: 
            h += max(len(set(tube)) - 1, 0)

        return h  


    def check_vecotry(self, current_state):
        return self.ws_game.check_victory(current_state)
