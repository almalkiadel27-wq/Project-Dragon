import streamlit as st
import requests
import os

st.set_page_config(page_title="Project Dragon 🐉", page_icon="🐉")
st.title("🐉 Project Dragon")
st.markdown("### Chinese AI Coding Agent - Open Source")
st.markdown("---")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("️ التنين نائم! أضف مفتاح GROQ_API_KEY في Settings > Secrets")
    st.stop()

# قائمة النماذج البديلة (من الأقوى إلى الأخف)
MODELS = [
    "llama-3.1-70b-versatile",  # بديل قوي جداً
    "llama-3.1-8b-instant",     # سريع جداً
    "gemma2-9b-it"              # خفيف وفعال
]

task = st.text_area("✍️ اكتب المهمة البرمجية:", height=120)

if st.button("🚀 نفّذ المهمة"):
    if task:
        with st.spinner(" التنين يبحث عن أفضل نموذج ويكتب الكود..."):
            success = False
            for model in MODELS:
                try:
                    response = requests.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                        json={
                            "model": model,
                            "messages": [
                                {"role": "system", "content": "أنت مبرمج خبير. اكتب كود Python نظيف مع شرح بالعربية."},
                                {"role": "user", "content": task}
                            ]
                        },
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        code_output = result["choices"][0]["message"]["content"]
                        st.success(f"✅ تم التنفيذ بنجاح باستخدام نموذج: `{model}`")
                        st.code(code_output, language="python")
                        success = True
                        break
                    else:
                        st.warning(f"⚠️ نموذج `{model}` غير متاح، جاري المحاولة بالتالي...")
                        
                except Exception:
                    continue
            
            if not success:
                st.error("❌ لم يتمكن التنين من العثور على نموذج متاح حالياً. تأكد من صحة المفتاح أو حاول لاحقاً.")
