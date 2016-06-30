from PIL import Image
from PIL import ImageOps
import os
path = r'H:\Project\crawler\html_crawler\pictures\cat'

path_list = []
file_list = []
for i in os.walk(path):
    path_list.append(i[0])
    file_list.append(i[2])

final_file_list = []
for i in range(1,len(path_list)):
    for j in range(0,len(file_list[i]),2):
        final_file_list.append(path_list[i]+'\\'+str(j)+'.jpg')

# for each in final_file_list:
#     print each


def clipimage(size):
    width = int(size[0])
    height = int(size[1])
    box = ()
    if(width > height):
        dx = width - height
        box = (dx/2, 0, height+dx/2, height)
    else:
        dx = height - width
        box = (0, dx/2, width, width+dx/2)
    return box

width_list = []
height_list = []
error_list = []
fp = open('sys_rpt//report.txt','w')
n = 1
for file_path in final_file_list:
    image = Image.open(file_path)
    print 'starting processing...'
    size = image.size
    box = clipimage(size)
    image = image.crop(box)
    image.thumbnail((50,50))
    image = ImageOps.grayscale(image)
    w,h = image.size
    width_list.append(w)
    height_list.append(h)
    if(w != h):
        fp.write(file_path+': width='+str(w)+', height='+str(h)+'\n')
    image.save('afterProcessCat//%s.jpg'%str(n),'jpeg')
    n+=2

width_list.sort()
height_list.sort()
fp.write(str(width_list[0])+'\n')
fp.write(str(height_list[0]))
fp.close()

