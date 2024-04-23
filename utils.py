from datetime import datetime


def format_schedule(schedule_data):
    # Assuming schedule_data is a list of dictionaries, each representing a class
    output = ""
    for item in schedule_data:
        day = item['day']
        time = item['time']
        subject = item['subject']
        teacher = item['teacher']
        room = item['room'] if item.get('room') else "N/A"
        output += f"**{day}**  {time}\n{subject} ({teacher})\nRoom: {room}\n\n"
    return output


def get_current_weekday():
    # Get the current day of the week as a string (e.g., "Monday")
    return datetime.today().strftime("%A")

# ... (Add other utility functions as needed)
