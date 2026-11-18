import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="Policy RAG Assistant", page_icon="📄")
st.title("📄 Company Policy RAG Assistant")
st.caption("Ask questions strictly grounded in your company policy PDFs.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("View Sources"):
                for s in msg["sources"]:
                    st.write(f"- **{s['source']}** (Page {s['page']}, dist={s['distance']})")

if prompt := st.chat_input("Ask a question about company policies..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching policy documents..."):
            try:
                response = requests.post(API_URL, json={"question": prompt}, timeout=30) 

                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data["sources"]

                    st.markdown(answer)
                    with st.expander("View Sources"):
                        for s in sources:
                            st.write(f"- **{s['source']}** (Page {s['page']}, dist={s['distance']})")

                    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
                else:
                    st.error(f"API Error ({response.status_code}): {response.text}")
            except Exception as e:
                st.error(f"Could not connect to backend: {e}")