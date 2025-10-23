import streamlit as st
import requests
import base64
import io
import uuid
from PIL import Image

# FastAPI backend URL
BACKEND_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(page_title="AI Assistant", layout="centered", initial_sidebar_state="collapsed")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "create_image_mode" not in st.session_state:
    st.session_state.create_image_mode = False
if "show_uploader" not in st.session_state:
    st.session_state.show_uploader = False
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "pending_images" not in st.session_state:
    st.session_state.pending_images = []
if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""

# Enhanced CSS
st.markdown("""
<style>
    .stApp {
        max-width: 750px;
        margin: 0 auto;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    [data-testid="stFileUploader"] {
        padding: 0.5rem 0;
    }
    .stDeployButton {display: none;}
    .stButton button {
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([10, 1])
with col1:
    st.title("AI Assistant")
with col2:
    if st.button("🗑️", help="Clear chat"):
        st.session_state.messages = []
        st.session_state.create_image_mode = False
        st.session_state.show_uploader = False
        st.session_state.pending_images = []
        st.session_state.current_prompt = ""
        try:
            requests.delete(f"{BACKEND_URL}/api/v1/chat/clear")
        except:
            pass
        st.rerun()

st.markdown("---")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "images" in message and message["images"]:
            cols = st.columns(min(len(message["images"]), 3))
            for idx, img in enumerate(message["images"]):
                with cols[idx % 3]:
                    st.image(img, use_container_width=True)
        
        if "content" in message and message["content"]:
            st.markdown(message["content"])
        
        if message["role"] == "assistant" and "download_image" in message:
            buf = io.BytesIO()
            message["download_image"].save(buf, format="PNG")
            st.download_button(
                label="⬇️ Download Image",
                data=buf.getvalue(),
                file_name=f"generated_{uuid.uuid4().hex[:8]}.png",
                mime="image/png",
                key=f"dl_{message.get('id')}"
            )

st.markdown("---")

# Input controls
button_col1, button_col2, button_col3 = st.columns([1, 1, 10])

with button_col1:
    if st.button("📎", help="Attach files", use_container_width=True):
        st.session_state.show_uploader = not st.session_state.show_uploader
        st.rerun()

with button_col2:
    if st.session_state.create_image_mode:
        if st.button("💬", help="Chat mode", use_container_width=True):
            st.session_state.create_image_mode = False
            st.rerun()
    else:
        if st.button("🎨", help="Create Image", use_container_width=True):
            st.session_state.create_image_mode = True
            st.rerun()

# Mode indicator
if st.session_state.create_image_mode:
    st.info("🎨 **Create Image Mode** - Upload image to modify, or describe what to create")

# File uploader
if st.session_state.show_uploader or st.session_state.create_image_mode:
    uploaded_files = st.file_uploader(
        "Upload images",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key=f"uploader_{st.session_state.uploader_key}"
    )
    
    # Store uploaded images in session state (don't process until send is clicked)
    if uploaded_files:
        st.session_state.pending_images = [Image.open(f) for f in uploaded_files]

# Show image preview
if st.session_state.pending_images:
    st.markdown("**Attached:**")
    cols = st.columns(min(len(st.session_state.pending_images), 4))
    for idx, img in enumerate(st.session_state.pending_images):
        with cols[idx % 4]:
            st.image(img, use_container_width=True)

# Input area with text input and send button
input_col, send_col = st.columns([9, 1])

with input_col:
    prompt = st.text_input(
        "Message",
        placeholder="Describe changes (optional)..." if st.session_state.create_image_mode else "Message AI Assistant...",
        label_visibility="collapsed",
        key="prompt_input"
    )

with send_col:
    send_clicked = st.button("➤", help="Send", use_container_width=True, type="primary")

# ONLY process when send button is explicitly clicked
if send_clicked:
    has_image = len(st.session_state.pending_images) > 0
    has_prompt = bool(prompt and prompt.strip())
    
    # Validate input
    if not has_image and not has_prompt:
        st.warning("⚠️ Please provide a message or upload an image")
        st.stop()
    
    # Add user message
    user_msg = {
        "role": "user",
        "content": prompt if has_prompt else "[Image uploaded]",
        "id": uuid.uuid4().hex
    }
    
    if has_image:
        user_msg["images"] = st.session_state.pending_images.copy()
    
    st.session_state.messages.append(user_msg)
    
    # Show user message
    with st.chat_message("user"):
        if has_image:
            cols = st.columns(min(len(st.session_state.pending_images), 3))
            for idx, img in enumerate(st.session_state.pending_images):
                with cols[idx % 3]:
                    st.image(img, use_container_width=True)
        if has_prompt:
            st.markdown(prompt)
        else:
            st.markdown("*[Image for processing]*")
    
    # Process based on mode
    with st.chat_message("assistant"):
        try:
            # CREATE IMAGE MODE
            if st.session_state.create_image_mode:
                if has_image and not has_prompt:
                    # Image only - auto enhance
                    status = st.empty()
                    status.markdown("🎨 **Enhancing image...**")
                    
                    image = st.session_state.pending_images[0]
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    image_base64 = base64.b64encode(buf.getvalue()).decode()
                    
                    response = requests.post(
                        f"{BACKEND_URL}/api/v1/tti/generate",
                        json={
                            "prompt": "enhance and improve this image",
                            "image_data": image_base64,
                            "mime_type": "image/png"
                        }
                    )
                    
                    status.empty()
                    
                    if response.status_code == 200:
                        data = response.json()
                        image_data = base64.b64decode(data["image_data"])
                        generated_image = Image.open(io.BytesIO(image_data))
                        
                        st.image(generated_image, use_container_width=True)
                        
                        buf = io.BytesIO()
                        generated_image.save(buf, format="PNG")
                        st.download_button(
                            label="⬇️ Download",
                            data=buf.getvalue(),
                            file_name=f"enhanced_{uuid.uuid4().hex[:8]}.png",
                            mime="image/png"
                        )
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "images": [generated_image],
                            "download_image": generated_image,
                            "content": "*Auto-enhanced*",
                            "id": uuid.uuid4().hex
                        })
                    else:
                        st.error("Failed to enhance image")
                        
                elif has_image and has_prompt:
                    # Image + prompt - modify
                    status = st.empty()
                    status.markdown("🎨 **Modifying image...**")
                    
                    image = st.session_state.pending_images[0]
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    image_base64 = base64.b64encode(buf.getvalue()).decode()
                    
                    response = requests.post(
                        f"{BACKEND_URL}/api/v1/tti/generate",
                        json={
                            "prompt": prompt,
                            "image_data": image_base64,
                            "mime_type": "image/png"
                        }
                    )
                    
                    status.empty()
                    
                    if response.status_code == 200:
                        data = response.json()
                        image_data = base64.b64decode(data["image_data"])
                        generated_image = Image.open(io.BytesIO(image_data))
                        
                        st.image(generated_image, use_container_width=True)
                        
                        buf = io.BytesIO()
                        generated_image.save(buf, format="PNG")
                        st.download_button(
                            label="⬇️ Download",
                            data=buf.getvalue(),
                            file_name=f"modified_{uuid.uuid4().hex[:8]}.png",
                            mime="image/png"
                        )
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "images": [generated_image],
                            "download_image": generated_image,
                            "id": uuid.uuid4().hex
                        })
                    else:
                        st.error("Failed to modify image")
                        
                elif not has_image and has_prompt:
                    # Prompt only - generate new
                    status = st.empty()
                    status.markdown("🎨 **Generating image...**")
                    
                    response = requests.post(
                        f"{BACKEND_URL}/api/v1/tti/generate",
                        json={"prompt": prompt}
                    )
                    
                    status.empty()
                    
                    if response.status_code == 200:
                        data = response.json()
                        image_data = base64.b64decode(data["image_data"])
                        generated_image = Image.open(io.BytesIO(image_data))
                        
                        st.image(generated_image, use_container_width=True)
                        
                        buf = io.BytesIO()
                        generated_image.save(buf, format="PNG")
                        st.download_button(
                            label="⬇️ Download",
                            data=buf.getvalue(),
                            file_name=f"generated_{uuid.uuid4().hex[:8]}.png",
                            mime="image/png"
                        )
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "images": [generated_image],
                            "download_image": generated_image,
                            "id": uuid.uuid4().hex
                        })
                    else:
                        st.error("Failed to generate image")
            
            # CHAT MODE - IMAGE ANALYSIS
            elif has_image:
                status = st.empty()
                
                if has_prompt:
                    status.markdown("🔍 **Analyzing with your question...**")
                else:
                    status.markdown("🔍 **Analyzing image...**")
                
                image = st.session_state.pending_images[0]
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                image_base64 = base64.b64encode(buf.getvalue()).decode()
                
                analyze_request = {
                    "image_data": image_base64,
                    "mime_type": "image/png"
                }
                
                if has_prompt:
                    analyze_request["prompt"] = prompt
                
                response = requests.post(
                    f"{BACKEND_URL}/api/v1/itt/analyze",
                    json=analyze_request
                )
                
                status.empty()
                
                if response.status_code == 200:
                    data = response.json()
                    description = data["description"]
                    st.markdown(description)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": description,
                        "id": uuid.uuid4().hex
                    })
                else:
                    st.error("Failed to analyze image")
            
            # CHAT MODE - TEXT ONLY
            elif has_prompt:
                status = st.empty()
                status.markdown("💭 **Thinking...**")
                
                response = requests.post(
                    f"{BACKEND_URL}/api/v1/chat/",
                    json={"message": prompt}
                )
                
                status.empty()
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data["response"]
                    st.markdown(ai_response)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": ai_response,
                        "id": uuid.uuid4().hex
                    })
                else:
                    st.error("Failed to get response")
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Clear after processing
    st.session_state.pending_images = []
    st.session_state.show_uploader = False
    st.session_state.uploader_key += 1
    st.rerun()

# Footer
st.markdown("<p style='text-align: center; color: #666; font-size: 0.8em; margin-top: 2rem;'>Powered by Gemini 2.5 Flash</p>", unsafe_allow_html=True)