import datetime
import pytz

def generate_ticket_no():
    try:
        with open("ticket_no.txt", "r") as f:
            last_no = int(f.read())
    except FileNotFoundError:
        last_no = 2870

    next_no = last_no + 1
    with open("ticket_no.txt", "w") as f:
        f.write(str(next_no))
    return str(next_no).zfill(6)

def print_route(start_index, end_index, num_passengers, places, manual_fares):
    if not (1 <= start_index <= len(places)) or not (1 <= end_index <= len(places)):
        print("Invalid input!")
        return

    route_key = tuple(sorted((start_index, end_index)))
    fare_per_person = manual_fares.get(route_key, abs(start_index - end_index) * 15)
    total_fare = fare_per_person * num_passengers

    start_point = f"{start_index}.{places[start_index - 1]}"
    end_point = f"{end_index}.{places[end_index - 1]}"
    depot = places[end_index - 1].upper()
    ticket_no = generate_ticket_no()
    header = "த.அ.போ.க - (மதுரை) லிட்"
    disclaimer = "*மோட்டார் வாகன விதிகளுக்கு உட்பட்டது*"

    kolkata_tz = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(kolkata_tz)
    time_str = now.strftime("%d-%m-%Y %H:%M:%S")

    width = 32
    print("=" * width)
    print(header.center(width))
    print((f"{depot} DEPOT").center(width))
    print(time_str.center(width))
    print(f"TICKET NO : {ticket_no}".ljust(width))
    print("-" * width)
    print("  CASH | GENERAL | MOFUSSIL EX ")
    print("-" * width)
    print(f"FROM  : {start_point}".ljust(width))
    print(f"TO    : {end_point}".ljust(width))
    print(f"QTY   : {num_passengers}".ljust(width))
    print(f"RATE  : Rs.{fare_per_person}".ljust(width))
    print(f"TOTAL : Rs.{total_fare}".ljust(width))
    print("-" * width)
    print(disclaimer.center(width))
    print("=" * width)

places = ["தேனி", "கனாவிலக்கு", "ஆண்டிபட்டி", "உசிலம்பட்டி", "செக்கானூரணி", "மதுரை"]

manual_fares = {
    (1, 2): 10,
    (1, 3): 15,
    (1, 4): 30,
    (1, 5): 45,
    (1, 6): 60,
    (2, 3): 10,
    (3, 4): 20
}

try:
    start = int(input("Enter start index (e.g., 1): "))
    end = int(input("Enter end index (e.g., 2): "))
    passengers = int(input("Enter number of passengers: "))
    if passengers <= 0:
        print("Number of passengers must be greater than 0.")
    else:
        print_route(start, end, passengers, places, manual_fares)
except ValueError:
    print("Please enter valid numeric values.")
