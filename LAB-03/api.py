from flask import Flask, request, jsonify
from cipher.rsa import RSACipher
from cipher.ecc.ecc_cipher import ECCCipher

app = Flask(__name__)

# ALGORITHM RSA CIPHER
rsa_cipher = RSACipher()

# Route để tạo khóa RSA (public và private)
@app.route('/api/rsa/generate_keys', methods=['GET'])
def rsa_generate_keys():
    rsa_cipher.generate_keys()  # Tạo cặp khóa RSA (public và private)
    return jsonify({'message': 'Keys generated successfully'})

# Route để mã hóa thông điệp bằng RSA
@app.route("/api/rsa/encrypt", methods=["POST"])
def rsa_encrypt():
    data = request.json
    message = data['message']  # Lấy thông điệp từ yêu cầu
    key_type = data['key_type']  # Lấy loại khóa (public hoặc private)
    private_key, public_key = rsa_cipher.load_keys()  # Tải khóa public và private

    # Chọn khóa dựa trên key_type ('public' hoặc 'private')
    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type'})  # Trả về lỗi nếu loại khóa không hợp lệ

    encrypted_message = rsa_cipher.encrypt(message, key)  # Mã hóa thông điệp với khóa đã chọn
    encrypted_hex = encrypted_message.hex()  # Chuyển đổi thông điệp đã mã hóa thành chuỗi hex
    return jsonify({'encrypted_message': encrypted_hex})  # Trả về thông điệp đã mã hóa

# Route để giải mã thông điệp bằng RSA
@app.route("/api/rsa/decrypt", methods=["POST"])
def rsa_decrypt():
    data = request.json
    ciphertext_hex = data['ciphertext']  # Lấy chuỗi hex của thông điệp đã mã hóa
    key_type = data['key_type']  # Lấy loại khóa (public hoặc private)
    private_key, public_key = rsa_cipher.load_keys()  # Tải khóa public và private

    # Chọn khóa dựa trên key_type ('public' hoặc 'private')
    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type'})  # Trả về lỗi nếu loại khóa không hợp lệ

    ciphertext = bytes.fromhex(ciphertext_hex)  # Chuyển đổi chuỗi hex trở lại thành bytes
    decrypted_message = rsa_cipher.decrypt(ciphertext, key)  # Giải mã thông điệp
    return jsonify({'decrypted_message': decrypted_message})  # Trả về thông điệp đã giải mã

# Route để ký thông điệp bằng khóa riêng
@app.route('/api/rsa/sign', methods=['POST'])
def rsa_sign_message():
    data = request.json
    message = data['message']  # Lấy thông điệp cần ký
    private_key, public_key = rsa_cipher.load_keys() # Ký thông điệp bằng khóa riêng
    # Tạo chữ ký với private key
    # signature = rsa_cipher.sign(message, private_key)
    signature = rsa_cipher.sign(message, private_key)
    return jsonify({'signature': signature})
    
# Route để xác thực chữ ký RSA
@app.route('/api/rsa/verify', methods=['POST'])
def rsa_verify_signature():
    data = request.json
    message = data['message']  # Lấy thông điệp cần xác thực
    signature = data['signature']  # Lấy chữ ký cần xác thực
    private_key, public_key = rsa_cipher.load_keys()  # Tải khóa công khai để xác thực chữ ký
    is_verified = rsa_cipher.verify(message, signature, public_key)  # Kiểm tra chữ ký
    return jsonify({'is_verified': is_verified})  # Trả về kết quả xác thực chữ ký (True/False)

ecc_cipher = ECCCipher()

@app.route('/api/ecc/generate_keys', methods=['GET'])
def ecc_generate_keys():
    ecc_cipher.generate_keys()
    return jsonify({'message': 'RSA keys generated successfully'})

# Endpoint để ký thông điệp bằng ECC
@app.route('/api/ecc/sign', methods=['POST'])
def ecc_sign_message():
    data = request.json
    message = data['message']
    private_key, _ = ecc_cipher.load_keys()
    signature = ecc_cipher.sign(message, private_key)
    signature_hex = signature.hex()
    return jsonify({'signature': signature_hex})

# Endpoint để xác thực chữ ký ECC
@app.route('/api/ecc/verify', methods=['POST'])
def ec_verify_signature():
    data = request.json
    message = data['message']
    signature_hex = data['signature']
    public_key, _ = ecc_cipher.load_keys()
    signature = bytes.fromhex(signature_hex)
    is_verified = ecc_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})

# Chạy ứng dụng Flask trên cổng 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)