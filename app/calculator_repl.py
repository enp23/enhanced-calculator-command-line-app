########################
# Calculator REPL       #
########################

from decimal import Decimal
import logging
from colorama import Fore, Style, init
init(autoreset=True)

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory


def calculator_repl():
    """
    Command-line interface for the calculator.

    Implements a Read-Eval-Print Loop (REPL) that continuously prompts the user
    for commands, processes arithmetic operations, and manages calculation history.
    """
    try:
        # Initialize the Calculator instance
        calc = Calculator()

        # Register observers for logging and auto-saving history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print(f"{Fore.CYAN}Calculator started. Type 'help' for commands.")

        while True:
            try:
                # Prompt the user for a command
                command = input("\nEnter command: ").lower().strip()

                if command == 'help':
                    # Display available commands
                    print(f"{Fore.CYAN}\nAvailable commands:")
                    print(f"{Fore.CYAN}  add, subtract, multiply, divide, power, root, modulus, int_div, percentage, abs_diff   - Perform calculations")
                    print(f"{Fore.CYAN}  history - Show calculation history")
                    print(f"{Fore.CYAN}  clear - Clear calculation history")
                    print(f"{Fore.CYAN}  undo - Undo the last calculation")
                    print(f"{Fore.CYAN}  redo - Redo the last undone calculation")
                    print(f"{Fore.CYAN}  save - Save calculation history to file")
                    print(f"{Fore.CYAN}  load - Load calculation history from file")
                    print(f"{Fore.CYAN}  exit - Exit the calculator")
                    continue

                if command == 'exit':
                    # Attempt to save history before exiting
                    try:
                        calc.save_history()
                        print(f"{Fore.GREEN}History saved successfully.")
                    except Exception as e:
                        print(f"{Fore.YELLOW}Warning: Could not save history: {e}")
                    print(f"{Fore.CYAN}Goodbye!")
                    break

                if command == 'history':
                    # Display calculation history
                    history = calc.show_history()
                    if not history:
                        print(f"{Fore.YELLOW}No calculations in history")
                    else:
                        print(f"{Fore.CYAN}\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(f"{Fore.WHITE}{i}. {entry}")
                    continue

                if command == 'clear':
                    # Clear calculation history
                    calc.clear_history()
                    print(f"{Fore.GREEN}History cleared")
                    continue

                if command == 'undo':
                    # Undo the last calculation
                    if calc.undo():
                        print(f"{Fore.GREEN}Operation undone")
                    else:
                        print(f"{Fore.YELLOW}Nothing to undo")
                    continue

                if command == 'redo':
                    # Redo the last undone calculation
                    if calc.redo():
                        print(f"{Fore.GREEN}Operation redone")
                    else:
                        print(f"{Fore.YELLOW}Nothing to redo")
                    continue

                if command == 'save':
                    # Save calculation history to file
                    try:
                        calc.save_history()
                        print(f"{Fore.GREEN}History saved successfully")
                    except Exception as e:
                        print(f"{Fore.RED}Error saving history: {e}")
                    continue

                if command == 'load':
                    # Load calculation history from file
                    try:
                        calc.load_history()
                        print(f"{Fore.GREEN}History loaded successfully")
                    except Exception as e:
                        print(f"{Fore.RED}Error loading history: {e}")
                    continue

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root', 'modulus', 'int_div', 'percentage', 'abs_diff']:
                    # Perform the specified arithmetic operation
                    try:
                        print(f"{Fore.WHITE}\nEnter numbers (or 'cancel' to abort):")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print(f"{Fore.YELLOW}Operation cancelled")
                            continue
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print(f"{Fore.YELLOW}Operation cancelled")
                            continue

                        # Create the appropriate operation instance using the Factory pattern
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # Perform the calculation
                        result = calc.perform_operation(a, b)

                        # Normalize the result if it's a Decimal
                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print(f"{Fore.GREEN}\nResult: {result}")
                    except (ValidationError, OperationError) as e:
                        # Handle known exceptions related to validation or operation errors
                        print(f"{Fore.RED}Error: {e}")
                    except Exception as e:
                        # Handle any unexpected exceptions
                        print(f"Unexpected error: {e}")
                    continue

                # Handle unknown commands
                print(f"{Fore.YELLOW}Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                # Handle Ctrl+C interruption gracefully
                print(f"{Fore.YELLOW}\nOperation cancelled")
                continue
            except EOFError:
                # Handle end-of-file (e.g., Ctrl+D) gracefully
                print(f"{Fore.YELLOW}\nInput terminated. Exiting...")
                break
            except Exception as e:
                # Handle any other unexpected exceptions
                print(f"{Fore.RED}Error: {e}")
                continue

    except Exception as e:
        # Handle fatal errors during initialization
        print(f"{Fore.RED}Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise
