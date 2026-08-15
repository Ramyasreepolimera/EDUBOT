from django.shortcuts import render,redirect
from django.contrib import messages
from studentapp.models import StudentModel
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives
from SmartChatbox.settings import DEFAULT_FROM_EMAIL 
from .models import StudyMaterialModel
from studentapp.models import StudentFeedbackModel
from django.contrib.auth import logout

# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        print(name, password)
        if name == 'admin' and password == 'admin':
            messages.success(request,'admin login successfully')
            return redirect('admin-dashboard')
        else:
            messages.info(request,'invalid credentials')
            return redirect('admin-login')

    return render(request, 'admin/admin-login.html')

def admin_dashboard(request):
    students = StudentModel.objects.filter(status='accept').count()
    materials = StudyMaterialModel.objects.all().count()
    videos = StudyMaterialModel.objects.exclude(videos="", videos_link=None).count()
    # material = materials.material_file
    context = {
        "students":students,
        "materials":materials,
        'videos':videos
    }
    return render(request,'admin/admin-dashbord.html',context)

def pending_students(request):
    pending_stu = StudentModel.objects.filter(status='pending')

    paginator = Paginator(pending_stu,4)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)

    if request.method == "GET":
        persion = request.GET.get('search')
        
        if persion:
            student = StudentModel.objects.filter(name__icontains=persion).filter(status='pending')
            count = student.count()
            if count==0:
                messages.info(request,'Student does not exists')
                return redirect('pending-Students')

            return render(request,'admin/pending-students.html',{"pending_stu":student})

    return render(request,'admin/pending-students.html',{"pending_stu":page})

def accept_stu(request,id):
    stu = StudentModel.objects.get(pk=id)
    stu.status = 'accept'
    stu.save(update_fields=['status'])
    stu.save()

    mail =stu.email
    html_content = f'Welcome to our college this is your password:{stu.password} to login in to your account'
    from_mail = DEFAULT_FROM_EMAIL
    to_mail = [mail]

    try:
        message = EmailMultiAlternatives('Authentication password for login',html_content,from_mail,to_mail)
        message.attach_alternative(html_content, 'text/html')
        if message.send():
            messages.success(request,'credentials has been sent successfully')
            return redirect('pending-Students')

    except:
            messages.error(request, 'there is problem try again ')
            return redirect('pending-Students')


    messages.success(request,'Student accepted successfully')
    return redirect('pending-Students')

def reject_stu(request,id):
    stu = StudentModel.objects.get(pk=id)
    stu.delete()
    messages.success(request,'student rejected successfully')
    return redirect('pending-Students')

def all_students(request):
    all_stu = StudentModel.objects.filter(status='accept')

    paginator = Paginator(all_stu,4)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)

    if request.method == "GET":
        persion = request.GET.get('query')
        
        if persion:
            student = StudentModel.objects.filter(name__icontains=persion)
            count = student.count()
            if count==0:
                messages.info(request,'Student does not exists')
                return redirect('all-Students')

            return render(request,'admin/all-students.html',{"all_stu":student})

    return render(request, 'admin/all-students.html',{"all_stu":page})

def delete_stu(request,id):
    stu = StudentModel.objects.get(pk=id)
    stu.delete()
    messages.success(request,'student Deleted successfully')
    return redirect('all-Students')

