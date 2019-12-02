import os

name_dict = {
    '定窑白瓷':'dingyao',
    '哥窑':'geyao',
    '钧窑':'junyao',
    '汝窑':'ruyao',
    '元青花瓷':'yuanqinghuaci'
}

img_dir = 'images'
img_list = os.listdir(img_dir)

for img_name in img_list:
    src_name = os.path.join(img_dir, img_name)
    name_sep = img_name.split('_')
    dst_name = os.path.join(img_dir, name_dict[name_sep[0]]+'_'+name_sep[1])
    os.rename(src_name, dst_name)