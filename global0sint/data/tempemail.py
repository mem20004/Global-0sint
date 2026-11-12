import os
import sys
import time
import requests
import shutil
import webbrowser

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

def generate_temp_email():
    """Генерирует временный email через mail.tm API"""
    try:
        resp_domains = requests.get('https://api.mail.tm/domains', timeout=10)
        domains = resp_domains.json()
        if not domains or 'hydra:member' not in domains:
            return None, None
        domain = domains['hydra:member'][0]['domain']
        resp_account = requests.post('https://api.mail.tm/accounts', json={
            'address': f"user{int(time.time())}@{domain}",
            'password': 'temp123'
        }, timeout=10)
        if resp_account.status_code != 201:
            return None, None
        account = resp_account.json()
        email = account.get('address')
        resp_token = requests.post('https://api.mail.tm/token', json={
            'address': email,
            'password': 'temp123'
        }, timeout=10)
        if resp_token.status_code != 200:
            return None, None
        token = resp_token.json().get('token')
        return email, token
    except Exception as e:
        print(center_text(f"Ошибка: {e}"))
        return None, None

def check_inbox(token):
    headers = {'Authorization': f'Bearer {token}'}
    try:
        resp = requests.get('https://api.mail.tm/messages', headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('hydra:member', [])
        return []
    except Exception as e:
        print(center_text(f"Ошибка: {e}"))
        return []

def fetch_email_body(token, message_id):
    headers = {'Authorization': f'Bearer {token}'}
    try:
        resp = requests.get(f'https://api.mail.tm/messages/{message_id}', headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('text', data.get('html', 'Нет текста'))
        return "Не удалось прочитать письмо"
    except Exception as e:
        return f"Ошибка: {e}"

def main():
    flash_screen(2, 0.1)
    clear_screen()
    print_banner()
    time.sleep(0.5)

    token = None
    email = None

    while True:
        print(center_text("\n" + "="*50))
        print(center_text("Temp Email - Global-0sint"))
        print(center_text("="*50))
        print(center_text("1. Создать временный email"))
        print(center_text("2. Проверить входящие"))
        print(center_text("3. Открыть почту в браузере"))
        print(center_text("0. Назад"))
        choice = input(center_text("Выберите опцию: ")).strip()

        if choice == "1":
            print(center_text("\nГенерация временного email..."))
            email, token = generate_temp_email()
            if email:
                print(center_text(f"\nВаш временный email: {email}"))
                print(center_text("Сохраните этот адрес! Письма приходят автоматически."))
            else:
                print(center_text("Не удалось создать email. Попробуйте позже."))
            input(center_text("\nPress Enter..."))

        elif choice == "2":
            if not token:
                print(center_text("Сначала создайте email (опция 1)"))
                input(center_text("Press Enter..."))
                continue
            print(center_text("\nПроверка входящих..."))
            messages = check_inbox(token)
            if not messages:
                print(center_text("Нет новых писем."))
            else:
                print(center_text(f"\nНайдено писем: {len(messages)}"))
                for i, msg in enumerate(messages, 1):
                    print(center_text(f"\n--- Письмо {i} ---"))
                    from_addr = msg.get('from', {}).get('address', 'Неизвестно')
                    subject = msg.get('subject', 'Без темы')
                    date = msg.get('createdAt', 'Неизвестно')
                    print(center_text(f"От: {from_addr}"))
                    print(center_text(f"Тема: {subject}"))
                    print(center_text(f"Дата: {date}"))
                    show = input(center_text("Прочитать тело письма? (y/n): ")).strip().lower()
                    if show == 'y':
                        body = fetch_email_body(token, msg.get('id'))
                        print(center_text(f"\nТекст письма:\n{body}"))
            input(center_text("\nPress Enter..."))

        elif choice == "3":
            if not email:
                print(center_text("Сначала создайте email (опция 1)"))
                input(center_text("Press Enter..."))
                continue
            url = f"https://mail.tm/inbox/{email}"
            webbrowser.open(url)
            print(center_text(f"Открыта почта в браузере: {url}"))
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
