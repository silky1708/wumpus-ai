from dataclasses import dataclass
import heapq
from typing import Callable, Iterator, List, Optional

from consts import ACTIONS, DOWN, LEFT, RIGHT, UP


class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0

    def empty(self):
        return len(self.heap) == 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def __len__(self):
        return len(self.heap)


@dataclass
class Position:
    x: int
    y: int

    def __hash__(self):
        return hash(f"{self.x},{self.y}")


class ShortestPathState:
    def __init__(
        self,
        pos: Position,
        cost: int,
        prev: Optional["ShortestPathState"] = None,
        action: Optional[str] = None,
    ):
        self.pos = pos
        self.cost = cost
        self.prev = prev
        self.action = action

    def __eq__(self, other):
        return self.pos == other.pos

    def __hash__(self) -> int:
        return hash(self.pos)


class ShortestPathSearchProblem:
    def __init__(self, start: Position, goal: Position, visited: List[List[bool]]):
        self.start = start
        self.goal = goal
        self.visited = visited

    def get_start_state(self) -> ShortestPathState:
        return ShortestPathState(self.start, 0)

    def is_goal_state(self, state: ShortestPathState) -> bool:
        return state.pos == self.goal

    def get_successors(self, state: ShortestPathState) -> Iterator[ShortestPathState]:
        m = len(self.visited)
        n = len(self.visited[0])

        for dir in (LEFT, DOWN, RIGHT, UP):
            x, y = dir
            children = Position(state.pos.x + x, state.pos.y + y)
            cond = (
                children.x >= 0
                and children.x < n
                and children.y >= 0
                and children.y < m
                and self.visited[children.y][children.x]
            )
            if cond:
                yield ShortestPathState(children, state.cost + 1, state, ACTIONS[dir])


def null_heuristic(
    problem: ShortestPathSearchProblem, state: ShortestPathSearchProblem
) -> int:
    return 0


def a_star_route(
    problem: ShortestPathSearchProblem,
    heuristic: Callable[
        [ShortestPathSearchProblem, ShortestPathState], int
    ] = null_heuristic,
) -> List[str]:
    pq = PriorityQueue()
    start_state = problem.get_start_state()
    pq.push(start_state, start_state.cost + heuristic(problem, start_state))
    visited = set()
    solution = []
    while not pq.empty():
        state = pq.pop()

        if problem.is_goal_state(state):
            while state:
                if state.action:
                    solution.insert(0, state.action)
                state = state.prev
            break

        visited.add(state)

        for child in problem.get_successors(state):
            if child not in visited:
                pq.push(child, child.cost + heuristic(problem, child))

    return solution
