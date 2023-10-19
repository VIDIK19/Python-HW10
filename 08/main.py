from datetime import date, datetime


def get_birthdays_per_week(users):
    today = date.today()
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    birthdays_per_week = {day: [] for day in weekdays}

    for user in users:
        birthday = user["birthday"]
        # If birthday has already passed this year, consider next year
        if birthday.replace(year=today.year) < today:
            birthday = birthday.replace(year=today.year + 1)

        # Check if the birthday falls within the next week
        if 0 <= (birthday - today).days < 7:
            day_name = weekdays[birthday.weekday()]
            
            # If birthday falls on a weekend, add it to Monday
            if birthday.weekday() >= 5:
                day_name = "Monday"
            
            birthdays_per_week[day_name].append(user["name"])

    # Remove days without birthdays
    return {k: v for k, v in birthdays_per_week.items() if v}
    return users


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")