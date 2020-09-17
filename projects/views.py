from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'projects/index.template.html')
    # return HttpResponse("project app")