def add_materials(request):
    if request.method == "POST":
        title = request.POST.get('title')
        subject = request.POST.get('subject')
        pdf = request.FILES['file']
    
        link = request.POST.get('link')
        if not request.POST.get('link') and not request.FILES.get('video',False):
            messages.warning(request,' upload video or  video link')
            return redirect('add-interview-videos')

        
        if request.POST.get('link') and request.FILES.get('video',False):
            link = request.POST.get('link')
            video = request.FILES['video']
            video_link = str(link)
            url = video_link.replace('https://www.youtube.com/watch?v=','https://youtube.com/embed/')
            StudyMaterialModel.objects.create(
            title = title,
            subject_name = subject,
            material_file = pdf,
            videos_link = url,
            videos = video,
            
        )
      

        if request.POST.get('link') and not request.FILES.get('video',False):
            link = request.POST.get('link')
            video_link = str(link)
            url = video_link.replace('https://www.youtube.com/watch?v=','https://youtube.com/embed/')
            StudyMaterialModel.objects.create(
            title = title,
            subject_name = subject,
            material_file = pdf,
            videos_link = url
        )
        if not request.POST.get('link') and request.FILES.get('video',False):
            video = request.FILES['video']

            StudyMaterialModel.objects.create(
                title = title,
                subject_name = subject,
                material_file = pdf,
                videos = video,
             
            )
            print(subject)
        messages.success(request,'Material added successfully')
        return redirect('add-study-material')
    return render(request, 'admin/add-study-material.html')

def manage_study_material(request):
    materials = StudyMaterialModel.objects.all().order_by('-material_id')

    paginator = Paginator(materials,4)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)

    if request.method == "GET":
        material = request.GET.get('query')
        
        if material:
            material = StudyMaterialModel.objects.filter(title__icontains=material)
            count = material.count()
            if count==0:
                messages.info(request,'Material does not exists')
                return redirect('manage-study-material')

            return render(request,'admin/manage-study-material.html',{"materials":material})


    return render(request,'admin/manage-study-material.html',{'materials':page})

def edit_material(request,id):
    material = StudyMaterialModel.objects.get(pk=id)

    if request.method == 'POST':
        title= request.POST.get('title')
        subject = request.POST.get('subject')
       

        link = request.POST.get('link')
        link = str(link)
        url = link.replace('https://www.youtube.com/watch?v=','https://youtube.com/embed/')

        if not request.FILES.get('file',False):
            material.title = title
            material.subject_name = subject
            # material.material_file = pdf
            material.videos_link = url

        if request.FILES.get('file',False):
            pdf = request.FILES['file']
            material.title = title
            material.subject_name = subject
            material.material_file = pdf
            material.videos_link = url

        if not request.FILES.get('video',False):
            material.title = title
            material.subject_name = subject
            # material.material_file = pdf
            material.videos_link = url

        if request.FILES.get('video',False):
            video = request.FILES['video']
            material.title = title
            material.subject_name = subject
            # material.material_file = pdf
            material.videos_link = url
            material.videos = video
        material.save()
        messages.success(request, 'material updated successfully')
        return redirect('manage-study-material')


    return render(request,'admin/edit-material.html',{'material':material})

def delete_material(request,id):
    material = StudyMaterialModel.objects.get(pk=id)
    material.delete()
    messages.success(request,'material deleted successfully')
    return redirect('manage-study-material')

def sentiment_analysis(request):
    feedback = StudentFeedbackModel.objects.all().order_by('-feedback_id')

    pagination = Paginator(feedback,3)
    page_no = request.GET.get('page')
    page = pagination.get_page(page_no)

    return render(request,'admin/sentiment-analysis.html',{'feedback':page})

def sentiment_graph(request):
    positive = StudentFeedbackModel.objects.filter(feedback_sentiment='Positive').count()
    very_positive = StudentFeedbackModel.objects.filter(feedback_sentiment='very Positive').count()
    negetive = StudentFeedbackModel.objects.filter(feedback_sentiment='Negative').count()
    very_negetive = StudentFeedbackModel.objects.filter(feedback_sentiment='very Negative').count()
    neutral = StudentFeedbackModel.objects.filter(feedback_sentiment='Neutral').count()

    context = {
        'positive':positive,
        'very_positive':very_positive,
        'negetive':negetive,
        'very_negetive':very_negetive,
        'neutral':neutral
    }
    return render(request,'admin/sentiment-graph.html',context)
    
def admin_logout(request):
    logout(request)
    messages.success(request,'Admin logout successfully')
    return redirect('home')
