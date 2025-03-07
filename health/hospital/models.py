from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='departments/', blank=True, null=True)


    def __str__(self):
        return self.name



 