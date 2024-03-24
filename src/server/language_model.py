from fastapi import FastAPI
from transformers import pipeline
import uvicorn
import time

# Load a GPT model
model_name = "gpt2"  # Example model
generator = pipeline("text-generation", model=model_name)

app = FastAPI(title="MODEL")

@app.get("/")
async def root():
    return {"message": "model"}

@app.get("/run_query")
async def run_query(query: str = ""):
    prompt = query  # Directly use the query string as the prompt

    # Record the start time
    start_time = time.time()

    # Generate text based on the prompt. Adjust the parameters as needed.
    generated_texts = generator(prompt, max_length=50, return_full_text=False)
    generated_text = generated_texts[0]['generated_text'] if generated_texts else ""

    # Calculate processing time
    processing_time = time.time() - start_time

    return {
        "query": query,
        "promt": generated_text,
        "time": processing_time
    }

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=6060)
