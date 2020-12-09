import os
import numpy as np
import json
import cv2

id_counter = 0 # To record the id
FILE_PATH = 'put your image folder path here!' #####
out = {'annotations': [], 
           'categories': [{"id": 1, "name": "cricoid_cartilage", "supercategory": ""}, {"id": 2, "name": "thyroid_cartilage", "supercategory": ""}], ##### change the categories to match your dataset!
           'images': [],
           'info': {"contributor": "", "year": "", "version": "", "url": "", "description": "", "date_created": ""},
           'licenses': {"id": 0, "name": "", "url": ""}
           }

def annotations_data(whole_path , image_id):
    # id, bbox, iscrowd, image_id, category_id
    global id_counter
    txt = open(whole_path,'r')
    for line in txt.readlines(): # if txt.readlines is null, this for loop would not run
        data = line.strip()
        data = data.split() 
        # convert the center into the top-left point!
        data[1] = float(data[1])* 800 - 0.5 * float(data[3])* 800 ##### change the 800 to your raw image width
        data[2] = float(data[2])* 600 - 0.5 * float(data[4])* 600 ##### change the 600 to your raw image height
        data[3] = float(data[3])* 800 ##### change the 800 to your raw image width
        data[4] = float(data[4])* 600 ##### change the 600 to your raw image height
        bbox = [data[1],data[2],data[3],data[4]]
        ann = {'id': id_counter,
            'bbox': bbox,
            'area': data[3] * data[4],
            'iscrowd': 0,
            'image_id': int(image_id),
            'category_id': int(data[0]) + 1            
        }
        out['annotations'].append(ann)
        id_counter = id_counter + 1 

def images_data(file_name):
    #id, height, width, file_name
    id = file_name.split('.')[0]
    file_name = id + '.jpg' ##### change '.jpg' to other image formats if the format of your image is not .jpg
    imgs = {'id': int(id),
            'height': 600, ##### change the 600 to your raw image height
            'width': 800, ##### change the 800 to your raw image width
            'file_name': file_name,
            "coco_url": "", 
            "flickr_url": "", 
            "date_captured": 0, 
            "license": 0
    }
    out['images'].append(imgs)
           
    
            

if __name__ == '__main__':
    files = os.listdir(FILE_PATH)
    files.sort()
    for file in files:
        whole_path = os.path.join(FILE_PATH,file)
        annotations_data(whole_path, file.split('.')[0])
        images_data(file)

    
    with open('instances_merge_train.json', 'w') as outfile: ##### change the str to the json file name you want
      json.dump(out, outfile, separators=(',', ':'))