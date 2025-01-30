import json
import random


class CardCollection:
    def __init__(self):
        self.cards = dict()
        self.errors = dict()

    def add_card(self, name, definition):
        if name in self.cards:
            print(f"The term \"{name}\" already exists.")
            return False
        if definition in self.cards.values():
            print(f"The definition \"{definition}\" already exists.")
            return False
        self.cards[name] = definition
        print(f"The pair (\"{name}\":\"{definition}\") has been added.")
        return True

    def remove_card(self, name):
        if name in self.cards:
            del self.cards[name]
            if name in self.errors:
                del self.errors[name]
            print("The card has been removed.")
            return True
        else:
            print(f"Can't remove \"{name}\": there is no such card.")
            return False

    def import_cards(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                if not isinstance(data, dict):
                    print("Invalid file format.")
                    return 0
                count = 0
                for name, value in data.items():
                    if isinstance(value, str):
                        definition = value
                        errors = 0
                    elif isinstance(value, dict):
                        definition = value.get('definition', '')
                        errors = value.get('errors', 0)
                    else:
                        print(f"Invalid data format for term {name}. Skipping.")
                        continue
                    self.cards[name] = definition
                    self.errors[name] = errors
                    count += 1
                print(f"{count} cards have been loaded.")
                return count
        except FileNotFoundError:
            print("File not found.")
            return 0

    def export_cards(self, filename):
        data = {
            term: {
                'definition': definition,
                'errors': self.errors.get(term, 0)
            }
            for term, definition in self.cards.items()
        }
        with open(filename, 'w') as file:
            json.dump(data, file)
        print(f"{len(self.cards)} cards have been saved.")

    def check_answer(self, name, answer):
        correct_definition = self.cards.get(name)
        if correct_definition == answer:
            print("Correct!")
            return True
        else:
            self.errors[name] = self.errors.get(name, 0) + 1
            if answer in self.cards.values():
                correct_name = [key for key, val in self.cards.items() if val == answer]
                print(f"Wrong. The right answer is \"{correct_definition}\", but your definition is correct for \"{correct_name[0]}\".")
            else:
                print(f"Wrong. The right answer is \"{correct_definition}\".")
            return False

    def get_random_cards(self, num_cards):
        return random.choices(list(self.cards.items()), k=num_cards)

    def check_name_existence(self, name):
        return name in self.cards

    def check_definition_existence(self, definition):
        return definition in self.cards.values()

    def get_hardest_cards(self):
        if not self.errors:
            return [], 0
        max_errors = max(self.errors.values(), default=0)
        if max_errors == 0:
            return [], 0
        hardest = [name for name, count in self.errors.items() if count == max_errors]
        return hardest, max_errors

    def reset_stats(self):
        self.errors.clear()
        print("Card statistics have been reset.")
