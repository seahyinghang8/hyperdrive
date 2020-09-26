# hyperdrive

The foundational structure to an automated filesystem

Python version 3.7.8

## Setup (For MacOS)

To install python requirements, run `pip install -r requirements.txt`

To install tesseract (OCR engine), run `brew install tesseract`

To install poppler (PDF to image converter), run `brew install poppler`

## Typechecking

To perform a basic typecheck, run `mypy file.py --ignore-missing-imports` where file.py is the program you are typechecking

To perform a strict typecheck, run `mypy file.py --disallow-untyped-defs --ignore-missing-imports` to ensure all functions are typechecked.

# Create makefile