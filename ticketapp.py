import streamlit as st
import datetime
import pytz

# File-based ticket number generator
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

# Ticket printer (returns text block)
def get_ticket_text(start_index, end_index, num_passengers, places, manual_fares):
    if not (1 <= start_index <= len(places)) or not (1 <= end_index <= len(places)):
        return "Invalid station index."

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
    lines = []
    lines.append("=" * width)
    lines.append(header.center(width))
    lines.append(f"{depot} DEPOT".center(width))
    lines.append(time_str.center(width))
    lines.append(f"TICKET NO : {ticket_no}".ljust(width))
    lines.append("-" * width)
    lines.append("  CASH | GENERAL | MOFUSSIL EX ".center(width))
    lines.append("-" * width)
    lines.append(f"FROM  : {start_point}".ljust(width))
    lines.append(f"TO    : {end_point}".ljust(width))
    lines.append(f"QTY   : {num_passengers}".ljust(width))
    lines.append(f"RATE  : Rs.{fare_per_person}".ljust(width))
    lines.append(f"TOTAL : Rs.{total_fare}".ljust(width))
    lines.append("-" * width)
    lines.append(disclaimer.center(width))
    lines.append("=" * width)

    return "\n".join(lines)

# UI starts here
st.title("🚌 பஸ் டிக்கெட் ஜெனரேட்டர்")

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

start_index = st.selectbox("Start Stop", range(1, len(places)+1), format_func=lambda x: f"{x}. {places[x-1]}")
end_index = st.selectbox("End Stop", range(1, len(places)+1), format_func=lambda x: f"{x}. {places[x-1]}")
num_passengers = st.number_input("Number of Passengers", min_value=1, step=1, value=1)

if st.button("🎟️ Generate Ticket"):
    ticket = get_ticket_text(start_index, end_index, num_passengers, places, manual_fares)
    st.text(ticket)
