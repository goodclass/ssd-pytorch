import os
import xml.etree.ElementTree as ET
from utils.utils import get_classes


VOCdevkit_path = 'VOCdevkit'
VOCdevkit_sets = [('2007', 'train'), ('2007', 'val')]
classes, _ = get_classes('conf/voc_classes.txt')


def convert_annotation(year, image_id, list_file):
    in_file = open(os.path.join(VOCdevkit_path, 'VOC%s/Annotations/%s.xml' % (year, image_id)), encoding='utf-8')
    tree = ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = 0
        if obj.find('difficult') != None:
            difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(float(xmlbox.find('xmin').text)), int(float(xmlbox.find('ymin').text)),
             int(float(xmlbox.find('xmax').text)), int(float(xmlbox.find('ymax').text)))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))


# 生成训练数据列表 2007_train.txt和2007_val.txt
if __name__ == "__main__":

    print("Generate 2007_train.txt and 2007_val.txt for train.")
    type_index = 0
    for year, image_set in VOCdevkit_sets:
        image_ids = open(os.path.join(VOCdevkit_path, 'VOC%s/ImageSets/Main/%s.txt' % (year, image_set)),
                         encoding='utf-8').read().strip().split()
        list_file = open('%s_%s.txt' % (year, image_set), 'w', encoding='utf-8')
        for image_id in image_ids:
            list_file.write('%s/VOC%s/JPEGImages/%s.jpg' % (os.path.abspath(VOCdevkit_path), year, image_id))

            convert_annotation(year, image_id, list_file)
            list_file.write('\n')
        type_index += 1
        list_file.close()
    print("Generate 2007_train.txt and 2007_val.txt for train done.")