import requests
import os
import time

# Link GitHub chứa code của Tool 1 và Tool 2
TOOL_1_URL = "https://raw.githubusercontent.com/tobiiyeuuemmmm/SICBO-TX/main/sicbo.py"
TOOL_2_URL = "https://raw.githubusercontent.com/tobiiyeuuemmmm/SICBO-TX/main/taixiu.py"
KEY_URL = "https://raw.githubusercontent.com/tobiiyeuuemmmm/SICBO-TX/main/key.txt"
KEY_FILE = "key.txt"

# Mã màu ANSI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Kiểm tra key online từ GitHub
def check_key(key):
    try:
        response = requests.get(KEY_URL, timeout=5)
        if response.status_code == 200:
            valid_keys = set(k.strip() for k in response.text.split("\n") if k.strip())  # Fix lỗi khoảng trắng & xuống dòng
            
            # Kiểm tra key hợp lệ
            if key.strip() in valid_keys or key.startswith(("testKEY", "adminKEY", "keymua", "getkey")):
                if key.startswith("getkey"):
                    print(GREEN + "🎁 Đây là key miễn phí! Hãy vào kênh Telegram để nhận key free mỗi ngày." + RESET)
                else:
                    print(GREEN + "✅ Key hợp lệ!" + RESET)
                return True
            else:
                print(RED + "❌ Key không hợp lệ!" + RESET)
                return False
    except:
        print(RED + "⚠️ Lỗi tải key! Kiểm tra lại kết nối mạng." + RESET)
    return False

# Lưu key vào file trên máy
def save_key(key):
    with open(KEY_FILE, "w") as f:
        f.write(key.strip())

# Đọc key từ file trên máy
def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            return f.read().strip()
    return None

# Nhập key mới
def get_key():
    while True:
        key = input(YELLOW + "🔑 Nhập key (hoặc 'off' để thoát): " + RESET).strip()

        if key.lower() == "off":
            print("👋 Thoát tool!")
            exit()

        if check_key(key):
            save_key(key)
            return key
        else:
            print(RED + "❌ Vui lòng thử lại." + RESET)

# Tải code từ GitHub và chạy trực tiếp
def run_tool(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            exec(response.text)  # Chạy code trực tiếp
        else:
            print(RED + "❌ Lỗi tải tool! Kiểm tra lại link GitHub." + RESET)
    except:
        print(RED + "❌ Lỗi khi chạy tool!" + RESET)

# Chạy tool
def main():
    os.system("clear")
    print(CYAN + "╔════════════════════════════════════╗")
    print("║   TOOL GỘP SICBO + TÀI XỈU         ║")
    print("║   QUẢN LÝ KEY ONLINE               ║")
    print("╠════════════════════════════════════╣")
    print("║ 🔑 Chủ Sở Hữu: @Sg205Rika          ║")
    print("║ 🔗 Link Share Tool:                ║")
    print("║   https://t.me/TxToolAkp           ║")
    print("║ 📢 Nhận thông báo & key free mỗi ngày! ║")
    print("╚════════════════════════════════════╝" + RESET)

    # Kiểm tra key đã lưu
    saved_key = load_key()
    if saved_key and check_key(saved_key):
        print(GREEN + f"🔑 Key đã lưu: {saved_key} (Dùng tiếp)" + RESET)
    else:
        saved_key = get_key()  # Nhập key mới nếu chưa có hoặc key cũ hết hạn

    while True:
        print(CYAN + "\n🔹 Chọn tool để chạy:" + RESET)
        print("[1] Tool Sicbo")
        print("[2] Tool Tài Xỉu")
        print("[getkey] Nhập key mới")
        print("[off] Thoát tool")

        choice = input(YELLOW + "🔢 Nhập lựa chọn: " + RESET).strip()

        if choice == "1":
            run_tool(TOOL_1_URL)
        elif choice == "2":
            run_tool(TOOL_2_URL)
        elif choice.lower() == "getkey":
            saved_key = get_key()  # Nhập lại key mới
        elif choice.lower() == "off":
            print(YELLOW + "👋 Thoát tool!" + RESET)
            break
        else:
            print(RED + "❌ Lựa chọn không hợp lệ! Vui lòng nhập lại." + RESET)

if __name__ == "__main__":
    main()
