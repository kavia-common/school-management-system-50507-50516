from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# Common mixins
class Timestamps(BaseModel):
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Teacher
class TeacherBase(BaseModel):
    first_name: str = Field(..., description="Teacher first name")
    last_name: str = Field(..., description="Teacher last name")
    email: EmailStr = Field(..., description="Unique email")
    subject: Optional[str] = Field(None, description="Subject specialization")
    phone: Optional[str] = Field(None, description="Contact phone number")


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    subject: Optional[str] = None
    phone: Optional[str] = None


class TeacherOut(TeacherBase, Timestamps):
    id: int


# Student
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    enrollment_date: Optional[date] = None
    grade: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    enrollment_date: Optional[date] = None
    grade: Optional[str] = None


class StudentOut(StudentBase, Timestamps):
    id: int


# Staff
class StaffBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: Optional[str] = None
    phone: Optional[str] = None


class StaffCreate(StaffBase):
    pass


class StaffUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    phone: Optional[str] = None


class StaffOut(StaffBase, Timestamps):
    id: int


# Exam
class ExamBase(BaseModel):
    title: str
    subject: str
    exam_date: date
    description: Optional[str] = None


class ExamCreate(ExamBase):
    pass


class ExamUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    exam_date: Optional[date] = None
    description: Optional[str] = None


class ExamOut(ExamBase, Timestamps):
    id: int
