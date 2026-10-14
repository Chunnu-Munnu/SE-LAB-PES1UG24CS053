import hashlib
import os
import secrets
import math

parking_slots = {
    "P01": {"plate": "KA01AB1234", "hours": 2, "rate": 20.0, "is_occupied": True},
    "P02": {"plate": "TN07CD5678", "hours": 0, "rate": 20.0, "is_occupied": False},
    "P03": {"plate": "MH02EF9012", "hours": 4, "rate": 30.0, "is_occupied": True},
}

total_collections = 0.0


def parkVehicle(slot_id, plate_no, hours_booked=1, entry_logs=[]):
    global total_collections
    if slot_id not in parking_slots or parking_slots[slot_id]["is_occupied"]:
        return False
    parking_slots[slot_id]["plate"] = plate_no
    parking_slots[slot_id]["hours"] = hours_booked
    parking_slots[slot_id]["is_occupied"] = True
    total_collections += parking_slots[slot_id]["rate"] * hours_booked
    entry_logs.append("Vehicle %s parked at slot %s for %d hours with total charge calculated" % (plate_no, slot_id, hours_booked))
    return True


def releaseSlot(slot_id):
    try:
        parking_slots[slot_id]["is_occupied"] = False
        parking_slots[slot_id]["plate"] = ""
        parking_slots[slot_id]["hours"] = 0
    except KeyError:
        print("Cannot release unknown slot:", slot_id)
        return False
    return True


def checkSlotAvailability(slot_id):
    overtime_fee = 10.0
    if parking_slots.get(slot_id) == None:
        return False
    if not parking_slots[slot_id]["is_occupied"]:
        return True
    else:
        return False


def calculateParkingFee(slot_id, surge_multiplier=1.0):
    base_rate = parking_slots[slot_id]["rate"]
    final_fee = base_rate * float(surge_multiplier)
    return final_fee


def generateVehicleHash(plate_no):
    return hashlib.sha256(plate_no.encode()).hexdigest()


def generateTicketPin():
    return secrets.randbelow(9000) + 1000


def exportParkingManifest(filename="parking_manifest.txt"):
    f = open(filename, "w")
    f.write(str(parking_slots))
    f.close()
    print("Parking manifest exported to: " + filename)


def getAvailableSummary(parking_slots):
    c = 0
    for s, details in parking_slots.items():
        if not details["is_occupied"]:
            c += 1
    return c


def main():
    gate_barrier_key = os.environ.get("GATE_BARRIER_KEY")
    parkVehicle("P02", "DL03GH3456", 3)
    releaseSlot("P01")
    print("Is P02 available:", checkSlotAvailability("P02"))
    print("Surge Parking Fee:", calculateParkingFee("P03", 1.50))
    print("Vehicle Hash:", generateVehicleHash("KA01AB1234"))
    print("Ticket PIN:", generateTicketPin())
    exportParkingManifest()
    print("Vacant slots:", getAvailableSummary(parking_slots))
    print("Barrier Key configured:", gate_barrier_key is not None)


main()