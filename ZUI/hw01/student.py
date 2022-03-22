from blockworld import BlockWorld
from queue import PriorityQueue
import numpy as np


class BlockWorldHeuristic(BlockWorld):
    def __init__(self, num_blocks=5, state=None):
        BlockWorld.__init__(self, num_blocks, state)

    def heuristic(self, goal):
        self_state = list(self.get_state())
        goal_state = list(goal.get_state())
        val = 0
        #print(self_state)
        #print(goal_state)

        # ToDo. Implement the heuristic here.
        for i in range(0, len(self_state)):
            self_state[i] = list(self_state[i])
            #print("len-"+str(len(self_state[i])))
            for j in range(0, len(self_state[i])):
                for g in range(0, len(goal_state)):
                    for h in range(0, len(list(goal_state[g]))):
                        if self_state[i][j] == goal_state[g][h]:
                            val += abs(j - h)
                           # print(abs(j - h))
        #print(self_state)
        #print(goal_state)
        return val


class AStar():

    def search(self, start, goal):
        path = list()
        # ToDo. Return a list of optimal actions that takes start to goal.

        opened = PriorityQueue()
        closed = list()
        state = start.clone()
        state.priority = 0
        opened.put((100, state))
        deep = 0
        while not opened.empty():
            priority, state = opened.get()

            if state in closed:  # State already visited ...
                continue
            else:
                closed.append(state)
            deep += 1
            for action, neighbor in state.get_neighbors():
                next_state = state.clone()
                next_state.apply(action)
                if next_state in closed:
                    continue
                path.append((state, action, next_state, deep))
                #print(state)
                next_state.priority = BlockWorldHeuristic.heuristic(next_state, goal) + 2*deep


                if next_state == goal:
                    r_path = list()
                    h = goal
                    print("mám to!")
                    stop = 0
                    while h != start and stop<100:
                        stop += 1
                        for p in path:
                            if p[2] == h:
                                r_path.append(p[1])
                                #print("tisknu p " + str(p))
                                #print(p[0].clone())
                                h = p[0]
                                #deep-=1
                                #print(p)
                                #path.remove(p)
                    print(r_path[::-1])
                    return r_path[::-1]
                else:
                    opened.put((next_state.priority, next_state))


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
