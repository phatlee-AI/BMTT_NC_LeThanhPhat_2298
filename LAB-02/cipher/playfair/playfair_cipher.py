# class PlayFairCipher:
#     def __init__(self) -> None:
#         pass
#     def __init__(self):
#         pass
#     def create_playfair_matrix(self, key):
#         key = key.replace('J', 'I')
#         key = key.upper()
#         key_set = set(key)
#         alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
#         remaining_letters = [letter for letter in alphabet if letter not in key_set]
#         matrix = list(key)
#         for letter in remaining_letters:
#             matrix.append(letter)
#             if len(matrix) == 25:
#                 break
#         playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
#         return playfair_matrix
#     def find_letter_coords(self, matrix, letter):
#         for row in range(len(matrix)):
#             for col in range(len(matrix[row])):
#                 if matrix[row][col] == letter:
#                     return row, col
#     def playfair_encrypt(self, plain_text, matrix):
#         plain_text = plain_text.replace('J', 'I')
#         plain_text = plain_text.upper()
#         encrypted_text = ""
#         for i in range(0, len(plain_text), 2):
#             pair = plain_text[i: i+2]
#             if len(pair) == 1:
#                 pair += 'X'
#             row1, col1 = self.find_letter_coords(matrix, pair[0])
#             row2, col2 = self.find_letter_coords(matrix, pair[1])
#             if row1 == row2:
#                 encrypted_text += matrix[row1][(col1+1) % 5] + matrix[row2][(col2+1) % 5]
#             elif col1 == col2:
#                 encrypted_text += matrix[(row1+1) % 5][col1] + matrix[(row2+1) % 5][col2]
#             else:
#                 encrypted_text += matrix[row1][col2] + matrix[row2][col1]
#         return encrypted_text
#     def playfair_decrypt(self, cipher_text, matrix):
#         cipher_text = cipher_text.upper()
#         decrypted_text = ""
#         for i in range(0, len(cipher_text), 2):
#             pair = cipher_text[i: i+2]
#             row1, col1 = self.find_letter_coords(matrix, pair[0])
#             row2, col2 = self.find_letter_coords(matrix, pair[1])
#             if row1 == row2:
#                 decrypted_text += matrix[row1][(col1-1) % 5] + matrix[row2][(col2-1) % 5]
#             elif col1 == col2:
#                 decrypted_text += matrix[(row1-1) % 5][col1] + matrix[(row2-1) % 5][col2]
#             else:
#                 decrypted_text += matrix[row1][col2] + matrix[row2][col1]
#         banro = ""
#         for i in range(0,len(decrypted_text)-2, 2):
#             if decrypted_text[i] == decrypted_text[i+2]:
#                 banro += decrypted_text[i]
#             else :
#                 banro += decrypted_text[i] + "" + decrypted_text[i+1]
#         if decrypted_text[-1] == "X":
#             banro += decrypted_text[-2]
#         else:
#             banro += decrypted_text[-2]
#             banro += decrypted_text[-1]
#         return banro
        
class PlayFairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.replace("J", "I")  # Replace "J" with "I"
        key = key.upper()
        key_set = set()
        matrix = []
        
        # Add key letters to the matrix, avoiding duplicates
        for letter in key:
            if letter not in key_set and letter != " ":
                matrix.append(letter)
                key_set.add(letter)
        
        # Add remaining letters of the alphabet (excluding "J")
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for letter in alphabet:
            if letter not in key_set:
                matrix.append(letter)
        
        # Reshape into a 5x5 matrix
        playfair_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        return None, None  # Letter not found (should not happen)

    def prepare_text(self, text):
        text = text.replace("J", "I")  # Replace "J" with "I"
        text = text.upper()
        prepared_text = ""
        
        # Add an "X" between double letters and at the end if odd length
        i = 0
        while i < len(text):
            prepared_text += text[i]
            if i + 1 < len(text):
                if text[i] == text[i+1]:
                    prepared_text += "X"  # Insert "X" between double letters
                else:
                    prepared_text += text[i+1]
                    i += 1
            else:
                prepared_text += "X"  # Add "X" if odd length
            i += 1
        return prepared_text

    def playfair_encrypt(self, plain_text, matrix):
        plain_text = self.prepare_text(plain_text)
        encrypted_text = ""
        
        for i in range(0, len(plain_text), 2):
            pair = plain_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            
            if row1 == row2:  # Same row
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:  # Same column
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:  # Rectangle
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
        
        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper()
        decrypted_text = ""
        
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            
            if row1 == row2:  # Same row
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:  # Same column
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:  # Rectangle
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]
        
        # Remove any padding "X" added during encryption
        if len(decrypted_text) >= 2 and decrypted_text[-1] == "X":
            decrypted_text = decrypted_text[:-1]
        
        return decrypted_text