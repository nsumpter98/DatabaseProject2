from django.db import models

# Create your models here.

# CustomerID,Gender,Age,Education,Occupation,MaritalStatus,ProductRating
# 1001,Male,35,Bachelor's,Digital Marketing,Married,4.5

class Person(models.Model):

    customer_id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=10, null=True)
    age = models.IntegerField(null=True)
    education = models.CharField(max_length=20, null=True)
    occupation = models.CharField(max_length=20, null=True)
    marital_status = models.CharField(max_length=10, null=True)
    product_rating = models.FloatField(max_length=10, null=True)


    def __str__(self):
        return str(self.customer_id)

# commands to create the database
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser
# python manage.py runserver