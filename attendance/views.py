import csv
from datetime import datetime
from typing import Iterable

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, FileResponse
from django.shortcuts import redirect, render

from attendance.models import Learner, LearnerRecord, LearnerStatus


class Echo:
    def write(self, value):
        return value
    
def stream_tsv(it: Iterable, filename: str) -> FileResponse:
    w = csv.writer(Echo(), delimiter="\t")
    return FileResponse(
        map(w.writerow, it),
        content_type="text/tab-separated-values",
        as_attachment=True,
        filename=filename
    )


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
        ctx["last_record"] = record

    return render(request, "attendance/index.html", ctx)


@login_required
def overview(request: HttpRequest):
    ctx = {
        "learners": Learner.objects.active().sorted(),
        "show_nav": True,
    }
    return render(request, "attendance/overview.html", ctx)


def overview_offline(request: HttpRequest):
    ctx = {
        "learners": Learner.objects.active().sorted(),
        "show_nav": False,
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
                r.get_action_display(),
                r.notes,
            ]
    return stream_tsv(get_rows(), "history.tsv")

def overview_tsv(request: HttpRequest):
    return redirect(datetime.now().strftime("/overview-dl/overview_%Y-%m-%d.tsv"))

def overview_tsv_dl(request: HttpRequest, filename: str):
    def get_rows():
        yield ["learner", "status", "time", "notes"]
        for l in Learner.objects.active().sorted():
            r = l.last_record_today
            yield [
                l.full_name,
                l.status.label,
                r and r.time.strftime("%H:%M"),
                r and r.notes,
            ]
    return stream_tsv(get_rows(), filename)