# models/models.py
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Float, ForeignKey, Boolean
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    dob = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)

    health_metrics = relationship("HealthMetric", back_populates="member", cascade="all, delete-orphan")
    goals = relationship("FitnessGoal", back_populates="member", cascade="all, delete-orphan")
    pt_sessions = relationship("PersonalTrainingSession", back_populates="member", cascade="all, delete-orphan")
    class_registrations = relationship("ClassRegistration", back_populates="member", cascade="all, delete-orphan")


class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)

    availabilities = relationship("Availability", back_populates="trainer", cascade="all, delete-orphan")
    pt_sessions = relationship("PersonalTrainingSession", back_populates="trainer", cascade="all, delete-orphan")
    classes = relationship("GroupClass", back_populates="trainer", cascade="all, delete-orphan")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    capacity = Column(Integer, nullable=False)

    pt_sessions = relationship("PersonalTrainingSession", back_populates="room", cascade="all, delete-orphan")
    classes = relationship("GroupClass", back_populates="room", cascade="all, delete-orphan")


class HealthMetric(Base):
    __tablename__ = "health_metrics"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    weight = Column(Float, nullable=True)
    heart_rate = Column(Integer, nullable=True)
    body_fat = Column(Float, nullable=True)

    member = relationship("Member", back_populates="health_metrics")


class FitnessGoal(Base):
    __tablename__ = "fitness_goals"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    description = Column(String, nullable=False)
    target_weight = Column(Float, nullable=True)
    target_body_fat = Column(Float, nullable=True)
    status = Column(String, default="active")  # active / completed / cancelled

    member = relationship("Member", back_populates="goals")


class Availability(Base):
    __tablename__ = "availabilities"

    id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    trainer = relationship("Trainer", back_populates="availabilities")


class PersonalTrainingSession(Base):
    __tablename__ = "pt_sessions"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, default="scheduled")  # scheduled / cancelled / completed

    member = relationship("Member", back_populates="pt_sessions")
    trainer = relationship("Trainer", back_populates="pt_sessions")
    room = relationship("Room", back_populates="pt_sessions")


class GroupClass(Base):
    __tablename__ = "group_classes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)

    trainer = relationship("Trainer", back_populates="classes")
    room = relationship("Room", back_populates="classes")
    registrations = relationship("ClassRegistration", back_populates="group_class", cascade="all, delete-orphan")


class ClassRegistration(Base):
    __tablename__ = "class_registrations"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("group_classes.id"), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    member = relationship("Member", back_populates="class_registrations")
    group_class = relationship("GroupClass", back_populates="registrations")

from sqlalchemy import Index

Index("ix_member_email", Member.email)
Index("ix_trainer_email", Trainer.email)
Index("ix_ptsession_start_time", PersonalTrainingSession.start_time)
