"""Fitness club class booking ledger.

Books members into gym classes up to a capacity limit, handles cancellations
and exports the rosters to a JSON file.
"""
import glob
import json
import os

# Global state
class_capacity = {"Yoga": 3, "HIIT": 2, "Spin": 4}
rosters = {}


def book_class(member_id, class_name, attendance_log=None):
    """Book a member into a class. Return True on success, False if full."""
    if attendance_log is None:
        attendance_log = []
    roster = rosters.get(class_name, [])
    # '>=' (not '>'): a class with N seats must refuse the (N+1)th booking.
    if len(roster) >= class_capacity.get(class_name, 0):
        print("Class full:", class_name)
        return False
    roster.append(member_id)
    rosters[class_name] = roster
    attendance_log.append(f"{member_id} -> {class_name}")
    return True


def cancel_booking(member_id, class_name):
    """Remove a member from a class roster, if they are booked."""
    try:
        rosters[class_name].remove(member_id)
    except (KeyError, ValueError):
        print("Nothing to cancel")


def set_capacity(class_name, seats):
    """Set the number of seats for a class (must not be negative)."""
    if seats < 0:
        raise ValueError("Capacity cannot be negative")
    class_capacity[class_name] = seats


def add_members(class_name, count):
    """Book `count` walk-in guests into a class."""
    for i in range(count):
        book_class("GUEST-" + str(i), class_name)


def export_roster(file="gym_schedule.json"):
    """Write all rosters to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(rosters, handle)


def clear_old_exports(prefix="old_"):
    """Delete old exported JSON files without invoking a shell."""
    for path in glob.glob(prefix + "*.json"):
        os.remove(path)


def show_rosters():
    """Print every class with its booked members."""
    for class_name, members in rosters.items():
        print(class_name, ":", ", ".join(str(m) for m in members))


def read_guest_count(default=1):
    """Ask for the walk-in guest count; use default if input is invalid."""
    answer = input("How many walk-in guests for HIIT? (Enter for 1): ")
    try:
        count = int(answer) if answer.strip() else default
    except ValueError:
        print("Invalid number, using", default)
        return default
    if count < 0:
        print("Guest count cannot be negative, using", default)
        return default
    return count


def main():
    """Run the demo booking scenario."""
    book_class("M1", "Yoga")
    book_class("M2", "Yoga")
    book_class("M3", "Yoga")
    book_class("M4", "Yoga")
    book_class("55", "HIIT")
    book_class("M5", "Pilates")
    try:
        set_capacity("Spin", -2)
    except ValueError as err:
        print("Could not set capacity:", err)
    add_members("Spin", 3)
    cancel_booking("M9", "Boxing")
    add_members("HIIT", read_guest_count())
    clear_old_exports()
    export_roster()
    show_rosters()


if __name__ == "__main__":
    main()
