# Chrome Password Analyzer (Educational Purpose)

Bu proje, Windows işletim sisteminde çalışan Google Chrome tarayıcısındaki kayıtlı giriş verilerinin nasıl saklandığını ve çözüldüğünü eğitim amaçlı göstermek için hazırlanmıştır.

## ⚠️ Uyarı

Bu proje yalnızca:

* Siber güvenlik eğitimi
* Adli bilişim çalışmaları
* Kendi sisteminizi analiz etme
* Tarayıcı şifreleme mantığını öğrenme

amaçlarıyla kullanılmalıdır.

Başkasına ait cihazlarda izinsiz kullanım:

* Yasa dışıdır
* Etik değildir
* Suç teşkil edebilir

Tüm sorumluluk kullanıcıya aittir.

---

# Nasıl Çalışıyor?


1. Chrome'un `Local State` dosyasını okur
2. Windows DPAPI sistemi ile ana anahtarı çözer
3. Chrome'un `Login Data` SQLite veritabanını kopyalar
4. Kayıtlı girişleri çeker
5. AES-GCM ile şifreleri çözmeye çalışır
6. Sonuçları `.txt` dosyasına kaydeder

---

# Gereksinimler

* Windows
* Python 3.x
* Google Chrome

## Kurulum

```bash
pip install pycryptodome pypiwin32
```

---

# Kullanım

```bash
python main.py
```

Çalıştırıldıktan sonra:

```bash
chrome_passwords_dump.txt
```

dosyası oluşur.

---

# Örnek Çıktı

```txt
Site: https://example.com
Kullanıcı: admin
Şifre: 123456
--------------------------------------------------
```

---

# Teknik Detaylar

Kullanılan teknolojiler:

* Python
* SQLite3
* Windows DPAPI
* AES-GCM
* Chrome Local State parsing

---

# Amaç

Bu proje:

* Chrome'un şifre saklama mantığını öğretmek
* Windows DPAPI kullanımını göstermek
* AES şifre çözme sürecini anlamak
* Python ile forensic analiz pratiği yapmak

için geliştirilmiştir.

---

# Sorumluluk Reddi

Bu proje tamamen eğitim ve araştırma amaçlıdır.

Projeyi kullanarak oluşabilecek:

* Veri kaybı
* Yetkisiz erişim
* Hukuki sorunlar
* Güvenlik ihlalleri

gibi durumlardan geliştirici sorumlu değildir.
