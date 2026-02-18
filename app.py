import streamlit as st
import time
from src.rag import LegalRAG
from src import config

# Sayfa Ayarları
st.set_page_config(page_title="Legal-RAG v2", page_icon="⚖️", layout="centered")
st.title("⚖️ Kat Mülkiyeti Kanunu Asistanı")

# Sidebar Ayarları
with st.sidebar:
    st.header("Bilgi")
    st.info("Bu sistem mevzuat.gov.tr üzerinden apartman yönetimi hakkındaki sorularınıza yardım eder.")

# --- 1. SİSTEM BAŞLATMA ---
if "rag_system" not in st.session_state:
    with st.spinner("Sistem hazırlanıyor..."):
        try:
            # RAG motorunu başlat
            st.session_state.rag_system = LegalRAG()
            
            st.success("Sistem Hazır!")
            time.sleep(0.5)
            st.rerun() # Arayüzü yenile
        except Exception as e:
            st.error(f"Sistem başlatılamadı: {e}")
            st.stop()


# --- 3. Sohbet ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Sorunuzu bekliyorum."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Sorunuzu buraya yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("İnceleniyor..."):
            try:
                # SADECE WEB ARAMASI
                cevap, kaynaklar, _ = st.session_state.rag_system.generate_answer(prompt)
                
                st.markdown(cevap)
                with st.expander("📚 Kaynaklar"):
                    for i, doc in enumerate(kaynaklar):
                        st.markdown(f"**Kaynak {i+1}:**\n> {doc[:200]}...")
                st.session_state.messages.append({"role": "assistant", "content": cevap})
            except Exception as e:
                st.error(f"Hata: {e}")
