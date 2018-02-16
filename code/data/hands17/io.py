import numpy as np
from skimage import io as skimio
import re


def read_image(image_name):
    # img = mpimg.imread(image_name)
    # img = spndim.imread(image_name)
    # img = (img - img.min()) / (img.max() - img.min()) * 255
    img = skimio.imread(image_name)
    return img


def save_image(image_name, img):
    # mpimg.imsave(image_name, img, cmap=mpplot.cm.gray)
    # spmisc.imsave(image_name, img)
    skimio.imsave(image_name, img)


def imagename2index(image_name):
    return int(re.match(r'^image_D(\d+)\.png', image_name).group(1))


def index2imagename(index):
    return 'image_D{:08d}.png'.format(index)


def write_h5(writer, index, poses):
    writer.create_dataset(
        'index',
        index.shape,
        compression='lzf',
        dtype=np.int32
    )
    writer.create_dataset(
        'poses',
        poses.shape,
        compression='lzf',
        dtype=float)
    writer['index'][:] = index
    writer['poses'][:] = poses


def write_txt(writer, index, poses):
    for ii, pp in zip(index, poses):
        writer.write(
            index2imagename(ii) +
            '\t' + '\t'.join("%.4f" % x for x in pp) +
            '\n')


def h5_to_txt(reader, writer):
    write_txt(writer, reader['index'][:, 0], reader['poses'])


def parse_line_annot(line):
    """ parse raw annotation, and appendix for crop-resize """
    annot_list = re.split(r'\s+', line.strip())
    if 64 == len(annot_list):
        pose_raw = np.reshape(
            [float(i) for i in annot_list[1:64]],
            (21, 3)
        )
    else:
        print('error - wrong pose annotation: {} --> {}'.format(
            line, annot_list))
        print(annot_list)
    return annot_list[0], pose_raw


def parse_line_appen2(line):
    append_list = re.split(r'\s+', line.strip())
    resce = np.array([float(i) for i in append_list])
    return resce


def get_line(filename, img_id):
    img_name_id = index2imagename(img_id)
    with open(filename, 'r') as f:
        for _, line in enumerate(f):
            img_name, _ = parse_line_annot(line)
            if img_name_id == img_name:
                return line


def parse_line_bbox(annot_line):
    line_l = re.split(r'\s+', annot_line.strip())
    bbox = np.reshape(
        [float(i) for i in line_l[1:5]],
        (2, 2)
    )
    return line_l[0], bbox
