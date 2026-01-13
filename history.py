import streamlit as st

def show_history():
    st.markdown("## Session History")
    history = st.session_state.get("history", [])
    if not history:
        st.write("No history yet.")
        return

    for idx, entry in enumerate(history, 1):
        with st.expander(f"{idx}. {entry['question'][:50]}..."):
            st.markdown(f"**Your Answer:**\n{entry['answer']}")
            st.markdown(f"**Feedback:**\n{entry['feedback']}")
    if st.button("Clear History"):
        st.session_state["history"] = []
        st.success("Session history cleared.")

