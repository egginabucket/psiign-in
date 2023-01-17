from __future__ import annotations

from functools import cached_property
from typing import Optional
from datetime import date

from django.db import models
from django.db.models import manager


class LearnerStatus(models.TextChoices):
    IN = "i", "in"
    ABS = "a", "absent"
    OUT_HOME = "oh", "out - home"
    OUT_LUNCH = "ol", "out - lunch"
    OUT_VAB = "ov", "out - VAB"
    OUT_YMCA = "oy", "out - YMCA"
    OUT_CRAGX = "oc", "out - Crag X"
    OUT_APPT = "oa", "out - appointment"
    OUT_OTHER = "ox", "out - other"

    @property
    def style(self) -> str:
        if self.value == self.IN:
            return "status-in"
        if self.value == self.ABS:
            return "status-absent"
        return "status-out"


class LearnerQuerySet(models.QuerySet["Learner"]):
    def active(self) -> LearnerQuerySet:
        return self.filter(is_active=True)

    def sorted(self) -> LearnerQuerySet:
        return self.order_by("first_name", "surname")


class LearnerManager(models.Manager["Learner"]):
    def get_queryset(self) -> LearnerQuerySet:
        return LearnerQuerySet(self.model, using=self._db)

    def active(self) -> LearnerQuerySet:
        return self.get_queryset().active()

    def sorted(self) -> LearnerQuerySet:
        return self.get_queryset().sorted()


class Learner(models.Model):
    records: "manager.RelatedManager[LearnerRecord]"
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    objects = LearnerManager()

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.surname}"

    @property
    def short_name(self) -> str:
        if type(self).objects.active().filter(first_name=self.first_name).count() > 1:
            return f"{self.first_name} {self.surname[0]}"
        return self.first_name

    @cached_property
    def last_record(self) -> Optional[LearnerRecord]:
        return self.records.order_by("-time").first()

    @cached_property
    def last_record_today(self) -> Optional[LearnerRecord]:
        return self.records.filter(time__date=date.today()).order_by("-time").first()

    @property
    def status(self) -> LearnerStatus:
        if self.last_record_today is None:
            return LearnerStatus.ABS
        return LearnerStatus(self.last_record_today.action)

    def __str__(self) -> str:
        return self.full_name


class LearnerRecord(models.Model):
    learner = models.ForeignKey(
        Learner,
        related_name="records",
        on_delete=models.CASCADE,
    )
    time = models.DateTimeField()
    action = models.CharField(max_length=2, choices=LearnerStatus.choices)
    notes = models.TextField(null=True)
