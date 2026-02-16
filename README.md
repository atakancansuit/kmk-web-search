# ⚖️ Legal-RAG v2

Bu proje, **Kat Mülkiyeti Kanunu** üzerine uzmanlaşmış yapay zeka destekli bir hukuk asistanıdır.
RAG (Retrieval-Augmented Generation) mimarisini kullanarak kullanıcının sorularını resmi kanun metinlerinden cevaplar.

## 🚀 Proje Mimarisi (v2)

Bu versiyon, önceki modele göre daha yalın ve güçlüdür:
1.  **Framework-Free**: LangChain karmaşası olmadan, saf Python (Native SDKs) ile yazıldı.
2.  **Cloud Native**: Vektör veritabanı **ChromaDB Cloud**, Embedding ise **OpenAI** tarafından sağlanır.
3.  **Hafif (Lightweight)**: Arkadaşlarınızın bilgisayarını yormaz, ağır modeller indirmez.
4.  **Model**: OpenAI `gpt-4o-mini` modeli ile hızlı ve doğru cevaplar üretir.

---

## 🛠️ Kurulum (Nasıl Çalıştırılır?)

Bu projeyi bilgisayarınıza indirdiğinizde çalıştırmak için şu adımları izleyin:

### 1. Kurulumu Yapın
Gerekli kütüphaneleri yüklemek için:
```bash
make setup
```

### 2. API Anahtarlarını Girin
`.env.example` dosyasının adını `.env` olarak değiştirin ve içeriğini doldurun:
*   `OPENAI_API_KEY`: Model için gerekli.
*   `CHROMA_API_KEY`: Veritabanı için gerekli.

### 3. Veri Yükleme (Ingestion)
PDF dosyasını okuyup veritabanına yüklemek için (Bu işlemi sadece bir kez yapmanız yeterli):
```bash
make ingest
```

### 4. Uygulamayı Başlatın
Arayüzü açmak için:
```bash
make run
```

---

## 📂 Dosya Yapısı (Ne Nerede?)

*   `src/config.py`: Tüm ayarların (Model isimleri, API keyler) durduğu kontrol merkezi.
*   `src/utils.py`: Veritabanı bağlantısı gibi ortak işleri yapan "alet çantası".
*   `src/ingestion.py`: "Fabrika". PDF'i okur, parçalar ve veritabanına yükler.
*   `src/rag.py`: "Motor". Soruyu alır, cevabı üretir.
*   `app.py`: "Vitrin". Kullanıcının gördüğü Streamlit ekranı.

## 💡 İpucu
Uygulama içinde sol menüden (Sidebar) "Local" veya "Cloud" veri kaynağı arasında geçiş yapabilirsiniz. "Local" seçeneği daha ekonomiktir.
