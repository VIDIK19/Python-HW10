from random import choice
​
gallows = [
    [" ", "+", "-", "+", ""],
    [" ", "|", " ", "|", " "],
    [" ", "|", " ", " ", " "],
    [" ", "|", " ", " ", " "],
    [" ", "|", " ", " ", " "],
    ["/", " ", "\\", " ", " "]
]
​
def draw_gallows(param=0):
    last_step = False
    gallows_for_print = []
    
    if param >= 1:
        gallows[2][3] = "O"
    if param >= 2:
        gallows[3][3] = "|"
    if param >= 3:
        gallows[3][2] = "/"
    if param >= 4:
        gallows[3][4] = "\\"
    if param >= 5:
        gallows[4][2] = "/"
    if param >= 6:
        gallows[4][4] = "\\"
        last_step = True
​
    for row in gallows:
        result = "".join(row)
        gallows_for_print.append(result)
    
    return "\n".join(gallows_for_print), last_step
​
# print(draw_gallows())
def get_random_word() -> str:
    with open("words.txt") as file:
        # return file.read().split("\n")
        # return file.readlines() need sanitize
        result = []
        counter = 0
        while counter <= 100:
            data = file.readline()
            if not data:
                break
            counter += 1
            result.append(data.replace("\n", ""))
    
    return choice(result)
​
def main():
    word = "gallows" # get_random_word()
    errors = 0
​
    question = []
    for i in word:
        question.append("_")
​
    print(draw_gallows(errors)[0])
    print(" ".join(question))
​
    while True:
        user_input = input("enter letter: ")
        if not user_input:
            break
        if len(user_input) > 1:
            print("enter only one letter")
            continue
        
        if user_input in word:
            indexes = []
            for index, letter in enumerate(word):
                if user_input == letter:
                    indexes.append(index)
            
            # index = word.index(user_input)
            for index in indexes:
                question[index] = user_input
        else:
            errors += 1
        
        str_gallows, last_step = draw_gallows(errors)
        print(str_gallows)
        print(" ".join(question))
        
        if last_step:
            print("You loose")
            break
        if "".join(question) == word:
            print("You win")
            break
​
​
if __name__ == "__main__":
   main()