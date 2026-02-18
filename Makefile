PYTHON = python3
PIP = pip

.PHONY: run setup clean help

help:
	@echo "🛠️  Komutlar (KMK Web Search):"
	@echo "  make setup          : Gerekli kütüphaneleri yükle"
	@echo "  make eval           : Modeli yeniden değerlendir (src/evaluation.py)"
	@echo "  make run            : Uygulamayı başlat (Streamlit)"
	@echo "  make clean          : Geçici dosyaları temizle"

setup:
	$(PIP) install -r requirements.txt

eval:
	$(PYTHON) src/evaluation.py

run:
	streamlit run app.py

clean:
	rm -rf __pycache__ src/__pycache__
	@echo "🧹 Temizlik tamamlandı."
