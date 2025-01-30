import sys


class Command:
    def execute(self, card_collection):
        pass


class AddCommand(Command):
    def execute(self, card_collection):
        while True:
            term = input("The card:\n")
            if not card_collection.check_name_existence(term):
                break
            else:
                print(f"The term \"{term}\" already exists. Try again:")

        while True:
            definition = input("The definition of the card:\n")
            if not card_collection.check_definition_existence(definition):
                break
            else:
                print(f"The definition \"{definition}\" already exists. Try again:")

        card_collection.add_card(term, definition)


class RemoveCommand(Command):
    def execute(self, card_collection):
        term = input("Which card?\n")
        card_collection.remove_card(term)


class ImportCommand(Command):
    def __init__(self, filename=None):
        super().__init__()
        self.filename = filename

    def execute(self, card_collection):
        if self.filename is None:
            filename = input("File name:\n")
        else:
            filename = self.filename
        card_collection.import_cards(filename)


class ExportCommand(Command):
    def __init__(self, filename=None):
        super().__init__()
        self.filename = filename

    def execute(self, card_collection):
        if self.filename is None:
            filename = input("File name:\n")
        else:
            filename = self.filename
        card_collection.export_cards(filename)


class AskCommand(Command):
    def execute(self, card_collection):
        while True:
            try:
                num_times = int(input("How many times to ask?\n"))
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")

        cards = card_collection.get_random_cards(num_times)
        for name, definition in cards:
            user_answer = input(f'Print the definition of "{name}":\n')
            card_collection.check_answer(name, user_answer)


class ExitCommand(Command):
    def __init__(self, commands=None):
        super().__init__()
        # commands to execute before exiting
        if commands is None:
            commands = []
        self.commands = commands

    def execute(self, card_collection):
        print("Bye bye!")
        if len(self.commands) > 0:
            for command in self.commands:
                command.execute(card_collection)
        sys.exit()


class LogCommand(Command):
    def __init__(self, log_buffer):
        super().__init__()
        self.log_buffer = log_buffer

    def execute(self, card_collection):
        filename = input("File name:\n")
        with open(filename, 'w') as f:
            f.write(''.join(self.log_buffer))
        print("The log has been saved.")


class HardestCardCommand(Command):
    def execute(self, card_collection):
        hardest, max_errors = card_collection.get_hardest_cards()
        if max_errors == 0:
            print("There are no cards with errors.")
        else:
            if len(hardest) == 1:
                print(f'The hardest card is "{hardest[0]}". You have {max_errors} errors answering it.')
            else:
                terms = '", "'.join(hardest)
                print(f'The hardest cards are "{terms}". You have {max_errors} errors answering them.')


class ResetStatsCommand(Command):
    def execute(self, card_collection):
        card_collection.reset_stats()
