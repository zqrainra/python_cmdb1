from django.shortcuts import render
from models import CPU
# Create your views here.
def index(request):
    cpus = CPU.objects.all()
    return render(request,'assets/index.html',{'cpus':cpus})