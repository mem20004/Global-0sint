#!/usr/bin/env python3
import os
import sys
import time
import random
import shutil
import importlib.util

def slow_print_lines(lines, delay=0.05):
    for line in lines:
        print(line)
        sys.stdout.flush()
        time.sleep(delay)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_terminal_size(rows=50, cols=120):
    try:
        sys.stdout.write(f"\x1b[8;{rows};{cols}t")
        sys.stdout.flush()
    except:
        pass

def get_terminal_size():
    try:
        size = shutil.get_terminal_size()
        return size.columns, size.lines
    except:
        return 120, 30

def center_art(art, vertical_padding=True):
    lines = art.split('\n')
    width, height = get_terminal_size()
    centered_lines = []
    for line in lines:
        padding = (width - len(line)) // 2
        if padding < 0:
            padding = 0
        centered_lines.append(' ' * padding + line)
    if vertical_padding:
        art_height = len(lines)
        top_padding = max(0, (height - art_height) // 3)
        bottom_padding = max(0, height - art_height - top_padding)
        return '\n' * top_padding + '\n'.join(centered_lines) + '\n' * bottom_padding
    else:
        return '\n'.join(centered_lines)

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

def matrix_effect(duration=1.5):
    chars = '01'
    end_time = time.time() + duration
    try:
        while time.time() < end_time:
            line = ''.join(random.choice(chars) for _ in range(80))
            sys.stdout.write(f"\x1b[37m{line}\x1b[0m\n")
            sys.stdout.flush()
            time.sleep(0.03)
    except KeyboardInterrupt:
        pass

def white_screen(duration=1.0):
    sys.stdout.write("\x1b[47m\x1b[2J\x1b[H")
    sys.stdout.flush()
    time.sleep(duration)
    sys.stdout.write("\x1b[40m\x1b[2J\x1b[H")
    sys.stdout.flush()

def flash_screen(times=2, delay=0.1):
    for _ in range(times):
        sys.stdout.write("\x1b[?5h")
        sys.stdout.flush()
        time.sleep(delay)
        sys.stdout.write("\x1b[?5l")
        sys.stdout.flush()
        time.sleep(delay)

def print_ascii_art_slow(art, vertical_padding=True, line_delay=0.07):
    centered = center_art(art, vertical_padding)
    lines = centered.split('\n')
    for line in lines:
        print(line)
        sys.stdout.flush()
        time.sleep(line_delay)

def startup_animation():
    matrix_effect(1.5)
    flash_screen(2, 0.1)
    set_terminal_size(50, 120)
    white_screen(1.0)
    welcome_art = r"""
 █     █░▓█████  ██▓    ▄████▄  ▒█████   ███▄ ▄███▓▓█████    
▓█░ █ ░█░▓█   ▀ ▓██▒   ▒██▀ ▀█ ▒██▒  ██▒▓██▒▀█▀ ██▒▓█   ▀    
▒█░ █ ░█ ▒███   ▒██░   ▒▓█    ▄▒██░  ██▒▓██    ▓██░▒███      
░█░ █ ░█ ▒▓█  ▄ ▒██░   ▒▓▓▄ ▄██▒██   ██░▒██    ▒██ ▒▓█  ▄    
░░██▒██▓ ░▒████▒░██████▒ ▓███▀ ░ ████▓▒░▒██▒   ░██▒░▒████▒   
░ ▓░▒ ▒  ░░ ▒░ ░░ ▒░▓  ░ ░▒ ▒  ░ ▒░▒░▒░ ░ ▒░   ░  ░░░ ▒░ ░   
  ▒ ░ ░   ░ ░  ░░ ░ ▒  ░ ░  ▒    ░ ▒ ▒░ ░  ░      ░ ░ ░  ░   
  ░   ░     ░     ░ ░  ░       ░ ░ ░ ▒  ░      ░      ░      
    ░       ░  ░    ░  ░ ░         ░ ░         ░      ░  ░   
                       ░                                     
                     ▄▄▄█████▓ ▒█████                        
                     ▓  ██▒ ▓▒▒██▒  ██▒                      
                     ▒ ▓██░ ▒░▒██░  ██▒                      
                     ░ ▓██▓ ░ ▒██   ██░                      
                       ▒██▒ ░ ░ ████▓▒░ ██▓ ██▓              
                       ▒ ░░   ░ ▒░▒░▒░  ▒▓▒ ▒▓▒              
                         ░      ░ ▒ ▒░  ░▒  ░▒               
                       ░      ░ ░ ░ ▒   ░   ░                
                                  ░ ░    ░   ░               
                                         ░   ░               
    """
    print_ascii_art_slow(welcome_art, vertical_padding=True, line_delay=0.07)
    time.sleep(1.5)
    flash_screen(2, 0.1)
    white_screen(1.0)
    main_banner = r"""
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
    print_ascii_art_slow(main_banner, vertical_padding=True, line_delay=0.07)
    time.sleep(1)
    flash_screen(2, 0.1)
    clear_screen()

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
    centered = center_art(banner, vertical_padding=False)
    lines = centered.split('\n')
    for line in lines:
        print(line)
        time.sleep(0.03)

def print_exit_banner():
    exit_art = r"""
▄▄▄█████▓ ██░ ██  ▄▄▄      ███▄    █  ██ ▄█▀  ██████      █████▒▒█████   ██▀███  
▓  ██▒ ▓▒▓██░ ██▒▒████▄    ██ ▀█   █  ██▄█▒ ▒██    ▒    ▓██   ▒▒██▒  ██▒▓██ ▒ ██▒
▒ ▓██░ ▒░▒██▀▀██░▒██  ▀█▄ ▓██  ▀█ ██▒▓███▄░ ░ ▓██▄      ▒████ ░▒██░  ██▒▓██ ░▄█ ▒
░ ▓██▓ ░ ░▓█ ░██ ░██▄▄▄▄██▓██▒  ▐▌██▒▓██ █▄   ▒   ██▒   ░▓█▒  ░▒██   ██░▒██▀▀█▄  
  ▒██▒ ░ ░▓█▒░██▓ ▓█   ▓██▒██░   ▓██░▒██▒ █▄▒██████▒▒   ░▒█░   ░ ████▓▒░░██▓ ▒██▒
  ▒ ░░    ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒░   ▒ ▒ ▒ ▒▒ ▓▒▒ ▒▓▒ ▒ ░    ▒ ░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
    ░     ▒ ░▒░ ░  ▒   ▒▒ ░ ░░   ░ ▒░░ ░▒ ▒░░ ░▒  ░ ░    ░       ░ ▒ ▒░   ░▒ ░ ▒░
  ░       ░  ░░ ░  ░   ▒     ░   ░ ░ ░ ░░ ░ ░  ░  ░      ░ ░   ░ ░ ░ ▒    ░░   ░ 
          ░  ░  ░      ░  ░        ░ ░  ░         ░                ░ ░     ░     
                      █    ██  ██████  ██▓ ███▄    █   ▄████                     
                      ██  ▓██▒██    ▒ ▓██▒ ██ ▀█   █  ██▒ ▀█▒                    
                     ▓██  ▒██░ ▓██▄   ▒██▒▓██  ▀█ ██▒▒██░▄▄▄░                    
                     ▓▓█  ░██░ ▒   ██▒░██░▓██▒  ▐▌██▒░▓█  ██▓                    
                     ▒▒█████▓▒██████▒▒░██░▒██░   ▓██░░▒▓███▀▒                    
                     ░▒▓▒ ▒ ▒▒ ▒▓▒ ▒ ░░▓  ░ ▒░   ▒ ▒  ░▒   ▒                     
                     ░░▒░ ░ ░░ ░▒  ░ ░ ▒ ░░ ░░   ░ ▒░  ░   ░                     
                      ░░░ ░ ░░  ░  ░   ▒ ░   ░   ░ ░ ░ ░   ░                     
                        ░          ░   ░           ░       ░
    """
    centered = center_art(exit_art, vertical_padding=True)
    lines = centered.split('\n')
    for line in lines:
        print(line)
        time.sleep(0.05)

def load_tool(tool_name):
    tool_path = os.path.join("data", f"{tool_name}.py")
    if not os.path.exists(tool_path):
        print(center_text(f"Tool {tool_name} not found."))
        input(center_text("Press Enter to continue..."))
        return
    spec = importlib.util.spec_from_file_location(tool_name, tool_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "main"):
        module.main()
    else:
        print(center_text("No main() function in tool."))
        input(center_text("Press Enter to continue..."))

def main():
    startup_animation()
    while True:
        print_banner()
        menu_text = """
        |======================================|
        | 1. IP Checker                        |
        | 2. Email Checker                     |
        | 3. Nick Checker                      |
        | 4. Subdomains Checker                |
        | 5. Ports Checker                     |
        | 6. Phone Checker                     |
        | 7. Directories Checker               |
        | 8. Files Checker                     |
        | 9. Google Dorks                      |
        | 10. Temp Email                       |
        | 11. DNS Lookup                       |
        | 12. Visualize                        |
        | 13. Telegram                         |
        |                                      |
        | 98. Universal Tools                  |
        | 99. Exit                             |
        |======================================|
        """
        centered_menu = center_text(menu_text)
        lines = centered_menu.split('\n')
        for line in lines:
            print(line)
            time.sleep(0.03)
        choice = input(center_text("Enter Your Option: ")).strip()
        if choice == "1":
            load_tool("ipchecker")
        elif choice == "2":
            load_tool("emailchecker")
        elif choice == "3":
            load_tool("nickchecker")
        elif choice == "4":
            load_tool("subdomainschecker")
        elif choice == "5":
            load_tool("portschecker")
        elif choice == "6":
            load_tool("phonechecker")
        elif choice == "7":
            load_tool("directorieschecker")
        elif choice == "8":
            load_tool("fileschecker")
        elif choice == "9":
            load_tool("googledork")
        elif choice == "10":
            load_tool("tempemail")
        elif choice == "11":
            load_tool("dnslookup")
        elif choice == "12":
            load_tool("visualize")
        elif choice == "13":
            load_tool("telegram")
        elif choice == "98":
            load_tool("universal")
        elif choice == "99":
            clear_screen()
            print_exit_banner()
            break
        else:
            print(center_text("Invalid option. Try again."))
            input(center_text("Press Enter to continue..."))
        clear_screen()

if __name__ == "__main__":
    main()