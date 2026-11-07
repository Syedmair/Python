import heapq
from collections import defaultdict

def execution_order(tasks, dependencies):
    task_set = set(tasks)

    # 1. Reject unknown task names
    for a, b in dependencies:
        for name in (a, b):
            if name not in task_set:
                raise ValueError(
                    f"Unknown task {name!r} in dependency ({a!r}, {b!r})"
                )

    # 2. Build graph (a set removes repeated pairs)
    edges = {(a, b) for a, b in dependencies}
    graph = defaultdict(list)       # a -> tasks that wait on a
    preds = defaultdict(set)        # b -> tasks b waits on
    indegree = {t: 0 for t in task_set}
    for a, b in edges:
        graph[a].append(b)
        preds[b].add(a)
        indegree[b] += 1

    # 3. Kahn's algorithm; a min-heap always yields the alphabetically first ready task
    ready = [t for t in task_set if indegree[t] == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        task = heapq.heappop(ready)
        order.append(task)
        for nxt in graph[task]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                heapq.heappush(ready, nxt)

    # 4. Anything left over is on, or blocked by, a cycle
    if len(order) < len(task_set):
        raise ValueError(
            "Circular dependency detected: " + " -> ".join(_find_cycle(task_set, indegree, preds))
        )
    return order


def _find_cycle(task_set, indegree, preds):
    """Walk backwards through unfinished predecessors until a task repeats."""
    remaining = {t for t in task_set if indegree[t] > 0}
    cycle = []