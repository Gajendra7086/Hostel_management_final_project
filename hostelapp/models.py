from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    is_warden_owner = models.BooleanField(default=False)
    is_hostler = models.BooleanField(default=False)
    username = models.EmailField(unique=True)
    mobile_no = models.IntegerField(null=True, blank=True)
    hostel_name = models.CharField(max_length=50, null=True, blank=True)
    details_status = models.BooleanField(default=False)
    addhar_no = models.CharField(max_length=12,null=True, blank=True)


class Hostel(models.Model):
    hostel_name_user = models.ForeignKey(User, on_delete=models.CASCADE)
    hostel_name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100)
    no_of_rooms = models.IntegerField()

    def __str__(self):
        return self.hostel_name


class Hostel_verification(models.Model):
    hostel_name = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    email = models.EmailField()
    code = models.CharField(max_length=6)


class Complain(models.Model):
    STATUS = [
        ('solved', 'Solved'),
        ('pending', 'Pending'),
        ('returned', 'Returned'),
    ]
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    hostel_name = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)
    complain_status = models.CharField(choices=STATUS, default="pending", max_length=8)
    date = models.DateField(default=timezone.now)


class Payment(models.Model):
    hostel_name = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    slip_no = models.BigIntegerField()
    date = models.DateField(default=timezone.now)
    name = models.CharField(max_length=100)
    month_year = models.CharField(max_length=20)
    amount = models.IntegerField()
    remark = models.CharField(max_length=256,null=True,blank=True)
