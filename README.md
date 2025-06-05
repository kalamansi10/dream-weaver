# Dream Weaver

Dream Weaver is an AI-powered story builder application that generates engaging stories with accompanying images and audio narration. Built with FastAPI and modern AI technologies, it creates immersive storytelling experiences.

## Features

### Currently Implemented
- **Story Generation**: Creates engaging stories using a local LLM (LlamaCpp)
- **Image Generation**: AI-generated illustrations using Stable Diffusion
- **RESTful API**: FastAPI-based endpoints for story and image generation
- **Health Monitoring**: System status and model availability checks

### Planned Features
- **Audio Narration**: Text-to-speech conversion for story narration
- **Story Customization**: Options for story style, length, and themes

## Technical Stack

- **Backend**: FastAPI
- **AI Models**:
  - Text Generation: LlamaCpp (Local LLM)
  - Image Generation: Stable Diffusion 2.1 (CPU/GPU)
  - Audio Generation: Coming soon
- **Dependencies**: See `requirements.txt`

## Prerequisites

- Python 3.8+
- Git
- Sufficient disk space for AI models (LLM + Stable Diffusion)
- GPU recommended for better performance
- (Optional) Hugging Face account and access token for gated models

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dream-weaver.git
   cd dream-weaver
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download required AI models:
   - Place your GGUF model file in the `models_llm` directory
   - Update the `MODEL_PATH` in your `.env` file

5. Create a `.env` file with necessary configurations:
   ```
   MODEL_PATH=models_llm/your-model.gguf
   # Stable Diffusion Configuration
   SD_MODEL_ID=stabilityai/stable-diffusion-2-1  # Default open source model
   # HF_TOKEN=your_huggingface_token  # Only needed for gated models
   ```

## Usage

1. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Access the API documentation at `http://localhost:8000/docs`

3. Generate a story with images using the `/stories/generate` endpoint with a POST request:
   ```json
   {
     "prompt": "Your story prompt here"
   }
   ```

## API Endpoints

- `GET /`: Welcome message
- `GET /health`: System health check
- `POST /stories/generate`: Generate a new story with images
- `POST /models/sd/download`: Download and load Stable Diffusion model
- `GET /models/sd/status`: Check Stable Diffusion model status

## Development Status

This project is under active development. Current focus:
- [x] Story text generation
- [x] Image generation
- [ ] Audio narration
- [ ] Enhanced story customization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your chosen license here]

## Acknowledgments

- LlamaCpp for the local LLM implementation
- FastAPI for the web framework
- LangChain for the AI chain orchestration
- Stability AI for Stable Diffusion

## Image Generation

The application uses Stable Diffusion for image generation. By default, it uses the open-source Stable Diffusion 2.1 model, which doesn't require authentication. If you want to use a different model:

1. For open-source models:
   - Set `SD_MODEL_ID` in your `.env` file to the model ID of your choice
   - Example: `SD_MODEL_ID=stabilityai/stable-diffusion-2-1`

2. For gated models (like Stable Diffusion 3.5):
   - Create a Hugging Face account
   - Accept the terms for the model you want to use
   - Generate an access token from your Hugging Face account settings
   - Add your token to `.env`: `HF_TOKEN=your_token_here`
   - Set `SD_MODEL_ID` to the gated model ID

### Image Generation Features
- CPU-optimized inference pipeline
- Configurable number of inference steps
- Automatic image saving with unique timestamps
- Base64 encoded image output for immediate display
- Static file serving for generated images