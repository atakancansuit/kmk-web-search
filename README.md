# KMK Hukuk Asistanı

## Proje Hakkında
KMK Hukuk Asistanı, apartman ve site yönetimi, Kat Mülkiyeti Kanunu ve ilgili mevzuat konularında kullanıcıların sorularını yanıtlamak üzere geliştirilmiş bir yapay zeka uygulamasıdır. Sistem, OpenAI GPT-4o modelini kullanarak kullanıcı sorularını analiz eder ve **Mevzuat.gov.tr**, **Resmi Gazete**, **Türkiye Barolar Birliği** gibi resmi ve güvenilir kaynaklar üzerinde gerçek zamanlı arama yaparak yanıt üretir.

Bu proje, yerel bir veritabanı yerine internet üzerindeki güncel hukuki kaynakları tarayarak çalıştığı için her zaman en güncel mevzuat bilgilerine erişim sağlar.

## Temel Özellikler
- **Resmi Kaynak Tarama:** Yanıtlar yalnızca doğrulanmış hukuk sitelerinden (mevzuat.gov.tr, resmigazete.gov.tr vb.) elde edilen verilerle oluşturulur.
- **Çoklu Sorgu Stratejisi:** Sorunun hem yasal mevzuat hem de yargı içtihatları (emsal kararlar) yönünü kapsayacak şekilde çoklu arama yapar.
- **Kaynak Gösterimi:** Üretilen yanıtta kullanılan kaynaklar ve ilgili bağlantılar şeffaf bir şekilde listelenir.
- **Kullanıcı Dostu Arayüz:** Streamlit tabanlı basit ve anlaşılır bir web arayüzü sunar.

## Kurulum

Projeyi çalıştırmak için aşağıdaki adımları izleyebilirsiniz.

### 1. Gereksinimler
Sistemin çalışması için Python 3.8 veya üzeri bir sürümün yüklü olması gerekmektedir. Proje dizininde gerekli kütüphaneleri yüklemek için terminalde şu komutu çalıştırın:

```bash
pip install -r requirements.txt
```

### 2. Ortam Değişkenleri
Projenin çalışabilmesi için bir OpenAI API anahtarına ihtiyacınız vardır. Proje ana dizininde `.env` adında bir dosya oluşturun ve API anahtarınızı aşağıdaki formatta ekleyin:

```env
OPENAI_API_KEY=sk-proj-...
```

## Kullanım

Kurulum tamamlandıktan sonra uygulamayı başlatmak için terminalde aşağıdaki komutu kullanın:

```bash
streamlit run app.py
```

Komut çalıştırıldığında, uygulamanız varsayılan tarayıcınızda (genellikle http://localhost:8501 adresinde) otomatik olarak açılacaktır.

## Yapılandırma

Uygulamanın kullandığı yapay zeka modeli ve yaratıcılık seviyesi gibi parametreleri `src/config.py` dosyası üzerinden değiştirebilirsiniz.

**Dosya Yolu:** `src/config.py`

- **Model Değişikliği:**
  `LLM_MODEL` değişkenini değiştirerek farklı bir model kullanabilirsiniz (Örn: "gpt-3.5-turbo").
  ```python
  LLM_MODEL = "gpt-4o"
  ```

- **Yaratıcılık Ayarı (Temperature):**
  `TEMPERATURE` değişkeni, modelin üreteceği yanıtların çeşitliliğini belirler. Hukuki konularda tutarlılık için bu değerin **0** olması önerilir.
  ```python
  TEMPERATURE = 0
  ```

- **Arama Siteleri:**
  `SEARCH_SITES` listesinden arama yapılacak kaynak siteleri ekleyip çıkarabilirsiniz.
  ```python
  SEARCH_SITES = ["mevzuat.gov.tr", "resmigazete.gov.tr", ...]
  ```
