from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserOTP(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    time_stamp=models.DateTimeField(auto_now=True)
    otp=models.SmallIntegerField()

#class Contact(models.Model):
#    user=models.ForeignKey(User, on_delete=models.CASCADE)
#http://www.learningaboutelectronics.com/Articles/How-to-insert-data-into-a-database-from-an-HTML-form-in-Django.php