import os
import sys
import time
import subprocess
import re
import webbrowser
import shutil

HOLEHE_DIR = os.path.join(os.path.dirname(__file__), "holehe")

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

def install_holehe():
    if os.path.exists(HOLEHE_DIR):
        print(center_text("Обновляем holehe..."))
        subprocess.run(["git", "-C", HOLEHE_DIR, "pull"], check=False)
    else:
        print(center_text("Клонируем holehe..."))
        subprocess.run(["git", "clone", "https://github.com/megadose/holehe", HOLEHE_DIR], check=True)
    print(center_text("Устанавливаем holehe..."))
    subprocess.run([sys.executable, "-m", "pip", "install", "--user", "-e", HOLEHE_DIR], check=False)
    subprocess.run([sys.executable, "-m", "pip", "install", "--user", "holehe"], check=False)

def run_holehe(email):
    try:
        result = subprocess.run(
            ["holehe", email],
            capture_output=True,
            text=True,
            timeout=40
        )
        return result.stdout + result.stderr
    except FileNotFoundError:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "holehe", email],
                capture_output=True,
                text=True,
                timeout=40,
                cwd=HOLEHE_DIR
            )
            return result.stdout + result.stderr
        except Exception as e:
            return f"Ошибка: {e}"

def parse_holehe_output(output):
    lines = output.splitlines()
    results = []
    total_checked = None
    for line in lines:
        match = re.match(r'^(\[[+\-x]\])\s+(\S+)', line.strip())
        if match:
            symbol = match.group(1)
            site = match.group(2)
            if symbol == '[+]':
                icon = '✔️'
            elif symbol == '[-]':
                icon = '✘'
            elif symbol == '[x]':
                icon = '⚠️'
            else:
                icon = '?'
            results.append(f"{icon} {site}")
    match_total = re.search(r'(\d+)\s+websites checked', output)
    if match_total:
        total_checked = match_total.group(1)
    return results, total_checked

def holehe_menu():
    clear_screen()
    print_banner()
    print(center_text("\n=== Holehe: проверка регистрации email на сайтах ===\n"))
    email = input(center_text("Введите email: ")).strip()
    if not email:
        print(center_text("Email не введён."))
        input(center_text("Press Enter..."))
        return
    if not os.path.exists(HOLEHE_DIR):
        install_holehe()
    else:
        try:
            subprocess.run(["holehe", "--help"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(center_text("Команда holehe не найдена. Устанавливаем..."))
            install_holehe()
    print(center_text(f"\nПроверяем {email}... Подождите."))
    raw = run_holehe(email)
    parsed, total = parse_holehe_output(raw)
    if parsed:
        print(center_text("\nРезультаты:\n"))
        for line in parsed:
            print(center_text(line))
            time.sleep(0.03)
        if total:
            print(center_text(f"\nПроверено сайтов: {total}"))
        print(center_text("\n---\n✔️ - зарегистрировано\n✘ - не зарегистрировано\n⚠️ - не удалось подключиться\n---"))
    else:
        print(center_text("\nНе удалось получить список. Возможно, ошибка holehe."))
        print(center_text("=== Сырой вывод для отладки ==="))
        print(center_text(raw))
    input(center_text("\nPress Enter..."))

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

def haveibeenpwned_to():
    open_url("https://haveibeenpwned.to", "haveibeenpwned.to")

def mozilla_monitor():
    open_url("https://monitor.mozilla.org", "Mozilla Monitor")

def main():
    flash_screen(2, 0.1)
    clear_screen()
    print_banner()
    time.sleep(0.5)

    while True:
        print(center_text("\n" + "="*50))
        print(center_text("Email Checker - Global-0sint"))
        print(center_text("="*50))
        print(center_text("1. holehe (проверка регистрации на сайтах)"))
        print(center_text("2. haveibeenpwned.to (открыть сайт с утечками)"))
        print(center_text("3. Mozilla Monitor (проверка утечек)"))
        print(center_text("0. Назад"))
        choice = input(center_text("Выберите опцию: ")).strip()
        if choice == "1":
            holehe_menu()
        elif choice == "2":
            haveibeenpwned_to()
        elif choice == "3":
            mozilla_monitor()
        elif choice == "0":
            break
        else:
            print(center_text("Неверный ввод."))
            input(center_text("Press Enter..."))
        clear_screen()
        print_banner()

if __name__ == "__main__":
    main()