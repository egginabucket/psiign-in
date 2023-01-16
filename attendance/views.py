from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from attendance.models import Learner, LearnerRecord, LearnerStatus
from datetime import datetime

def index(request: HttpRequest):
    ctx = {
        "learners": Learner.objects.filter(is_active=True).order_by("first_name", "surname"),
        "actions": LearnerStatus,
    }
    if request.method == "POST":
        LearnerRecord.objects.create(time=datetime.now(), learner=Learner.objects.get(id=int(request.POST["learner"])), action=request.POST["action"])
    
    return render(request, "attendance/index.html", ctx)

    

@login_required
def overview(request: HttpRequest):
    ctx = {
        "learners": Learner.objects.filter(is_active=True).order_by("first_name", "surname")
    }
    return render(request, "attendance/overview.html", ctx)

