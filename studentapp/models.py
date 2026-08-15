from django.db import models
from adminapp.models import StudyMaterialModel

# Create your models here.

class StudentModel(models.Model):
    stu_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    s_id = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=250)
    mobile_no = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    pin = models.CharField(max_length=6)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    religion = models.CharField(max_length=50)
    profile = models.ImageField(upload_to='images/',null=True)
    face = models.ImageField(null=True,upload_to='images/')
    status = models.CharField(max_length=250,default='pending')


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Student_details_table'

class TempMediaModel(models.Model):
    im_id = models.AutoField(primary_key=True)
    
    new_img = models.ImageField(upload_to='images/')
    
    class Meta:
        db_table = 'imagesource'


class StudentFeedbackModel(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(StudentModel,on_delete=models.CASCADE,null=True)
    stu_material = models.ForeignKey(StudyMaterialModel, on_delete=models.CASCADE,null=True)
    feedback = models.TextField()
    feedback_sentiment = models.CharField(max_length=50)
    feedback_date = models.DateTimeField(auto_now_add=True)
    material = models.IntegerField(help_text='rating1', null=True)
    video = models.IntegerField(help_text='rating2', null=True)


    class Meta:
        db_table = 'student_feedback'
