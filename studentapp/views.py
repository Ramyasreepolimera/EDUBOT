from django.shortcuts import render,redirect
from django.contrib import messages
from .models import StudentModel,StudentFeedbackModel,TempMediaModel
import random
from django.contrib.auth import logout
from adminapp.models import StudyMaterialModel
from textblob import TextBlob
import cv2
import os
# from matplotlib import image

from deepface import DeepFace



# Create your views here.


def stu_login(request):
   
    if request.method == 'POST' and 'img' in request.FILES:
        email = request.POST.get('email')
        password = request.POST.get('password')
            
        try:
            person = StudentModel.objects.get(email=email,password=password)
            if person.status == 'accept':

                img = request.FILES['img']
                obj = TempMediaModel.objects.create(new_img=img)
                imge ='media/'+ str(obj.new_img)
              
                path = 'media/'+ str(person.profile)
           
                img1= cv2.imread(path)
                img2= cv2.imread(imge)
                  
                result = DeepFace.verify(img1,img2)
                
                os.remove(imge)
                obj.delete()   

                if result['verified']==True:
                    request.session['stu_id']=person.stu_id 
                    # login(request,person)
                    messages.success(request,'Images are equal Student logged In successfully')
                    return redirect('stu-dashboard')
                    
                else:
                    print('images are not equal')
                    messages.error(request,'images are not equal')
                    return redirect('stu-login')
        except:
            messages.error(request,'Invalid Credentials')
            return redirect('stu-login')
        
    return render(request, 'student/stu-login.html')

def stu_register(request):
    if request.method == 'POST' and 'profile' in request.FILES:
        name = request.POST.get('name')
        s_id = request.POST.get('s_id')
        s_email = request.POST.get('email')
        # password = request.POST.get('password')
        mobile_number = request.POST.get('mobile')
        address = request.POST.get('address')
        pin_number = request.POST.get('pin')
        state = request.POST.get('state')
        country = request.POST.get('country')
        religion = request.POST.get('religion')
        profile = request.FILES['profile']

        # random password generating
        lower = 'abcdefghijklmnopqrstuvwxyz'
        upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        numbers = '0123456789'
        symbols = '!@#$%^&*'
        mix = lower+upper+numbers+symbols
        size = 8
        password = ''.join(random.sample(mix,size))

        # random student id generating
        # m = upper+numbers
        # le = 10
        # s_id = ''.join(random.sample(m,le)) 

        try:
            StudentModel.objects.get(email=s_email)
            messages.info(request, 'email already exists')
            return redirect('register')
        except:
            StudentModel.objects.create(
                name=name,
                s_id = s_id,
                email = s_email,
                password = password,
                mobile_no = mobile_number,
                address = address,
                pin = pin_number,
                state = state,
                country = country,
                religion = religion,
                profile = profile
            )

            messages.success(request, 'You have registered successfully wait for admin action')
            return redirect('stu-login')
        
    return render(request, 'student/register.html')

def stu_dashboard(request):
    feedback = StudentFeedbackModel.objects.all()[0:4]

    return render(request,'student/stu-dashboard.html',{"feedback":feedback})
def edubot(request):
    return render(request,'student/edubot.html')
def about(request):
    return render(request,'student/about.html')

def materials(request):
    material = StudyMaterialModel.objects.all()

    return render(request,'student/materials.html',{"material":material})

def profile(request):
    id = request.session['stu_id']
    stu = StudentModel.objects.get(pk=id)

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        pin = request.POST.get('pin')
        state = request.POST.get('state')
        religion = request.POST.get('religion')

        if not request.FILES.get('profile',False):
            stu.name = name
            stu.email = email
            stu.mobile_no = mobile
            stu.address = address
            stu.pin = pin
            stu.state = state
            stu.religion = religion

        if request.FILES.get('profile',False):
            image= request.FILES['profile']
            stu.name = name
            stu.email = email
            stu.mobile_no = mobile
            stu.address = address
            stu.pin = pin
            stu.state = state
            stu.religion = religion
            stu.profile = image
        stu.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')

    return render(request,'student/profile.html',{"student":stu})

def stu_feedback(request,id):
    stu_id= request.session['stu_id']
    stu = StudentModel.objects.get(pk=stu_id)
    # s = stu.stu_id
    stu_material = StudyMaterialModel.objects.get(pk=id)
    
    print(stu_material)
    if request.method == "POST":

        material = request.POST.get('material')
        video = request.POST.get('video')
        feedback = request.POST.get('feedback')

        if not request.POST.get('material'):
            messages.info(request,"Please rate for study material")
            return redirect('feedback')
    
        if not request.POST.get('video'):
            messages.info(request,"Please rate for videos")
            return redirect('feedback')
        
        if request.POST.get('feedback'):
            messages.success(request,"Feedback submited successfully")
            
        # sen = SentimentIntensityAnalyzer()
        analysis = TextBlob(feedback)
        # analysis = sen.polarity_scores(feedback)
        print(analysis)
        # print(analysis.sentiment)

        sentiment = ""
        if analysis.polarity >= 0.5:
            sentiment='very Positive'
        elif analysis.polarity > 0 and analysis.polarity < 0.5:
            sentiment='Positive'
        elif analysis.polarity < 0 and analysis.polarity > -0.5:
            sentiment='Negative' 
        elif analysis.polarity <= -0.5:
            sentiment='very Negative'       
        else:
            sentiment='Neutral'
        # print(sentiment['comound'])
        StudentFeedbackModel.objects.create(
            feedback = feedback,
            feedback_sentiment = sentiment,
            material = material,
            video = video,
            student = stu,
            stu_material =stu_material
        )
    
    return render(request,'student/stu-feedback.html')

def stu_logout(request):
    logout(request)
    messages.success(request, 'Student Logout successfully')
    return redirect('home')
