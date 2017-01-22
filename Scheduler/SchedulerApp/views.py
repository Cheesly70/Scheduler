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
        #request.session["total_load"] = total_load

        #if not session:
          #total_load = 0
        #request.session['total_load'] = total_load
        #global total_load
        #total_load = int(request.GET.get("total_load"))
        # the following allows the rendered template to iterate
        # over the total number of courses a user selects
        string = "x" * total_load
        # grab the second value -> desired_load for semester
        my_course_load = request.GET.get("desired_load")
        return render(request, 'SchedulerApp/courseform.html', {'prelim1': string,
                                                                'load': total_load,})
                                                            #'prelim2': second_val,})
    # return error or redirect ro main form

def processmainform(request):
    # here is where the top sort logic goes
    # return HttpResponse("<h1>testing testing 123</h1>")
    '''
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
    # tel = {'jack': 4098, 'sape': 4139}
    # tel['guido'] = 4127
    # tel
    # {'sape': 4139, 'guido': 4127, 'jack': 4098}


    # put data from main form into python dictionary
    course_dict = {}
    if request.method == 'GET':
        total_load = int(request.session.get('total_load'))
        for i in range(1, total_load + 1):
            i = str(i) # since strings are immutable
            course_dict[str(request.GET.get("course " + i))] = [str(request.GET.get("prereqval " + i))]
        context = {'course_dict':course_dict,}
        print course_dict
    #return render(request, 'SchedulerApp/test.html', context)


    # iterate the dictionary to form a list of unique courses from the main form
    course_list = []
    for key, value in course_dict.iteritems():
        course_list.append(key)
        course_list.extend([x.strip() for x in value[0].split(',')])
    # clear out the duplicates in the course list
    course_list = sorted(set(course_list))
    #print course_list

    # create graph (path_existence matrix) from the list & dictionary above
    graph = []
    row = []
    for course in course_list:
        for other_course in course_list:
            try:
                # see if the course is a key in the dictionary
                try_this = str(course) in [x.strip() for x in course_dict[str(other_course)][0].split(',')]
            except KeyError:
                row.append(0)
            else:
                #if str(course) in [x.strip() for x in course_dict[str(other_course)][0].split(',')]:
                if try_this:
                    row.append(1)
                else:
                    row.append(0)
        # if no more other_courses left in list, then add the row to the graph
        graph.append(row)
        # reset row to be empty
        row = []
    print graph


    return HttpResponse("<h1>Testing</h1>")

    '''
    General Idea:
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
