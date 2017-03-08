import copy


global_indegree0_list = []
can_take_with_prereqs_dict = {}

def top_sort(indegree0_courses, graph, num_courses_wanted, can_take_with_prereqs_list, res_set):
    global_indegree0_list = indegree0_courses[:]
    can_take_with_prereqs_dict = copy.deepcopy(can_take_with_prereqs_list)

    hset = top_sort_aux(num_courses_wanted, [], graph, res_set)

    return res_set
    #, graph, courses_sofar

def top_sort_aux(num_courses_wanted, courses_sofar, graph, res_set):
    # base case
    if num_courses_wanted == 0:
        res_set.extend(courses_sofar)
        return

    # recursion
    for i in range(len(global_indegree0_list)):
        prefix = global_indegree0_list[i]
        print prefix

        # check this to determine whether to use append or extend
        if len(global_indegree0_list > 2):
            rest = global_indegree0_list[0:i].extend(global_indegree0_list[i+1 :])
        else:
            rest = global_indegree0_list[0:i].append(global_indegree0_list[i+1 :])

        # recalculate global_indegree0_list, by adding values, not removing
        # this way only need to index into the list instead of worrying about deletions
        recalculate_ind_0(global_indegree0_list)

        # recurse
        top_sort_aux(num_courses_wanted - 1, courses_sofar.append(prefix), clean_graph(graph, prefix), res_set)


def recalculate_ind_0(graph, ind0_list):
    for course in graph:
        if graph[course] == [] and can_take_with_prereqs_dict[course] is True:
            ind0_list.append(str(course))
    return ind0_list

def clean_graph(graph, node):
    new_graph = copy.deepcopy(graph)
    for course in new_graph:
        if node in new_graph[course]:
            new_graph[course].remove(node)
    return new_graph

if __name__ == "__main__":
    ind0lst = ['a', 'b', 'c']
    num_courses = 4
    can_take_with_prereqs = {'a': False, 'b': False, 'c': False, 'd': True, 'e': False, 'f': True}
    graph = {'a':[], 'b':[], 'c':[], 'd':['a', 'b'], 'e':['c'], 'f':['d', 'e']}

    res = top_sort(ind0lst, graph, num_courses, can_take_with_prereqs, [])

    print res
