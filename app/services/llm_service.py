from llama_cpp import Llama
from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

llm_instance = None
MODEL_PATH = os.path.join(os.getcwd(), os.getenv('MODEL_PATH'))
# You might want to make MODEL_PATH configurable via .env or a config file

def load_local_llm():
    global llm_instance
    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: Model file not found at {MODEL_PATH}")
        print("Please download a GGUF model and place it in the 'models_llm' directory.")
        llm_instance = None
        return

    try:
        print(f"Loading local LLM from: {MODEL_PATH}...")
        llm_instance = LlamaCpp(
            model_path=MODEL_PATH,
            n_gpu_layers=-1,  # Offload all possible layers to GPU. Set to 0 for CPU only.
            n_batch=512,      # Adjust based on your resources
            n_ctx=4096,       # Context window, e.g., Mistral 7B has a large context
            temperature=0.6,
            max_tokens=1024,   # Max tokens for the story
            verbose=True,     # For debugging, set to False in production
            # f16_kv=True,    # Can improve speed and reduce VRAM on some GPUs if llama.cpp built with it
        )
        print("Local LLM loaded successfully.")
    except Exception as e:
        print(f"Critical: Could not load local LLM: {e}")
        llm_instance = None

story_prompt_template_str = """<|im_start|>system
You are a creative storyteller. Generate a short, engaging story based on the user's prompt. The story should be about 3-5 paragraphs long.<|im_end|>
<|im_start|>user
{user_prompt}<|im_end|>
<|im_start|>assistant
"""
# The "Assistant:" part primes the model to start generating the story.

story_prompt_template = PromptTemplate(
    input_variables=["user_prompt"],
    template=story_prompt_template_str
)

# Create a LangChain chain
# This chain takes a prompt, feeds it to the LLM, and parses the output as a string.
story_generation_chain = None # Will be initialized after LLM loads

def initialize_story_chain():
    global story_generation_chain
    if llm_instance:
        story_generation_chain = story_prompt_template | llm_instance | StrOutputParser()
        print("Story generation chain initialized.")
    else:
        print("LLM instance not available. Story chain not initialized.")

async def generate_story_text(prompt: str) -> str:
    """
    Generates story text based on a user prompt using the local LLM.
    """
    global story_generation_chain
    if not llm_instance:
        load_local_llm() # Attempt to load if not already loaded
        initialize_story_chain() # Then initialize chain

    if not story_generation_chain:
        error_msg = "Sorry, the local storyteller is not available right now."
        print(error_msg)
        return error_msg

    try:
        # For LlamaCpp with LangChain, it's better to use `ainvoke` if the underlying
        # LlamaCpp class supports async, or run sync in threadpool.
        # The LangChain LlamaCpp wrapper should handle threading for its synchronous underlying library.
        print(f"Generating story with local LLM for prompt: {prompt}")
        response = await story_generation_chain.ainvoke({"user_prompt": prompt})
        return response.strip() # Remove any leading/trailing whitespace
    except Exception as e:
        print(f"Error generating story text with local LLM: {e}")
        return "Sorry, I couldn't generate a story with the local model right now."