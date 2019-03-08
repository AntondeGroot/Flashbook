# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 21:18:48 2019

@author: Anton
"""

import PIL
import pylab

pylab.ioff() 

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.pyplot import cm
import numpy as np

# Get data
timedict_fb = {"01": {"Neurofysica 1": 1, "book2": 2, "book3": 3,"book4": 4},"02": {"book1": 10, "book2": 20, "book5": 300},"03": {"book5" : 5}}
timedict_fc = {"01": {"Book1": 10, "book2": 2, "book3": 3,"book4": 4},"02": {"book1": 10, "book7": 200, "book5": 300},"03": {"book6" : 5}}



#% FUNCTIONS
def GetValues(timedict):
    totaldict = {}
    for date in timedict.keys():
        for book in timedict[date]:
            value = timedict[date][book]
            if book in totaldict.keys():
                totaldict[book] += value
            else:
                totaldict[book] = value
    totaldict
    
    today = "02"
    
    totalbooks = [book for book in totaldict.keys()]
    totalvalues = [value for value in totaldict.values()]
    if today in timedict.keys():
        todaybooks = [book for book in timedict[today].keys()]
        todayvalues = [value for value in timedict[today].values()]
    else:
        todaybooks = []
        todayvalues = []
    return (totalbooks,totalvalues,todaybooks, todayvalues)

def takeSecond(elem):
    return elem[1]

def textcard(TEXT,width,textpos):
    height_card = 0.5
    fig = Figure(figsize=[width, height_card],dpi=100)
    fig.patch.set_facecolor((254/255,240/255,231/255,1))
    ax = fig.gca()
    ax.plot([height_card, 0,0, height_card],color = (254/255,240/255,231/255,1))
    
    ax.axis('off')
    ax.get_xaxis().set_visible(False)
    ax.text(textpos/3+0.25, height_card/2,TEXT, fontsize = 20, horizontalalignment='center', verticalalignment='center',wrap = True)    
    
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    return PIL.Image.frombytes("RGB", size, raw_data, decoder_name='raw', )

def drawcard(X,Y,legend):
    
    
    height_card = 2
    fig = Figure(figsize=[4, height_card],dpi=100)
    fig.patch.set_facecolor((254/255,240/255,231/255,1)) #flashbook theme color rescaled to [0,1]
    ax = fig.gca()
    for i,_ in enumerate(X):
        ax.bar(X[i],Y[i],edgecolor = 'black', color = legend[i][0] ,width = 1,  align='center', fill=True,linestyle = '--',snap = False,hatch = hatchlist[i])    
    ax.axis('on')
    ax.get_xaxis().set_visible(False)
    
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    return PIL.Image.frombytes("RGB", size, raw_data, decoder_name='raw', )

def drawlegend(totalbooks,totalvalues,legendbackup,hatchlist):
    labels = totalbooks
    tv_it = iter(totalvalues)
    labels = [f"{x} -- {next(tv_it)}" for x in totalbooks]
    colors = [legendbackup[x] for x in totalbooks]
    
    
    f = lambda m,c : plt.plot([],[],marker="s", color=c, ls="none")[0]
    handles = [f("s", colors[i]) for i in range(len(colors))]
    hatch_it = iter(hatchlist)
    label_it = iter(labels)
    handles = [mpatches.Patch(facecolor=c,hatch=next(hatch_it),label=next(label_it)) for c in colors]
    #labels = list(legendbackup.keys())
    legend = plt.legend(handles, labels, loc=2, framealpha=1, frameon=False,markerscale=3.6,markerfirst = True,fontsize=15)
    
    height_card = 2
    fig = Figure(figsize=[4, 4],dpi=100)
    fig = legend.figure
    fig.patch.set_facecolor((254/255,240/255,231/255,1))
    
    ax = fig.gca()
    ax.axis('off')
    ax.get_xaxis().set_visible(False)
    
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    return PIL.Image.frombytes("RGB", size, raw_data, decoder_name='raw', )


def sortsubdata(data):
    temp1 = data[0]
    temp2 = data[1]
    totalbooks2 = []
    totalvalues2 = []
    #first order FC entries, then FB then combine the two
    for i,x in enumerate(temp1):
        if x not in totalbooks2:
            totalbooks2.append(x)
            totalvalues2.append(temp2[i])
    
    tb_it = iter(totalbooks2)
    tv_it = iter(totalvalues2)
    X2 = [(next(tb_it),next(tv_it)) for _ in totalbooks2]
    #%
    # sort list with key
    X2.sort(key=takeSecond)
    return X2


#% COLLECT ALL DATA
data_fb = GetValues(timedict_fb)
data_fc = GetValues(timedict_fc)    
# COMBINE DATA
X = sortsubdata(data_fc) + sortsubdata(data_fb)

totalvalues = []
totalbooks = []
for i,x in enumerate(X):
    if x[0] not in totalbooks:
        totalbooks.append(x[0])
        totalvalues.append(x[1]) 


#variable n should be number of curves to plot (I skipped this earlier thinking that it is obvious when looking at picture - sorry my bad mistake xD): n=len(array_of_curves_to_plot)
color = cm.nipy_spectral(np.linspace(0,1,len(totalbooks)))


#CREATE LEGEND: colors and hatches (pattern displayed on barplots)
hatch_it = iter(["","/","-","\\"]*len(totalbooks))  
hatchlist = []
for _ in enumerate(totalbooks):
    hatchlist.append(next(hatch_it))


legend = {}
legendtoday = {}

for i,book in enumerate(totalbooks):   
    legend[book] = tuple((color[i],hatchlist[i] ))

#%%

legendbackup = legend    
#%


#CREATE TEXT IMAGES
txt1 = textcard("Today",4,4)
txt2 = textcard(f"Last {10} days", 4,4)
txt3 = textcard("Flashbook",2,4).rotate(90, expand = 1)
txt4 = textcard("Flashcard",2,4).rotate(90, expand = 1)

#CREATE IMAGES
#colorlist = [legend[x] for x in data_fb[2]]
im1 = drawcard(data_fb[2],data_fb[3],colorlist)
im2 = drawcard(data_fb[0],data_fb[1],colorlist)
im3 = drawcard(data_fc[2],data_fc[3],colorlist)


X_it = iter(data_fc[0])
Y_it  = iter(data_fc[1])

legend_it = iter(list(legend.values()))
X = [(next(X_it),next(Y_it),next(legend_it)) for x in range(len(data_fc[0]))]
X.sort(key=takeSecond)
X_fc       = [x[0] for x in X]
Y_fc       = [x[1] for x in X]
legend_fc  = [x[2] for x in X]

im4 = drawcard(X_fc,Y_fc,legend_fc)
im5 = drawlegend(totalbooks,totalvalues,legendbackup,hatchlist)
#colors = list(legendbackup.values())


# COMBINE ALL PICS
width = im1.width + im2.width + txt3.width+im5.width
height = im1.height*2 + txt1.height
new_im = PIL.Image.new('RGB', (width, height), (254,240,231))
new_im.paste(txt1, (txt3.width,0))
new_im.paste(txt3, (0,txt1.height))
new_im.paste(txt4, (0,txt1.height+txt3.height))
new_im.paste(txt2, (txt3.width + txt1.width,0))
new_im.paste(im1, (txt3.width,txt1.height))
new_im.paste(im2, (txt3.width+im1.width,txt2.height))
new_im.paste(im3, (txt3.width,txt1.height+im1.height))
new_im.paste(im4, (txt3.width+im1.width ,txt2.height+im2.height))
new_im.paste(im5, (txt3.width+im1.width+im2.width ,txt2.height))
new_im.paste
new_im.show()
