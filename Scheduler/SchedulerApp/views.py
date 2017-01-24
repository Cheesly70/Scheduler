from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    return render(request, 'SchedulerApp/home.html')

def get_main_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':
        # store these session variables for use in other views
        total_load = int(request.GET.get("total_load"))
        request.session['total_load'] = total_load

        # the following allows the rendered template to iterate
        # over the total number of courses a user selects
        string = "x" * total_load
        # grab the second value -> desired_load for semester
        my_course_load = int(request.GET.get("desired_load"))
        request.session['my_course_load'] = my_course_load
        return render(request, 'SchedulerApp/courseform.html', {'prelim1': string,})

    # else redirect to home page
    return render(request, 'SchedulerApp/home.html')


def process_main_form(request):

    ''' Thoughts:
    # step1: process response information and put into lists
    # step2: create graph out of prcessed information
    # step3: run top sort on graph
    # Last: render results appropriately
    # Optional: provide output as pdf (check out outputting with django pdfs)
    '''

    # Global variables for the session
    # grab total # of courses and the # of courses being considered
    # by user, from the getmainform view using django sessions
    total_load = int(request.session.get('total_load'))
    my_course_load = int(request.session.get('my_course_load'))

    ############################################################################

    # create list containing the value attributes for the flag inputs form
    # the main form checkbox input fields
    # That is used as a list to check against to determine if the checkbox was checked on form
    flag_values = []
    for num in range (1, total_load + 1):
        num = str(num)
        flag_values.append("flag " + num)

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

            # check if flag checkbox for course has been checked
            flag = request.GET.get("flag " + i, None)
            can_take_with_prereqs[course_str] = flag in flag_values

    print course_dict
    print can_take_with_prereqs

    ##########################################################################################################

    # iterate the dictionary to form a 'list' of unique courses
    # from the main form union all unique dictionary keys with the courses in the
    # values part of the  dictionary
    values_list = set()
    for lst in course_dict.values():
        for elm in lst:
            values_list.add(elm.strip()) # get rid of strip() ************************'''
    # union the unique keys of the dictionary with the unique dictionary values
    course_list = sorted(list(set(course_dict.keys()).union(values_list)))
    if 'none' in course_list:
        course_list.remove('none')
    print course_list

    ###########################################################################################################

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

    print graph

    ###########################################################################################################

    # run the top sort on the graph, considering courses that can be taken
    # concurrently with their prerequisites
    # code coming soon
    # note the index of each course row major is based on course_list
    # but we can use zip to get at the columns



    ''' potentially could use zip the matrix (to get the matrix columns as list index values)
    and check for existence of 1 or 0 to determine whether that column/course has prereqs'''

    '''
    # create a list of all courses that have no prerequisites
    # check if the # of items in the list is <= to the # of courses
    the student wants to take for the upcoming semester...if it's equal
    then create all possibilities amongst the prerequisites and the courses
    themeselves if they can be taken with their prerequisites
    '''


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
