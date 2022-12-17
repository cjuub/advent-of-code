from collections import deque
from pathlib import Path

from networkx import shortest_path, DiGraph

lines = [x.strip() for x in Path("input.txt").open("r").readlines()]

valves = {}
for line in lines:
    s1 = line.split("; ")
    valve = s1[0].split(" ")[1]
    flow_rate = int(s1[0].split("=")[1])
    s2 = s1[1].replace("tunnels lead to valves ", "")
    s2 = s2.replace("tunnel leads to valve ", "")
    connected_valves = s2.split(", ")
    valves[valve] = (flow_rate, connected_valves)


q = deque()
q.append(("AA", 1, 0, ()))
visited = {("AA", 1, 0, ())}
to_open = len([x for x in valves.values() if x[0] > 0])
old_best_pressure = 0
best_pressure = 0
while not len(q) == 0:
    curr_valve, time, released, opened = q.popleft()
    if time > 30:
        break
    will_release = 0
    for t in range(time, 31):
        for v in opened:
            fr, _ = valves[v]
            will_release += fr

    best_pressure = max(best_pressure, released + will_release)
    if best_pressure != old_best_pressure:
        old_best_pressure = best_pressure

    for v in opened:
        fr, _ = valves[v]
        released += fr

    if time == 13 and released < 50:
        continue

    if time == 14 and released < 100:
        continue

    if time == 15 and released < 200:
        continue

    if time == 16 and released < 300:
        continue

    flow, connections = valves[curr_valve]

    if curr_valve not in opened and flow > 0:
        new_opened = list(opened)
        new_opened.append(curr_valve)
        new_opened.sort()
        new_opened = tuple(new_opened)
        w = (curr_valve, time + 1, released, new_opened)
        q.append(w)

    for connection in connections:
        w = (connection, time + 1, released, opened)
        if w not in visited:
            visited.add(w)
            q.append(w)


print(f"Part 1: {best_pressure}")

graph = DiGraph()
for valve, (flow, connections) in valves.items():
    for connection in connections:
        graph.add_edge(valve, connection)


to_open_start = []
for valve in valves:
    if valves[valve][0] > 0:
        to_open_start.append(valve)


cache = {}


def shortest_path_to(v1, v2):
    if (v1, v2) in cache:
        return cache[(v1, v2)]
    res = shortest_path(graph, v1, v2)
    if isinstance(res, str):
        res = [res]
    cache[(v1, v2)] = tuple(res[1:])
    return cache[(v1, v2)]


