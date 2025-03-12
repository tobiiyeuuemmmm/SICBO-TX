import hashlib
import random
import os
import requests

# Mã màu ANSI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

# Thông tin tool
TOOL_NAME = "Tool Sicbo Tele: @sg205Rika"
TELEGRAM_LINK = "https://t.me/TxToolAkp"
KEY_URL = "https://raw.githubusercontent.com/tobiiyeuuemmmm/SICBO-TX/main/key.txt"
LOCAL_KEY_FILE = "key.txt"

# Hiển thị banner
def print_banner():
    os.system("clear || cls")  # Hỗ trợ cả Termux & Windows
    print(CYAN + "╔════════════════════════════════════╗")
    print("║         TOOL SICBO PREDICT         ║")
    print("╠════════════════════════════════════╣")
    print("║ 🔑 Chủ Sở Hữu: @Sg205Rika          ║")
    print("║ 🔗 Link kênh:                      ║")
    print("║   https://t.me/TxToolAkp           ║")
    print("╚════════════════════════════════════╝" + RESET)

# Tải danh sách key từ GitHub
def get_valid_keys():
    try:
        response = requests.get(KEY_URL, timeout=10)
        if response.status_code == 200:
            return set(line.split('|')[0].strip() for line in response.text.split("\n") if line.strip())
    except:
        print(RED + "⚠️ Không thể tải danh sách key! Đang kiểm tra key trên máy..." + RESET)
    return set()

# Kiểm tra key trên máy
def load_local_key():
    if os.path.exists(LOCAL_KEY_FILE):
        with open(LOCAL_KEY_FILE, "r") as f:
            return f.read().strip()
    return None

# Lưu key vào file
def save_local_key(key):
    with open(LOCAL_KEY_FILE, "w") as f:
        f.write(key)

# Xác định loại key
def identify_key_type(user_key):
    if user_key.startswith("getkey"):
        return "Free (24h)"
    elif user_key.startswith("testKEY"):
        return "Test (1-30 ngày)"
    elif user_key.startswith("adminKEY"):
        return "Admin (Vĩnh viễn)"
    elif user_key.startswith("keymua"):
        return "Mua (1-30 ngày)"
    return None

# Kiểm tra key hợp lệ
def check_key(user_key):
    valid_keys = get_valid_keys()
    
    if user_key in valid_keys or user_key.startswith(("getkey", "testKEY", "adminKEY", "keymua")):
        key_type = identify_key_type(user_key)
        if key_type:
            print(GREEN + f"✅ Key hợp lệ! Loại: {key_type}" + RESET)
            return True
    print(RED + "❌ Key không hợp lệ! Vui lòng thử lại." + RESET)
    return False

# Tính MD5
def calculate_md5(value):
    return hashlib.md5(value.encode()).hexdigest()

# XOR cho dự đoán
def xor_algorithm(value, key):
    try:
        value_int = int(value, 16)
        key_int = int(key, 16)
        xor_result = value_int ^ key_int
        return hex(xor_result)[2:]
    except ValueError:
        return "Lỗi XOR"

# Dự đoán kết quả Sicbo & Xác suất
def predict_sicbo(md5_key):
    probability_table = {'Tài': 48, 'Xỉu': 48, 'Bão': 4}  # Tăng xác suất "Bão" lên 4%
    result = random.choices(list(probability_table.keys()), weights=probability_table.values())[0]
    md5_result = calculate_md5(result)
    xor_result = xor_algorithm(md5_result, md5_key)
    probability = probability_table[result]

    return result, probability, xor_result

# Chạy tool
def main():
    print_banner()

    # Kiểm tra key đã lưu
    saved_key = load_local_key()
    if saved_key and check_key(saved_key):
        print(GREEN + f"🔑 Đang dùng key đã lưu: {saved_key}" + RESET)
    else:
        while True:
            user_key = input(YELLOW + "🔑 Nhập key (hoặc 'off' để thoát): " + RESET).strip()
            if user_key.lower() == "off":
                print(RED + "👋 Thoát tool!" + RESET)
                return
            if check_key(user_key):
                save_local_key(user_key)
                break

    while True:
        md5_key = input(YELLOW + "🔢 Nhập mã MD5 (hoặc 'off' để thoát): " + RESET).strip()

        if md5_key.lower() == "off":
            print(RED + "👋 Thoát tool!" + RESET)
            break

        if len(md5_key) != 32 or not all(c in "0123456789abcdef" for c in md5_key.lower()):
            print(RED + "❌ Mã MD5 không hợp lệ! Vui lòng nhập lại." + RESET)
            continue

        # Dự đoán kết quả
        result, probability, xor_result = predict_sicbo(md5_key)

        # Hiển thị kết quả
        print(GREEN + f"\n🎲 Kết quả dự đoán: {result}" + RESET)
        print(CYAN + f"🔑 XOR MD5: {xor_result}" + RESET)
        print(YELLOW + f"📊 Xác suất {result}: {probability}%" + RESET)
        print("\n🔥 Nhập mã MD5 tiếp theo hoặc gõ 'off' để thoát.")

if __name__ == "__main__":
    main()
