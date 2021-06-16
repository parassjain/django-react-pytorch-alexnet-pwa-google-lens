from django.db import models

# Create your models here.
def upload_path(instance, filename):
    return '/'.join(['cover',str(instance.title), filename])  

class React(models.Model):
    name = models.CharField(max_length=30)
    detail = models.CharField(max_length=500)
    ai_result = models.CharField(max_length=200, null=True)    
    cover = models.ImageField(blank=True,null=True, upload_to = upload_path)
    img_url = models.CharField(max_length=200, null=True)

class Post(models.Model):
    title = models.CharField(max_length=100, null=True, default="sample", blank=True)
    content = models.TextField(null=True,default="sample content", blank=True)
    image = models.ImageField(upload_to='post_images')
    image_url = models.CharField(max_length=200, null=True)
    pytorch_label = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.title