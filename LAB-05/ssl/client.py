import socket
import ssl
import threading

server_address = ('localhost', 12345)

def receive_data(ssl_socket):
    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            print("Nhận từ server:", data.decode('utf-8'))
    except Exception as e:
        print(f"Lỗi nhận dữ liệu: {e}")
    finally:
        ssl_socket.close()
        print("Kết thúc nhận dữ liệu")

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        with context.wrap_socket(client_socket, server_hostname=server_address[0]) as ssl_socket:
            ssl_socket.connect(server_address)
            print(f"Đã kết nối tới server {server_address}")

            receive_thread = threading.Thread(
                target=receive_data,
                args=(ssl_socket,),
                daemon=True
            )
            receive_thread.start()

            try:
                while True:
                    message = input("> ")
                    if message.lower() == 'exit':
                        break
                    ssl_socket.send(message.encode('utf-8'))
            except (KeyboardInterrupt, EOFError):
                print("\nĐang thoát...")
            finally:
                ssl_socket.shutdown(socket.SHUT_RDWR)
    except Exception as e:
        print(f"Lỗi kết nối: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()