# app/cli.py

from app.database import SessionLocal, init_db
from models.models import (
    Member, Trainer, Room, HealthMetric, FitnessGoal,
    PersonalTrainingSession, GroupClass, ClassRegistration, Availability
)
from datetime import datetime

session = SessionLocal()


# ----------------------------------------------------
#   MEMBER OPERATIONS
# ----------------------------------------------------

def register_member():
    print("\n--- Register New Member ---")
    name = input("Name: ")
    dob = input("DOB (YYYY-MM-DD): ")
    gender = input("Gender: ")
    email = input("Email: ")
    phone = input("Phone: ")

    dob_val = datetime.strptime(dob, "%Y-%m-%d") if dob else None

    m = Member(name=name, dob=dob_val, gender=gender, email=email, phone=phone)
    session.add(m)
    session.commit()

    print(f"Member registered with ID #{m.id}")


def update_member():
    print("\n--- Update Member Profile ---")
    member_id = int(input("Member ID: "))

    m = session.get(Member, member_id)
    if not m:
        print("Member not found.")
        return

    m.name = input(f"Name ({m.name}): ") or m.name
    m.email = input(f"Email ({m.email}): ") or m.email
    m.phone = input(f"Phone ({m.phone}): ") or m.phone

    session.commit()
    print("Profile updated.")


def log_health_metric():
    print("\n--- Log Health Metric ---")
    member_id = int(input("Member ID: "))

    weight = float(input("Weight (kg): "))
    hr = int(input("Heart rate: "))
    bf = float(input("Body Fat %: "))

    metric = HealthMetric(
        member_id=member_id,
        weight=weight,
        heart_rate=hr,
        body_fat=bf
    )

    session.add(metric)
    session.commit()

    print("Health metric logged.")


def register_for_class():
    print("\n--- Register for Group Class ---")
    member_id = int(input("Member ID: "))
    class_id = int(input("Class ID: "))

    reg = ClassRegistration(member_id=member_id, class_id=class_id)
    session.add(reg)
    session.commit()

    print("Registration successful.")


# ----------------------------------------------------
#   TRAINER OPERATIONS
# ----------------------------------------------------

def set_trainer_availability():
    print("\n--- Set Trainer Availability ---")
    trainer_id = int(input("Trainer ID: "))

    start = input("Start time (YYYY-MM-DD HH:MM): ")
    end = input("End time (YYYY-MM-DD HH:MM): ")

    start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")

    a = Availability(trainer_id=trainer_id, start_time=start_dt, end_time=end_dt)
    session.add(a)
    session.commit()

    print("Availability added.")


def view_trainer_schedule():
    print("\n--- Trainer Schedule ---")
    trainer_id = int(input("Trainer ID: "))

    t = session.get(Trainer, trainer_id)
    if not t:
        print("Trainer not found.")
        return

    print(f"\nSchedule for {t.name}")

    print("\nPersonal Training Sessions:")
    for s in t.pt_sessions:
        print(f"- Session #{s.id} with member #{s.member_id} at {s.start_time}")

    print("\nGroup Classes:")
    for c in t.classes:
        print(f"- Class #{c.id} '{c.name}' at {c.start_time}")



# ----------------------------------------------------
#   ADMIN OPERATIONS
# ----------------------------------------------------

def create_group_class():
    print("\n--- Create Group Class ---")

    name = input("Class name: ")
    trainer_id = int(input("Trainer ID: "))
    room_id = int(input("Room ID: "))
    capacity = int(input("Capacity: "))

    start = input("Start time (YYYY-MM-DD HH:MM): ")
    end = input("End time (YYYY-MM-DD HH:MM): ")

    start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")

    gc = GroupClass(
        name=name,
        trainer_id=trainer_id,
        room_id=room_id,
        start_time=start_dt,
        end_time=end_dt,
        capacity=capacity
    )

    session.add(gc)
    session.commit()

    print(f"Group class created with ID #{gc.id}")

def create_trainer():
    name = input("Trainer name: ")
    email = input("Email: ")
    specialty = input("Specialty: ")

    t = Trainer(name=name, email=email, specialty=specialty)
    session.add(t)
    session.commit()
    print(f"Trainer #{t.id} created.")

def create_room():
    session = SessionLocal()
    print("\n=== Create a Room ===")
    name = input("Room name: ").strip()
    capacity = int(input("Capacity: "))

    # Check duplicate name (rooms must have unique names)
    existing = session.query(Room).filter_by(name=name).first()
    if existing:
        print("A room with this name already exists.")
        session.close()
        return

    room = Room(name=name, capacity=capacity)
    session.add(room)
    session.commit()

    print(f"Room created successfully with ID: {room.id}")
    session.close()


def book_pt_session():
    print("\n--- Book Personal Training Session ---")

    member_id = int(input("Member ID: "))
    trainer_id = int(input("Trainer ID: "))
    room_id = int(input("Room ID: "))

    start = input("Start time (YYYY-MM-DD HH:MM): ")
    end = input("End time (YYYY-MM-DD HH:MM): ")

    start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")

    s = PersonalTrainingSession(
        member_id=member_id,
        trainer_id=trainer_id,
        room_id=room_id,
        start_time=start_dt,
        end_time=end_dt
    )

    session.add(s)
    session.commit()

    print(f"Session booked with ID #{s.id}")



# ----------------------------------------------------
#   MENUS
# ----------------------------------------------------

def member_menu():
    while True:
        print("\n=== MEMBER MENU ===")
        print("1. Register Member")
        print("2. Update Profile")
        print("3. Log Health Metric")
        print("4. Register for Group Class")
        print("0. Back")

        choice = input("Select: ")

        if choice == "1": register_member()
        elif choice == "2": update_member()
        elif choice == "3": log_health_metric()
        elif choice == "4": register_for_class()
        elif choice == "0": break


def trainer_menu():
    while True:
        print("\n=== TRAINER MENU ===")
        print("1. Set Availability")
        print("2. View Schedule")
        print("0. Back")

        choice = input("Select: ")

        if choice == "1": set_trainer_availability()
        elif choice == "2": view_trainer_schedule()
        elif choice == "0": break


def admin_menu():
    while True:
        print("\n=== ADMIN MENU ===")
        print("1. Create Trainer")
        print("2. Create Group Class")
        print("3. Book Personal Training Session")
        print("4. Create a room")
        print("0. Back")

        choice = input("Select: ")

        if choice == "1": create_trainer()
        elif choice == "2": create_group_class()
        elif choice == "3": book_pt_session()
        elif choice == "4": create_room()
        elif choice == "0": break



# ----------------------------------------------------
#   MAIN MENU
# ----------------------------------------------------

def main():
    init_db()

    while True:
        print("\n=== FITNESS CLUB SYSTEM ===")
        print("1. Member")
        print("2. Trainer")
        print("3. Admin")
        print("0. Exit")

        choice = input("Select role: ")

        if choice == "1": member_menu()
        elif choice == "2": trainer_menu()
        elif choice == "3": admin_menu()
        elif choice == "0":
            print("Goodbye.")
            break


if __name__ == "__main__":
    main()
