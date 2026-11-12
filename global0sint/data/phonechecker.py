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

def check_phoneinfoga():
    try:
        subprocess.run(["phoneinfoga", "version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_phoneinfoga():
    print(center_text("Установка PhoneInfoga..."))
    cmd_install = 'curl -sSL https://raw.githubusercontent.com/sundowndev/phoneinfoga/master/support/scripts/install | bash'
    subprocess.run(cmd_install, shell=True, check=True)
    subprocess.run(["sudo", "mv", "./phoneinfoga", "/usr/local/bin/phoneinfoga"], check=True)
    print(center_text("PhoneInfoga установлен."))

def run_phoneinfoga(number):
    print(center_text(f"\nЗапуск PhoneInfoga для номера: {number}\n"))
    cmd = ["phoneinfoga", "scan", "-n", number]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in process.stdout:
        print(center_text(line.rstrip()))
        time.sleep(0.02)
    process.wait()
    print(center_text("\nPhoneInfoga завершил сканирование."))

def check_phoneintel():
    try:
        subprocess.run(["phoneintel", "--help"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_phoneintel():
    print(center_text("Устанавливаем phoneintel через pip..."))
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "phoneintel"], check=True)
        print(center_text("phoneintel установлен."))
    except Exception as e:
        print(center_text(f"Ошибка установки: {e}"))

def run_phoneintel(number):
    print(center_text(f"\nЗапуск phoneintel для номера: {number}\n"))
    cmd = ["phoneintel", "--info", number]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in process.stdout:
        print(center_text(line.rstrip()))
        time.sleep(0.02)
    process.wait()
    print(center_text("\nphoneintel завершил работу."))

def main():
    flash_screen(2, 0.1)
    clear_screen()
    print_banner()
    time.sleep(0.5)

    while True:
        print(center_text("\n" + "="*50))
        print(center_text("Phone Checker - Global-0sint"))
        print(center_text("="*50))
        print(center_text("1. PhoneInfoga (информация по номеру)"))
        print(center_text("2. PhoneIntel (информация по номеру)"))
        print(center_text("0. Назад"))
        choice = input(center_text("Выберите опцию: ")).strip()
        if choice == "1":
            if not check_phoneinfoga():
                confirm = input(center_text("PhoneInfoga не установлен. Установить? (y/n): ")).strip().lower()
                if confirm != 'y':
                    print(center_text("Установка отменена."))
                    input(center_text("Press Enter..."))
                    continue
                try:
                    install_phoneinfoga()
                except Exception as e:
                    print(center_text(f"Ошибка установки: {e}"))
                    input(center_text("Press Enter..."))
                    continue
            number = input(center_text("Введите номер телефона (+79111234567): ")).strip()
            if not number:
                print(center_text("Номер не введён."))
                input(center_text("Press Enter..."))
                continue
            run_phoneinfoga(number)
            input(center_text("Press Enter..."))
        elif choice == "2":
            if not check_phoneintel():
                confirm = input(center_text("phoneintel не установлен. Установить через pip? (y/n): ")).strip().lower()
                if confirm != 'y':
                    print(center_text("Установка отменена."))
                    input(center_text("Press Enter..."))
                    continue
                install_phoneintel()
                if not check_phoneintel():
                    print(center_text("Не удалось установить phoneintel."))
                    input(center_text("Press Enter..."))
                    continue
            number = input(center_text("Введите номер телефона (+79111234567): ")).strip()
            if not number:
                print(center_text("Номер не введён."))
                input(center_text("Press Enter..."))
                continue
            run_phoneintel(number)
            input(center_text("Press Enter..."))
        elif choice == "0":
            break
        else:
            print(center_text("Неверный ввод."))
            input(center_text("Press Enter..."))
        clear_screen()
        print_banner()

if __name__ == "__main__":
    main()
