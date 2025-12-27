"""
Example script to demonstrate `clara_utils` usage.
Run:
    python examples/try_clara.py
"""
import sys
import os
# ensure repo root is on path so `clara_utils` can be imported when running from examples/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clara_utils import estimate_tokens, simulate_compress_text, compress_with_model, get_token_counts

large_text = """
Artificial Intelligence (AI) has become one of the most transformative technologies of the 21st century, fundamentally changing how we live, work, and interact with the world around us. The field of AI encompasses a wide range of technologies, from machine learning and deep learning to natural language processing and computer vision. These technologies power many of the applications we use daily, from smartphone assistants like Siri and Alexa to recommendation systems on Netflix and Amazon.

Machine learning, a subset of AI, involves training algorithms on large datasets to learn patterns and make predictions without being explicitly programmed. Deep learning, inspired by the structure and function of biological neural networks, uses artificial neural networks with multiple layers (hence "deep") to process complex data. This approach has led to breakthrough achievements in image recognition, natural language understanding, and game-playing AI systems.
"""

print("\n=== Token Estimation ===")
est = estimate_tokens(large_text)
print(f"Estimated tokens: {est}")

print("\n=== Simulated Compression (48x) ===")
comp = simulate_compress_text(large_text, ratio=48)
print(comp)

print("\n=== Token Counts (orig vs simulated) ===")
orig_count = get_token_counts([large_text])[0]
comp_count = get_token_counts([comp])[0]
print(f"Original tokens: {orig_count}")
print(f"Compressed tokens: {comp_count}")
print(f"Compression ratio (approx): {orig_count / max(1, comp_count):.1f}x")

print("\n=== Try model-based compression (if available) ===")
# Prepare documents for model API: list of document-lists
documents = [[large_text]]
outputs, err = compress_with_model(documents, model_name="apple/CLaRa-7B-Base", max_new_tokens=128)
if err:
    print("Model compression failed (usually because model download/config):")
    print(err)
else:
    print("Model output:", outputs)
