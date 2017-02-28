class TopSort:

    global_indegree0_list = []

    def top_sort(indegree0_courses, graph, num_courses_wanted):
        hset = top_sort_aux(num_courses_wanted, courses_sofar, graph, res_set)
        global_indegree0_list = indegree0_courses[:]

    def top_sort_aux(num_courses_wanted, courses_sofar, graph, res_set):
        # base case
        if num_courses_wanted == 0:
            res_set.add(courses_sofar)
            return

        # recursion
        for i in range(len(global_indegree0_list)):
            prefix = global_indegree0_list[i]

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
            if graph[course] == []:
                ind0_list.append(str(course))
        return ind0_list

    def clean_graph():
        pass
