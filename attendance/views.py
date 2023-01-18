import csv
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, FileResponse
from django.shortcuts import render

from attendance.models import Learner, LearnerRecord, LearnerStatus


class Echo:
    def write(self, value):
        return value


def index(request: HttpRequest):
    ctx = {
        "learners": Learner.objects.active().sorted(),
        "actions": LearnerStatus,
    }
    if (request.method or "").lower() in "post":
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


@login_required
def history_tsv(request: HttpRequest):
    def get_rows():
        yield ["learner", "date", "time", "action", "notes"]
        for r in LearnerRecord.objects.all():
            yield [
                r.learner.full_name,
                r.time.strftime("%Y-%m-%d"),
                r.time.strftime("%H:%M"),
                r.action,
                r.notes,
            ]

    w = csv.writer(Echo(), delimiter="\t")
    return FileResponse(
        map(w.writerow, get_rows()),
        content_type="text/tab-separated-values",
        as_attachment=True,
        filename="history.tsv",
    )
