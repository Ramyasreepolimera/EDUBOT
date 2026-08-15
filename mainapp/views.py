from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'main/index.html')

def about(request):
    return render(request,'main/about.html')

def courses(request):
    return render(request, 'main/courses.html')

def courses_details(request):
    return render(request,'main/course-details.html')

def contact(request):
    return render(request,'main/contact.html')