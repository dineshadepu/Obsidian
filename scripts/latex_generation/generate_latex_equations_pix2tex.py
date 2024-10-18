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


latex_equation_txt_files_path = os.path.dirname(__file__)
for i, image in enumerate(files_full_path):
    img = Image.open(image)
    model = LatexOCR()
    ans = model(img)

    with open(os.path.join(latex_equation_txt_files_path, filenames_without_extension[i]+".txt"), "w") as file:
        file.write(ans)
