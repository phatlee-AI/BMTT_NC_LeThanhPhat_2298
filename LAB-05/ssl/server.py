import socket
import ssl
import threading

server_address = ('localhost', 12345)
clients = []

def handle_client(ssl_socket):
    clients.append(ssl_socket)
    client_addr = ssl_socket.getpeername()
    print(f"Đã kết nối với: {client_addr}")

    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Nhận từ {client_addr}: {message}")

            # Gửi lại cho tất cả client khác
            for client in clients[:]:  # Dùng bản sao để tránh lỗi khi modify list
                if client != ssl_socket:
                    try:
                        client.send(data)
                    except:
                        clients.remove(client)
                        client.close()
    except Exception as e:
        print(f"Lỗi xử lý client {client_addr}: {e}")
    finally:
        if ssl_socket in clients:
            clients.remove(ssl_socket)
        ssl_socket.close()
        print(f"Đã ngắt kết nối: {client_addr}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        certfile="certificates/server-cert.crt",
        keyfile="certificates/server-key.key"
    )

    print("Server SSL đang chờ kết nối...")
    try:
        while True:
            client_socket, addr = server_socket.accept()
            try:
                ssl_socket = context.wrap_socket(client_socket, server_side=True)
                threading.Thread(target=handle_client, args=(ssl_socket,)).start()
            except Exception as e:
                print(f"Lỗi thiết lập SSL: {e}")
                client_socket.close()
    except KeyboardInterrupt:
        print("\nĐang tắt server...")
    finally:
        for client in clients[:]:
            client.close()
        server_socket.close()

if __name__ == "__main__":
    main()