from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from attendance.models import Learner, LearnerRecord, LearnerStatus
from datetime import datetime


def index(request: HttpRequest):
    ctx = {
        "learners": Learner.objects.active().sorted(),
        "actions": LearnerStatus,
    }
    if request.method == "POST":
        record = LearnerRecord(
            time=datetime.now(),
            learner=Learner.objects.get(id=int(request.POST["learner"])),
            action=request.POST["action"],
        )
        if notes := request.POST.get("notes"):
            record.notes = notes
        record.save()

    return render(request, "attendance/index.html", ctx)


@login_required
def overview(request: HttpRequest):
    ctx = {
        "learners": Learner.objects.active().sorted(),
    }
    return render(request, "attendance/overview.html", ctx)
