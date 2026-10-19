# -*- coding: utf-8 -*-
import socket
import sys
import datetime


def get_local_ip():
    """Получить IP компьютера в локальной сети."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Подключение к внешнему адресу не отправляет данные,
        # но позволяет ОС выбрать правильный сетевой интерфейс
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'


def start_server(host='0.0.0.0', port=5000):
    local_ip = get_local_ip()

    print('=' * 60)
    print(' СЕРВЕР ПРИЁМА СООБЩЕНИЙ С ТЕЛЕФОНА')
    print('=' * 60)
    print(f' IP этого ПК в локальной сети: {local_ip}')
    print(f' Порт: {port}')
    print(f' Введите этот IP в приложение на телефоне')
    print('=' * 60)
    print(' Ожидаю подключения...\n')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
    except OSError as e:
        print(f'[ОШИБКА] Не удалось занять порт {port}: {e}')
        print('Попробуйте другой порт или закройте программу, занимающую его.')
        sys.exit(1)

    server_socket.listen(5)

    try:
        while True:
            conn, addr = server_socket.accept()
            try:
                data = conn.recv(4096)
                if data:
                    message = data.decode('utf-8', errors='replace')
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    print(f'[{timestamp}] {addr[0]}: {message}')
                    sys.stdout.flush()
            except Exception as e:
                print(f'[ОШИБКА при чтении] {e}')
            finally:
                conn.close()
    except KeyboardInterrupt:
        print('\n\nСервер остановлен пользователем.')
    finally:
        server_socket.close()


if __name__ == '__main__':
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f'Некорректный порт: {sys.argv[1]}')
            sys.exit(1)
    start_server(port=port)