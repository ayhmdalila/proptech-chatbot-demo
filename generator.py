from model import model, tokenizer

def generate_response(chat_history):
    # Keep only the last 5 messages from the chat history
    chat_history = chat_history[-5:]

    text = tokenizer.apply_chat_template(conversation=chat_history, tokenize=False, add_generation_prompt=True, truncation=True, max_length=16384)
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(**model_inputs, max_new_tokens=512)
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response