from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from dotenv import load_dotenv
import os

load_dotenv()

model_name = os.environ['MODEL']

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    dtype="auto",
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained(model_name)


# Check if CUDA (GPU) is available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

#model.generation_config.pad_token_id = tokenizer.pad_token_id