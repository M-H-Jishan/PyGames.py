import random
import time

OPERATORS = ["+", "-", "*"]
MIN_OPERAND = 3
MAX_OPERAND = 12
TOTAL_PROBLEMS = 10

def generate_problem():
    left = random.randint(MIN_OPERAND, MAX_OPERAND)
    right = random.randint(MIN_OPERAND, MAX_OPERAND)
    operator = random.choice(OPERATORS)
    
    expr = f"{left} {operator} {right}"
    if operator == "+":
        answer = left + right
    elif operator == "-":
        answer = left - right
    elif operator == "*":
        answer = left * right
    return expr, answer

wrong = 0
input("Press enter to start!")
print("----------------------")

start_time = time.time()

for i in range(TOTAL_PROBLEMS):
    expr, answer = generate_problem()
    while True:
        try:
            guess = input(f"Problem #{i + 1}: {expr} = ")
            if int(guess) == answer:
                print("Correct!")
                break
            else:
                print("Incorrect, try again.")
                wrong += 1
        except ValueError:
            print("Please enter a valid number.")

end_time = time.time()
total_time = round(end_time - start_time, 2)

print("----------------------")
print("Nice work! You finished in", total_time, "seconds!")
print("Total wrong attempts:", wrong)
