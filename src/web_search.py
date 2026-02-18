from ddgs import DDGS

class WebSearcher:
    """
    İnternet araması yapan yardımcı sınıf.
    Varsayılan olarak 'mevzuat.gov.tr' üzerinde arama yapar.
    """
    def __init__(self, region="tr-tr"):
        self.region = region

    def search(self, query, sites=None, max_results=5):
        """
        Verilen sorguyu belirtilen sitelerde arar (Strict Mode).
        sites: List of strings (e.g. ["mevzuat.gov.tr", "resmigazete.gov.tr"])
        """
        if not sites:
            sites = ["mevzuat.gov.tr"] # Varsayılan

        # Site sorgusunu oluştur: (site:a.com OR site:b.com)
        site_query = " OR ".join([f"site:{s}" for s in sites])
        strict_query = f"{query} ({site_query})"
        
        print(f"Bilgi: İnternette aranıyor: '{strict_query}'")
        
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(strict_query, region=self.region, max_results=max_results))
            
            # Ekstra güvenlik: Sonuçların gerçekten siteleri içerdiğinden emin ol
            # Bu kontrol biraz gevşetilmeli çünkü href alt domain veya http/https farklı olabilir
            filtered_results = []
            for res in results:
                href = res.get('href', '')
                if any(site in href for site in sites):
                    filtered_results.append(res)
            
            return filtered_results
            
        except Exception as e:
            print(f"Hata: İnternet araması başarısız: {e}")
            return []
