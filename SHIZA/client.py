import socket
import threading

def receive_messages(client_socket):
    """Получение и отображение сообщений от сервера."""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(message)
        except (ConnectionResetError, BrokenPipeError):
            print("Соединение с сервером потеряно.")
            break

def start_client(host='127.0.0.1', port=12345):
    """Запуск клиента."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Подключен к серверу {host}\n") # :{port} 

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    try:
        while True:
            message = input('Введите сообщение: ')
            client_socket.sendall(message.encode())
    except (ConnectionResetError, BrokenPipeError):
        print("Соединение с сервером потеряно.")
    finally:
        client_socket.close()
        print("Клиент отключен.")

if __name__ == "__main__":
    start_client()
