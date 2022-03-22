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
        # print(self_state)
        # print(goal_state)

        # ToDo. Implement the heuristic here.
        for i in range(0, len(self_state)):
            # print("len-"+str(len(self_state[i])))
            #for j in range(0, len(self_state[i])):
                for g in range(0, len(goal_state)):
                    #for h in range(0, len(list(goal_state[g]))):
                        #if self_state[i][j] == goal_state[g][h]:
                            # val += abs(j - h)
                            #val += abs(j - h) * (len(self_state[i]) - j)
                            if self_state[i][-1] == goal_state[g][-1]:
                                val -= 1
                                if len(self_state[i]) > 1 and len(goal_state[g]) > 1:
                                    if self_state[i][-2] == goal_state[g][-2]:
                                        val -= 2
                                        if len(self_state[i]) > 2 and len(goal_state[g]) > 2:
                                            if self_state[i][-3] == goal_state[g][-3]:
                                                val -= 3
                                                if len(self_state[i]) > 3 and len(goal_state[g]) > 3:
                                                    if self_state[i][-4] == goal_state[g][-4]:
                                                        val -= 4
                                                        if len(self_state[i]) > 4 and len(goal_state[g]) > 4:
                                                            if self_state[i][-5] == goal_state[g][-5]:
                                                                val -= 5
                                                                if len(self_state[i]) > 5 and len(goal_state[g]) > 5:
                                                                    if self_state[i][-6] == goal_state[g][-6]:
                                                                        val -= 6
                                                                        if len(self_state[i]) > 6 and len(goal_state[g]) > 6:
                                                                            if self_state[i][-7] == goal_state[g][-7]:
                                                                                val -= 7
                        # print(abs(j - h))
        # print(self_state)
        # print(goal_state)
        return val


class AStar():

    def search(self, start, goal):
        path = list()
        # ToDo. Return a list of optimal actions that takes start to goal.

        opened = PriorityQueue()
        closed = list()
        state = start.clone()
        state.priority = 0
        opened.put((0, state))
        deep = 0
        while not opened.empty():
            priority, state = opened.get()

            if state == goal:
                r_path = list()
                h = goal
                print("mám to!")
                stop = 0
                while h != start and stop < 100:
                    stop += 1
                    for p in path:
                        if p[2] == h:
                            r_path.append(p[1])
                            # print("tisknu p " + str(p))
                            # print(p[0].clone())
                            h = p[0]
                            # deep-=1
                            # print(p)
                            # path.remove(p)
                print(r_path[::-1])
                return r_path[::-1]

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
                # print(state)
                next_state.priority = BlockWorldHeuristic.heuristic(next_state, goal) + 0 * deep
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
