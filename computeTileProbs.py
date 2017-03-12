#!/usr/bin/python

from __future__ import division
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

class tiling:
    """A discrete tiling of the plane"""
    def __init__(self, x_offset = 0, y_offset = 0, x_width = 2048, y_width = 2048):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.x_width  = x_width
        self.y_width  = y_width

class square:
    """A box to test whether a given configuration is correctly segmenting"""
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def tiling_overlap(self, tiling):
        if ((self.x1-tiling.x_offset) // tiling.x_width) != ((self.x0-tiling.x_offset) // tiling.x_width) : 
            return True
        if ((self.y1-tiling.y_offset) // tiling.y_width) != ((self.y0-tiling.y_offset) // tiling.y_width) : 
            return True
        return False

tile_size=64
offset_list = [0, tile_size/2, tile_size/4, 3*tile_size/4]
color_list  = ["red", "blue", "green", "cyan"] * tile_size
size_and_probability_tuple_list = []
for square_size in range(tile_size):
    print("".join(map(str,[square_size+1, "/", tile_size])))
    probability_numerator   = [0]*len(offset_list)
    probability_denominator = [0]*len(offset_list)
    probability             = []
    for y0 in range(tile_size):
        for x0 in range(tile_size):
            my_square = square(x0, y0, x0+square_size, y0+square_size)
            tiling_overlap=[]
            for n,offset in enumerate(offset_list):
            #for n,offset in enumerate([0]): #Just one pass first (n=1)
                my_tiling = tiling(offset, offset, tile_size, tile_size) 
                tiling_overlap.extend([my_square.tiling_overlap(my_tiling)])
                if not all(tiling_overlap):
                    probability_numerator[n] += 1
                probability_denominator[n] += 1
    for n in range(len(offset_list)):
        probability.append(probability_numerator[n] / probability_denominator[n])
        size_and_probability_tuple_list.extend([(square_size,probability[n])])
    # print ("".join(map(str,["k = ", square_size,"; prob = ", probability])))

print (size_and_probability_tuple_list)
print (zip(*size_and_probability_tuple_list))
# print (color_list)

list_of_xs = []
list_of_ys = []
for n in range(len(offset_list)):
    xys=size_and_probability_tuple_list[n::len(offset_list)]
    list_of_xs.append([ xy[0] for xy in xys ])
    list_of_ys.append([ xy[1] for xy in xys ])

fig, ax = plt.subplots()
color_codes=['rs','b^', 'go', 'y*']
for n in range(len(offset_list)):
    plt.plot(list_of_xs[n],list_of_ys[n],color_codes[n])
plt.xlim([0,tile_size])
plt.xticks(range(0,tile_size+1,8))
tick_spacing=0.1
ax.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
plt.grid()
# plt.yticks(np.arange(0,1,8))

# alternative... kinda annoying
# fig, ax = plt.subplots()
# ax.scatter(*zip(*size_and_probability_tuple_list[::-1]),
#             s=8,
#             color=color_list[::-1],
#             alpha=0.5)

plt.savefig('4_pass.png', bbox_inches='tight')
plt.show()        

quit()
