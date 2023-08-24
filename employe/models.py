from django.db import models

# Create your models here.
class Emp(models.Model):
    name=models.CharField(max_length=200)
    emp_id=models.CharField(max_length=200)
    phone=models.CharField(max_length=20)
    address=models.CharField(max_length=200)
    working=models.BooleanField(default=True)
    department=models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

# Create your models here.
class Userlogin(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    email=models.CharField(max_length=20)
    islogin=models.CharField(max_length=200)

    def __str__(self):
        return self.username