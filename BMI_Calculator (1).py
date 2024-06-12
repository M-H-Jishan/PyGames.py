import numpy as np

def get_height():
    while True:
        height_unit = input("Would you like to enter your height in meters or feet and inches? (m/ft): ").strip().lower()
        if height_unit == "m":
            height = get_float_from_user("Please enter your height in meters: ")
            return height, height_unit
        elif height_unit == "ft":
            feet, inches = get_height_in_feet_and_inches_decimal()
            return (feet, inches), height_unit

        else:
            print("Invalid input. Please enter 'm' for meters or 'ft' for feet and inches.")

def get_height_in_feet_and_inches_decimal():
    while True:
        user_input = input("Please enter your height in feet.inches (e.g., '5.8'): ")
        try:
            height_decimal = float(user_input)
            feet = int(height_decimal)
            inches = (height_decimal - feet) * 12
            return feet, inches
        except ValueError:
            print("Invalid input. Please enter height in the format 'feet.inches' (e.g., '5.8').")

def get_weight():
    while True:
        weight_unit = input("Would you like to enter your weight in kilograms or pounds? (kg/lb): ").strip().lower()
        if weight_unit in ["kg", "lb"]:
            weight = get_float_from_user(f"Please enter your weight in {weight_unit}: ")
            return weight, weight_unit
        else:
            print("Invalid input. Please enter 'kg' for kilograms or 'lb' for pounds.")

def get_float_from_user(prompt):
    while True:
        user_input = input(prompt)
        try:
            number = float(user_input)
            return number
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def convert_height_to_meters(height, unit):
    if unit == "m":
        return height
    elif unit == "ft":
        feet, inches = height
        total_inches = feet * 12 + inches
        meters = total_inches * 0.0254
        return meters

def convert_weight_to_kg(weight, unit):
    if unit == "kg":
        return weight
    elif unit == "lb":
        kg = weight * 0.453592
        return kg

def calculate_bmi(height_meters, weight_kg):
    # Convert height and weight to NumPy arrays
    np_height = np.array(height_meters)
    np_weight = np.array(weight_kg)
    
    # Calculate BMI
    bmi = np_weight / np_height ** 2
    return bmi

def provide_bmi_suggestion(bmi):
    print("BMI Categories:")
    print("Underweight: BMI less than 18.5")
    print("Normal weight: BMI between 18.5 and 24.9")
    print("Overweight: BMI between 25 and 29.9")
    print("Obesity: BMI 30 or greater")
    print()

    if bmi < 18.5:
        print(f"Your BMI is {bmi:.2f}, which is considered underweight.")
        print("A normal BMI is between 18.5 and 24.9. You may need to gain weight for a healthier BMI.")
    elif 18.5 <= bmi <= 24.9:
        print(f"Your BMI is {bmi:.2f}, which is within the normal range.")
        print("Maintain your current weight to stay within this healthy BMI range.")
    elif 25 <= bmi <= 29.9:
        print(f"Your BMI is {bmi:.2f}, which is considered overweight.")
        print("A normal BMI is between 18.5 and 24.9. You may need to lose weight for a healthier BMI.")
    else:
        print(f"Your BMI is {bmi:.2f}, which indicates obesity.")
        print("A normal BMI is between 18.5 and 24.9. You may need to lose weight for a healthier BMI.")

def main():
    print("Welcome to the BMI Calculator!")

    height, height_unit = get_height()
    weight, weight_unit = get_weight()

    height_meters = convert_height_to_meters(height, height_unit)
    weight_kg = convert_weight_to_kg(weight, weight_unit)

    bmi = calculate_bmi(height_meters, weight_kg)

    provide_bmi_suggestion(bmi)

if __name__ == "__main__":
    main()
