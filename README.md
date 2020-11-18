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

If you make a change to the python code for hyperwidget, just restart the notebook kernel.

If you make a change to the javascript code for hyperwidget, go to the the dir `tools/hyperwidget` and run
```
cd js/
npm run build
```
You should refresh the browser and the changes will be reflected.

## Troubleshooting Installation

If the javascript code for the widget does not get updated after you run `npm run build`, it means the symbolic link is not established.
Go to the directory where jupyter/nbextension is located.
Run `jupyter --path`, and under `data:`, there should be a list of jupyter data paths.
Go through each of these paths and look for the jupyter data paths that contain the folder `nbextensions`.
Once you have found the `nbextensions` folder, go inside it and find a folder `hyperwidget`.
Remove that folder and then run the following commands:
```
jupyter nbextension install --py --symlink --sys-prefix hyperwidget
jupyter nbextension enable --py --sys-prefix hyperwidget
```
Check that `hyperwidget` folder inside nbextensions is now a symlink.
The javascript code should now be automatically updated.

## Sample Data

Download the sample data from [here](https://drive.google.com/file/d/1vey_K4gS-yB_Zb-AvyifWzGDH6O4QY_X/view?usp=sharing).
Download the full data from [here](https://drive.google.com/file/d/1Iv2PKdtzrfInyPbHMhoIZHZR8170zi3c/view?usp=sharing)
Create a folder `data/` in the project root folder and unzip the contßents of the sample data there.

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

To test the code on a jupyter notebook, run
```
jupyter notebook
```
