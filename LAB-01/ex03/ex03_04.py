def truy_cap_phan_tu(tuple_data):
    first_element = tuple_data[0]
    last_element = tuple_data[-1]
    return first_element, last_element

input_tuple = eval(input("Nhập Tuple, cách nhau bằng dấu phẩy:"))
first, last = truy_cap_phan_tu(input_tuple)
print(f"Phần tử đầu tiên và cuối cùng của Tuple là: {first}, {last}")