import os
import streamlit as st
from title_engine import generate_titles

st.set_page_config(page_title="TitleSpark AI", page_icon="🎬", layout="centered")

st.markdown("""
<style>
.block-container {max-width: 900px; padding-top: 2.2rem; padding-bottom: 3rem;}
.hero {padding: 1.7rem; border-radius: 20px; background: linear-gradient(135deg,#171c35,#313e75); color:white; margin-bottom:1rem;}
.hero h1 {font-size:2.3rem; margin-bottom:.35rem;}
.hero p {color:#e0e6ff; margin-bottom:0;}
div.stButton > button {border-radius: 10px; min-height: 2.7rem;}
</style>
""", unsafe_allow_html=True)

if "generated_titles" not in st.session_state:
    st.session_state.generated_titles = []
if "generation_mode" not in st.session_state:
    st.session_state.generation_mode = "template"

def get_secret(name):
    value = os.getenv(name, "").strip()
    if value:
        return value
    try:
        return str(st.secrets.get(name, "")).strip()
    except Exception:
        return ""

api_key = get_secret("OPENAI_API_KEY")

st.markdown("""
<div class="hero">
  <h1>🎬 TitleSpark AI</h1>
  <p>Catchy YouTube title ideas — seconds mein.</p>
</div>
""", unsafe_allow_html=True)

st.write("Apni video ka topic enter karo aur apne channel ke liye title ideas banao.")
if not api_key:
    st.info("Demo mode active hai. Real AI enable karne ke liye deployment secrets mein OPENAI_API_KEY add karo.")

with st.form("generator"):
    topic = st.text_input("Video ka topic", placeholder="Misal: Best AI tools for students", max_chars=300)
    left, right = st.columns(2)
    with left:
        style = st.selectbox("Title style", ["Curiosity", "Educational", "List", "Challenge", "SEO-friendly", "Funny"])
    with right:
        language = st.selectbox("Language", ["English", "Roman Urdu", "Urdu"])
    count = st.slider("Kitne titles chahiye?", 5, 15, 10)
    submitted = st.form_submit_button("✨ Generate titles", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("Pehle video ka topic likho.")
    else:
        with st.spinner("Title ideas ban rahe hain..."):
            try:
                titles, mode = generate_titles(topic.strip(), style, language, count, api_key)
                st.session_state.generated_titles = titles
                st.session_state.generation_mode = mode
            except Exception as exc:
                st.error(str(exc))

if st.session_state.generated_titles:
    st.subheader("Tumhare title ideas")
    if st.session_state.generation_mode == "template":
        st.caption("Demo templates use ho rahe hain; real AI generation ke liye API key configure karo.")
    else:
        st.success("AI title ideas ready hain. Publish karne se pehle accuracy check kar lena.")
    for index, title in enumerate(st.session_state.generated_titles, 1):
        st.markdown(f"**{index}. {title}**")
    st.text_area("Copy all titles", "\n".join(st.session_state.generated_titles), height=230)
    st.download_button(
        "⬇️ Download titles (.txt)",
        data="\n".join(st.session_state.generated_titles),
        file_name="youtube_title_ideas.txt",
        mime="text/plain",
        use_container_width=True,
    )

with st.expander("Title tips"):
    st.markdown("""
    - Main keyword naturally include karo.
    - Title ko video ke actual content ke mutabiq rakho.
    - Misleading promises se bacho.
    - Publish se pehle title ko apne audience ke liye review karo.
    """)

st.divider()
st.caption("TitleSpark AI · MVP starter. This version does not yet include user accounts, saved history, subscriptions, or payments.")
