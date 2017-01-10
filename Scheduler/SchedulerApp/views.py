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
    return HttpResponse("<h1>testing testing 123</h1>")
