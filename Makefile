PYTHON = python3
PIP = pip

.PHONY: run setup ingest ingest-openai clean help

help:
	@echo "🛠️  Komutlar (Legal-RAG v2):"
	@echo "  make setup          : Gerekli kütüphaneleri yükle"
	@echo "  make run            : Uygulamayı başlat (Streamlit)"
	@echo "  make ingest         : 🏠 Local Embedding ile veritabanını oluştur (Ücretsiz)"
	@echo "  make ingest-openai  : 🌍 OpenAI Embedding ile veritabanını oluştur (Ücretli, Cloud)"
	@echo "  make clean          : Yerel veritabanı dosyalarını temizle (chroma_db)"

setup:
	$(PIP) install -r requirements.txt

run:
	streamlit run app.py

ingest:
	@echo "🌱 Veri Yükleme (Ingestion) Başlatılıyor..."
	$(PYTHON) -c "from src.ingestion import ingest_data; ingest_data(force_recreate=True)"


clean:
	rm -rf __pycache__ src/__pycache__
	@echo "🧹 Temizlik tamamlandı."
