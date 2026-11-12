#!/usr/bin/env python3
import os
import sys

def get_py_files():
    py_files = []
    root_dir = os.path.dirname(os.path.abspath(__file__))
    # Корень
    for f in os.listdir(root_dir):
        if f.endswith('.py') and f != 'z.py':
            py_files.append(os.path.join(root_dir, f))
    # Папка data (только непосредственные файлы)
    data_dir = os.path.join(root_dir, 'data')
    if os.path.isdir(data_dir):
        for f in os.listdir(data_dir):
            if f.endswith('.py'):
                py_files.append(os.path.join(data_dir, f))
    return py_files

def read_multiline():
    print("\nВведите новый код (многострочный). Для завершения ввода введите пустую строку (Enter дважды):")
    lines = []
    while True:
        line = sys.stdin.readline()
        if line.rstrip('\n') == '':
            if lines and lines[-1] == '':
                break
            lines.append('')
        else:
            lines.append(line.rstrip('\n'))
    if lines and lines[-1] == '':
        lines.pop()
    return '\n'.join(lines)

def main():
    py_files = get_py_files()
    if not py_files:
        print("Нет .py файлов для замены.")
        return

    while True:
        print("\nНайденные .py файлы (только корень и data, без holehe):")
        for idx, path in enumerate(py_files, 1):
            print(f"{idx}. {path}")
        print("0. Выход")
        choice = input("\nВыберите номер файла для замены: ").strip()
        if choice == '0':
            return
        if not choice.isdigit():
            print("Некорректный ввод, введите число.")
            continue
        idx = int(choice)
        if idx < 1 or idx > len(py_files):
            print("Номер вне диапазона.")
            continue

        target_file = py_files[idx-1]
        print(f"\nВыбран файл: {target_file}")
        print("Текущее содержимое:")
        print("-" * 40)
        with open(target_file, 'r', encoding='utf-8') as f:
            print(f.read())
        print("-" * 40)

        new_code = read_multiline()
        if not new_code.strip():
            print("Пустой код. Файл не изменён.")
            continue

        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(new_code)
        print(f"\nФайл {target_file} успешно обновлён.")
        input("Нажмите Enter, чтобы продолжить...")

if __name__ == "__main__":
    main()
