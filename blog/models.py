from django.db import models

# Create your models here.
class Blog(models.Model):
    title          = models.CharField(max_length=126)
    content        = models.TextField()
    name           = models.TextField()
    last_name      = models.TextField()
    job_experience = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        pass