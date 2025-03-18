import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow
import requests
import rsa
import os

class RSACipher:
    def __init__(self):
        self.public_key = None
        self.private_key = None

    def generate_keys(self):
        # Tạo cặp khóa RSA
        (self.public_key, self.private_key) = rsa.newkeys(2048)
        
        # Tạo đường dẫn đến thư mục keys trong thư mục rsa
        keys_dir = os.path.join(os.path.dirname(__file__), 'keys')
        
        # Tạo thư mục keys nếu chưa tồn tại
        if not os.path.exists(keys_dir):
            os.makedirs(keys_dir)
        
        # Lưu khóa vào file trong thư mục keys
        with open(os.path.join(keys_dir, 'public.pem'), 'wb') as f:
            f.write(self.public_key.save_pkcs1('PEM'))
        with open(os.path.join(keys_dir, 'private.pem'), 'wb') as f:
            f.write(self.private_key.save_pkcs1('PEM'))

    def load_keys(self):
        # Đọc khóa từ thư mục keys trong thư mục rsa
        keys_dir = os.path.join(os.path.dirname(__file__), 'keys')
        try:
            with open(os.path.join(keys_dir, 'public.pem'), 'rb') as f:
                self.public_key = rsa.PublicKey.load_pkcs1(f.read())
            with open(os.path.join(keys_dir, 'private.pem'), 'rb') as f:
                self.private_key = rsa.PrivateKey.load_pkcs1(f.read())
            return self.private_key, self.public_key
        except:
            return None, None

    def encrypt(self, message, key):
        return rsa.encrypt(message.encode(), key)

    def decrypt(self, ciphertext, key):
        try:
            return rsa.decrypt(ciphertext, key).decode()
        except:
            return None

    def sign(self, message, private_key):
        try:
            # Chuyển đổi message thành bytes nếu chưa phải
            if isinstance(message, str):
                message = message.encode('utf-8')
            
            # Tạo chữ ký
            signature = rsa.sign(message, private_key, 'SHA-256')
            return signature.hex()  # Trả về chữ ký dạng hex string
        except Exception as e:
            print(f"Error signing message: {str(e)}")
            return None

    def verify(self, message, signature, public_key):
        try:
            if isinstance(message, str):
                message = message.encode('utf-8')
            signature_bytes = bytes.fromhex(signature)
            rsa.verify(message, signature_bytes, public_key)
            return True
        except:
            return False

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self): #Gọi API để tạo cặp khóa RSA (public/private).
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message) 

    def call_api_encrypt(self): #Gọi API để mã hóa thông điệp bằng khóa công khai.
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.txt_plain_text.toPlainText(),
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setText(data["encrypted_message"])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)

    def call_api_decrypt(self): #Gọi API để giải mã thông điệp bằng khóa riêng.
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txt_cipher_text.toPlainText(),
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setText(data["decrypted_message"])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)

    def call_api_sign(self): #Gọi API để ký thông điệp.
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {
            "message": self.ui.txt_info.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign_text.setText(data["signed_message"])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
            
    def call_api_verify(self): #Gọi API để ký thông điệp.
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signatute": self.ui.txt_sign_text.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if (data["is_verified"]):
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Successfully")
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Fail")
                    msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())