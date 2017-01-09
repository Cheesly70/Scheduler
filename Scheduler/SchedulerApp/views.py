from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    #return HttpResponse("<h2>HEY!</h2>")
    return render(request, 'SchedulerApp/home.html') #{'form': form,
                                                      #'class_num': classnum,})

def mainform(request): # test
    return HttpResponse("<h1>testing testing 123</h1>")

def getmainfom(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        first_val = request.POST.get('total_load')
        second_val = request.POST.get('desired_load')
    return render(request, 'SchedulerApp/courseform.html', {'prelim1': first_val,
                                                            'prelim2': second_val,})

def processmainform(request):
    return HttpResponse("<h1>testing testing 123</h1>")
