from blockworld import BlockWorld
from queue import PriorityQueue


class BlockWorldHeuristic(BlockWorld):
    def __init__(self, num_blocks=5, state=None):
        BlockWorld.__init__(self, num_blocks, state)

    def heuristic(self, goal):
        self_state = self.get_state()
        goal_state = goal.get_state()

        # ToDo. Implement the heuristic here.

        return 0.


class AStar():

    def search(self, start, goal):
        path = list()
        # ToDo. Return a list of optimal actions that takes start to goal.

        opened = PriorityQueue()
        closed = list()
        state = start.clone()
        state.priority = 0
        opened.put((100, state))

        while not opened.empty():
            priority, state = opened.get()

            if state in closed:  # State already visited ...
                continue
            else:
                closed.append(state)

            for action, neighbor in state.get_neighbors():
                next_state = state.clone()
                next_state.apply(action)
                next_state.priority = BlockWorldHeuristic.heuristic(next_state, goal)
                #print(state)

                if next_state == goal:
                    print(next_state)
                    path.append(action)
                    print(path)
                    return path
                else:
                    opened.put((next_state.priority, next_state))

        # You can access all actions and neighbors like this:
        print("neighbor")
        for action, neighbor in start.get_neighbors():
            print(str(action) + " ---" + str(neighbor))

        return None


if __name__ == '__main__':
    # Here you can test your algorithm. You can try different N values, e.g. 6, 7.
    N = 5

    start = BlockWorldHeuristic(N)
    goal = BlockWorldHeuristic(N)

    print("Searching for a path:")
    print(f"{start} -> {goal}")
    print()

    astar = AStar()
    path = astar.search(start, goal)

    if path is not None:
        print("Found a path:")
        print(path)

        print("\nHere's how it goes:")

        s = start.clone()
        print(s)

        for a in path:
            s.apply(a)
            print(s)

    else:
        print("No path exists.")

    print("Total expanded nodes:", BlockWorld.expanded)
