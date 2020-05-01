import logging

from fastapi import APIRouter, Depends, responses
from fastapi.params import Path, Query

from app.db import mark_hours, clean_students_id, find_trainer, get_training_info, get_students_grades, Optional, \
    get_email_name_like_students
from app.models.attendance import MarkAttendanceRequest
from app.models.user import TokenUser
from app.utils.db import get_db
from app.utils.security import get_current_user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.get("/{training_id}/grades")
def mark_attendance(db=Depends(get_db),
                    user: TokenUser = Depends(get_current_user),
                    training_id: int = Path(..., gt=0)):
    trainer = find_trainer(db, user.email)
    training_info = get_training_info(db, training_id) if training_id is not None else None
    if trainer is None or training_info.trainer_id != trainer.id:
        return responses.JSONResponse(status_code=200, content={
            "ok": False,
            "error": {
                "code": 1,
                "description": "You are not a trainer for this group",
            }
        })
    return {
        "group_name": training_info.group_name,
        "start": training_info.start,
        "grades": get_students_grades(db, training_id)
    }


@router.post("/mark")
def mark_attendance(data: MarkAttendanceRequest,
                    db=Depends(get_db),
                    user: TokenUser = Depends(get_current_user)):
    """
    Put hours for training session for give students. Update hours if student already has hours for training
    """
    trainer = find_trainer(db, user.email)
    if trainer is None or get_training_info(db, data.training_id).trainer_id != trainer.id:
        return responses.JSONResponse(status_code=200, content={
            "ok": False,
            "error": {
                "code": 1,
                "description": "You are not a trainer for this group",
            }
        })
    training_info = get_training_info(db, data.training_id)
    max_hours = training_info.academic_duration
    cleaned_students = clean_students_id(db, tuple(data.students_hours.keys()))
    hours_to_mark = [(s.id, min(max_hours, data.students_hours[s.id])) for s in cleaned_students]
    mark_hours(db, data.training_id, hours_to_mark)
    return hours_to_mark


@router.get("/suggest_student")
def suggest_students(input_term: str = Query(..., alias="term"),
                     current_user: Optional[TokenUser] = Depends(get_current_user),
                     db=Depends(get_db)):
    if find_trainer(db, current_user.email) is not None:
        suggested_students = get_email_name_like_students(db, input_term)

        return [
            {
                "value": f"{student.id}_{student.full_name}_{student.email}",
                "label": f"{student.full_name} ({student.email})"
            }
            for student in
            suggested_students]

        # return [{"value": student.email, "label": f"{student.full_name} ({student.email})"} for student in
        #         suggested_students]
