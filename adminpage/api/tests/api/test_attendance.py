from datetime import date, datetime, timedelta
from typing import Tuple

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from api.views.attendance import AttendanceErrors
from sport.models import Trainer, Training, Attendance

before_training = datetime(2020, 1, 15, 17, 0, 0, tzinfo=timezone.utc)
training_start = datetime(2020, 1, 15, 18, 0, 0, tzinfo=timezone.utc)
during_training = datetime(2020, 1, 15, 19, 0, 0, tzinfo=timezone.utc)
training_end = datetime(2020, 1, 15, 20, 0, 0, tzinfo=timezone.utc)
long_after_training = training_start + settings.TRAINING_EDITABLE_INTERVAL + timedelta(hours=5)

assert before_training < training_start < during_training < training_end < long_after_training


@pytest.fixture
@pytest.mark.freeze_time(before_training)
def setup(
        semester_factory,
        sport_factory,
        group_factory,
        trainer_factory,
        student_factory,
        enroll_factory,
) -> Tuple[Training, Trainer, User]:
    semester_start = date(2020, 1, 1)
    semester_end = date(2020, 2, 20)
    choice_deadline = date(2020, 1, 10)
    sem = semester_factory(
        "S1",
        semester_start,
        semester_end,
        choice_deadline
    )

    trainer_user = trainer_factory(
        username="user",
        password="pass"
    )

    sport = sport_factory("sport1", False)
    group = group_factory(
        "G1",
        capacity=1,
        sport=sport,
        semester=sem,
        trainer=trainer_user.trainer,
        is_club=True,
    )

    training = Training.objects.create(
        group=group,
        schedule=None,
        start=training_start,
        end=training_end,
        training_class=None,
    )

    student_user = student_factory(
        username="student",
        password="student",
        email="student@example.com",
    )

    enroll_factory(student_user.student, group)

    return training, trainer_user, student_user


@pytest.mark.django_db
@pytest.mark.freeze_time(before_training)
def test_attendance_before_training(setup):
    training, trainer_user, student_user = setup
    client = APIClient()
    client.force_authenticate(trainer_user)

    data = {
        "training_id": training.pk,
        "students_hours": [
            {
                "student_id": student_user.student.pk,
                "hours": 1
            },
        ],
    }

    response = client.post(
        f"/{settings.PREFIX}api/attendance/mark",
        data=data,
        format='json'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["code"] == AttendanceErrors.TRAINING_NOT_EDITABLE[0]


@pytest.mark.django_db
@pytest.mark.freeze_time(long_after_training)
def test_attendance_long_after_training(setup):
    training, trainer_user, student_user = setup
    client = APIClient()
    client.force_authenticate(trainer_user)

    data = {
        "training_id": training.pk,
        "students_hours": [
            {
                "student_id": student_user.student.pk,
                "hours": 1
            },
        ],
    }

    response = client.post(
        f"/{settings.PREFIX}api/attendance/mark",
        data=data,
        format='json'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["code"] == AttendanceErrors.TRAINING_NOT_EDITABLE[0]


@pytest.mark.django_db
@pytest.mark.freeze_time(during_training)
def test_attendance_during_training_success(setup):
    training, trainer_user, student_user = setup
    client = APIClient()
    client.force_authenticate(trainer_user)
    hours_put = 1
    data = {
        "training_id": training.pk,
        "students_hours": [
            {
                "student_id": student_user.student.pk,
                "hours": hours_put
            },
        ],
    }

    response = client.post(
        f"/{settings.PREFIX}api/attendance/mark",
        data=data,
        format='json'
    )

    assert response.status_code == status.HTTP_200_OK
    assert Attendance.objects.filter(
        student=student_user.student.pk,
        hours=hours_put
    ).count() == 1


@pytest.mark.django_db
@pytest.mark.freeze_time(during_training)
def test_attendance_during_training_outbound(setup, student_factory):
    training, trainer_user, student_user = setup
    client = APIClient()
    client.force_authenticate(trainer_user)
    hours_put = 1
    hours_overflow = training.academic_duration + 0.5
    hours_underflow = -1

    student_user_overflow = student_factory(
        username="overflow",
        email="overflow@example.com"
    )

    student_user_underflow = student_factory(
        username="underflow",
        email="underflow@example.com"
    )

    data = {
        "training_id": training.pk,
        "students_hours": [
            {
                "student_id": student_user.student.pk,
                "hours": hours_put
            },
            {
                "student_id": student_user_overflow.student.pk,
                "hours": hours_overflow
            },
            {
                "student_id": student_user_underflow.student.pk,
                "hours": hours_underflow
            },
        ],
    }

    response = client.post(
        f"/{settings.PREFIX}api/attendance/mark",
        data=data,
        format='json'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["code"] == AttendanceErrors.OUTBOUND_GRADES[0]
    assert response.data["negative_marks"][0] == {
        "email": student_user_underflow.email,
        "hours": hours_underflow,
    }
    assert response.data["overflow_marks"][0] == {
        "email": student_user_overflow.email,
        "hours": hours_overflow,
    }
    assert Attendance.objects.count() == 0
