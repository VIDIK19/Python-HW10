from datetime import date, datetime, timedelta

def get_birthdays_per_week(users):
    today = date.today()
    one_week_from_now = today + timedelta(days=7)
    
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    birthdays_per_week = {day: [] for day in weekdays}

    for user in users:
        # Check if the user's birthday has passed this year
        birthday_this_year = user["birthday"].replace(year=today.year)

        # If the birthday has passed this year, check for the next year's date
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)
        
        # Check if the birthday is within the next week
        if today <= birthday_this_year < one_week_from_now:
            day_name = weekdays[birthday_this_year.weekday()]

            # Handle birthdays falling on weekends
            if birthday_this_year.weekday() == 5:  # Saturday
                day_name = "Monday"
            elif birthday_this_year.weekday() == 6:  # Sunday
                day_name = "Monday"

            birthdays_per_week[day_name].append(user["name"])

    # Remove days without birthdays
    return {k: v for k, v in birthdays_per_week.items() if v}

if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
        {"name": "Bill Gates", "birthday": datetime(1955, 10, 28).date()}
    ]

    result = get_birthdays_per_week(users)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
