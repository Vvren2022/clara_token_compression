#!/usr/bin/env python3
"""
Simplified CLaRa Inference Test
This script tests the CLaRa inference with simpler model loading
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def check_environment():
    """Check the environment and dependencies"""
    print("=" * 60)
    print("CLaRa Environment Check")
    print("=" * 60)
    
    # Check Python version
    print(f"\n[*] Python version: {sys.version}")
    
    # Check key packages
    packages_to_check = [
        'torch',
        'transformers',
        'huggingface_hub',
        'peft',
        'datasets',
        'accelerate',
    ]
    
    print("\n[*] Checking installed packages:")
    for pkg in packages_to_check:
        try:
            mod = __import__(pkg)
            version = getattr(mod, '__version__', 'unknown')
            print(f"  ✓ {pkg}: {version}")
        except ImportError:
            print(f"  ✗ {pkg}: NOT INSTALLED")
    
    # Check GPU
    try:
        import torch
        print(f"\n[*] GPU Information:")
        print(f"  CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"  GPU count: {torch.cuda.device_count()}")
            print(f"  GPU name: {torch.cuda.get_device_name(0)}")
            print(f"  CUDA version: {torch.version.cuda}")
        else:
            print("  No GPU detected - will run on CPU")
    except Exception as e:
        print(f"  Error checking GPU: {e}")
    
    # Check repo structure
    print(f"\n[*] Repository structure:")
    repo_items = {
        'openrlhf/': 'Main training framework',
        'openrlhf/models/modeling_clara.py': 'CLaRa model definition',
        'inference.ipynb': 'Inference notebook',
        'example/': 'Example data',
        'scripts/': 'Training scripts',
    }
    
    for item, desc in repo_items.items():
        path = os.path.join(os.path.dirname(__file__), item)
        exists = os.path.exists(path)
        status = "✓" if exists else "✗"
        print(f"  {status} {item:<35} - {desc}")
    
    return True

def test_model_availability():
    """Test if we can access the model"""
    print("\n" + "=" * 60)
    print("CLaRa Model Availability Test")
    print("=" * 60)
    
    try:
        from transformers import AutoTokenizer
        
        print("\n[*] Checking if CLaRa model is available on Hugging Face...")
        model_name = "apple/CLaRa-7B-Base"
        
        # Try to download just the config
        try:
            print(f"\n[*] Attempting to load config for '{model_name}'...")
            # This will download the config without downloading the full model
            from huggingface_hub import hf_hub_download, repo_info
            
            repo = repo_info(model_name)
            print(f"  ✓ Model found on Hugging Face")
            print(f"    - Last modified: {repo.last_modified}")
            print(f"    - Private: {repo.private}")
            
            # Try downloading config
            try:
                config_path = hf_hub_download(repo_id=model_name, filename="config.json")
                print(f"  ✓ Config downloaded: {config_path}")
                
                # Read config to check model_type
                import json
                with open(config_path) as f:
                    config = json.load(f)
                    print(f"  - Model type: {config.get('model_type', 'NOT SET')}")
                    print(f"  - Architecture: {config.get('architectures', 'Unknown')}")
                    
            except Exception as e:
                print(f"  ! Could not download config: {e}")
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
    except Exception as e:
        print(f"  ✗ Failed to check model availability: {e}")

def test_local_inference():
    """Test if we can run inference with a small example"""
    print("\n" + "=" * 60)
    print("CLaRa Local Inference Test")
    print("=" * 60)
    
    print("\n[*] This test requires downloading the full model (~15GB)")
    print("[*] Model variants available:")
    models = [
        "apple/CLaRa-7B-Base",
        "apple/CLaRa-7B-Instruct", 
        "apple/CLaRa-7B-E2E"
    ]
    for m in models:
        print(f"    - {m}")
    
    print("\n[*] To test inference, you can:")
    print("    1. Ensure you have ~15GB free disk space")
    print("    2. Ensure you have a GPU (16GB+ VRAM recommended)")
    print("    3. Run the inference.ipynb notebook for interactive testing")
    print("    4. Or use the example scripts in the scripts/ directory")
    
    print("\n[*] Example usage code:")
    print("""
    from transformers import AutoModel
    
    # Load model
    model = AutoModel.from_pretrained(
        'apple/CLaRa-7B-Base',
        trust_remote_code=True
    ).to('cuda')
    
    # Example documents
    documents = [["Document 1 text", "Document 2 text", ...]]
    questions = [""]
    
    # Generate paraphrases
    output = model.generate_from_paraphrase(
        questions=questions,
        documents=documents, 
        max_new_tokens=64
    )
    print(output)
    """)

if __name__ == "__main__":
    try:
        # Run checks
        check_environment()
        test_model_availability()
        test_local_inference()
        
        print("\n" + "=" * 60)
        print("Environment check complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
