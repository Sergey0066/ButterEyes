import cv2
import os
import subprocess
import platform

def capture_webcam_image(folder="webcam", filename="webcam_snapshot.png"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Ошибка: не удалось открыть вебкамеру.")
        return

    ret, frame = cap.read()
    if ret:
        filepath = os.path.join(folder, filename)
        cv2.imwrite(filepath, frame)
        print(f"Изображение сохранено в {filepath}")
    else:
        print("Ошибка: не удалось получить изображение с вебкамеры.")

    cap.release()
    cv2.destroyAllWindows()

def get_connected_devices(output_file="device.txt"):
    """Собирает информацию о подключенных устройствах и сохраняет в файл."""
    print("Сбор информации о подключенных устройствах...")

    devices_info = []

    # Информация о микрофоне, клавиатуре и мышке (для Windows)
    try:
        devices = subprocess.check_output(
            "wmic path Win32_PnPEntity get Name",
            shell=True,
            text=True,
            encoding="utf-8",  # Используем UTF-8 для обработки символов
            errors="replace"  # Заменяем недекодируемые символы на знак вопроса
        )
        devices_info.append("=== УСТРОЙСТВА ПОДКЛЮЧЕННЫЕ К ПК ===")
        devices_info.extend(devices.splitlines())
    except Exception as e:
        devices_info.append(f"Ошибка при получении информации о подключенных устройствах: {e}")

    # Системная информация
    devices_info.append("\n=== ОБЩАЯ ИНФОРМАЦИЯ О СИСТЕМЕ ===")
    devices_info.append(f"Система: {platform.system()} {platform.release()}")
    devices_info.append(f"Имя устройства: {platform.node()}")
    devices_info.append(f"Процессор: {platform.processor()}")

    # Сохранение в файл
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(devices_info))

    print(f"Информация о подключенных устройствах сохранена в {output_file}")

def run_system_script():
    """Запуск другого скрипта system.py."""
    try:
        subprocess.run(["python", "system.py"], check=True)
        print("Скрипт system.py выполнен успешно.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при запуске system.py: {e}")

if __name__ == "__main__":
    webcam_folder = "webcam"

    # Снимок с вебкамеры
    capture_webcam_image(folder=webcam_folder)

    # Сохранение информации о подключенных устройствах
    get_connected_devices(output_file="device.txt")

    # Запуск скрипта system.py
    run_system_script()
