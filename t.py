def ask(text: str) -> bool:
    while True:
        try:
            selection = input(f"{text.rstrip()} [Y/n]:").strip().lower()
            if selection in ("y", ""):
                return True
            if selection == "n":
                return False
            print("Please enter 'y' or 'n'.")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user.")
            return False
            
print(ask("what?"))