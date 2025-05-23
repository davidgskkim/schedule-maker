import pandas as pd
import re

SHIFT_TIMES = {
    "Open": ["10-5"],
    "Close": ["5-11:30"],
}

DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

def clean_name(name: str) -> str:
    # Remove anything that is not a letter or space, then strip
    return re.sub(r"[^a-zA-Z ]", "", name).strip()

def parse_schedule(file_path):
    df = pd.read_excel(file_path)

    employees = []

    for idx, row in df.iterrows():
        raw_name = str(row["Unnamed: 0"]).strip()
        name = clean_name(raw_name)  # Clean the name here
        availability = []

        for day in DAYS:
            value = str(row[day]).strip().upper()
            if value in ["OFF", "NAN"]:
                continue

            day_shifts = []

            if value == "ON":
                day_shifts = SHIFT_TIMES["Open"] + SHIFT_TIMES["Close"]
            elif value == "OPEN":
                day_shifts = SHIFT_TIMES["Open"]
            elif value == "CLOSE":
                day_shifts = SHIFT_TIMES["Close"]
            elif "-" in value:
                day_shifts = [value]

            for time in day_shifts:
                if time == "5-11:30" and day == "SAT":
                    availability.extend([f"{day} 5-11:30 A", f"{day} 5-11:30 B"])
                elif time == "5-11:30" and day == "SUN":
                    availability.extend([f"{day} 5-11:30 A", f"{day} 5-11:30 B"])
                elif time == "10-5" and day == "SAT":
                    availability.extend([f"{day} 10-5", f"{day} 12-5"])
                else:
                    availability.append(f"{day} {time}")

        ideal = str(row["Ideal"]).strip()
        ideal_shifts = int(ideal) if ideal.isdigit() else 4

        preference = row.get("Preference", 3)
        try:
            preference = int(preference)
        except:
            preference = 3

        if name.lower() != "geumseong":
            employees.append(
                {
                    "name": name,
                    "availability": availability,
                    "ideal_shifts": ideal_shifts,
                    "preference": preference,
                }
            )

    return employees
