from django.shortcuts import render

def home(request):
    return render(request, "restaurant_manage/index.html")

def view_or_write(request):
    return render(request, "restaurant_manage/view_or_write.html")