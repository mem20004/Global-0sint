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

def run_wiwok():
    print(center_text("\n=== wiwok: универсальный поиск по email, номеру, нику ===\n"))
    query = input(center_text("Введите email/ник/номер телефона (номер слитно, например +79123456789): ")).strip()
    if not query:
        print(center_text("Пустой ввод."))
        input(center_text("Press Enter..."))
        return
    wiwok_dir = os.path.join(os.path.dirname(__file__), "wiwok")
    if not os.path.isdir(wiwok_dir):
        print(center_text("Клонируем wiwok..."))
        try:
            subprocess.run(["git", "clone", "https://github.com/kirozaku/wiwok", wiwok_dir], check=True)
        except Exception as e:
            print(center_text(f"Ошибка клонирования: {e}"))
            input(center_text("Press Enter..."))
            return
    setup_flag = os.path.join(wiwok_dir, ".setup_done")
    if not os.path.exists(setup_flag):
        print(center_text("Выполняем установку wiwok (python3 wiwok.py --setup)..."))
        try:
            subprocess.run(["python3", os.path.join(wiwok_dir, "wiwok.py"), "--setup"], cwd=wiwok_dir, check=True)
            open(setup_flag, 'w').close()
        except Exception as e:
            print(center_text(f"Ошибка установки: {e}"))
    print(center_text(f"Запуск wiwok для {query}...\n"))
    try:
        process = subprocess.Popen(["python3", os.path.join(wiwok_dir, "wiwok.py"), query], cwd=wiwok_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        for line in process.stdout:
            print(center_text(line.rstrip()))
            time.sleep(0.02)
        process.wait()
    except Exception as e:
        print(center_text(f"Ошибка выполнения: {e}"))
    input(center_text("\nPress Enter..."))

def main():
    flash_screen(2, 0.1)
    clear_screen()
    print_banner()
    time.sleep(0.5)

    while True:
        print(center_text("\n" + "="*50))
        print(center_text("Universal Tools - Global-0sint"))
        print(center_text("="*50))
        print(center_text("1. wiwok (email, номер, ник)"))
        print(center_text("0. Назад"))
        choice = input(center_text("Выберите опцию: ")).strip()
        if choice == "1":
            run_wiwok()
        elif choice == "0":
            break
        else:
            print(center_text("Неверный ввод."))
            input(center_text("Press Enter..."))
        clear_screen()
        print_banner()

if __name__ == "__main__":
    main()
