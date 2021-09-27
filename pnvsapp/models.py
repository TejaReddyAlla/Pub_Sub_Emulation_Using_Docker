from django.db import models

# Create your models here.

class PalindromeCheck(models.Model):
    num= models.IntegerField(default=0)
    IsPalindrome=models.BooleanField()
