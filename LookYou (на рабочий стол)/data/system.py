import os
import time
import tkinter as tk

def display_loading_window(duration=3):
    """Создает всплывающее окно с сообщением о загрузке."""
    root = tk.Tk()
    root.title("Загрузка")
    root.geometry("300x100")
    root.resizable(False, False)

    label = tk.Label(root, text="Пожалуйста, подождите,\nидет загрузка данных...", font=("Arial", 12))
    label.pack(expand=True)

    root.after(duration * 1000, root.destroy)
    root.mainloop()

def get_files_from_downloads():
    """Получает все файлы из папки 'Загрузки'."""
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    file_list = []
    if os.path.exists(downloads_path):
        for root, dirs, files in os.walk(downloads_path):
            for file in files:
                file_list.append(os.path.join(root, file))
    else:
        print("Папка 'Загрузки' не найдена.")
    return file_list

def get_files_from_roaming():
    """Получает все файлы из папки 'AppData\\Roaming'."""
    roaming_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming")
    file_list = []
    if os.path.exists(roaming_path):
        for root, dirs, files in os.walk(roaming_path):
            for file in files:
                file_list.append(os.path.join(root, file))
    else:
        print("Папка 'AppData\\Roaming' не найдена.")
    return file_list

def get_folders_from_d_drive():
    """Получает названия папок с диска D."""
    d_drive_path = "D:\\"
    folder_list = []
    if os.path.exists(d_drive_path):
        for folder in os.listdir(d_drive_path):
            if os.path.isdir(os.path.join(d_drive_path, folder)):
                folder_list.append(folder)
    else:
        print("Диск D не найден.")
    return folder_list

def save_info_to_file(downloads, roaming, d_folders, output_file="infofile.txt"):
    """Сохраняет информацию о файлах и папках в указанный файл."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=== ФАЙЛЫ В ЗАГРУЗКАХ ===\n")
        f.write("\n".join(downloads) + "\n\n")
        f.write("=== ФАЙЛЫ В 'AppData\\Roaming' ===\n")
        f.write("\n".join(roaming) + "\n\n")
        f.write("=== ПАПКИ НА ДИСКЕ D ===\n")
        f.write("\n".join(d_folders) + "\n")
    print(f"Информация сохранена в файл: {output_file}")

if __name__ == "__main__":
    display_loading_window()

    downloads_files = get_files_from_downloads()
    roaming_files = get_files_from_roaming()
    d_drive_folders = get_folders_from_d_drive()

    save_info_to_file(downloads_files, roaming_files, d_drive_folders)
