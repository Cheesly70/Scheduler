from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    return render(request, 'SchedulerApp/home.html')

def getmainform(request):
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


def processmainform(request):

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



    # creating mapping/dictionary of courses to prerequisites
    def create_course_map();
        # put data from main form into python dictionary
        course_dict = {}
        if request.method == 'GET':
            #total_load = int(request.session.get('total_load'))
            for i in range(1, total_load + 1):
                i = str(i) # since strings are immutable and we can't concatenate strs and ints
                course_str = str(request.GET.get("course " + i))
                course_dict[course_str] = str(request.GET.get("prereqval " + i)).split(',')

            print course_dict
            print can_take_with_prereqs
        return course_dict

    def take_course_with_prereqs(course_dict):
        # dictionary that tells whether a course can be taken with its prerequisites
        can_take_with_prereqs = {}

        # create list containing the value attributes for the flag inputs form
        # the main form checkbox input fields
        # That is used as a list to check against to determine if the checkbox was checked on form
        flag_values = []
        for num in range (1, total_load + 1):
            num = str(num)
            flag_values.append("flag " + num)

        for i in range(1, total_load + 1):
            i = str(i) # since strings are immutable and we can't concatenate strs and ints
            course_str = str(request.GET.get("course " + i))
            # check if flag checkbox for course has been checked
            flag = request.GET.get("flag " + i, None)
            can_take_with_prereqs[course_str] = flag in flag_values

        return can_take_with_prereqs

    # defin method to iterate the dictionary to form a 'list' of unique courses
    # from the main form union all unique dictionary keys with the courses in the
    # values part of the  dictionary
    def get_course_list(course_dict):
        value_list = set()
        for lst in course_dict.values():
            for elm in lst:
                values.add(elm.strip())
        # union the unique keys of the dictionary with the unique dictionary values
        course_list = list(set(course_dict.keys()).union(values))
        if 'none' in course_list:
            course_list.remove('none')
        print course_list

        return course_list



    ''' LOL Yes Aaron I will use list comprehension below to generate a matrix containg all zeros
        then g back through and put 1's where matrix[prereq][course] is
        true
    '''
    def create_courses_matrix(course_list, course_dict):
        # create directed graph (matrix) from the list & dictionary above
        graph = []
        row = []
        for course in course_list:
            for other_course in course_list:
                try:
                    # check if course is a prereq for other_course
                    # (is course in the dictionary-value list for other_course)
                    # the .lower() is in case a user enters a mix of upper and lowercase course names
                    is_prereq = str(course) in [x.strip().lower() for x in course_dict[str(other_course)]]
                except KeyError:
                    row.append(0)
                else:
                    if is_prereq:
                        row.append(1)
                    else:
                        row.append(0)
            # if no more other_courses left in list, then add the row to the graph
            graph.append(row)
            # reset row to be empty
            row = []
        print graph
        return graph


    # run the top sort on the graph, considering courses that can be taken
    # concurrently with their prerequisites
    # code coming soon
    def top_sort():



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
