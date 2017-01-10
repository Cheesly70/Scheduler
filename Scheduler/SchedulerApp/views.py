from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    #return HttpResponse("<h2>HEY!</h2>")
    return render(request, 'SchedulerApp/home.html') #{'form': form,
                                                      #'class_num': classnum,})

#def mainform(request): # test
#    return HttpResponse("<h1>testing testing 123</h1>")

def getmainform(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        first_val = int(request.POST.get("total_load"))
        # the following allos the rendered template to iterate
        # over the total number of courses a user selects
        string = "x" * first_val
        second_val = request.POST.get("desired_load")
    return render(request, 'SchedulerApp/courseform.html', {'prelim1': string,
                                                            'prelim2': second_val,})

def processmainform(request):
    # here is where the top sort logic goes
    #return HttpResponse("<h1>testing testing 123</h1>")

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
