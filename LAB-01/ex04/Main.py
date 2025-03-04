from QuanLySinhVien import QuanLySinhVien
qlsv = QuanLySinhVien()
while (1 == 1):
    print("1. Thêm sinh viên.")
    print("2. Cập nhật sinh viên theo ID.")
    print("3. Xóa sinh viên theo ID.")
    print("4. Tìm kiếm sinh viên theo ten.")
    print("5. Sắp xếp sinh viên theo diem trung binh.")
    print("6. Sắp xếp sinh viên theo tên chuyên ngành.")
    print("7. Hiển thị danh sách sinh viên.")
    print("0. Thoát chương trình.")
    choice = int(input("Nhập lựa chọn của bạn:"))
    if (choice == 1):
        print("\n1. Them sinh vien")
        qlsv.nhapSinhVien()
        print("\nThem sinh vien thanh cong!")
    elif (choice == 2):
        if (qlsv.soLuongSinhVien() > 0):
            print("\n2. Cap nhat thong tin sinh vien.")
            print("\nNhap ID: ")
            ID = int(input())
            qlsv.updateSinhVien(ID)
        else:
            print("\nDanh sach sinh vien rong.")
    elif (choice == 3):
        if (qlsv.soLuongSinhVien() > 0):
            print("\n3. Xoa sinh vien.")
            print("\nNhap ID: ")
            ID = int(input())
            if (qlsv.deleteById(ID)):
                print("\nSinh vien co id = ", ID, " da bi xoa.")
            else:
                print("\nKhong tim thay sinh vien co id = ", ID)
        else:
            print("\nDanh sach sinh vien rong.")
    elif (choice == 4):
        if (qlsv.soLuongSinhVien() > 0):
            print("\n4. Sap xep sinh vien theo ten.")
            print("\nNhap ten de tim kiem:")
            ten = input()
            searchResult = qlsv.findByName(ten)
            qlsv.showSinhVien(searchResult)
        else:
            print("\nDanh sach sinh vien rong.")
    elif (choice == 5):
        if (qlsv.soLuongSinhVien() > 0):
            print("\n5. Sap xep sinh vien theo diem trung binh (GPA).")
            qlsv.sortByDiemTB()
            qlsv.showSinhVien(qlsv.getListSinhVien())
        else:
            print("\nDanh sach sinh vien rong.")
    elif (choice == 6):
        if (qlsv.soLuongSinhVien() > 0):
            print("\n6. Sap xep sinh vien theo ten")
            qlsv.sortByName()
            qlsv.showSinhVien(qlsv.getListSinhVien())
        else:
            print("\nDanh sach sinh vien rong.")
    elif (choice == 7):
        if (qlsv.soLuongSinhVien() > 0):
            print("\n7. Hien thi danh sach sinh vien.")
            qlsv.showSinhVien(qlsv.getListSinhVien())
        else:
            print("\nDanh sach sinh vien rong.")
    elif (choice == 0):
        print("\nThoat chuong trinh.")
        break
    else:
        print("\nKhong co lua chon nay. Vui long chon lai.")
        print("\nHay chon chuc nang trong hop menu.")