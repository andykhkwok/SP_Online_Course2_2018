#!/usr/bin/env python3
""" Automate a script to send a thank you mail, print a report of donor or quit the program."""
from operator import itemgetter
import os
import datetime
import json
import json_save.json_save_meta as js


class Donor(js.JsonSaveable):
    _donation = js.List()
    _name = js.String()

    def __init__(self, name, donation=None):
        if name == '':
            self._name = 'Anonymous'
        else:
            self._name = name
        if donation is None:
            self._donation = []
        elif isinstance(donation, (int, float)):
            self._donation = [donation]
        else:
            self._donation = donation

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = str(name)

    @property
    def donation(self):
        return self._donation

    @donation.setter
    def donation(self, donation):
        if type(donation) == list:
            self._donation = donation
        else:
            raise TypeError("Donation has to be a list of int")

    def add_donation(self, donation_amount):
        if donation_amount >= 0:
            self._donation.append(donation_amount)
        else:
            raise ValueError("Donation amount must be greater than 0.")

    def __repr__(self):
        return "Donor({} : {})".format(self._name, self._donation)

    def __str__(self):
        return "Donor: {} donated {}\n".format(self._name, self._donation)

    def donation_occurrences(self):
        return len(self._donation)

    def total_donation_amount(self):
        return sum(self._donation)

    def average_total_donor_amount(self):
        try:
            return self.total_donation_amount() / self.donation_occurrences()
        except ValueError:
            return self._donation

    def stats(self):
        return [self.total_donation_amount(), self.donation_occurrences(), self.average_total_donor_amount()]


class DonorList(js.JsonSaveable):
    _donors = js.List()
    file_name = "donor_list_json_file.json"
    new_donors_list = js.List()

    def __init__(self, donors=[]):
        if donors is None:
            self._donors = []
        elif isinstance(donors, Donor):
            self._donors = [donors]
        else:
            self._donors = donors

    """def save_to_json(self):
        target_directory = os.getcwd()
        target_file_path = os.path.join(target_directory, self.file_name)
        new_donors_list = table_dictionary.to_json()
        with open(target_file_path, 'w') as fp:
            js.to_json(new_donors_list, fp, indent=4)"""

    def save_to_json(self):
        target_directory = os.getcwd()
        target_file_path = os.path.join(target_directory, self.file_name)
        donor_to_json = table_dictionary.to_json()
        with open(target_file_path, "w") as fp:
            fp.write(donor_to_json)

    def load_from_json(self):
        target_directory = os.getcwd()
        target_file_path = os.path.join(target_directory, self.file_name)
        with open(target_file_path, 'r') as fp:
            donor_load = fp.read()
        return js.from_json(donor_load)

    def populate_dict(self):
        target_directory = os.getcwd()
        target_file_path = os.path.join(target_directory, self.file_name)
        if os.path.exists(target_file_path):
            abd = self.load_from_json()
            self._donors = abd._donors
        else:
            self.init_dict()

    def init_dict(self):
        self._donors = [
            Donor('Toni Orlando', [150.00, 200.00, 100.00]),
            Donor('Amanda Clark', [1800.00]),
            Donor('Robin Hood', [1234.56, 4500.34, 765.28]),
            Donor('Gina Travis', [523.10, 75.00]),
            Donor('Mark Johnson', [850.00, 20.14])
        ]

    @property
    def donors(self):
        return self._donors

    def __str__(self):
        d_list = ''
        for d in self._donors:
            d_list += d + '\n'
        return d_list

    def __repr__(self):
        d_list = 'repr'
        for d in self._donors:
            d_list += str(d)
        return d_list

    def add_donor_list(self, donor):
        return self._donors.append(donor)

    def names_only_list(self):
        names_list = []
        for d in self._donors:
            names_list.append(d.name)
        return names_list

    def find_donor_history(self, name):
        for d in self._donors:
            if d.name == name:
                return d

    def display_donor_list(self):
        """Prints the full list of donors and corresponding donation history."""
        for d in self._donors:
            print("{:<20}: {}".format(d.name, d.donation))
        pass

    """def __iter__(self):
        return iter(self._donors)"""

    def stat_donor_list(self):
        new_list = []
        for k in self._donors:
            sum_donations = k.total_donation_amount()
            total_gifts = k.donation_occurrences()
            average_gift = k.average_total_donor_amount()
            new_list.append([k.name, sum_donations, total_gifts, average_gift])
        sorted_new_list = sorted(new_list, key=itemgetter(1), reverse=True)
        return sorted_new_list


