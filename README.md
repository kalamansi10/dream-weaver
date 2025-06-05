# Dream Weaver

Dream Weaver is an AI-powered story builder application that generates engaging stories with accompanying images and audio narration. Built with FastAPI and modern AI technologies, it creates immersive storytelling experiences.

## Features

### Currently Implemented
- **Story Generation**: Creates engaging stories using a local LLM (LlamaCpp)
- **RESTful API**: FastAPI-based endpoints for story generation
- **Health Monitoring**: System status and model availability checks

### Planned Features
- **Image Generation**: AI-generated illustrations for stories
- **Audio Narration**: Text-to-speech conversion for story narration
- **Story Customization**: Options for story style, length, and themes

## Technical Stack

- **Backend**: FastAPI
- **AI Models**:
  - Text Generation: LlamaCpp (Local LLM)
  - Image Generation: Coming soon
  - Audio Generation: Coming soon
- **Dependencies**: See `requirements.txt`

## Prerequisites

- Python 3.8+
- Git
- Sufficient disk space for AI models
- GPU recommended for better performance

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
   ```

## Usage

1. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Access the API documentation at `http://localhost:8000/docs`

3. Generate a story using the `/stories/generate` endpoint with a POST request:
   ```json
   {
     "prompt": "Your story prompt here"
   }
   ```

## API Endpoints

- `GET /`: Welcome message
- `GET /health`: System health check
- `POST /stories/generate`: Generate a new story

## Development Status

This project is under active development. Current focus:
- [x] Story text generation
- [ ] Image generation
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