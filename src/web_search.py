from ddgs import DDGS

class WebSearcher:
    """
    İnternet araması yapan yardımcı sınıf.
    Varsayılan olarak 'mevzuat.gov.tr' üzerinde arama yapar.
    """
    def __init__(self, region="tr-tr"):
        self.region = region

    def search(self, query, site="mevzuat.gov.tr", max_results=5):
        """
        Verilen sorguyu belirtilen sitede arar (Strict Mode).
        """
        if not site:
            print("Uyarı: Site belirtilmedi, arama yapılmadı.")
            return []

        strict_query = f"{query} site:{site}"
        print(f"Bilgi: İnternette aranıyor: '{strict_query}'")
        
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(strict_query, region=self.region, max_results=max_results))
            
            # Ekstra güvenlik: Sonuçların gerçekten siteyi içerdiğinden emin ol
            filtered_results = [res for res in results if site in res.get('href', '')]
            return filtered_results
            
        except Exception as e:
            print(f"Hata: İnternet araması başarısız: {e}")
            return []
