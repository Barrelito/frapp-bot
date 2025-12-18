import sys
print(sys.path)
try:
    import langchain
    print(f"Langchain found: {langchain.__file__}")
    print(f"Langchain version: {langchain.__version__}")
except ImportError as e:
    print(f"Langchain import failed: {e}")

try:
    import langchain.chains
    print(f"Langchain chains found: {langchain.chains.__file__}")
except ImportError as e:
    print(f"Langchain chains import failed: {e}")

try:
    from langchain.chains import RetrievalQA
    print("RetrievalQA imported successfully")
except ImportError as e:
    print(f"RetrievalQA import failed: {e}")
