#!/usr/bin/python3
"""
updated mailroom program for Python 220 Lesson 4 assignment (metaprogramming)
(1) changed main() to read donor database from json file instead of being hard-coded
    into DONOR_DB dict
(2) added to quit_program() to write donor database to json file before quitting
note that user does not interact with reading and writing of donor database file
"""
from donors import Donors
import json_save_zip.json_save.json_save_dec as js

DONOR_FILE = "donors.json"

def send_thank_you(db):
    """Add a donor/donation and print out a thank you letter"""
    # loop for user input: donor name, or list, or quit
    while True:
        name = input("\nDonor Full Name (type 'list' for donor list or 'q' to quit): ")
        if name in ('q', 'quit'):
            return
        if name == 'list':
            print(db.list_donors())
            continue
        # if name == donor name:
        #   loop for user to input valid donation amount
        while True:
            amount = input("Donation amount (type 'q' to quit): ")
            if amount in ('q', 'quit'):
                return
            try:
                db.add_donation(name, amount)
            except ValueError:
                print('Invalid input, try again')
            else:
                break
        print('\n' + db.thank_you_letter(name))


def create_a_report(db):
    """Print a summary of donors and amounts donated to screen"""
    print("\n"+db.summary_report())


def send_all_letters(db):
    """Write thank you letters to all donors to text files, filename = <donor_name>.txt"""
    dir_name = input("Output directory ('.' for current dir): ")
    db.send_all_letters(dir_name)


def run_projection(db):
    """Run projection showing total contribution of challenge scenario"""
    while True:
        factor = input("\nChallenge factor ('q' to quit): ")
        if factor in ('q', 'quit'):
            return
        min_filter = input("Minimum donation to challenge (<return> for none, 'q' to quit): ")
        if min_filter in ('q', 'quit'):
            return
        max_filter = input("Maximum donation to challenge (<return> for none, 'q' to quit): ")
        if max_filter in ('q', 'quit'):
            return
        try:
            scenario = Donors.challenge(db,
                                        float(factor),
                                        float(min_filter) if min_filter else None,
                                        float(max_filter) if max_filter else None)
        except ValueError:
            print('Invalid inputs, try again')
        else:
            break
    print()
    for d in scenario.db.values():
        print(f"   {d.name}: ${sum(d.donations):,.2f} = {factor} * "
              f"("+' + '.join(list(map(lambda x: f"${x:,.2f}", d.donations)))+')')
    print(f"\n   Total contribution required: ${scenario.total_value():,.2f}\n")


def main_menu_error(_):
    """print error message if invalid menu item is entered"""
    print("Invalid choice, try again")


def quit_program(db):
    """save donor database to json, then exit program"""
    with open(DONOR_FILE, 'w') as f:
        f.write(db.to_json())
    quit()


def main():
    """Main menu for mailroom program"""
    with open(DONOR_FILE, "r") as f:
        djson = f.read()
    donor_db = js.from_json(djson)

    switch_menu_dict = {
        "1": send_thank_you,
        "2": create_a_report,
        "3": send_all_letters,
        "4": run_projection,
        "q": quit_program,
        "quit": quit_program
        }
    while True:
        print("\nMAIN MENU")
        print("   1 = Send a Thank You")
        print("   2 = Create a Report")
        print("   3 = Send Letters to Everyone")
        print("   4 = Run A Projection")
        print("   q = Quit")
        choice = input("   ? ")
        switch_menu_dict.get(choice, main_menu_error)(donor_db)


if __name__ == '__main__':
    main()
