# Vision-and-Text-Multimodal-Generation-and-Analysis

A powerful AI assistant that combines natural language chat, image analysis, and image generation capabilities in a user-friendly interface. Built with FastAPI backend and Streamlit frontend.



\## 🌟 Features



\### 💬 Chat Mode (Default)



Three ways to interact:



1\. \*\*Regular Chat\*\*

&nbsp;  - Natural conversation with AI

&nbsp;  - Type your message and click send (➤)

&nbsp;  - Perfect for questions, discussions, and general assistance



2\. \*\*Image Analysis (General)\*\*

&nbsp;  - Upload any image for AI analysis

&nbsp;  - Click 📎, choose image, click send

&nbsp;  - AI provides detailed description of the image



3\. \*\*Image Analysis (Specific)\*\*

&nbsp;  - Upload image with specific questions

&nbsp;  - Click 📎, upload image, type your question, click send

&nbsp;  - AI answers questions about the image



\### 🎨 Create Image Mode



Three creation options:



1\. \*\*Text-to-Image Generation\*\*

&nbsp;  - Generate images from text descriptions

&nbsp;  - Type detailed description, click send

&nbsp;  - AI creates image matching your description



2\. \*\*Image Enhancement\*\*

&nbsp;  - Automatically enhance existing images

&nbsp;  - Upload image, click send

&nbsp;  - AI improves image quality and aesthetics



3\. \*\*Custom Image Modification\*\*

&nbsp;  - Modify images with specific instructions

&nbsp;  - Upload image, describe changes, click send

&nbsp;  - AI applies your requested modifications



\## 🔧 Technical Architecture



\### Backend (FastAPI)



\- \*\*Core APIs:\*\*

&nbsp; - `/api/v1/chat/` - Text chat endpoint

&nbsp; - `/api/v1/itt/analyze` - Image analysis endpoint

&nbsp; - `/api/v1/tti/generate` - Image generation endpoint



\- \*\*Features:\*\*

&nbsp; - Fast and asynchronous processing

&nbsp; - RESTful API design

&nbsp; - Base64 image handling

&nbsp; - Supports multiple AI models



\### Frontend (Streamlit)



\- \*\*User Interface:\*\*

&nbsp; - Clean, chat-like interface

&nbsp; - Easy mode switching

&nbsp; - Real-time response display

&nbsp; - Image upload/download capabilities



\## 🚀 Setup Instructions



\### Prerequisites



```bash

Python 3.8+

pip

Virtual environment (recommended)

```



\### Installation



1\. Clone the repository:

```bash

git clone \[repository-url]

cd image\_generation

```



2\. Create and activate virtual environment:

```bash

python -m venv venv

source venv/bin/activate  # Linux/Mac

venv\\\\Scripts\\\\activate   # Windows

```



3\. Install dependencies:

```bash

pip install -r requirements.txt

```



\### Configuration



1\. Configure backend settings in `com/mhire/app/config/config.py`

2\. Set up environment variables in `.env`



\### Running the Application



1\. Start the backend server:

```bash

uvicorn com.mhire.app.main:app --host 0.0.0.0 --port 8000

```



2\. Launch the Streamlit interface:

```bash

streamlit run streamlit.py

```



Access the application at `http://localhost:8501`



\## 🔄 API Flow



\### Chat Mode



```mermaid

graph LR

&nbsp;   A\[User Input] --> B{Type?}

&nbsp;   B -->|Text Only| C\[/api/v1/chat/]

&nbsp;   B -->|Image Upload| D\[/api/v1/itt/analyze]

&nbsp;   D -->|With Prompt| E\[Custom Analysis]

&nbsp;   D -->|Without Prompt| F\[General Analysis]

```



\### Create Image Mode



```mermaid

graph LR

&nbsp;   A\[User Input] --> B{Type?}

&nbsp;   B -->|Text Only| C\[/api/v1/tti/generate]

&nbsp;   B -->|Image Upload| D\[Image Processing]

&nbsp;   D -->|With Prompt| E\[Custom Modification]

&nbsp;   D -->|Without Prompt| F\[Auto Enhancement]

```



\## 📦 Project Structure



```

image\_generation/

├── streamlit.py           # Frontend interface

├── requirements.txt       # Dependencies

├── com/

│   └── mhire/

│       └── app/

│           ├── main.py    # FastAPI app

│           ├── config/    # Configuration

│           └── services/  # Backend services

```



\## 🤝 Contributing



1\. Fork the repository

2\. Create feature branch

3\. Commit changes

4\. Push to branch

5\. Open pull request



\## 📄 License



This project is licensed under the MIT License - see the LICENSE file for details.



\## 🙏 Acknowledgments



\- FastAPI for the backend framework

\- Streamlit for the user interface

\- Gemini 2.5 Flash for AI capabilities

\- All contributors and maintainers



Update `.env` with your API key.



\## Run



```bash

streamlit run streamlit.py

```



This starts both FastAPI backend (port 8000) and Streamlit frontend (port 8501).



\## Features



\- \*\*💬 Chat\*\*: Natural conversations with memory (temporary, clears on reload)

\- \*\*🎨 Text-to-Image\*\*: Generate images from text prompts

\- \*\*🔍 Image-to-Text\*\*: Analyze and describe uploaded images



