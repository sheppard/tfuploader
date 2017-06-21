import tempfile
import os
from PIL import Image, ImageOps
from wq.io.util import guess_type
from tqdm import tqdm


def export_images(groups, size):
    groups = groups.copy()
    dirname = tempfile.mkdtemp()
    image_paths = []

    print("Exporting Images...")
    for group, objs in list(groups.items()):
        if len(objs) < 20:
            print("  * Skipping %s (not enough images to train)" % group)
            groups.pop(group)
        else:
            os.mkdir(os.path.join(dirname, group))

    for group, source, name in tqdm(list(flatten(groups))):
        image_path = os.path.join(group, name)
        image_paths.append(image_path)
        export_image(
            source,
            os.path.join(dirname, image_path),
            size
        )
    return dirname, image_paths


def flatten(groups):
    for group, objs in groups.items():
        for source, name in objs:
            yield group, source, name


def export_image(source, dest, size):
    size = int(size)
    mime = guess_type(source)
    if not mime.startswith('image/'):
        raise Exception("Unknown file type %s for %s!" % (mime, source))

    img = Image.open(source)
    if hasattr(img, '_getexif'):
        exif = img._getexif()
    else:
        exif = None
    if exif:
        orientation = exif.get(0x0112, 1)
    else:
        orientation = 1

    rotate = {
        3: Image.ROTATE_180,
        6: Image.ROTATE_270,
        8: Image.ROTATE_90
    }
    if orientation in rotate:
        img = img.transpose(rotate[orientation])

    img = ImageOps.fit(img, (size, size), Image.ANTIALIAS)
    img.save(dest, 'JPEG')
