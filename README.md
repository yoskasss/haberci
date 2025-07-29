# Haberci 📰

Kivy ile yazılmış, farklı haber sitelerinden başlıkları ve içerikleri çekip gösteren basit bir masaüstü haber uygulaması.

## Özellikler

- Haber başlıklarını listeler
- Başlığa tıklayınca detay popup'ı açılır
- Karanlık/aydınlık tema desteği
- Farklı site ve CSS selector ayarı ile yeni kaynak eklenebilir

## Kurulum

1. **Gereksinimler**
    - Python 3.7+
    - [Kivy](https://kivy.org/#download)
    - requests
    - beautifulsoup4

2. **Kurulum Komutları**
    ```bash
    pip install kivy requests beautifulsoup4
    ```

3. **Çalıştırma**
    ```bash
    python app.py
    ```

## Kullanım

- Sol üstteki menüden haber kaynağı URL'si ve CSS selector'ı değiştirilebilir.
- Karanlık mod anahtarı ile tema değiştirilebilir.
- Haber başlıklarına tıklayarak detay popup'ı açılır.

## Haber Kaynağı Ayarları

Varsayılan olarak Hurriyet Gündem sayfası ve `.category__list a` selector'ı kullanılır.  
Farklı bir site eklemek için menüden URL ve CSS selector girilebilir.

Örnek:
- URL: `https://www.hurriyet.com.tr/gundem/`
- CSS Seçici: `a.news-title`



## Katkı

PR ve önerilere açıktır!

---
