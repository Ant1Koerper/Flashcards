from card_collection import CardCollection
from command import *
import sys
import builtins
import argparse

parser = argparse.ArgumentParser(
    description="This program helps you learn flashcards."
)
parser.add_argument("-i", "--import_from")
parser.add_argument("-e", "--export_to")

args = parser.parse_args()


class Logger:
    def __init__(self, original_stdout, log_buffer):
        self.original_stdout = original_stdout
        self.log_buffer = log_buffer

    def write(self, text):
        self.original_stdout.write(text)
        self.log_buffer.append(text)

    def flush(self):
        self.original_stdout.flush()


def main():
    # Initialize log buffer
    log_buffer = []

    original_stdout = sys.stdout
    sys.stdout = Logger(original_stdout, log_buffer)

    original_input = builtins.input

    def custom_input(prompt=''):
        user_input = original_input(prompt)
        log_buffer.append(user_input + '\n')
        return user_input

    builtins.input = custom_input
    # initialize card collection
    card_collection = CardCollection()

    # Import if file name is provided
    if args.import_from is not None:
        ImportCommand(args.import_from).execute(card_collection)

    # Export before exiting if file name is provided
    if args.export_to is not None:
        execute_before_exiting = [ExportCommand(args.export_to)]
    else:
        execute_before_exiting = []

    commands = {
        "add": AddCommand(),
        "remove": RemoveCommand(),
        "import": ImportCommand(),
        "export": ExportCommand(),
        "ask": AskCommand(),
        "exit": ExitCommand(commands=execute_before_exiting),
        "log": LogCommand(log_buffer),
        "hardest card": HardestCardCommand(),
        "reset stats": ResetStatsCommand()
    }
    while True:
        action = input("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")
        if action in commands:
            commands[action].execute(card_collection)
        else:
            print("Invalid action. Please choose from the available options.")


if __name__ == "__main__":
    main()
