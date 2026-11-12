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

def check_tool(tool_name):
    try:
        subprocess.run([tool_name, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_tool(tool_package):
    print(center_text(f"Устанавливаем {tool_package}..."))
    try:
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", tool_package, "-y"], check=True)
        print(center_text(f"{tool_package} установлен."))
    except Exception as e:
        print(center_text(f"Ошибка установки {tool_package}: {e}"))

def check_geointel():
    try:
        subprocess.run(["geointel", "--help"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_geointel():
    print(center_text("Устанавливаем geointel через pip..."))
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "geointel"], check=True)
        print(center_text("geointel установлен."))
    except Exception as e:
        print(center_text(f"Ошибка установки: {e}"))

def run_exiftool(file_path):
    print(center_text(f"\nЗапуск exiftool для {file_path}\n"))
    cmd = ["exiftool", file_path]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in process.stdout:
        print(center_text(line.rstrip()))
        time.sleep(0.02)
    process.wait()
    print(center_text("\n---\nЧтобы узнать больше о метаданных, закиньте вывод в нейросеть и задайте вопросы.\n---"))

def run_ffmpeg(file_path):
    print(center_text(f"\nЗапуск ffmpeg для {file_path}\n"))
    cmd = ["ffmpeg", "-i", file_path]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in process.stdout:
        print(center_text(line.rstrip()))
        time.sleep(0.02)
    process.wait()
    print(center_text("\n---\nЧтобы узнать больше о метаданных, закиньте вывод в нейросеть и задайте вопросы.\n---"))

def run_mediainfo(file_path):
    print(center_text(f"\nЗапуск mediainfo для {file_path}\n"))
    cmd = ["mediainfo", file_path]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in process.stdout:
        print(center_text(line.rstrip()))
        time.sleep(0.02)
    process.wait()
    print(center_text("\n---\nЧтобы узнать больше о метаданных, закиньте вывод в нейросеть и задайте вопросы.\n---"))

def run_geointel(file_path):
    print(center_text(f"\nЗапуск geointel для {file_path}\n"))
    cmd = ["geointel", "--image", file_path]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in process.stdout:
        print(center_text(line.rstrip()))
        time.sleep(0.02)
    process.wait()
    print(center_text("\n---\nЧтобы узнать больше о метаданных, закиньте вывод в нейросеть и задайте вопросы.\n---"))

def get_file_path():
    path = input(center_text("Введите путь к файлу (можно с ~, например ~/video.mp4): ")).strip()
    if not path:
        return None
    expanded_path = os.path.expanduser(path)
    if not os.path.isfile(expanded_path):
        print(center_text(f"Файл не найден: {expanded_path}"))
        return None
    return expanded_path

def main():
    flash_screen(2, 0.1)
    clear_screen()
    print_banner()
    time.sleep(0.5)

    while True:
        print(center_text("\n" + "="*50))
        print(center_text("Files Checker - Global-0sint"))
        print(center_text("Поддерживаемые форматы: JPG, PNG, PDF, DOCX, MP4, MOV и др."))
        print(center_text("="*50))
        print(center_text("1. exiftool (метаданные фото/видео/документов)"))
        print(center_text("2. ffmpeg (информация о мультимедиа)"))
        print(center_text("3. mediainfo (технические параметры)"))
        print(center_text("4. geointel (геолокация по изображению)"))
        print(center_text("0. Назад"))
        choice = input(center_text("Выберите опцию: ")).strip()
        if choice == "1":
            file_path = get_file_path()
            if not file_path:
                input(center_text("Press Enter..."))
                continue
            if not check_tool("exiftool"):
                confirm = input(center_text("exiftool не установлен. Установить через apt? (y/n): ")).strip().lower()
                if confirm != 'y':
                    print(center_text("Установка отменена."))
                    input(center_text("Press Enter..."))
                    continue
                install_tool("exiftool")
                if not check_tool("exiftool"):
                    print(center_text("Не удалось установить exiftool."))
                    input(center_text("Press Enter..."))
                    continue
            run_exiftool(file_path)
            input(center_text("Press Enter..."))
        elif choice == "2":
            file_path = get_file_path()
            if not file_path:
                input(center_text("Press Enter..."))
                continue
            if not check_tool("ffmpeg"):
                confirm = input(center_text("ffmpeg не установлен. Установить через apt? (y/n): ")).strip().lower()
                if confirm != 'y':
                    print(center_text("Установка отменена."))
                    input(center_text("Press Enter..."))
                    continue
                install_tool("ffmpeg")
                if not check_tool("ffmpeg"):
                    print(center_text("Не удалось установить ffmpeg."))
                    input(center_text("Press Enter..."))
                    continue
            run_ffmpeg(file_path)
            input(center_text("Press Enter..."))
        elif choice == "3":
            file_path = get_file_path()
            if not file_path:
                input(center_text("Press Enter..."))
                continue
            if not check_tool("mediainfo"):
                confirm = input(center_text("mediainfo не установлен. Установить через apt? (y/n): ")).strip().lower()
                if confirm != 'y':
                    print(center_text("Установка отменена."))
                    input(center_text("Press Enter..."))
                    continue
                install_tool("mediainfo")
                if not check_tool("mediainfo"):
                    print(center_text("Не удалось установить mediainfo."))
                    input(center_text("Press Enter..."))
                    continue
            run_mediainfo(file_path)
            input(center_text("Press Enter..."))
        elif choice == "4":
            file_path = get_file_path()
            if not file_path:
                input(center_text("Press Enter..."))
                continue
            if not check_geointel():
                confirm = input(center_text("geointel не установлен. Установить через pip? (y/n): ")).strip().lower()
                if confirm != 'y':
                    print(center_text("Установка отменена."))
                    input(center_text("Press Enter..."))
                    continue
                install_geointel()
                if not check_geointel():
                    print(center_text("Не удалось установить geointel."))
                    input(center_text("Press Enter..."))
                    continue
            run_geointel(file_path)
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