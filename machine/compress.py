import os
import sys
from PIL import Image

def compress_me(path, saved_path,file, verbose=False):
    # filename = os.path.join(sys.)
    image = Image.open(path)
    image.resize((300, 500), Image.ANTIALIAS)
    image.save(saved_path, quality=95)
    image.save("path\\to\\save\\image_scaled_opt.jpg",optimize=True,quality=95)






#  >>> from PIL import Image
#  # My image is a 200x374 jpeg that is 102kb large
#  >>> foo = Image.open("path\\to\\image.jpg")
#  >>> foo.size
#   (200,374)
#  # I downsize the image with an ANTIALIAS filter (gives the highest quality)
#  >>> foo = foo.resize((160,300),Image.ANTIALIAS)
#  >>> foo.save("path\\to\\save\\image_scaled.jpg",quality=95)
#  # The saved downsized image size is 24.8kb
#  >>> foo.save("path\\to\\save\\image_scaled_opt.jpg",optimize=True,quality=95)
#  # The saved downsized image size is 22.9kb
# The optimize flag will do an extra pass on the image to find a way to reduce its size as much as possible. 1.9kb might not seem like much, but over hundreds/thousands of pictures, it can add up.

# Now to try and get it down to 5kb to 10 kb, you can change the quality value in the save options. Using a quality of 85 instead of 95 in this case would yield: Unoptimized: 15.1kb Optimized : 14.3kb Using a