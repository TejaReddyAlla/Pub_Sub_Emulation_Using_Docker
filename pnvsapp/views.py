
from django.shortcuts import render
from django.http import HttpResponse
from .models import PalindromeCheck

# Create your views here.

def home(request):
    
    return render(request, 'home.html',{'name':'Random Surfer'})

def pc(request):

    val1=(request.GET["num1"])
    res = val1==val1[::-1]

    record=PalindromeCheck(num=val1,IsPalindrome=res)
    print(record)
    record.save()

    return render(request, "result.html", {'result':res})

def recoup(request):

    records=PalindromeCheck.objects.all()
    print(records)
    return render(request,"recoup.html",{'rows':records})

