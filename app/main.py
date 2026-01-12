# app/main.py
from datetime import datetime
from sqlalchemy import and_, func
from models.models import (
    Member, Trainer, Room, HealthMetric, FitnessGoal,
    Availability, PersonalTrainingSession, GroupClass, ClassRegistration
)
from app.database import SessionLocal, init_db

def register_member(session, name, email, dob=None, gender=None, phone=None):
    # MEMBER OP 1: registration
    existing = session.query(Member).filter_by(email=email).first()
    if existing:
        print("Email already registered.")
        return None
    member = Member(name=name, email=email, dob=dob, gender=gender, phone=phone)
    session.add(member)
    session.commit()
    print(f"Registered member #{member.id}: {member.name}")
    return member


def update_member_profile(session, member_id, **kwargs):
    # MEMBER OP 2: update profile
    member = session.get(Member, member_id)
    if not member:
        print("Member not found.")
        return
    for field in ["name", "email", "gender", "phone"]:
        if field in kwargs and kwargs[field] is not None:
            setattr(member, field, kwargs[field])
    session.commit()
    print(f"Updated profile for member #{member.id}")


def log_health_metric(session, member_id, weight=None, heart_rate=None, body_fat=None):
    # MEMBER OP 3: log metric (history, not overwrite)
    member = session.get(Member, member_id)
    if not member:
        print("Member not found.")
        return
    metric = HealthMetric(
        member_id=member_id,
        weight=weight,
        heart_rate=heart_rate,
        body_fat=body_fat,
        recorded_at=datetime.utcnow()
    )
    session.add(metric)
    session.commit()
    print(f"Logged health metric #{metric.id} for member #{member_id}")


def register_for_class(session, member_id, class_id):
    # MEMBER OP 4: register for a group class with capacity check
    gc = session.get(GroupClass, class_id)
    if not gc:
        print("Class not found.")
        return
    member = session.get(Member, member_id)
    if not member:
        print("Member not found.")
        return

    # Check capacity
    current_count = session.query(func.count(ClassRegistration.id))\
                           .filter(ClassRegistration.class_id == class_id)\
                           .scalar()
    if current_count >= gc.capacity:
        print("Class is full.")
        return

    # Avoid duplicate registration
    existing = session.query(ClassRegistration)\
                      .filter_by(member_id=member_id, class_id=class_id)\
                      .first()
    if existing:
        print("Member already registered in this class.")
        return

    reg = ClassRegistration(member_id=member_id, class_id=class_id)
    session.add(reg)
    session.commit()
    print(f"Member #{member_id} registered in class #{class_id}")


def set_trainer_availability(session, trainer_id, start_time, end_time):
    # TRAINER OP 1: set availability, prevent overlap
    trainer = session.get(Trainer, trainer_id)
    if not trainer:
        print("Trainer not found.")
        return

    overlap = session.query(Availability).filter(
        Availability.trainer_id == trainer_id,
        Availability.start_time < end_time,
        Availability.end_time > start_time
    ).first()

    if overlap:
        print("New availability overlaps with an existing one.")
        return

    slot = Availability(
        trainer_id=trainer_id,
        start_time=start_time,
        end_time=end_time
    )
    session.add(slot)
    session.commit()
    print(f"Added availability #{slot.id} for trainer #{trainer_id}")


def view_trainer_schedule(session, trainer_id):
    # TRAINER OP 2: view PT sessions + classes
    trainer = session.get(Trainer, trainer_id)
    if not trainer:
        print("Trainer not found.")
        return

    print(f"Schedule for trainer #{trainer.id} - {trainer.name}")
    print("Personal Training Sessions:")
    for s in trainer.pt_sessions:
        print(f"  Session #{s.id} with member #{s.member_id} in room #{s.room_id} at {s.start_time}")

    print("\nGroup Classes:")
    for c in trainer.classes:
        print(f"  Class #{c.id} '{c.name}' in room #{c.room_id} at {c.start_time}")


def admin_create_class(session, name, trainer_id, room_id, start_time, end_time, capacity):
    # ADMIN OP 1: create a new group class
    trainer = session.get(Trainer, trainer_id)
    room = session.get(Room, room_id)

    if not trainer or not room:
        print("Trainer or Room not found.")
        return

    # Check room clash with existing classes
    clash = session.query(GroupClass).filter(
        GroupClass.room_id == room_id,
        GroupClass.start_time < end_time,
        GroupClass.end_time > start_time
    ).first()
    if clash:
        print("Room is already booked for another class in that time.")
        return

    gc = GroupClass(
        name=name,
        trainer_id=trainer_id,
        room_id=room_id,
        start_time=start_time,
        end_time=end_time,
        capacity=capacity
    )
    session.add(gc)
    session.commit()
    print(f"Created group class #{gc.id} '{name}'")


def admin_book_pt_session(session, member_id, trainer_id, room_id, start_time, end_time):
    # ADMIN OP 2: book PT session, check room + trainer conflicts
    member = session.get(Member, member_id)
    trainer = session.get(Trainer, trainer_id)
    room = session.get(Room, room_id)

    if not member or not trainer or not room:
        print("Member, Trainer, or Room not found.")
        return

    # Check trainer already booked
    trainer_conflict = session.query(PersonalTrainingSession).filter(
        PersonalTrainingSession.trainer_id == trainer_id,
        PersonalTrainingSession.start_time < end_time,
        PersonalTrainingSession.end_time > start_time
    ).first()
    if trainer_conflict:
        print("Trainer is not available in that time slot.")
        return

    # Check room already booked
    room_conflict = session.query(PersonalTrainingSession).filter(
        PersonalTrainingSession.room_id == room_id,
        PersonalTrainingSession.start_time < end_time,
        PersonalTrainingSession.end_time > start_time
    ).first()
    if room_conflict:
        print("Room is already booked for that time.")
        return

    session_obj = PersonalTrainingSession(
        member_id=member_id,
        trainer_id=trainer_id,
        room_id=room_id,
        start_time=start_time,
        end_time=end_time
    )
    session.add(session_obj)
    session.commit()
    print(f"Booked PT session #{session_obj.id}")

def main():
    init_db()
    session = SessionLocal()


    if session.query(Trainer).count() == 0:
        t = Trainer(name="Alice Trainer", email="alice@fitclub.com", specialty="Strength")
        session.add(t)
    if session.query(Room).count() == 0:
        r = Room(name="Studio A", capacity=20)
        session.add(r)
    session.commit()
    
if __name__ == "__main__":
    main()