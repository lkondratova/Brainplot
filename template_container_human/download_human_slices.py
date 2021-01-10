#download human slices
import os
import requests
from PIL import Image, ImageDraw, ImageColor, ImageFilter, ImageFont
dirpath = os.getcwd()
if os.path.exists(dirpath+'/slice_numbers')==False:
    os.makedirs(dirpath+'/slice_numbers')
blank = 'https://scalablebrainatlas.incf.org/templates/NMM1103/coronal_T1/1103_3_0000.jpg'
# the slices # correspond to those in parentheses on https://scalablebrainatlas.incf.org/human/NMM1103
#the first slice 64
#the last slice 243
for i in range(64, 244):
    temp = blank[0:(len(blank) - (4+len(str(i))))]
    url = temp+str(i)+'.jpg'
    r = requests.get(url)
    with open(str(dirpath+'/slice_numbers'+'/'+str(i)+'.png'),'wb') as f: 
        f.write(r.content)