table_dictionary = DonorList()
"""table_dictionary = DonorList([
    Donor('Toni Orlando1', [150.00, 200.00, 100.00]),
    Donor('Amanda Clark', [1800.00]),
    Donor('Robin Hood', [1234.56, 4500.34, 765.28]),
    Donor('Gina Travis', [523.10, 75.00]),
    Donor('Mark Johnson', [850.00, 20.14])
])"""
table_dictionary.populate_dict()

actions_dictionary = {'1': 'Send a Thank You', '2': 'Create a Report', '3': 'Send letters to everyone', '4': 'Quit',
                      '5': 'Save to file', '6': 'Load from file'}


def sending_thank_you():
    """Lists all the donors or prompts for a name and donation amount to compile the thank you email."""
    while True:
        send_to_name = input(
            "First: Who do you want to send the email to? Type 'list' for a list of all the donors. ")
        if send_to_name == 'list':
            table_dictionary.display_donor_list()
            # send_to_name = input("Second: Who do you want to send the email to? Type 'list' for a list of all the donors. ")
        else:
            break
    names_list = table_dictionary.names_only_list()
    if send_to_name not in names_list:
        table_dictionary.add_donor_list(Donor(send_to_name, []))
    # donation_amount = input("What donation amount do you want to thank them for? ")
    while True:
        try:
            donation_amount = float(input('What donation amount do you want to thank them for? '))
            if donation_amount > 0:
                break
            else:
                print("Number has to be positive.")
        except ValueError:
            print("Input must be a number.")
    d = table_dictionary.find_donor_history(send_to_name)
    d.add_donation(donation_amount)
    print("Dear {}, Thank you for your generous contribution of ${:.2f} to our program.".format(send_to_name,
                                                                                                donation_amount))


def print_report():
    """Prints the donor table in equally amount of column width with each donor, total amount, number of gifts and average donation."""
    table_header = ['Donor Name', 'Total Given', 'Num Gifts', 'Average Gifts']
    len_header = len(table_header)
    print("|".join(["{:<20}"] * len_header).format(*table_header))
    print("-" * (20 * len_header + (len_header - 1)))
    sorted_new_list = table_dictionary.stat_donor_list()
    for row in sorted_new_list:
        print("{0:<20} ${1:>19.2f} {2:>20} ${3:>19.2f}".format(*row))
    return sorted_new_list


def send_everyone_letters(target_directory=os.getcwd()):
    """Sends a letter to everyone in the table for their first donation in the list."""
    file_name_extension = '.txt'
    today_date_short = calculate_date()
    # names_only_list = table_dictionary.names_only_list()
    print(table_dictionary.donors)
    for file_name in table_dictionary.donors:
        target_file_path = os.path.join(target_directory,
                                        str(file_name.name).replace(' ',
                                                                    '_') + today_date_short + file_name_extension)
        try:
            with open(str(target_file_path), 'w') as tf:
                letter_content = ("Dear {},\n"
                                  "\tThank you for your kind donation of $ {:.2f}.\n"
                                  "\tIt will be put to very good use.\n"
                                  "\t\tSincerely,\n"
                                  "\t\t\t-The Team").format(file_name.name, file_name.total_donation_amount())
                tf.write(letter_content)
        except FileNotFoundError as err:
            print("File path is not correct.")
            print(err)
    print("Done")


def select_action_dictionary(prompt, switch_func_dict):
    """User selects an action by its corresponding order number."""
    while True:
        choice_actions = input(prompt)
        try:
            if switch_func_dict[choice_actions]() == "quit":
                print("Before quitting.")
                break
        except KeyError:
            print("Please enter only one of the listed options.")


def print_menu():
    """Prints the action list to the console"""
    str_result = ''
    for i in actions_dictionary:
        str_result += ("{}) {}".format(i, actions_dictionary[i]))
        str_result += '\n'
    str_result += 'Select the corresponding number for the action you want to take action: '
    return str_result


def calculate_date():
    today_date = datetime.datetime.now()
    result_today_date = "_" + str(today_date.year) + "_" + str(today_date.month) + "_" + str(today_date.day)
    return result_today_date


def quit_program():
    """Quits the program."""
    return "quit"



switch_func_dict = {
    '1': sending_thank_you,
    '2': print_report,
    '3': send_everyone_letters,
    '4': quit_program,
    '5': table_dictionary.save_to_json,
    '6': table_dictionary.load_from_json
}

if __name__ == '__main__':
    select_action_dictionary(print_menu(), switch_func_dict)
