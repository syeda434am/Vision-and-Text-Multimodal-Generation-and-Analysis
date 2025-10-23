# Vision-and-Text Multimodal Generation and Analysis

A powerful AI assistant that combines natural language chat, image analysis, and image generation capabilities in a user-friendly interface. Built with FastAPI backend and Streamlit frontend, powered by Gemini 2.5 Flash.

## ✨ Features

### 💬 Chat Mode (Default)

**1. Regular Chat**
- Natural conversation with AI
- Type your message and click send (➤)
- Perfect for questions, discussions, and general assistance
- Temporary memory (clears on reload)

**2. Image Analysis (General)**
- Upload any image for AI analysis
- Click 📎, choose image, click send
- AI provides detailed description of the image

**3. Image Analysis (Specific)**
- Upload image with specific questions
- Click 📎, upload image, type your question, click send
- AI answers questions about the image

### 🎨 Create Image Mode

**1. Text-to-Image Generation**
- Generate images from text descriptions
- Type detailed description, click send
- AI creates image matching your description

**2. Image Enhancement**
- Automatically enhance existing images
- Upload image, click send
- AI improves image quality and aesthetics

**3. Custom Image Modification**
- Modify images with specific instructions
- Upload image, describe changes, click send
- AI applies your requested modifications

## 🏗️ Technical Architecture

### Backend (FastAPI)

**Core APIs:**
- `/api/v1/chat/` - Text chat endpoint
- `/api/v1/itt/analyze` - Image-to-text analysis endpoint
- `/api/v1/tti/generate` - Text-to-image generation endpoint

**Features:**
- Fast and asynchronous processing
- RESTful API design
- Base64 image handling
- Support for multiple AI models

### Frontend (Streamlit)

**User Interface:**
- Clean, chat-like interface
- Easy mode switching
- Real-time response display
- Image upload/download capabilities

## 🔄 API Flow

### Chat Mode
- **Text Only:** User Input → `/api/v1/chat/` → Response
- **Image Upload (General):** User Input + Image → `/api/v1/itt/analyze` → General Analysis
- **Image Upload (Specific):** User Input + Image + Prompt → `/api/v1/itt/analyze` → Custom Analysis

### Create Image Mode
- **Text-to-Image:** Text Prompt → `/api/v1/tti/generate` → Generated Image
- **Image Enhancement:** Image Upload → `/api/v1/tti/generate` → Enhanced Image
- **Custom Modification:** Image + Instructions → `/api/v1/tti/generate` → Modified Image

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone [repository-url]
   cd image_generation
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

### Running the Application

You need to run both the FastAPI backend and Streamlit frontend:

1. **Start FastAPI backend (Terminal 1):**
   ```bash
   uvicorn com.mhire.app.main:app --host 0.0.0.0 --port 8000
   ```

2. **Start Streamlit frontend (Terminal 2):**
   ```bash
   streamlit run streamlit.py
   ```

Access the application at `http://localhost:8501`

The FastAPI backend runs on port 8000 and Streamlit frontend runs on port 8501.

## 🛠️ Configuration

Edit `com/mhire/app/config/config.py` to customize:
- API endpoints
- Model parameters
- Backend settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Streamlit](https://streamlit.io/) - User interface
- [Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/) - AI capabilities
- All contributors and maintainers

---

**Note:** Make sure to keep your `.env` file secure and never commit it to version control. Add it to `.gitignore`.