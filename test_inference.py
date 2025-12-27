#!/usr/bin/env python3
"""
Test inference script for CLaRa model
This script tests the CLaRa model inference capability
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from transformers import AutoModel, AutoTokenizer
import torch

def test_inference():
    """Test basic CLaRa inference"""
    
    print("=" * 60)
    print("CLaRa Inference Test")
    print("=" * 60)
    
    try:
        # Load the model from Hugging Face
        # Note: Make sure you have enough disk space and internet connection
        print("\n[1] Loading CLaRa-7B-Base model from Hugging Face...")
        print("    This may take a while on first download (~15GB)...\n")
        
        model_name = "apple/CLaRa-7B-Base"
        
        # Check if CUDA is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[*] Using device: {device}")
        print(f"[*] CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"[*] GPU: {torch.cuda.get_device_name(0)}")
        
        # Load model with trust_remote_code=True (required for CLaRa)
        print(f"\n[2] Loading model '{model_name}'...")
        print("[*] With trust_remote_code=True for custom modeling_clara.py...")
        model = AutoModel.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map="auto" if device == "cuda" else "cpu"
        )
        print("[✓] Model loaded successfully!")
        
        # Example documents and questions
        print("\n[3] Preparing test data...")
        documents = [
            [
                "Weldenia is a monotypic genus of flowering plant in the family Commelinaceae, first described in 1829. It has one single species: Weldenia candida, which grows originally in Mexico and Guatemala.",
                "Hagsatera is a genus of flowering plants from the orchid family, Orchidaceae. There are two known species, native to Mexico and Guatemala",
                "Alsobia is a genus of flowering plants in the family Gesneriaceae, native to Mexico, Guatemala and Costa Rica. The two species are succulent, stoloniferous herbs and were previously included in the genus 'Episcia'. Recent molecular studies have supported the separation of 'Alsobia' from 'Episcia'"
            ]
        ]
        
        # Test 1: Paraphrase generation
        print("\n" + "=" * 60)
        print("TEST 1: Paraphrase Generation")
        print("=" * 60)
        
        questions = ["" for _ in range(len(documents))]
        print(f"[*] Input documents: {len(documents[0])} documents")
        print("[*] Running paraphrase generation...")
        
        out = model.generate_from_paraphrase(
            questions=questions,
            documents=documents,
            max_new_tokens=64
        )
        
        print("\n[✓] Paraphrase Generation Results:")
        print(f"Output: {out}\n")
        
        # Test 2: QA inference (if method exists)
        print("=" * 60)
        print("TEST 2: Question Answering")
        print("=" * 60)
        
        test_questions = [
            "What is Weldenia?",
            "Where does Hagsatera grow?",
            "What family does Alsobia belong to?"
        ]
        
        print("[*] Test questions:")
        for i, q in enumerate(test_questions, 1):
            print(f"   {i}. {q}")
        
        print("\n[*] Running QA inference...")
        
        # Try to call generate_from_qa if available
        try:
            qa_results = model.generate_from_qa(
                questions=test_questions,
                documents=documents,
                max_new_tokens=64
            )
            print("\n[✓] QA Results:")
            for i, result in enumerate(qa_results, 1):
                print(f"   Q{i}: {result}")
        except AttributeError:
            print("[!] generate_from_qa method not available, skipping test 2")
        except Exception as e:
            print(f"[!] Error in QA generation: {e}")
        
        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
        
        return True
        
    except FileNotFoundError as e:
        print(f"\n[ERROR] Model not found: {e}")
        print("[INFO] Please ensure the model is available on Hugging Face")
        return False
    except torch.cuda.OutOfMemoryError:
        print("\n[ERROR] GPU out of memory!")
        print("[INFO] Try using CPU instead or reduce batch size")
        return False
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_inference()
    exit(0 if success else 1)
