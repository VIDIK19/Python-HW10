from datetime import date, datetime, timedelta

def get_birthdays_per_week(users):
    today = date.today()
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    birthdays_per_week = {day: [] for day in weekdays}

    for user in users:
        birthday = user["birthday"]
        current_year_birthday = birthday.replace(year=today.year)
        # Calculate the number of days until the next birthday
        days_to_birthday = (current_year_birthday - today).days
        if current_year_birthday < today:  # The birthday has passed this year
            days_to_birthday = (current_year_birthday.replace(year=today.year + 1) - today).days
        
        # Calculate the birthday weekday index, ensuring we shift weekend birthdays to Monday
        birthday_weekday = (today + timedelta(days=days_to_birthday)).weekday()
        if birthday_weekday >= 5:  # Shift weekend birthdays to Monday
            day_name = "Monday"
        else:
            day_name = weekdays[birthday_weekday]  # Weekday birthday
        
        # Add only upcoming or current day birthdays to the weekdays list
        if 0 <= days_to_birthday <= 6:
            birthdays_per_week[day_name].append(user["name"])

    # Remove weekdays without any birthdays
    birthdays_per_week = {day: names for day, names in birthdays_per_week.items() if names}
    return birthdays_per_week

if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 2, 24).date()},
        {"name": "Bill Gates", "birthday": datetime(1955, 10, 28).date()},
        # Test for a birthday this week but on a weekend
        {"name": "Test User", "birthday": (today + timedelta(days=today.weekday() + 1)).replace(year=today.year).date()} 
    ]

    result = get_birthdays_per_week(users)
    print(result)  # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")

