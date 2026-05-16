from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.formatted_text import HTML

def get_file_name():
    try:
        file_completer = PathCompleter(only_directories=False, expanduser=True)
        user_input = prompt(
            HTML('Введите путь к картинке: '),
            completer=file_completer,
            complete_while_typing=True
        )
        
        return user_input
    except (KeyboardInterrupt, EOFError):
        print("\nОперация отменена пользователем.")
        return None

if __name__ == "__main__":
    file_path = get_file_name()
    print(f"\nВы выбрали: {file_path}")