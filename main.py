import time

import vk
import itertools
from vk.exceptions import VkAPIError

was_deleted = set()
VEZDEKOD_ID = 197700721


def all_are_friends(combb, gg):
    for man in combb:
        for man2 in combb:
            if man != man2 and man2 not in gg[man]:
                return False
    return True


def find_klika_with_size(people_set, size, g):
    all_comb = itertools.combinations(people_set, size)
    for comb in all_comb:
        if all_are_friends(comb, g):
            return (True, comb)
    return (False, "pososi")


def rm_nodes_with(n, graph_without_isolated):
    graph_copy = dict(graph_without_isolated)
    for (key, value) in graph_copy.items():
        if len(value) <= n:
            for v in value:
                graph_without_isolated[v].remove(key)
                # if len(new_graph[v]) == 0:
                #     new_graph.pop(v)
            graph_without_isolated.pop(key)
            was_deleted.add(key)

    graph_copy = dict(graph_without_isolated)
    for (key, value) in graph_copy.items():
        if len(value) == 0:
            graph_without_isolated.pop(key)
            was_deleted.add(key)


def is_complete_graph(nodes, new_graph):
    for i in range(0, len(nodes) - 1):
        for j in range(i + 1, len(nodes)):
            assert((nodes[j] in new_graph[nodes[i]]) == (nodes[i] in new_graph[nodes[j]]))
            if not(nodes[j] in new_graph[nodes[i]]):
                return False

    return True


def is_complete_graph_msk(mask, nodes, new_graph):
    assert(len(mask) == len(nodes))

    subnodes = []
    for i in range(0, len(mask)):
        if mask[i] == 1:
            subnodes.append(nodes[i])

    return is_complete_graph(subnodes, new_graph)


def number_to_binary_array(number, result_array_len):
    result_array = []
    count = 0
    while number != 0:
        if number % 2 == 1:
            count += 1
        result_array.append(number % 2)
        number //= 2

    while len(result_array) != result_array_len:
        result_array.append(0)

    result_array.reverse()
    return result_array, count


def findMaxClique(friends_dict, new_graph):
    arr = list(friends_dict - was_deleted)

    max_size = 0

    for i in range(pow(2, len(arr))):
        bin_array, size = number_to_binary_array(i, len(arr))
        if size > max_size and is_complete_graph_msk(bin_array, arr, new_graph):
            max_size = size

    return max_size


def dfs(node, graph, result):
    result[-1].add(node)
    cur_friends_dfs = graph.pop(node, None)
    for fr in cur_friends_dfs:
        if fr in graph:
            result[-1].add(fr)
            dfs(fr, graph, result)


def get_graph_components(graphh):
    result = []
    copy_graph = dict(graphh)
    for (memberr, friendss) in copy_graph.items():
        if memberr in graphh:
            result.append(set())
            dfs(memberr, graphh, result)

    return result


if __name__ == '__main__':
    session = vk.AuthSession(app_id=..., user_login=..., user_password=..., scope='friends')

    vk_api = vk.API(session, v="5.130")
    print(vk_api.groups.getMembers(group_id=VEZDEKOD_ID))
    members_set = set()
    arr1 = list(map(int, vk_api.groups.getMembers(group_id=VEZDEKOD_ID, offset=0)['items']))
    arr2 = list(map(int, vk_api.groups.getMembers(group_id=VEZDEKOD_ID, offset=1000)['items']))
    arr3 = list(map(int, vk_api.groups.getMembers(group_id=VEZDEKOD_ID, offset=2000)['items']))
    members = set(arr1 + arr2 + arr3)

    print(members)
    graph = dict()
    for member in members:
        graph[member] = set()
    for member in members:
        try:
            all_friends = list(map(int, vk_api.friends.get(user_id=member)['items']))
            for f in all_friends:
                if f in members:
                    graph[member].add(f)
                    graph[f].add(member)
        except VkAPIError as ex:
             print("api_error", ex.message, member)
        time.sleep(0.4)

    # NEED TO NOT RESTART WHOLE PROGRAM
    with open("friend_dict_Roma.txt", "w") as fout:
        for member in members:
            fout.write(str(member) + " : ")
            for f in graph[member]:
                fout.write(str(f) + " ")
            fout.write("\n")

    max_possib_kl = 35
    while True:
        klikers = 0
        for p in graph.keys():
            if len(graph[p]) >= max_possib_kl:
                klikers += 1
        if klikers >= max_possib_kl:
            break
        max_possib_kl -= 1

    possible_klikers = set()
    for key in graph.keys():
        if len(graph[key]) >= max_possib_kl:
            possible_klikers.add(key)

    while True:
        found = find_klika_with_size(possible_klikers, max_possib_kl, graph)
        if found[0]:
            print("Maximal klika ids: " + str(found[1]))
            break
        max_possib_kl -= 1
        for key in graph.keys():
            if len(graph[key]) >= max_possib_kl:
                possible_klikers.add(key)
