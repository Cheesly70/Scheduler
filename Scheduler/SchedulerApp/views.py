from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def index(request):
    #return HttpResponse("<h2>HEY!</h2>")
    return render(request, 'SchedulerApp/home.html') #{'form': form,
                                                      #'class_num': classnum,})

#def mainform(request): # test
#    return HttpResponse("<h1>testing testing 123</h1>")

def getmainform(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':
        total_load = int(request.GET.get("total_load"))
        request.session['total_load'] = total_load

        # the following allows the rendered template to iterate
        # over the total number of courses a user selects
        string = "x" * total_load
        # grab the second value -> desired_load for semester
        my_course_load = int(request.GET.get("desired_load"))
        request.session['my_course_load'] = my_course_load
        return render(request, 'SchedulerApp/courseform.html', {'prelim1': string,})


    # return error or redirect ro main form

def processmainform(request):


    ''' Thoughts:
    # step1: process response information and put into lists
    # step2: create graph out of prcessed information
    # step3: run top sort on graph
    # Last: render results appropriately
    # Optional: provide output as pdf (check out outputting with django pdfs)


    # use ignore case when processing list of prereqs list
    # check if both the course list and prereq list are empty return a HttpResponseRedirect
    # or something like it
    # create list to populate with course names

    '''

    # grab total # of courses and the # of courses being considered
    # by user, from the getmainform view using django sessions
    total_load = int(request.session.get('total_load'))
    my_course_load = int(request.session.get('my_course_load'))

    # create list containing the value attributes for the flag inputs
    # from the main form checkbox input fields
    # used below to check if checkbox was checked on form
    flag_values = []
    for num in range (1, total_load + 1):
        num = str(num)
        flag_values.append("flag " + num)

    # dictionary that maps the course to its boolean flag value of true (1) or false (0)
    flag_boolean = {}
    # put data from main form into python dictionary
    course_dict = {}
    if request.method == 'GET':
        #total_load = int(request.session.get('total_load'))
        for i in range(1, total_load + 1):
            i = str(i) # since strings are immutable and we can't concatenate strs and ints
            course_str = str(request.GET.get("course " + i))
            course_dict[course_str] = [str(request.GET.get("prereqval " + i))]

            # check if flag checkbox for course has been checked
            flag = request.GET.get("flag " + i, None)
            if flag in flag_values:
                flag_boolean[course_str] = 1
            else:
                flag_boolean[course_str] = 0
        #context = {'course_dict':course_dict,}
        print course_dict
        print flag_boolean
    #return render(request, 'SchedulerApp/test.html', context)



    # iterate the dictionary to form a 'list' of unique courses from the main form
    course_list = []
    for key, value in course_dict.iteritems():
        course_list.append(key)
        # the .lower() is in case user types uppercase 'None' for prereqs
        course_list.extend([x.strip().lower() for x in value[0].split(',')])
    # clear out the duplicates in the course list
    course_list = sorted(set(course_list))
    # if a course has no prereqs need to handle the "none" input since "none"
    # is not a valid course to add to the list
    if 'none' in course_list:
        while 'none' in course_list:
            course_list.remove('none')
    print course_list

    # create directed graph (matrix) from the list & dictionary above
    graph = []
    row = []
    for course in course_list:
        for other_course in course_list:
            try:
                # check if course is a prereq for other_course
                # (is course in the dictionary-value list for other_course)
                # the .lower() is in case a user enters a mix of upper and lowercase course names
                is_prereq = str(course) in [x.strip().lower() for x in course_dict[str(other_course)][0].split(',')]
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


    # run the top sort on the graph, considering courses that can be taken
    # concurrently with their prerequisites
    # code coming soon


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
