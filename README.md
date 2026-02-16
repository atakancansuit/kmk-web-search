# KMK Web Search: Apartman Yönetimi Hukuk Asistanı

## Proje Hakkında
Bu proje, apartman yönetimi, Kat Mülkiyeti Kanunu, komşuluk ilişkileri ve gayrimenkul hukuku alanındaki sorulara yanıt vermek üzere geliştirilmiş özelleştirilmiş bir yapay zeka asistanıdır.

Sistem, OpenAI GPT-4o-mini dil modelini temel alarak çalışır ancak yanıtlarını yalnızca Türkiye Cumhuriyeti'nin resmi mevzuat portalı olan **mevzuat.gov.tr** üzerinden gerçekleştirdiği gerçek zamanlı aramalarla oluşturur. Bu sayede, genel geçer bilgiler yerine güncel, doğrulanabilir ve hukuki dayanağı olan yanıtlar sunulması hedeflenmiştir.

**Sistemin Temel Özellikleri:**
1.  **Resmi Kaynak Odaklılık:** Yanıtlar yalnızca `mevzuat.gov.tr` kaynaklarından derlenir.
2.  **Şeffaflık:** Asistan, verdiği her bilginin kaynağını ve ilgili internet bağlantısını kullanıcı ile paylaşır.
3.  **Yüksek Tutarlılık:** Deterministik ayarlar sayesinde benzer sorulara tutarlı ve standart yanıtlar üretilir.
4.  **Hafif Mimari:** Herhangi bir yerel veritabanı veya ağır indeksleme işlemi gerektirmez; tamamen web tabanlı arama motoru entegrasyonu ile çalışır.

---

## Kurulum ve Çalıştırma Rehberi

Bu projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları takip edebilirsiniz.

### Ön Hazırlık
Projenin çalışabilmesi için bilgisayarınızda **Python 3.8** veya üzeri bir sürümün yüklü olması gerekmektedir.

### 1. Kurulumu Gerçekleştirin
Projeyi indirdiğiniz dizinde bir terminal açın ve gerekli kütüphanelerin yüklenmesi için aşağıdaki komutu çalıştırın:

```bash
make setup
```

Eğer `make` komutu sisteminizde tanımlı değilse, alternatif olarak şu komutu kullanabilirsiniz:
```bash
pip install -r requirements.txt
```

### 2. Yapılandırma Ayarlarını Girin
Proje dizininde yer alan `.env.example` dosyasının adını `.env` olarak değiştirin. Bu dosyayı bir metin editörü ile açarak `OPENAI_API_KEY` alanına kendi OpenAI API anahtarınızı giriniz.

Örnek `.env` içeriği:
```env
OPENAI_API_KEY=sk-proj-...
```

### 3. Uygulamayı Başlatın
Kurulum ve yapılandırma tamamlandıktan sonra uygulamayı başlatmak için terminale şu komutu girin:

```bash
make run
```

Alternatif başlatma komutu:
```bash
streamlit run app.py
```

Uygulama başarıyla başladığında, tarayıcınızda otomatik olarak açılacaktır. Açılmazsa terminalde belirtilen yerel adresi (genellikle `http://localhost:8501`) tarayıcınıza kopyalayabilirsiniz.

---

## Dosya Yapısı ve Teknik Detaylar

Projenin teknik mimarisi aşağıdaki dosyalardan oluşmaktadır:

*   **src/rag.py**: Ana işlem motorudur. Kullanıcı sorusunu analiz eder, arama stratejisini belirler ve sonuçları işleyerek nihai yanıtı oluşturur.
*   **src/web_search.py**: Arama modülüdür. `duckduckgo-search` kütüphanesini kullanarak `site:mevzuat.gov.tr` filtresi ile arama yapar.
*   **src/config.py**: Sistemin çalışma parametrelerini (model adı, arama limitleri, sistem talimatları) barındırır.
*   **app.py**: Kullanıcı arayüzünü (Streamlit) oluşturan dosyadır.