q = deque()
start = ("AA", "AA", 1, 0, (), tuple(to_open_start), (), ())
q.append(start)
visited = {start}
old_best_pressure = 0
best_pressure = 0
while not len(q) == 0:
    curr_valve_1, curr_valve_2, time, released, opened, left_to_open, curr_path_1, curr_path_2 = q.popleft()
    if time > 27:
        break

    released_in_time = 0
    for v in opened:
        fr, _ = valves[v]
        released_in_time += fr

    released += released_in_time
    will_release = released_in_time * (26 - time)

    best_pressure = max(best_pressure, released + will_release)
    if best_pressure != old_best_pressure:
        old_best_pressure = best_pressure

    if len(left_to_open) == 0:
        continue

    if time == 13 and released < 200:
        continue

    if time == 14 and released < 400:
        continue

    if time == 15 and released < 600:
        continue

    if time == 16 and released < 700:
        continue

    flow_1, connections_1 = valves[curr_valve_1]
    flow_2, connections_2 = valves[curr_valve_2]
    if (not curr_path_1 and flow_1 > 0 and curr_valve_1 not in opened) or (not curr_path_2 and flow_2 > 0 and curr_valve_2 not in opened):
        if not curr_path_1 and not curr_path_2 and flow_1 > 0 and flow_2 > 0 and curr_valve_2 != curr_valve_1 and curr_valve_1 not in opened and curr_valve_2 not in opened:
            new_opened = list(opened)
            new_opened.append(curr_valve_1)
            new_opened.append(curr_valve_2)
            new_opened.sort()
            new_opened = tuple(new_opened)
            new_left_to_open = list(left_to_open)
            new_left_to_open.remove(curr_valve_1)
            new_left_to_open.remove(curr_valve_2)
            new_left_to_open.sort()
            new_left_to_open = tuple(new_left_to_open)

            w = (curr_valve_1, curr_valve_2, time + 1, released, new_opened, new_left_to_open, (), ())
            if w not in visited:
                visited.add(w)
                q.append(w)

        elif not curr_path_1 and flow_1 > 0 and curr_valve_1 not in opened:
            new_opened = list(opened)
            new_opened.append(curr_valve_1)
            new_opened.sort()
            new_opened = tuple(new_opened)
            new_left_to_open = list(left_to_open)
            new_left_to_open.remove(curr_valve_1)
            new_left_to_open.sort()
            new_left_to_open = tuple(new_left_to_open)

            if not curr_path_2:
                for left in new_left_to_open:
                    new_curr_path_2 = shortest_path_to(curr_valve_2, left)
                    w = (curr_valve_1, new_curr_path_2[0], time + 1, released, new_opened, new_left_to_open, (), new_curr_path_2[1:])
                    if w not in visited:
                        visited.add(w)
                        q.append(w)
            else:
                w = (curr_valve_1, curr_path_2[0], time + 1, released, new_opened, new_left_to_open, (), curr_path_2[1:])
                if w not in visited:
                    visited.add(w)
                    q.append(w)

        elif not curr_path_2 and flow_2 > 0 and curr_valve_2 not in opened:
            new_opened = list(opened)
            new_opened.append(curr_valve_2)
            new_opened.sort()
            new_opened = tuple(new_opened)
            new_left_to_open = list(left_to_open)
            new_left_to_open.remove(curr_valve_2)
            new_left_to_open.sort()
            new_left_to_open = tuple(new_left_to_open)

            if not curr_path_1:
                for left in new_left_to_open:
                    new_curr_path_1 = shortest_path_to(curr_valve_1, left)
                    w = (new_curr_path_1[0], curr_valve_2, time + 1, released, new_opened, new_left_to_open, new_curr_path_1[1:], ())
                    if w not in visited:
                        visited.add(w)
                        q.append(w)
            else:
                w = (curr_path_1[0], curr_valve_2, time + 1, released, new_opened, new_left_to_open, curr_path_1[1:], ())
                if w not in visited:
                    visited.add(w)
                    q.append(w)
    else:

        if not curr_path_1 or not curr_path_2:
            if not curr_path_1 and not curr_path_2:
                for left1 in left_to_open:
                    for left2 in left_to_open:
                        if left1 == left2:
                            continue

                        new_curr_path_1 = shortest_path_to(curr_valve_1, left1)
                        new_curr_path_2 = shortest_path_to(curr_valve_2, left2)
                        w = (new_curr_path_1[0], new_curr_path_2[0], time + 1, released, opened, left_to_open, new_curr_path_1[1:], new_curr_path_2[1:])
                        if w not in visited:
                            visited.add(w)
                            q.append(w)

            elif not curr_path_1:
                for left in left_to_open:
                    new_curr_path_1 = shortest_path_to(curr_valve_1, left)
                    w = (new_curr_path_1[0], curr_path_2[0], time + 1, released, opened, left_to_open, new_curr_path_1[1:], curr_path_2[1:])
                    if w not in visited:
                        visited.add(w)
                        q.append(w)

            elif not curr_path_2:
                for left in left_to_open:
                    new_curr_path_2 = shortest_path_to(curr_valve_2, left)
                    w = (curr_path_1[0], new_curr_path_2[0], time + 1, released, opened, left_to_open, curr_path_1[1:], new_curr_path_2[1:])
                    if w not in visited:
                        visited.add(w)
                        q.append(w)
        else:
            w = (curr_path_1[0], curr_path_2[0], time + 1, released, opened, left_to_open, curr_path_1[1:], curr_path_2[1:])
            if w not in visited:
                visited.add(w)
                q.append(w)

print(f"Part 2: {best_pressure}")
