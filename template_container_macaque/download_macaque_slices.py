#download macaque slices
import os
import requests
from PIL import Image, ImageDraw, ImageColor, ImageFilter, ImageFont
dirpath = os.getcwd()
os.makedirs(dirpath+'/slice_numbers')
blank = 'https://scalablebrainatlas.incf.org/templates/CBCetal15/coronal_b0/civm_rhesus_v1_b0_0000.jpg'
#the first slice 23
#the last slice 494
for i in range(23, 495):
    temp = blank[0:(len(blank) - (4+len(str(i))))]
    url = temp+str(i)+'.jpg'
    r = requests.get(url)
    with open(str(dirpath+'/slice_numbers'+'/'+str(i)+'.png'),'wb') as f: 
        f.write(r.content)