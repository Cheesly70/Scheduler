from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from math import factorial
import itertools

def index(request):
    return render(request, 'SchedulerApp/home.html')


def get_main_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':
        # store these session variables for use in other views
        total_load = int(request.GET.get("total_load"))
        request.session['total_load'] = total_load

        # the following allows the rendered template to iterate
        # over the total number of courses a user selects, in order to
        # generate the main form
        string = "x" * total_load

        # grab the second value -> desired_load for semester
        my_course_load = int(request.GET.get("desired_load"))
        request.session['my_course_load'] = my_course_load
        return render(request, 'SchedulerApp/courseform.html', {'prelim1': string,})

    # else redirect to home page
    return render(request, 'SchedulerApp/home.html')


def process_main_form(request):

    ''' Thoughts:
    # Optional: provide output as pdf (check out outputting with django pdfs)
    '''

    # Global variables for the session
    # grab total # of courses and the # of courses being considered
    # by user, from the getmainform view using django sessions
    total_load = int(request.session.get('total_load'))
    my_course_load = int(request.session.get('my_course_load'))

    ############################################################################

    #*****************************************MAP OF COURSE TO PREREQS*****************************************
    #*************************************ALSO DETERMINE IF FLAG WAS CHECKED***********************************

    # dictionary that tells whether a course can be taken with its prerequisites
    can_take_with_prereqs = {}

    # creating mapping/dictionary of courses to prerequisites
    # put data from main form into python dictionary
    course_dict = {}
    if request.method == 'GET':
        #total_load = int(request.session.get('total_load'))
        for i in range(1, total_load + 1):
            i = str(i) # since strings are immutable and we can't concatenate strs and ints
            course_str = str(request.GET.get("course " + i))
            # also strip off any white space and make the courses lowercase as they're inputted in dict
            course_dict[course_str] = [x.strip().lower() for x in str(request.GET.get("prereqval " + i)).split(',')]
            # replace 'none' input by user with empty list'
            if 'none' in course_dict[course_str]:
                course_dict[course_str] = []

            # check if flag checkbox for course has been checked
            flag = request.GET.get("flag " + i, None)
            can_take_with_prereqs[course_str] = flag is not None

    print "Course dictionary (w/o 'none' values): " + str(course_dict) + "\n"
    print "Can take with prereqs: " + str(can_take_with_prereqs) + "\n"

    #************************************GENERATE UNIQUE COURSE LIST*******************************************

    # iterate the dictionary to form a 'list' of unique courses
    # from the main form union all unique dictionary keys with the courses in the
    # values part of the  dictionary
    values_list = set()
    for lst in course_dict.values():
        for elm in lst:
            values_list.add(elm)
    # union the unique keys of the dictionary with the unique dictionary values
    course_list = sorted(list(set(course_dict.keys()).union(values_list)))
    if [] in course_list:
        course_list.remove([])

    print "Unique course list: " + str(course_list) + "\n"

    #*****************************************MAIN GRAPH STUFF**************************************************

    # create directed graph (matrix) from the list & dictionary above w/ list comprehensions
    # first create a matrix/graph of all zeros
    graph = [[0 for i in range(len(course_list))] for j in range(len(course_list))]

    # go through graph and put 1's in the cells if the course is a prereq
    # grab the prereqs of the current course and change the appropriate
    # cell in the matrix to a 1
    for course in course_dict:
        # grab the prereqs
        prereqs_list = course_dict[course]
        for prereq in prereqs_list:
            # put a 1 in matrix[prereq][course]
            # need index of prereq and index of course
            graph[course_list.index(prereq)][course_list.index(course)] = 1

    print "Graph[prereq][course] " + str(graph) + "\n"

    #*****************************************TOP SORT STUFF************************************************

    # create list of courses that have no dependencies
    courses_without_prereqs = []

    # if  a course is not a key from the course_list, then it must be a prereq
    # so it can be added to the lost of coursess wth no dependencies
    # and if a key has no prereqs, also add it to that list

    for course in course_list:
        if course not in course_dict.keys():
            courses_without_prereqs.append(course)
        else:
            if course_dict[course] == []:
                courses_without_prereqs.append(course)

    print "Courses w/o prereqs: " + str(courses_without_prereqs) + "\n"


    # run the top sort on the graph, considering courses that can be taken
    # concurrently with their prerequisites, and the limit of allowed courses
    # for the semester as indicated by user on the preliminary form
    # Thought: note the index of each course row major is based on course_list
    # but we can use zip to get at the columns
    # code coming soon

    # list of top-sort results
    results = []
    # intermediate top sort results list
    intermediate_top = []

    combined_list = []

    if len(courses_without_prereqs) >= my_course_load:
        # then can only make combos amongst the courses in courses_without_prereqs
        # and the courses in the can_take_with_prereqs list
        # combine into one list, and do all combos of size courses_without_prereqs
        # But only add the courses whose prereqs are already in the list
        combined_list.extend(courses_without_prereqs)

        for course in can_take_with_prereqs:
            if can_take_with_prereqs[course]: # if the value in dictionary is "true"
                for prereq in course_dict[course]:
                    if prereq not in courses_without_prereqs:
                        pass
                combined_list.append(course)
        combined_list = sorted(list(set(combined_list)))

        print str(combined_list) + "\n"

        # now make # of items in list choose my_course_load amount of orderings
        # basically n choose k number of sortings [n!/k!*(n-k)]!
        # create a list for each sort and add to results list
        #len_combined_list = len(combined_list)
        #total_combos = factorial(len_combined_list) / (factorial(my_course_load) * factorial((len_combined_list) - my_course_load))
        #print total_combos
        #for i in range(total_combos):

        # itertools is really nifty!
        combos = list(itertools.combinations(combined_list, my_course_load))
        print combos



    else:
        # if the number of courses in courses_without_prereqs is less than my_course_load
        # then we do the top sort with the courses in courses_without_prereqs as the starting
        # values in each iteration
        # code coming soon
        pass




    # for testing purposes
    return HttpResponse("<h1>Testing</h1>")

    '''
    One possible Top sort Idea (old):
        -Create a graph based on input
        -Use DFS to go deep into the graph. When you can't go any further
        you've found the sink node (that you mark with the predefined local var)
    Pseudocode for top sort (this method takes a graph):
        - Mark all nodes unvisited
        - create local var that will represent ordering_label that will be applied to each node
        - Since you can start anywhere in the graph we can do the following:
            - for each vertex v in graph G
                - if v is not yet explored
                    - DFS on (G,v)
    Pseudocode for DFS (this method takes a graph and a vertex v):
        - mark v explored
        - for each edge (v,u)
            - if u is unexplored
                - DFS(G,u)
        *****we get here because there are no outgoing arcs*****
        - set the label for the current vertex (local var we defined in the top sort method)
        - decrement the label so that the next deepest node gets that ordering value

    '''
