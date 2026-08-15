from django.db import models


# Create your models here.

class StudyMaterialModel(models.Model):
    material_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=240)
    subject_name = models.CharField(max_length=250)
    material_file = models.FileField(upload_to='materials/',null=True)
    videos = models.FileField(upload_to='videos/',null=True)
    videos_link = models.CharField(max_length=250,null=True)


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'StudyMaterials'
        




    
