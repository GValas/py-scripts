

import piexif
from datetime import datetime
from PIL import Image
import glob
import os
import time


def creation_date(file):
    t = os.path.getmtime(file)
    d = datetime.fromtimestamp(t)
    s = d.strftime("%Y:%m:%d %H:%M:%S")
    return s.encode("utf-8")


def get_files_to_process(dir):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(dir):
        for file in f:
            if '.jpg' in file or '.JPG' in file:
                files.append(os.path.join(r, file))
    return files


def update_pics(files):
    print(f'parsing {pics_dir}')
    print(f'processing {len(files)} files')

    for file in files:

        # img = Image.open(file)
        pic_dict = piexif.load(file)
        oth_dict = pic_dict['0th']
        exif_dict = pic_dict['Exif']

        # key must be present and value not null
        has_idf = piexif.ImageIFD.DateTime in oth_dict \
            and oth_dict[piexif.ImageIFD.DateTime] != b'0000:00:00 00:00:00'
        has_exif_digitized = piexif.ExifIFD.DateTimeDigitized in exif_dict \
            and exif_dict[piexif.ExifIFD.DateTimeDigitized] != b'0000:00:00 00:00:00'
        has_exif_original = piexif.ExifIFD.DateTimeOriginal in exif_dict \
            and exif_dict[piexif.ExifIFD.DateTimeOriginal] != b'0000:00:00 00:00:00'

        # at least one field must be missing
        if has_idf and has_exif_digitized and has_exif_original:
            continue

        # get best date proxy
        best_date = None
        if has_exif_digitized:
            best_date = exif_dict[piexif.ExifIFD.DateTimeDigitized]
        elif has_exif_original:
            best_date = exif_dict[piexif.ExifIFD.DateTimeOriginal]
        elif has_idf:
            best_date = oth_dict[piexif.ImageIFD.DateTime]
        else:
            best_date = creation_date(file)

        # date needed for update
        if best_date is None:
            print(f'{file} has no best date ! ')
            continue

        # updating fields
        if not has_idf:
            oth_dict[piexif.ImageIFD.DateTime] = best_date

        if not has_exif_original:
            exif_dict[piexif.ExifIFD.DateTimeOriginal] = best_date

        if not has_exif_digitized:
            exif_dict[piexif.ExifIFD.DateTimeDigitized] = best_date

        piexif.remove(file)
        exif_bytes = piexif.dump(pic_dict)
        piexif.insert(exif_bytes, file)
        print(f'{file} updated ')


if __name__ == "__main__":
    os.system('clear')
    pics_dir = os.path.join(os.getcwd(), 'data')
    files = get_files_to_process(pics_dir)
    update_pics(files)
