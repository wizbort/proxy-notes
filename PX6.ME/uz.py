#!/usr/bin/env python3
import subprocess
import sys

SERVICE = "Wi-Fi"

# Настройки твоего HTTPS-прокси
PROXY_HOST = "YOUR_PROXY_IP"
PROXY_PORT = "8000"
PROXY_USER = "1g9mxb"
PROXY_PASS = "RtmX2D"

def enable_proxy():
    # Включаем системный HTTP/HTTPS прокси
    subprocess.run([
        "networksetup", "-setwebproxy", SERVICE, PROXY_HOST, PROXY_PORT, "on"
    ])
    subprocess.run([
        "networksetup", "-setsecurewebproxy", SERVICE, PROXY_HOST, PROXY_PORT, "on"
    ])
    # Указываем, что прокси требует авторизацию
    subprocess.run([
        "networksetup", "-setwebproxyusername", SERVICE, PROXY_USER
    ])
    subprocess.run([
        "networksetup", "-setwebproxypassword", SERVICE, PROXY_PASS
    ])
    subprocess.run([
        "networksetup", "-setsecurewebproxyusername", SERVICE, PROXY_USER
    ])
    subprocess.run([
        "networksetup", "-setsecurewebproxypassword", SERVICE, PROXY_PASS
    ])
    print(f"Системный HTTPS-прокси включён: {PROXY_HOST}:{PROXY_PORT}")

def disable_proxy():
    # Выключаем прокси
    subprocess.run(["networksetup", "-setwebproxystate", SERVICE, "off"])
    subprocess.run(["networksetup", "-setsecurewebproxystate", SERVICE, "off"])
    print("Системный HTTPS-прокси выключен")

def check_ip():
    # Проверяем внешний IP
    try:
        result = subprocess.run(
            ["curl", "-s", "https://api.ipify.org"],
            capture_output=True, text=True, timeout=5
        )
        print("Текущий внешний IP:", result.stdout.strip())
    except subprocess.TimeoutExpired:
        print("Не удалось проверить IP")

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ["on", "off", "check"]:
        print("Использование: python uz_proxy.py [on|off|check]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "on":
        enable_proxy()
        check_ip()
    elif cmd == "off":
        disable_proxy()
    elif cmd == "check":
        check_ip()