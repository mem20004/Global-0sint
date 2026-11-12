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

def check_dig():
    try:
        subprocess.run(["dig", "-v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_dig():
    print(center_text("Устанавливаем dnsutils (dig)..."))
    try:
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "dnsutils", "-y"], check=True)
        print(center_text("dig установлен."))
    except Exception as e:
        print(center_text(f"Ошибка установки: {e}"))

def run_dig(domain, record_type="ANY"):
    print(center_text(f"\nDNS lookup для {domain} (тип {record_type}):\n"))
    cmd = ["dig", domain, record_type, "+noall", "+answer"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        output = result.stdout.strip()
        if output:
            for line in output.split('\n'):
                print(center_text(line))
                time.sleep(0.02)
        else:
            print(center_text(f"Записей типа {record_type} не найдено."))
    except Exception as e:
        print(center_text(f"Ошибка: {e}"))

def main():
    flash_screen(2, 0.1)
    clear_screen()
    print_banner()
    time.sleep(0.5)

    if not check_dig():
        confirm = input(center_text("dig не установлен. Установить dnsutils? (y/n): ")).strip().lower()
        if confirm == 'y':
            install_dig()
        else:
            print(center_text("dig не установлен. Работа будет ограничена."))

    while True:
        print(center_text("\n" + "="*50))
        print(center_text("DNS Lookup - Global-0sint"))
        print(center_text("="*50))
        print(center_text("1. A запись (IPv4)"))
        print(center_text("2. AAAA запись (IPv6)"))
        print(center_text("3. MX запись (почта)"))
        print(center_text("4. NS запись (DNS серверы)"))
        print(center_text("5. TXT запись (текст)"))
        print(center_text("6. CNAME запись (алиасы)"))
        print(center_text("7. SOA запись (зона)"))
        print(center_text("8. ВСЕ записи"))
        print(center_text("0. Назад"))

        choice = input(center_text("Выберите опцию: ")).strip()
        record_map = {
            "1": "A",
            "2": "AAAA",
            "3": "MX",
            "4": "NS",
            "5": "TXT",
            "6": "CNAME",
            "7": "SOA",
            "8": "ANY"
        }

        if choice == "0":
            break
        elif choice in record_map:
            domain = input(center_text("Введите домен (например, google.com): ")).strip()
            if not domain:
                print(center_text("Домен не введён."))
                input(center_text("Press Enter..."))
                continue
            run_dig(domain, record_map[choice])
            input(center_text("\nPress Enter..."))
        else:
            print(center_text("Неверный ввод."))
            input(center_text("Press Enter..."))

        clear_screen()
        print_banner()

if __name__ == "__main__":
    main()
