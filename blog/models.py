from django.db import models

# Create your models here.
class Blog(models.Model):
    name           = models.TextField()
    last_name      = models.TextField()
    job_experience = models.TextField()
