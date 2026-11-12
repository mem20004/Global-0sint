import os
import sys
import time
import subprocess
import shutil

def slow_print_lines(lines, delay=0.05):
    for line in lines:
        print(line)
        sys.stdout.flush()
        time.sleep(delay)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_size():
    try:
        size = shutil.get_terminal_size()
        return size.columns, size.lines
    except:
        return 120, 30

def center_text(text):
    lines = text.split('\n')
    width, _ = get_terminal_size()
    centered = []
    for line in lines:
        padding = (width - len(line)) // 2
        if padding < 0:
            padding = 0
        centered.append(' ' * padding + line)
    return '\n'.join(centered)

def flash_screen(times=2, delay=0.1):
    for _ in range(times):
        sys.stdout.write("\x1b[?5h")
        sys.stdout.flush()
        time.sleep(delay)
        sys.stdout.write("\x1b[?5l")
        sys.stdout.flush()
        time.sleep(delay)

def print_banner():
    banner = r"""
  ▄████  ██▓     ▒█████   ▄▄▄▄    ▄▄▄       ██▓        ▒█████    ██████  ██▓ ███▄    █ ▄▄▄█████▓
 ██▒ ▀█▒▓██▒    ▒██▒  ██▒▓█████▄ ▒████▄    ▓██▒       ▒██▒  ██▒▒██    ▒ ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒
▒██░▄▄▄░▒██░    ▒██░  ██▒▒██▒ ▄██▒██  ▀█▄  ▒██░       ▒██░  ██▒░ ▓██▄   ▒██▒▓██  ▀█ ██▒▒ ▓██░ ▒░
░▓█  ██▓▒██░    ▒██   ██░▒██░█▀  ░██▄▄▄▄██ ▒██░       ▒██   ██░  ▒   ██▒░██░▓██▒  ▐▌██▒░ ▓██▓ ░ 
░▒▓███▀▒░██████▒░ ████▓▒░░▓█  ▀█▓ ▓█   ▓██▒░██████▒   ░ ████▓▒░▒██████▒▒░██░▒██░   ▓██░  ▒██▒ ░ 
 ░▒   ▒ ░ ▒░▓  ░░ ▒░▒░▒░ ░▒▓███▀▒ ▒▒   ▓▒█░░ ▒░▓  ░   ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░▓  ░ ▒░   ▒ ▒   ▒ ░░   
  ░   ░ ░ ░ ▒  ░  ░ ▒ ▒░ ▒░▒   ░   ▒   ▒▒ ░░ ░ ▒  ░     ░ ▒ ▒░ ░ ░▒  ░ ░ ▒ ░░ ░░   ░ ▒░    ░    
░ ░   ░   ░ ░   ░ ░ ░ ▒   ░    ░   ░   ▒     ░ ░      ░ ░ ░ ▒  ░  ░  ░   ▒ ░   ░   ░ ░   ░      
      ░     ░  ░    ░ ░   ░            ░  ░    ░  ░       ░ ░        ░   ░           ░          
                               ░
    """
    sys.stdout.write("\x1b[2J\x1b[H")
    lines = center_text(banner).split('\n')
    for line in lines:
        print(line)
        time.sleep(0.03)

def open_url(url, title):
    try:
        if sys.platform == "win32":
            os.startfile(url)
        elif sys.platform == "darwin":
            subprocess.run(["open", url], check=True)
        else:
            subprocess.run(["xdg-open", url], check=True)
        print(center_text(f"Открыт сайт: {title} ({url})"))
    except Exception as e:
        print(center_text(f"Не удалось открыть браузер: {e}"))
        print(center_text(f"Откройте вручную: {url}"))
    input(center_text("\nPress Enter..."))

def clone_telethon():
    telethon_dir = os.path.join(os.path.dirname(__file__), "Telethon")
    if os.path.isdir(telethon_dir):
        print(center_text("Telethon уже склонирован. Обновляем..."))
        try:
            subprocess.run(["git", "-C", telethon_dir, "pull"], check=False)
        except Exception as e:
            print(center_text(f"Ошибка обновления: {e}"))
    else:
        print(center_text("Клонируем Telethon..."))
        try:
            subprocess.run(["git", "clone", "https://github.com/LonamiWebs/Telethon", telethon_dir], check=True)
            print(center_text("Telethon успешно склонирован."))
        except Exception as e:
            print(center_text(f"Ошибка клонирования: {e}"))
    input(center_text("\nPress Enter..."))

def awesome_telegram():
    open_url("https://github.com/ItIsMeCall911/Awesome-Telegram-OSINT", "Awesome-Telegram-OSINT")

def main():
    flash_screen(2, 0.1)
    clear_screen()
    print_banner()
    time.sleep(0.5)

    while True:
        print(center_text("\n" + "="*50))
        print(center_text("Telegram - Global-0sint"))
        print(center_text("="*50))
        print(center_text("1. Telethon (клон репозитория)"))
        print(center_text("2. Awesome Telegram OSINT (открыть сайт)"))
        print(center_text("0. Назад"))
        choice = input(center_text("Выберите опцию: ")).strip()

        if choice == "1":
            clone_telethon()
        elif choice == "2":
            awesome_telegram()
        elif choice == "0":
            break
        else:
            print(center_text("Неверный ввод."))
            input(center_text("Press Enter..."))

        clear_screen()
        print_banner()

if __name__ == "__main__":
    main()
