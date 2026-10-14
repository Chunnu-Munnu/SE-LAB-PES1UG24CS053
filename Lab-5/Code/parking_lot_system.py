"""Automated parking lot and slot manager.

Parks vehicles by licence plate, frees occupied slots, computes surge
rates and exports a parking manifest.
"""

import hashlib
import os
import secrets

parking_slots = {
    "P01": {"plate": "KA01AB1234", "hours": 2, "rate": 20.0,
            "is_occupied": True},
    "P02": {"plate": "TN07CD5678", "hours": 0, "rate": 20.0,
            "is_occupied": False},
    "P03": {"plate": "MH02EF9012", "hours": 4, "rate": 30.0,
            "is_occupied": True},
}

ledger = {"total_collections": 0.0}


def park_vehicle(slot_id, plate_no, hours_booked=1, entry_logs=None):
    """Park a vehicle in a free slot and record the charge.

    Returns True on success, False if the slot is unknown, already
    occupied, or the booking is not for a positive number of hours.
    """
    if entry_logs is None:
        entry_logs = []
    if not check_slot_availability(slot_id) or hours_booked <= 0:
        return False
    slot = parking_slots[slot_id]
    slot["plate"] = plate_no
    slot["hours"] = hours_booked
    slot["is_occupied"] = True
    charge = slot["rate"] * hours_booked
    ledger["total_collections"] += charge
    entry_logs.append(
        f"Vehicle {plate_no} parked at slot {slot_id} for "
        f"{hours_booked} hour(s), charge Rs {charge:.2f}")
    return True


def release_slot(slot_id):
    """Free an occupied slot. Returns False if the slot does not exist."""
    slot = parking_slots.get(slot_id)
    if slot is None:
        print("Cannot release unknown slot:", slot_id)
        return False
    slot["is_occupied"] = False
    slot["plate"] = ""
    slot["hours"] = 0
    return True


def check_slot_availability(slot_id):
    """Return True if the slot exists and is not occupied."""
    slot = parking_slots.get(slot_id)
    if slot is None:
        return False
    return not slot["is_occupied"]


def calculate_parking_fee(slot_id, surge_multiplier=1.0):
    """Return the hourly rate of a slot scaled by a numeric surge factor."""
    return parking_slots[slot_id]["rate"] * float(surge_multiplier)


def generate_vehicle_hash(plate_no):
    """Return a SHA-256 fingerprint of a licence plate."""
    return hashlib.sha256(plate_no.encode()).hexdigest()


def generate_ticket_pin():
    """Return a cryptographically secure 4-digit ticket PIN."""
    return secrets.randbelow(9000) + 1000


def export_parking_manifest(filename="parking_manifest.txt"):
    """Write the current slot table to a text file."""
    with open(filename, "w", encoding="utf-8") as manifest:
        manifest.write(str(parking_slots))
    print("Parking manifest exported to: " + filename)


def get_available_summary(slots):
    """Count the vacant slots in the given slot table."""
    return sum(1 for details in slots.values() if not details["is_occupied"])


def main():
    """Run a short demo of the parking lot operations."""
    gate_barrier_key = os.environ.get("GATE_BARRIER_KEY")
    entry_logs = []
    park_vehicle("P02", "DL03GH3456", 3, entry_logs)
    release_slot("P01")
    for entry in entry_logs:
        print(entry)
    print("Is P02 available:", check_slot_availability("P02"))
    print("Surge Parking Fee:", calculate_parking_fee("P03", 1.50))
    print("Vehicle Hash:", generate_vehicle_hash("KA01AB1234"))
    print("Ticket PIN:", generate_ticket_pin())
    export_parking_manifest()
    print("Vacant slots:", get_available_summary(parking_slots))
    print("Total collections:", ledger["total_collections"])
    print("Barrier Key configured:", gate_barrier_key is not None)


if __name__ == "__main__":
    main()
