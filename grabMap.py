#!/usr/bin/python

import os
import config
import requests
from PIL import Image, ImageDraw

# import requests
# from PIL import Image
# from StringIO import StringIO

# r = requests.get('https://example.com/image.jpg')
# i = Image.open(StringIO(r.content))

import shutil

lat=43.064268
lng=-89.406771
pixels_to_shift=400
lat_shift=pixels_to_shift*(-0.98039216)
lng_shift=pixels_to_shift*(1.33333333)
strides=4
lat_list=[ str(lat+x*(lat_shift)*0.000001) for x in range(strides) ]
lng_list=[ str(lng+x*(lng_shift)*0.000001) for x in range(strides) ]
map_size=500
zoom_level=20
image_format="png32"
map_num=0
large_size = strides*pixels_to_shift
large_image         = Image.new('RGBA', (large_size,large_size))
green_layer         = Image.new('RGBA', (large_size,large_size), (153,213,148))
orange_layer        = Image.new('RGBA', (large_size,large_size), (252,141,89))
green_boxes_mask_1  = Image.new('L',    (large_size,large_size), 0)
green_boxes_mask_2  = Image.new('L',    (large_size,large_size), 0)
orange_boxes_mask_1 = Image.new('L',    (large_size,large_size), 0)
orange_boxes_mask_2 = Image.new('L',    (large_size,large_size), 0)
for i_lat, lat in enumerate(lat_list):
    for i_lng, lng in enumerate(lng_list):
        url="".join(map(str,["https://maps.googleapis.com/maps/api/staticmap?center=",
                             lat,
                             ",",
                             lng,
                             "&zoom=",
                             zoom_level,
                             "&size=",
                             map_size,
                             "x",
                             map_size,
                             "&format=",
                             image_format,
                             "&maptype=satellite&key=",
                             config.api_key]))

        out_filename="img_{:03d}.png".format(map_num)
        if not os.path.isfile(out_filename):
            response = requests.get(url, stream=True)
            with open(out_filename , 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
        map_num+=1
        this_image=Image.open(out_filename,'r')
        large_image.paste(this_image,(i_lng*pixels_to_shift,i_lat*pixels_to_shift))

large_image_2 = large_image.copy()

boxes=[ [408,12,500,160],
        [535,27,626,140],
        [633,20,708,150],
        [728,19,804,135],
        [831,28,907,144],
        [954,0,1025,168],
        [432,481,504,632],
        [564,464,640,614],
        [743,455,817,567],
        [690,588,733,668],
        [884,457,961,623],
        [620,736,667,803],
        [684,744,788,804],
        [851,730,1031,817] ]

tile_size=500

for box in boxes:
    if box[3]//tile_size != box[1]//tile_size or box[2]//tile_size != box[0]//tile_size:
        draw = ImageDraw.Draw(orange_boxes_mask_1)
        draw.rectangle(box,fill=192)
    else:
        draw = ImageDraw.Draw(green_boxes_mask_1)
        draw.rectangle(box,fill=192)
        draw = ImageDraw.Draw(green_boxes_mask_2)
        draw.rectangle(box,fill=192)

large_image = Image.composite(green_layer, large_image, green_boxes_mask_1)
large_image = Image.composite(orange_layer, large_image, orange_boxes_mask_1)

for height in range(0, large_size, tile_size):
    draw = ImageDraw.Draw(large_image) 
    draw.line((0, height, large_size, height), fill="#ff0000", width=4)
for width  in range(0, large_size, tile_size):
    draw = ImageDraw.Draw(large_image) 
    draw.line((width, 0, width, large_size), fill="#ff0000", width=4)


for box in boxes:
    if (box[3]//tile_size != box[1]//tile_size or box[2]//tile_size != box[0]//tile_size) and ((box[3]+250)//tile_size != (box[1]+250)//tile_size or (box[2]+250)//tile_size != (box[0]+250)//tile_size):
        draw = ImageDraw.Draw(orange_boxes_mask_2)
        draw.rectangle(box,fill=192)
    else:
        draw = ImageDraw.Draw(green_boxes_mask_2)
        draw.rectangle(box,fill=192)

large_image_2 = Image.composite(green_layer, large_image_2, green_boxes_mask_2)
large_image_2 = Image.composite(orange_layer, large_image_2, orange_boxes_mask_2)

for height in range(250, large_size, tile_size):
    draw = ImageDraw.Draw(large_image_2) 
    draw.line((0, height, large_size, height), fill="#ff0000", width=4)
for width  in range(250, large_size, tile_size):
    draw = ImageDraw.Draw(large_image_2) 
    draw.line((width, 0, width, large_size), fill="#ff0000", width=4)

large_image_2.save("Large_Image_2.png", "PNG")

quit()
