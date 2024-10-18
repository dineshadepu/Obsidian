# Installation

We use python package `pix2tex` to generate latex equations from images, which can be found at 
https://pypi.org/project/pix2tex/.  In order to install the software run the following in the command line

```bash
pip install pix2tex[gui]
```

# Usage

# GUI

Fire the `gui` by running `pix2tex_gui` and paste the image, which will generate latex equation.

# As an API 

For automation process and further use we can use API for generating the images. This is done as follows
```python
from PIL import Image
from pix2tex.cli import LatexOCR

img = Image.open('path/to/image.png')
model = LatexOCR()
print(model(img))
```

## Automate generating the equations



```python
import os
from pathlib import Path
from PIL import Image
from pix2tex.cli import LatexOCR

dirname = os.path.dirname(__file__)
mypath = os.path.join(os.path.dirname(__file__), '..', '..', 'images', 'latex_equation_images')

filenames = next(os.walk(mypath), (None, None, []))[2]
filenames_without_extension = []
for filename in filenames:
    filenames_without_extension.append(Path(filename).stem)
files_full_path = [os.path.join(mypath, f) for (dirpath, dirnames, filenames) in os.walk(mypath) for f in filenames]
print(filenames_without_extension)
print(files_full_path)


latex_equation_txt_files_path = os.path.join(os.path.dirname(__file__), 'latex_equations_text_files')
for i, image in enumerate(files_full_path):
    img = Image.open(image)
    model = LatexOCR()
    ans = model(img)

    with open(os.path.join(latex_equation_txt_files_path, filenames_without_extension[i]+".txt"), "w") as file:
        file.write(ans)

```
Run this python code at the room of your `Obsidian` folder. This will generate latex equations file.