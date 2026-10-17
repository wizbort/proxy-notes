#!/usr/bin/env python3
import subprocess
import tkinter as tk
import psutil

PROXY_CMD = 'cloudflared access tcp --hostname proxy.wizbort.tech --url tcp://127.0.0.1:1080'
HOST = '127.0.0.1'
PORT = '1080'
SERVICE = 'Wi-Fi'

def start_proxy():
    # Запускаем cloudflared
    subprocess.Popen(PROXY_CMD, shell=True)
    # Настраиваем HTTP/HTTPS прокси
    subprocess.run(['networksetup', '-setwebproxy', SERVICE, HOST, PORT])
    subprocess.run(['networksetup', '-setsecurewebproxy', SERVICE, HOST, PORT])
    subprocess.run(['networksetup', '-setwebproxystate', SERVICE, 'on'])
    subprocess.run(['networksetup', '-setsecurewebproxystate', SERVICE, 'on'])
    status_label.config(text="Прокси включен")

def stop_proxy():
    # Убиваем cloudflared
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline_list = proc.info['cmdline']
            if cmdline_list is None:
                continue
            cmdline = ' '.join(cmdline_list)
            if 'cloudflared' in proc.info['name'] or 'cloudflared' in cmdline:
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Выключаем HTTP/HTTPS прокси и сбрасываем адреса
    subprocess.run(['networksetup', '-setwebproxystate', SERVICE, 'off'])
    subprocess.run(['networksetup', '-setsecurewebproxystate', SERVICE, 'off'])
    subprocess.run(['networksetup', '-setwebproxy', SERVICE, '', '0'])
    subprocess.run(['networksetup', '-setsecurewebproxy', SERVICE, '', '0'])

    status_label.config(text="Прокси выключен")

root = tk.Tk()
root.title("Toggle Proxy")
tk.Button(root, text="ON", command=start_proxy).pack(pady=5)
tk.Button(root, text="OFF", command=stop_proxy).pack(pady=5)
status_label = tk.Label(root, text="Статус: неизвестен")
status_label.pack(pady=5)
root.mainloop()