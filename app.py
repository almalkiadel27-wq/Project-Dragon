import streamlit as st
import requests
import os

st.set_page_config(page_title="Project Dragon 🐉", page_icon="🐉")

st.title("🐉 Project Dragon")
st.markdown("### Chinese AI Coding Agent - Open Source")
st.markdown("---")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("️ التنين نائم! الرجاء إضافة مفتاح GROQ_API_KEY في Settings > Secrets")
    st.stop()

# عرض حالة المفتاح (للتشخيص فقط - احذفه لاحقاً)
st.info(f" المفتاح يبدأ بـ: `{GROQ_API_KEY[:10]}...`")

task = st.text_area("✍️ اكتب المهمة البرمجية:", height=120)

if st.button("🚀 نفّذ المهمة"):
    if task:
        with st.spinner("🐉 التنين يفكر..."):
            try:
                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": "أنت مبرمج خبير."},
                        {"role": "user", "content": task}
                    ]
                }
                
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                st.markdown(f"**حالة الاستجابة:** {response.status_code}")
                
                if response.status_code != 200:
                    st.error("❌ الـ API أرجع خطأ:")
                    st.code(response.text, language="json")
                    st.stop()
                
                result = response.json()
                st.json(result)  # عرض الـ response كامل
                
            except Exception as e:
                st.error(f"خطأ: {e}")
