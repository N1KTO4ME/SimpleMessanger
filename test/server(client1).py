import socket

def start_server(host='0.0.0.0', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Сервер запущен на {host}:{port}")

    client_socket, client_address = server_socket.accept()
    print(f"Подключен клиент {client_address}")

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Клиент: {message}")
            reply = input("Вы: ")
            client_socket.sendall(reply.encode())
    except (ConnectionResetError, BrokenPipeError):
        print("Соединение потеряно.")
    finally:
        client_socket.close()
        server_socket.close()
        print("Сервер закрыт.")

if __name__ == "__main__":
    start_server()