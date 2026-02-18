from openai import OpenAI
import json
from src import config
from src.web_search import WebSearcher

class LegalRAG:
    """
    RAG Motoru (OpenAI + ChromaDB Cloud + Web Search)
    """
    def __init__(self, model_name=None):
        """
        Sistemi başlatır.
        """
        self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
        
        # Web Arama Modülü
        self.web_searcher = WebSearcher()
        
        # Model seçimi (varsayılan: config.LLM_MODEL)
        self.model_name = model_name if model_name else config.LLM_MODEL
        print(f"Bilgi: LegalRAG '{self.model_name}' modeli ile başlatıldı.")

    
    def analyze_query(self, query):
        """
        Kullanıcı sorgusunu analiz eder ve aranacak anahtar kelimeleri belirler.
        """
        try:
            try:
                response = self.openai_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": config.QUERY_ANALYSIS_PROMPT},
                        {"role": "user", "content": query}
                    ],
                    temperature=0,
                    response_format={"type": "json_object"}
                )
            except Exception as e:
                if "response_format" in str(e):
                    print(f"Uyarı: '{self.model_name}' JSON modunu desteklemiyor. Normal modda deneniyor...")
                    response = self.openai_client.chat.completions.create(
                        model=self.model_name,
                        messages=[
                            {"role": "system", "content": config.QUERY_ANALYSIS_PROMPT},
                            {"role": "user", "content": query}
                        ],
                        temperature=0
                    )
                else:
                    raise e
            analysis = json.loads(response.choices[0].message.content)
            print(f"Bilgi: Sorgu Analizi: {analysis}")
            return analysis
        except Exception as e:
            print(f"HATA: Sorgu analizi yapılamadı: {e}")
            return {"search_queries": [query], "intent": "general", "original_topic": query}

    def generate_answer(self, query):
        """
        YENİ AKIŞ (WEB ONLY):
        1. Analyze: Soruyu anla, arama terimlerini çıkar.
        2. Web Search: Mevzuat.gov.tr'de ara.
        3. Synthesize & Answer: Cevap ver.
        """
        
        # 2. WEB ARAMASI YAP (Çoklu Sorgu Desteği)
        web_context = "Web aramasında ilgili bir sonuç bulunamadı."
        web_sources = []
        all_results = []
        seen_links = set()

        try:
            analysis = self.analyze_query(query)
            # Analizden gelen sorguları al, yoksa orijinal sorguyu kullan
            search_queries = analysis.get("search_queries", [query])
        except Exception as e:
            print(f"Uyarı: Analiz hatası, orijinal sorgu kullanılıyor. {e}")
            search_queries = [query]

        # En fazla 2 farklı sorguyu çalıştır (Çeşitlilik için)
        for i, search_query in enumerate(search_queries[:2]):
            print(f"Bilgi: İnternette aranıyor ({i+1}/{len(search_queries[:2])})... ('{search_query}') Siteler: {config.SEARCH_SITES}")
            
            # Her sorgu için limit biraz düşürülebilir veya toplam limit korunabilir
            results = self.web_searcher.search(search_query, sites=config.SEARCH_SITES, max_results=config.WEB_SEARCH_LIMIT)
            
            for res in results:
                if res.get('href') not in seen_links:
                    seen_links.add(res.get('href'))
                    all_results.append(res)
        
        if all_results:
            web_context = "" # Varsayılan mesajı temizle
            # Toplam sonuç sayısını sınırla (Örn: 20)
            for res in all_results[:20]:
                web_context += f"BAŞLIK: {res.get('title')}\nİÇERİK: {res.get('body')}\nLİNK: {res.get('href')}\n---\n"
                web_sources.append(f"[WEB] {res.get('title')} ({res.get('href')})")
        
        # RAGAS için tam metin içeriği (bağlam)
        context_texts = [res.get('body', '') for res in all_results] if all_results else []

        # 4. CEVAP ÜRET
        user_content = f"""
        KULLANICI SORUSU: {query}
        
        ---
        🔍 İNTERNET ARAMA SONUÇLARI (Mevzuat ve Hukuk Kaynakları):
        {web_context}
        
        ---
        Lütfen yukarıdaki bilgileri kullanarak soruyu cevapla.
        """

        messages = [
            {"role": "system", "content": config.SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ]

        response = self.openai_client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=config.TEMPERATURE
        )
        
        answer = response.choices[0].message.content
        
        return answer, web_sources, context_texts

