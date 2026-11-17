

import streamlit as st
from chatbot import get_response, get_pdf_response
from rag import process_pdf, ask_pdf_question


# Page configuration
st.set_page_config(
    page_title="Buddy AI",
    page_icon="🤖",
    layout="wide"
)



# Custom CSS
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F8F9FC;
    color: #202938;
}

/* Main content width */
.block-container {
    padding-top: 2rem;
    max-width: 1000px;
}

/* Main heading */
.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: 750;
    color: #202938;
    letter-spacing: -1px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #718096;
    font-size: 16px;
    margin-bottom: 32px;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    border: 1px solid #E8EAF2;
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 14px;
    background-color: #FFFFFF;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E8EAF2;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    border: 1px solid #E0E3ED;
    background-color: #FFFFFF;
    color: #273449;
    transition: 0.2s ease;
}

.stButton > button:hover {
    border-color: #8B7CF6;
    color: #6D5CE7;
}

/* Chat input */
[data-testid="stChatInput"] {
    border-radius: 14px;
}

/* Footer */
.footer {
    text-align: center;
    color: #94A3B8;
    font-size: 13px;
    margin-top: 35px;
}

</style>
""", unsafe_allow_html=True)

# Initialize chat storage
if "chats" not in st.session_state:
    st.session_state.chats = [
        {
            "id": 1,
            "title": "New Chat",
            "messages": []
        }
    ]
    st.session_state.active_chat_id = 1


# Get active chat
active_chat = next(
    chat for chat in st.session_state.chats
    if chat["id"] == st.session_state.active_chat_id
)



# Sidebar
with st.sidebar:

    st.title("🤖 Buddy AI")
    st.caption("Your Smart AI Companion")

    st.divider()

    if st.button("➕ New Chat", use_container_width=True):

        new_id = max(
            chat["id"] for chat in st.session_state.chats
        ) + 1

        st.session_state.chats.append({
            "id": new_id,
            "title": "New Chat",
            "messages": []
        })

        st.session_state.active_chat_id = new_id
        st.rerun()

    st.divider()

    st.subheader("💬 Recent Conversations")

    for chat in reversed(st.session_state.chats):

        if st.button(
            "💬 " + chat["title"],
            key=f"chat_{chat['id']}",
            use_container_width=True
        ):

            st.session_state.active_chat_id = chat["id"]
            st.rerun()

    st.divider()

    st.subheader("📄 Document Assistant")

    uploaded_pdf = st.file_uploader(
        "Upload your PDF",
        type=["pdf"]
    )

    if uploaded_pdf is not None:

        if st.button("Process PDF", use_container_width=True):

            with st.spinner("Processing your PDF..."):

                index, chunks, message = process_pdf(uploaded_pdf)

                if index is not None:

                    st.session_state.pdf_index = index
                    st.session_state.pdf_chunks = chunks
                    st.session_state.pdf_name = uploaded_pdf.name

                    st.success(message)

                else:
                    st.error(message)

    st.divider()

    st.caption("Powered by Gemini + Groq")
    st.caption("Made with Python and Streamlit")


# Main heading
st.markdown(
    '<div class="main-title">🤖 Buddy AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask anything. Learn anything. Explore with AI.</div>',
    unsafe_allow_html=True
)


# Welcome message for an empty chat

# Welcome message for an empty chat
if not active_chat["messages"]:

    st.markdown(
        '<div class="main-title">👋 Welcome to Buddy AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Your Smart AI Companion — Ask, Learn and Explore.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("### What can I help you with today?")

    col1, col2 = st.columns(2)

    with col1:
        st.info("💡 **Learn Anything**\n\nUnderstand concepts in simple words.")

        st.info("📄 **Chat with PDFs**\n\nUpload a document and ask questions.")

    with col2:
        st.info("💻 **Coding Assistant**\n\nGenerate code and understand programming.")

        st.info("🔍 **Web Search**\n\nFind information about recent topics.")



# Display previous messages
for message in active_chat["messages"]:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
user_input = st.chat_input("Message your AI assistant...")


if user_input:

    # Store user message
    active_chat["messages"].append({
        "role": "user",
        "content": user_input
    })

    # Set chat title from first question
    if active_chat["title"] == "New Chat":
        active_chat["title"] = user_input[:30]

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("🤔 Thinking..."):

            answer = get_response(active_chat["messages"])

            st.markdown(answer)
# Generate AI response
with st.chat_message("assistant"):

    with st.spinner("🤔 Thinking..."):

        # Check whether a PDF has been processed
        if "pdf_index" in st.session_state:

            # Retrieve relevant information from PDF
            relevant_context = ask_pdf_question(
                user_input,
                st.session_state.pdf_index,
                st.session_state.pdf_chunks
            )

            # Generate answer using Gemini or Groq
            answer = get_pdf_response(
                user_input,
                relevant_context
            )

        else:

            # Normal chatbot response
            answer = get_response(
                active_chat["messages"]
            )

        st.markdown(answer)

# Store assistant response
active_chat["messages"].append({
    "role": "assistant",
    "content": answer
})


    # Store assistant response
active_chat["messages"].append({
    "role": "assistant",
    "content": answer
    })


# Footer
st.markdown(
    '<div class="footer">AI Assistant • Gemini + Groq</div>',
    unsafe_allow_html=True
)
