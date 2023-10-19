from get_birds import get_birds

def calc_birds() -> int:
    return len(get_birds())

if __name__ == "__main__":
    print(f"We have {calc_birds()} bird")