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

def check_nmap():
    try:
        subprocess.run(["nmap", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_nmap():
    print(center_text("Устанавливаем nmap через apt..."))
    try:
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "nmap", "-y"], check=True)
        print(center_text("nmap установлен."))
    except Exception as e:
        print(center_text(f"Ошибка установки: {e}"))

def run_nmap(target):
    print(center_text(f"\nЗапуск nmap для {target}...\n"))
    cmd = ["nmap", target]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in process.stdout:
        print(center_text(line.rstrip()))
        time.sleep(0.02)
    process.wait()
    print(center_text("\nnmap завершил сканирование."))

def main():
    flash_screen(2, 0.1)
    clear_screen()
    print_banner()
    time.sleep(0.5)

    while True:
        print(center_text("\n" + "="*50))
        print(center_text("Ports Checker - Global-0sint"))
        print(center_text("="*50))
        print(center_text("1. Nmap (сканирование портов)"))
        print(center_text("0. Назад"))
        choice = input(center_text("Выберите опцию: ")).strip()
        if choice == "1":
            if not check_nmap():
                confirm = input(center_text("nmap не установлен. Установить через apt? (y/n): ")).strip().lower()
                if confirm != 'y':
                    print(center_text("Установка отменена."))
                    input(center_text("Press Enter..."))
                    continue
                install_nmap()
                if not check_nmap():
                    print(center_text("Не удалось установить nmap."))
                    input(center_text("Press Enter..."))
                    continue
            target = input(center_text("Введите домен или IP: ")).strip()
            if not target:
                print(center_text("Цель не введена."))
                input(center_text("Press Enter..."))
                continue
            run_nmap(target)
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
