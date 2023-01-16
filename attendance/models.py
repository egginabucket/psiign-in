from __future__ import annotations

from functools import cached_property
from typing import Optional
from datetime import date

from django.db import models
from django.db.models import manager


class LearnerStatus(models.TextChoices):
    IN = "i", "in"
    ABS = "a", "absent"
    OUT_LUNCH = "ol", "out (lunch)"
    OUT_PHYS = "op", "out (physical inquiry)"
    OUT_APPT = "oa", "out (appointment)"

    @property
    def style(self) -> str:
        if self.value == self.IN:
            return "status-in"
        if self.value == self.ABS:
            return "status-absent"
        return "status-out"


class Learner(models.Model):
    records: "manager.RelatedManager[LearnerRecord]"
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.surname}"

    @property
    def short_name(self) -> str:
        if (
            self.__class__.objects.filter(
                is_active=True, first_name=self.first_name
            ).count()
            > 1
        ):
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
