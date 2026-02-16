from openai import OpenAI
import json
from src import config
from src.web_search import WebSearcher

class LegalRAG:
    """
    RAG Motoru (OpenAI + ChromaDB Cloud + Web Search)
    """
    def __init__(self):
        """
        Sistemi başlatır.
        """
        self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
        
        # Web Arama Modülü
        self.web_searcher = WebSearcher()

    
    def analyze_query(self, query):
        """
        Kullanıcı sorgusunu analiz eder ve aranacak anahtar kelimeleri belirler.
        """
        try:
            response = self.openai_client.chat.completions.create(
                model=config.LLM_MODEL,
                messages=[
                    {"role": "system", "content": config.QUERY_ANALYSIS_PROMPT},
                    {"role": "user", "content": query}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
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
        
        # 1. ANALİZ ET
        try:
            analysis = self.analyze_query(query)
            # En iyi sorguyu seç (ilk sorgu)
            search_query = analysis.get("search_queries", [query])[0]
        except Exception as e:
            print(f"Uyarı: Analiz hatası, orijinal sorgu kullanılıyor. {e}")
            search_query = query
        
        # 2. WEB ARAMASI YAP (Mevzuat.gov.tr)
        web_context = "Web aramasında ilgili bir sonuç bulunamadı."
        web_sources = []
        
        print(f"Bilgi: Web araması başlatılıyor... ('{search_query}')")
        
        search_results = self.web_searcher.search(search_query, site="mevzuat.gov.tr", max_results=config.WEB_SEARCH_LIMIT)
        
        if search_results:
            web_context = "" # Varsayılan mesajı temizle
            for res in search_results:
                web_context += f"BAŞLIK: {res.get('title')}\nİÇERİK: {res.get('body')}\nLİNK: {res.get('href')}\n---\n"
                web_sources.append(f"[WEB] {res.get('title')} ({res.get('href')})")
        
        # 4. CEVAP ÜRET
        user_content = f"""
        KULLANICI SORUSU: {query}
        
        ---
        🔍 İNTERNET ARAMA SONUÇLARI (Mevzuat.gov.tr):
        {web_context}
        
        ---
        Lütfen yukarıdaki bilgileri kullanarak soruyu cevapla.
        """

        messages = [
            {"role": "system", "content": config.SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ]

        response = self.openai_client.chat.completions.create(
            model=config.LLM_MODEL,
            messages=messages,
            temperature=config.TEMPERATURE
        )
        
        answer = response.choices[0].message.content
        
        return answer, web_sources

