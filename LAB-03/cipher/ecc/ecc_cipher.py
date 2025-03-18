import ecdsa, os

if not os.path.exists('cipher/ecc/keys'):
    os.makedirs('cipher/ecc/keys')

class ECCCipher:
    def __init__(self):
        pass

    def generate_keys(self):
        sk = ecdsa.SigningKey.generate()  # Tạo khóa riêng tư
        vk = sk.get_verifying_key()      # Lấy khóa công khai từ khóa riêng tư
        
        with open('cipher/ecc/keys/privateKey.pem', 'wb') as p:
            p.write(sk.to_pem())
        
        with open('cipher/ecc/keys/publicKey.pem', 'wb') as p:
            p.write(vk.to_pem())

    def load_keys(self):
        with open('cipher/ecc/keys/privateKey.pem', 'rb') as p:
            sk = ecdsa.SigningKey.from_pem(p.read())
        
        with open('cipher/ecc/keys/publicKey.pem', 'rb') as p:
            vk = ecdsa.VerifyingKey.from_pem(p.read())
        
        return sk, vk

    def sign(self, message, key):
        # Ký dữ liệu bằng khóa riêng tư
        return key.sign(message.encode('ascii'))

    def verify(self, message, signature, key):
        try:
            return key.verify(signature, message.encode('ascii'))
        except ecdsa.BadSignatureError:
            return False

# Nếu bạn muốn kiểm thử nhanh:
if __name__ == "__main__":
    ecc = ECCCipher()
    ecc.generate_keys()
    sk, vk = ecc.load_keys()

    msg = "Hello, ECC!"
    signature = ecc.sign(msg, sk)
    
    is_verified = ecc.verify(msg, signature, vk)
    print("Chữ ký hợp lệ:" if is_verified else "Chữ ký không hợp lệ")

    # Thử với thông điệp khác
    is_verified_fake = ecc.verify("Fake Message", signature, vk)
    print("Chữ ký hợp lệ với thông điệp giả mạo:" if is_verified_fake else "Chữ ký không hợp lệ với thông điệp giả mạo")

# Nếu có gì cần cải tiến, cứ thoải mái nói nhé! 🚀
