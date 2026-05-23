import streamlit as st

import requests
import os

# API_URL = os.getenv("API_URL", "http://localhost:8000")

# f"{API_URL}/ask"

st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🏥",
    layout="centered"
)

def clean_text(text):
    return text.replace("□", "-").replace("•", "-")

#st.title("🏥 Medical AI Assistant")

st.markdown('<div class="big-title">🏥 Medical AI Assistant</div>', unsafe_allow_html=True)

# ✅ UI STYLING
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-family: 'Arial';
}

.big-title {
    font-size: 34px;
    font-weight: bold;
    color: #2E86C1;
}

.answer-box {
    background-color: #f4f6f7;
    padding: 20px;
    border-radius: 12px;
    font-size: 18px;
    line-height: 1.6;
    color: #111;
    white-space: pre-wrap;
}

.error-box {
    color: red;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.write(
    "Ask questions from your medical PDFs using local AI"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader(
    "Upload Medical PDF",
    type=["pdf"]
)

if uploaded_file:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf"
        )
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/upload",
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            st.success(data.get("message", "File uploaded"))
        else:
            st.error(f"Upload failed: {response.status_code}")
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")

question = st.text_area(
    "Enter your medical question"
)

if st.button("Ask AI"):

    if question.strip() == "":
        st.warning("Please enter a question")

    else:

        with st.spinner("Generating answer..."):

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json={
                        "question": question
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()

                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": data["answer"]
                    })

                    st.subheader("AI Answer")

                    st.write(clean_text(data["answer"]))

                    # st.subheader("Sources")

                    # st.json(data["sources"])
                else:
                    st.error(f"Server error: {response.status_code}")
            except Exception as e:
                st.error(f"Error getting response: {str(e)}")

st.subheader("Chat History")

for chat in reversed(
    st.session_state.chat_history
):

    st.markdown(
        f"### Question\n{chat['question']}"
    )

    st.markdown(
        f"### Answer\n{chat['answer']}"
    )

    st.divider()