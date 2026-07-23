from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "google/gemma-3-4b-it"

tokenizer = None
model = None


def load_model():
    """
    Load the tokenizer and model once.
    """

    global tokenizer, model

    if tokenizer is not None and model is not None:
        print("Model already loaded.")
        return

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype="auto",
        device_map="auto"
    )

    print("Model loaded successfully!")


def generate_answer(prompt, max_new_tokens=256, return_json=False):
    """
    Generate an answer using the loaded model.
    """

    if tokenizer is None or model is None:
        raise RuntimeError(
            "Model is not loaded. Call load_model() first."
        )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        temperature=0.2,
        do_sample=False,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id
    )

    # Decode only the generated tokens
    generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()

    if return_json:

        start = answer.find("{")

        end = answer.rfind("}")

        if start != -1 and end != -1 and end > start:

            answer = answer[start:end + 1]

    return answer