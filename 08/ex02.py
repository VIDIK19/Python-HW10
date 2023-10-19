from collections import UserString
from datetime import date, timedelta

start_date = date.today()
end_date = start_date + timedelta(7)

print(f"{start_date = }, {end_date = }")

def get_bd(users: list) -> list:
    start_day = date.today()
    end_date = start_date + timedelta(7)

    for user in users:
        bd: date = user["birthday"]
        print(bd)
        bd.replace(year=start_date.year)
        print(bd)


print(f"{start_date = }, {end_date = }")

if __name__ == '__main__':
    users = [{"name": "Bill", "birthday": date(1990, 9, 28)}, 
             {"name": "Marry", "birthday": date(2000, 10, 2)}]

