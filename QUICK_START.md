# CLaRa Quick Start Guide

## 🚀 Quick Test (CPU - No GPU needed)
```bash
cd "c:\utube project\general experiment code file\ml-clara"
python test_complete_inference.py
```
✓ Takes ~30 seconds, checks everything is set up

## 🔥 Full Inference Test (Requires GPU)
```bash
cd "c:\utube project\general experiment code file\ml-clara"
jupyter notebook inference.ipynb
```
Then run the cells in the notebook.

## 📦 What Was Done For You

✅ Cloned repository from: https://github.com/apple/ml-clara/tree/main  
✅ Installed all dependencies:
   - torch, transformers, peft, datasets, accelerate, huggingface_hub

✅ Created 3 test scripts:
   1. `test_complete_inference.py` - Full setup test
   2. `check_inference.py` - Environment checker  
   3. `test_inference.py` - Direct model test

✅ Created documentation:
   - `INFERENCE_SETUP.md` - Complete setup guide
   - `QUICK_START.md` - This file

## 💻 Your System Status

```
Python: 3.13.5 ✓
PyTorch: 2.9.1 ✓  
Transformers: 4.57.3 ✓
CUDA/GPU: ✗ (Not available)
```

## ⚠️ Important: GPU Needed for Real Use

The CLaRa-7B model is **15GB** and runs:
- **With GPU (A100, RTX 4090)**: Fast (real-time)
- **With CPU**: Very slow (minutes per inference)

To use GPU:
1. Install CUDA Toolkit
2. Install PyTorch with CUDA support
3. Verify: `python -c "import torch; print(torch.cuda.is_available())"`

## 🔗 Key Files

| File | Purpose |
|------|---------|
| `inference.ipynb` | Interactive notebook - best for testing |
| `openrlhf/models/modeling_clara.py` | Model implementation |
| `README.md` | Full documentation |
| `scripts/` | Training and evaluation scripts |
| `test_complete_inference.py` | Quick validation script |

## 🎯 Test the Model

### Method 1: Jupyter Notebook (Easiest)
```bash
jupyter notebook inference.ipynb
```
Run the cells step by step.

### Method 2: Python Script
```python
from transformers import AutoModel
import torch

model = AutoModel.from_pretrained(
    'apple/CLaRa-7B-Base',
    trust_remote_code=True
).to('cuda')  # or 'cpu' for CPU

documents = [["Your document text here"]]
questions = [""]

output = model.generate_from_paraphrase(
    questions=questions,
    documents=documents,
    max_new_tokens=64
)
print(output)
```

## 📊 Expected Output

When you run inference, you'll get:
- **Paraphrases**: Semantic rewrites of input documents
- **QA Output**: Answers based on document context
- **Compressed Representations**: 32-64x compression with semantic preservation

## 🆘 Help

All files are in:
```
c:\utube project\general experiment code file\ml-clara\
```

For detailed help:
- See `INFERENCE_SETUP.md` for troubleshooting
- See `README.md` in the repository for full documentation
- Check `openrlhf/models/modeling_clara.py` for implementation details

## ✨ Next: Try Interactive Testing

```bash
cd "c:\utube project\general experiment code file\ml-clara"
jupyter notebook inference.ipynb
```

Good luck! 🎉
