import streamlit as st
import requests
import os

st.set_page_config(page_title="Project Dragon 🐉", page_icon="🐉")

st.title("🐉 Project Dragon")
st.markdown("### Chinese AI Coding Agent - Open Source")
st.markdown("مدعوم بنموذج **Qwen 2.5 Coder** عبر Groq")
st.markdown("---")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("⚠️ التنين نائم! الرجاء إضافة مفتاح GROQ_API_KEY في Settings > Secrets")
    st.stop()

task = st.text_area("✍️ اكتب المهمة البرمجية:", height=120)

if st.button("🚀 نفّذ المهمة"):
    if task:
        with st.spinner("🐉 التنين يفكر..."):
            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                    json={
                        "model": "qwen-2.5-coder-32b",
                        "messages": [
                            {"role": "system", "content": "أنت مبرمج خبير. اكتب كود Python نظيف مع شرح بالعربية."},
                            {"role": "user", "content": task}
                        ]
                    }
                )
                result = response.json()
                st.code(result["choices"][0]["message"]["content"], language="python")
            except Exception as e:
                st.error(f"خطأ: {e}")

