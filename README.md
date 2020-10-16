# Hyperdrive

The foundational structure for an automated filesystem

Python version 3.7.8

## Setup (For MacOS)

To install python requirements, run
```
pip install -r requirements.txt
```

To install tesseract (OCR engine), run 
```
brew install tesseract
```

To install poppler (PDF to image converter), run 

```
brew install poppler
```

To install the spacy model, run the following:
```
python -m spacy download en_core_web_sm
```

To install the jupyter widget, first ensure you have `npm` installed. Next, run the following:
```
cd tools/hyperwidget
pip install -e .
jupyter nbextension install --py --symlink --sys-prefix hyperwidget
jupyter nbextension enable --py --sys-prefix hyperwidget
```

## Sample Data

Download the sample data from [here](https://drive.google.com/file/d/14Wdmii6le7KQDEW9T4eZD4emKbvdCjse/view).
Create a folder `data/` in the project root folder and unzip the contents of the sample data there.

## Typechecking

To perform a strict typecheck, run
```
mypy main.py --disallow-untyped-defs --ignore-missing-imports
```

## Run the Code

To test the code on an example, run
```
python main.py
```

You can also test hyperwidget on the jupyter notebook by running
```
jupyter notebook
```