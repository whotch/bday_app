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

# Load birthdays from the CSV file
def load_bdays():
    if not os.path.exists(BIRTHDAY_FILE):
        return []
    birthdays = []
    with open(BIRTHDAY_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            birthdays.append(row)
    return sort_bdays(birthdays)

# Save birthdays to the CSV file
def save_bdays(birthdays):
    with open(BIRTHDAY_FILE, "w", newline="") as file:
        fieldnames = ["name", "date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sort_bdays(birthdays))

# Sort birthdays by month, day, and year
def sort_bdays(birthdays):
    return sorted(
        birthdays,
        key=lambda b: (
            int(b["date"][:2]),  # Month (MM)
            int(b["date"][3:5]),  # Day (DD)
            int(b["date"][6:]) if len(b["date"]) > 5 else 1900  # Year (YYYY or default 1900)
        )
    )


# Add birthdays to the list
def add_bday(birthdays):
    # Prompt user input
    name = input("Enter name: ")
    date = input("Enter their birthday (MM-DD or MM-DD-YYYY): ")
    
    # Store birthday
    try:
        # Check if the input matches MM-DD or MM-DD-YYYY
        if len(date) == 5:  # MM-DD format
            datetime.strptime(date, "%m-%d")
            
            # Append with a default year (e.g., 1900) for consistency
            birthdays.append({"name": name, "date": f"{date}-1900"})
        
        elif len(date) == 10:  # MM-DD-YYYY format
            datetime.strptime(date, "%m-%d-%Y")
            birthdays.append({"name": name, "date": date})
        
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
    
    name = input("Enter the name of the person whose birthday you want to change: ")
    for birthday in birthdays:
        
        # Find name match
        if birthday["name"].lower() == name.lower():
            print(f"Current birthday for {name}: {birthday['date']}")
            
            # Change existing birthday
            new_date = input("Enter the new birthday (MM-DD or MM-DD-YYYY): ")
            try:
                # Validate the new date
                if len(new_date) == 5:  # MM-DD format
                    datetime.strptime(new_date, "%m-%d")
                    birthday["date"] = f"{new_date}-1900"
                elif len(new_date) == 10:  # MM-DD-YYYY format
                    datetime.strptime(new_date, "%m-%d-%Y")
                    birthday["date"] = new_date
                else:
                    raise ValueError("Invalid date format.")
                print(f"Birthday updated for {name} to {birthday['date']}!")
                save_bdays(birthdays)
                return

            except ValueError:
                print("Invalid date format. Please use MM-DD or MM-DD-YYYY.")
                return
   
    print(f"No birthday found for {name}.")

# Remove a birthday from the list
def remove_bday(birthdays):
    if not birthdays:
        print("\nNo birthdays stored yet.")
        return
    
    name = input("Enter the name of the person whose birthday you want to remove: ")
    for i, birthday in enumerate(birthdays):
        if birthday["name"].lower() == name.lower():
            print(f"Removing birthday for {name}: {birthday['date']}")
            birthdays.pop(i)
            print(f"Birthday for {name} has been removed.")
            save_bdays(birthdays)
            return
    
    print(f"No birthday found for {name}.")


# Check for today's birthdays
def check_todays_bdays(birthdays):
    # Get today's date in MM-DD format
    today = datetime.now().strftime("%m-%d")
    
    # Match MM-DD
    todays_birthdays = [
        b["name"] for b in birthdays if b["date"][:5] == today
    ]

    # Print birthdays if any
    if todays_birthdays:
        print("\n🎉 Today's Birthdays 🎉")
        for name in todays_birthdays:
            print(f"- {name}")
    else:
        print("\nNo birthdays today.")

# List all stored birthdays
def list_bdays(birthdays):
    if not birthdays:
        print("\nNo birthdays stored.")
        return
    print("\nStored Birthdays:")
    for b in sort_bdays(birthdays):
        print(f"- {b['name']}: {b['date']}")

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
        print("5. LIST All Birthdays")
        print("6. EXIT")

        choice = input("\nChoose an option: ")
        if choice == "1":
            add_bday(birthdays)
        elif choice == "2":
            change_bday(birthdays)
        elif choice == "3":
            remove_bday(birthdays)
        elif choice == "4":
            check_todays_bdays(birthdays)
        elif choice == "5":
            list_bdays(birthdays)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again. Seriously that's super embarassing.")

if __name__ == "__main__":
    main()
