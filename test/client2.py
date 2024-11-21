import socket

def start_client(host='127.0.0.1', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Подключен к серверу {host}:{port}")

    try:
        while True:
            message = input("Вы: ")
            client_socket.sendall(message.encode())
            reply = client_socket.recv(1024).decode()
            if not reply:
                break
            print(f"Сервер: {reply}")
    except (ConnectionResetError, BrokenPipeError):
        print("Соединение потеряно.")
    finally:
        client_socket.close()
        print("Клиент отключен.")

if __name__ == "__main__":
    start_client()