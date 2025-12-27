"""
Simple CLaRa helper utilities for token estimation and compression simulation.
This module provides:
- estimate_tokens(text, tokenizer_name=None)
- simulate_compress_text(text, ratio=48)
- compress_with_model(documents, model_name='apple/CLaRa-7B-Base')
- get_token_counts(texts, tokenizer_name=None)

Note: `compress_with_model` will try to load the CLaRa model with
`trust_remote_code=True`. This may fail if the HF config is not standard
or the model is not available. In that case, use `simulate_compress_text`.
"""
from typing import List, Tuple, Optional


def estimate_tokens(text: str, tokenizer_name: Optional[str] = None) -> int:
    """Estimate token count for `text`.

    Tries to use a HuggingFace tokenizer if `tokenizer_name` is provided or
    if `gpt2` tokenizer can be loaded. Falls back to a rough estimation of
    1 token ≈ 4 characters.
    """
    try:
        if tokenizer_name:
            from transformers import AutoTokenizer
            tok = AutoTokenizer.from_pretrained(tokenizer_name)
            return len(tok.encode(text))
        else:
            # Try a lightweight tokenizer (gpt2)
            from transformers import AutoTokenizer
            tok = AutoTokenizer.from_pretrained("gpt2")
            return len(tok.encode(text))
    except Exception:
        # Fallback estimate
        return max(1, len(text) // 4)


def simulate_compress_text(text: str, ratio: int = 48) -> str:
    """Return a simulated compressed version of `text` using a heuristic.

    The function tries to keep the most informative sentences up to the
    target token budget derived from `ratio`. This is a lightweight
    approximation to help you experiment without downloading large models.
    """
    if not text:
        return ""

    # Compute approximate token budget
    original_tokens = estimate_tokens(text)
    target_tokens = max(8, int(original_tokens / ratio))

    # Split into sentences and select the longest informative ones until
    # we reach the token budget (heuristic)
    import re

    # Basic sentence split (works well enough for demo text)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    # Score sentences by length (longer -> more info heuristically)
    scored = sorted(sentences, key=lambda s: len(s), reverse=True)

    selected = []
    selected_tokens = 0
    for s in scored:
        est = estimate_tokens(s)
        if selected_tokens + est <= target_tokens or not selected:
            selected.append(s.strip())
            selected_tokens += est
        if selected_tokens >= target_tokens:
            break

    # Fall back to first sentence if nothing selected
    if not selected:
        selected = [sentences[0]]

    # Join selected sentences into a compressed paragraph
    compressed = " ".join(selected)
    # Trim to roughly target token budget by characters
    max_chars = max(50, target_tokens * 4)
    if len(compressed) > max_chars:
        compressed = compressed[:max_chars].rsplit(" ", 1)[0] + "..."

    return compressed


def get_token_counts(texts: List[str], tokenizer_name: Optional[str] = None) -> List[int]:
    """Return token counts for each string in `texts` using tokenizer if available.

    Falls back to estimate if tokenizer cannot be loaded.
    """
    counts = []
    try:
        if tokenizer_name:
            from transformers import AutoTokenizer
            tok = AutoTokenizer.from_pretrained(tokenizer_name)
            for t in texts:
                counts.append(len(tok.encode(t)))
            return counts
        else:
            # try gpt2
            from transformers import AutoTokenizer
            tok = AutoTokenizer.from_pretrained("gpt2")
            for t in texts:
                counts.append(len(tok.encode(t)))
            return counts
    except Exception:
        for t in texts:
            counts.append(max(1, len(t) // 4))
        return counts


def compress_with_model(documents: List[List[str]], questions: Optional[List[str]] = None,
                        model_name: str = "apple/CLaRa-7B-Base",
                        max_new_tokens: int = 128, device: Optional[str] = None) -> Tuple[Optional[List[str]], Optional[str]]:
    """Try to load the CLaRa model and run `generate_from_paraphrase`.

    Returns (outputs, error_message). If outputs is None, an error occurred and
    `error_message` contains details.
    """
    try:
        import torch
        from transformers import AutoModel
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        model = AutoModel.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map="auto" if device == "cuda" else "cpu"
        )

        if questions is None:
            questions = ["" for _ in range(len(documents))]

        outputs = model.generate_from_paraphrase(
            questions=questions,
            documents=documents,
            max_new_tokens=max_new_tokens
        )
        return outputs, None
    except Exception as e:
        return None, str(e)


if __name__ == "__main__":
    # Quick demo when executed directly
    sample = (
        "Artificial Intelligence (AI) has become one of the most transformative technologies of the 21st century, "
        "fundamentally changing how we live, work, and interact. Machine learning and deep learning power many apps." 
    )
    print("Original tokens (estimate):", estimate_tokens(sample))
    print("Simulated compressed text:\n", simulate_compress_text(sample, ratio=48))
