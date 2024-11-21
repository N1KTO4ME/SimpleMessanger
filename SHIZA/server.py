import socket
import threading

# Настройки сервера
HOST = '0.0.0.0'
PORT = 12345

# Списки для хранения клиентов и их номеров
clients = []
client_numbers = {}

def broadcast(message, exclude_client=None):
    """Рассылает сообщение всем клиентам, кроме отправителя."""
    for client in clients:
        if client != exclude_client:
            try:
                client.sendall(message.encode())
            except:
                # Удаляем клиента, если возникли проблемы с подключением
                clients.remove(client)

def handle_client(client_socket, client_address, client_number):
    """Обрабатывает общение с одним клиентом."""
    print(f"Клиент {client_number} подключен: {client_address}")
    client_socket.sendall(f"Добро пожаловать! Ваш номер: {client_number}".encode())

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"\nКлиент {client_number}: {message}")
            broadcast(f"Клиент {client_number}: {message}", exclude_client=client_socket)
    except (ConnectionResetError, BrokenPipeError):
        print(f"Клиент {client_number} отключен.")
    finally:
        client_socket.close()
        clients.remove(client_socket)
        del client_numbers[client_socket]
        broadcast(f"Клиент {client_number} покинул чат.")

def start_server():
    """Запускает сервер."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Одновременное ожидание до 5 клиентов
    print(f"Сервер запущен на {HOST}:{PORT}\n\n")
    print(f"______________Привет! Это группа для общения______________\nНачало чата:\n") 

    client_counter = 1  # Счетчик для номеров клиентов
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)
            client_numbers[client_socket] = client_counter
            threading.Thread(
                target=handle_client,
                args=(client_socket, client_address, client_counter),
                daemon=True
            ).start()
            client_counter += 1
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
