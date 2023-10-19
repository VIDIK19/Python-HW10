from datetime import date, datetime, timedelta

def get_birthdays_per_week(users):
    today = date.today()
    weekday_today = today.weekday()
    birthdays_per_week = {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}

    for user in users:
        birthday = user["birthday"].replace(year=today.year)
        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)
        
        days_until_birthday = (birthday - today).days
        # Convert days to weekday name
        if 0 <= days_until_birthday <= 4:
            day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][days_until_birthday]
        elif days_until_birthday == 5 or days_until_birthday == 6:  # Weekends
            day_name = "Monday"
        else:
            continue  # Skip if the birthday is not within the next week

        birthdays_per_week[day_name].append(user["name"])

    return {k: v for k, v in birthdays_per_week.items() if v}  # Remove days without birthdays

if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
        {"name": "Bill Gates", "birthday": datetime(1955, 10, 28).date()}
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
