#################
## William Hotch
## 1/24/2025
## bday_app.py
#################

from datetime import datetime
import csv
import os

# File to store birthdays
BIRTHDAY_FILE = "bdays.csv"

# Return birthdays sorted ignoring year
def sort_bdays(birthdays):
    sorted_bdays = sorted(
        birthdays.items(),
        key=lambda x: (
            int(x[1][:2]),  # Month (MM)
            int(x[1][3:5]),  # Day (DD)
            int(x[1][6:]) if len(x[1]) > 5 else 9999  # Year (YYYY or default 9999)
        )
    )

    return sorted_bdays

# Load birthdays from the CSV file
def load_bdays():
    if not os.path.exists(BIRTHDAY_FILE):
        return {}
    
    birthdays = {}
    with open(BIRTHDAY_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            birthdays[row["name"].lower()] = row["date"]
    
    return birthdays


# Save sorted birthdays to the CSV file
def save_bdays(birthdays):
    with open(BIRTHDAY_FILE, "w", newline="") as file:
        fieldnames = ["name", "date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for name, date in sorted(birthdays.items(), key=lambda x: datetime.strptime(x[1], "%m-%d-%Y")):
            writer.writerow({"name": name, "date": date})


# Add birthdays 
def add_bday(birthdays):
    # Prompt user input
    name = input("Enter name: ").strip()
    date = input("Enter their birthday (MM-DD or MM-DD-YYYY): ").strip()
    
    # Store birthday
    try:
        # Check if the input is MM-DD or MM-DD-YYYY
        if len(date) == 5:  # MM-DD format
            datetime.strptime(date, "%m-%d")
            # Append with a placeholder year (9999) for consistency
            birthdays[name.lower()] = f"{date}-9999"
        
        elif len(date) == 10:  # MM-DD-YYYY format
            datetime.strptime(date, "%m-%d-%Y")
            birthdays[name.lower()] = date
        
        else:
            raise ValueError("Invalid date format.")
        
        print(f"Birthday added for {name}!")
        save_bdays(birthdays)
    
    except ValueError:
        print("Invalid date format. Please use MM-DD or MM-DD-YYYY. Also you're ugly.")


# Change an existing birthday
def change_bday(birthdays):
    
    if not birthdays:
        print("\nNo birthdays stored yet.")
        return
    
    name = input("Enter the name of the person whose birthday you want to change: ").strip().lower()
    
    if name in birthdays:
        
        print(f"Current birthday for {name.title()}: {birthdays[name]}")
        new_date = input("Enter the new birthday (MM-DD or MM-DD-YYYY): ").strip()

        try:
            if len(new_date) == 5:
                datetime.strptime(new_date, "%m-%d")
                birthdays[name] = f"{new_date}-9999"
            elif len(new_date) == 10:
                datetime.strptime(new_date, "%m-%d-%Y")
                birthdays[name] = new_date
            else:
                raise ValueError("Invalid date format.")
            
            print(f"Birthday updated for {name.title()} to {birthdays[name]}!")
            save_bdays(birthdays)

        except ValueError:
            print("Invalid date format. Please use MM-DD or MM-DD-YYYY. Silly goose.")
   
    print(f"No birthday found for {name.title()}.")


# Remove a birthday from the list
def remove_bday(birthdays):
    if not birthdays:
        print("\nNo birthdays stored yet.")
        return
    
    name = input("Enter the name of the person whose birthday you want to remove: ").strip().lower()
    
    if name in birthdays:
        print(f"Removing birthday for {name.title()}: {birthdays[name]}")
        del birthdays[name]
        save_bdays(birthdays)
        print(f"Birthday for {name.title()} has been removed.")
    else:
        print(f"No birthday found for {name.title()}.")


# Check for today's birthdays
def check_todays_bdays(birthdays):
    # Get today's date in MM-DD format
    today = datetime.now().strftime("%m-%d")
    
    # Match MM-DD
    todays_birthdays = [name.title() for name, date in birthdays.items() if date[:5] == today]

    # Print birthdays if any
    if todays_birthdays:
        print("\n🎉 Today's Birthdays 🎉")
        for name in todays_birthdays:
            print(f"- {name.title()}")
    else:
        print("\nNo birthdays today.")

# List upcoming birthdays
def next_bdays(birthdays, count=3):
    if not birthdays:
        print("\nNo birthdays stored.")
        return

    today = datetime.now().strftime("%m-%d")
    today_month, today_day = map(int, today.split("-"))

    next_bdays = []
    found = False

    sorted_bdays = sort_bdays(birthdays)

    # Iterate at most twice to allow wraparound
    for _ in range(2):  # Ensures loop twice at most
        for name, date in sorted_bdays:
            month, day, *_ = map(int, date.split("-"))  # Ignore year
            
            if len(next_bdays) < count:
                if (month > today_month) or (month == today_month and day > today_day) or next_bdays:
                    next_bdays.append((name, f"{month:02d}-{day:02d}"))
            else:
                break
        
        if len(next_bdays) >= count:
            break  # Stop if we've found enough birthdays

    # Display results
    print("\n🎉 Next Upcoming Birthdays 🎉")
    for name, date in next_bdays:
        print(f"- {name.title()}: {date}")


# List all stored birthdays
def list_bdays(birthdays):
    if not birthdays:
        print("\nNo birthdays stored.")
        return
    
    print("\nStored Birthdays:")

    sorted_bdays = sort_bdays(birthdays)
    
    for name, date in sorted_bdays:
        print(f"- {name.title()}: {date}")


# # Import birthdays from a CSV file
# def import_bdays_from_file(birthdays):
#     filename = "bdays_old.csv"
#     if not os.path.exists(filename):
#         print(f"File '{filename}' not found.")
#         return
#     try:
#         with open(filename, "r") as file:
#             reader = csv.DictReader(file)
#             new_entries = 0      
#             for row in reader:
#                 name = row["name"].strip().lower()
#                 date = row["date"].strip()
#                 # Validate date format
#                 try:
#                     datetime.strptime(date, "%m-%d-%Y")  # Ensure proper format
#                     if name not in birthdays:
#                         birthdays[name] = date
#                         new_entries += 1
#                 except ValueError:
#                     print(f"Skipping invalid date format: {row['date']} for {row['name']}")    
#         save_bdays(birthdays)
#         print(f"Successfully imported {new_entries} new birthdays.")
#     except Exception as e:
#         print(f"Error reading file: {e}")


# Main program loop
def main():
    # Load birthdays from the file
    birthdays = load_bdays()
    print("\nBirthday Checker")

    while True:
        print("\n1. ADD a Birthday")
        print("2. CHANGE a Birthday")
        print("3. REMOVE a Birthday")
        print("4. CHECK Today's Birthdays")
        print("5. List NEXT Birthdays")
        print("6. LIST All Birthdays")
        print("7. EXIT")

        choice = input("\nChoose an option: ").strip()
        if choice == "1":
            add_bday(birthdays)
        elif choice == "2":
            change_bday(birthdays)
        elif choice == "3":
            remove_bday(birthdays)
        elif choice == "4":
            check_todays_bdays(birthdays)
        elif choice == "5":
            next_bdays(birthdays)
        elif choice == "6":
            list_bdays(birthdays)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again. Seriously that's super embarassing.")

if __name__ == "__main__":
    main()
