import os
files = os.listdir('data/images/80m/exp10')
files.sort()
print(files)
filtedFiles = list(filter(lambda f: f.endswith('.jpg') and not (f.startswith('Original Image') or f.startswith('Resized Image')),files))
print(filtedFiles)
# def check(f):
#     if f.endswith('.jpg') and not (f.startswith('Original Image') or f.startswith('Resized Image')):
#         print(True)
#     else:   print(False)

# check('Original Image.jpg')