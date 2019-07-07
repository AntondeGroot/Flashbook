# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 21:18:48 2019

@author: Anton
"""
import PIL
import pylab
import wx
import textwrap
pylab.ioff() 
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.pyplot import cm
import numpy as np
from pathlib import Path
# Get data
import json
import time
from datetime import datetime
import imageoperations as imop

#% FUNCTIONS
def GetValues(timedict,datethreshold):
    totaldict = {}
    today = time.strftime("%d%m%y")
    
    dtoday = datetime.strptime(today,"%d%m%y")
    
    for date in timedict.keys():
        dthen = datetime.strptime(date,"%d%m%y")
        if (dtoday-dthen).days < datethreshold: #if within N days
            for book in timedict[date]:
                value = timedict[date][book]
                if book in totaldict.keys():
                    totaldict[book] += value
                else:
                    totaldict[book] = value
    
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

def drawcard(legend):
    from matplotlib.ticker import MaxNLocator
    
    """ legend has a Color/Hatch tuple """
    
    #y_values = SecToMin(y_values) # convert seconds to minutes
    #legend_list = [legend_dict[bookname] for bookname in x_values]
    
    # sort tuples X-values/Y-values/Legend by Y-values
    #x_it, y_it, legend_it = iter(x_values),iter(y_values),iter(legend_list)
    #tuple_list = [(next(x_it), next(y_it), next(legend_it)) for _ in x_values]
    #tuple_list.sort(key=takeSecond)
    #x_values_sorted = [entry[0] for entry in tuple_list]
    #y_values_sorted = [entry[1] for entry in tuple_list]
    #legend_list_sorted = [entry[2] for entry in tuple_list]
    
    CARD_SIZE = (4,2)
    
    fig = Figure(figsize=CARD_SIZE, dpi=100)
    fig.patch.set_facecolor((254/255, 240/255, 231/255, 1)) #flashbook theme color rescaled to [0,1]
    ax = fig.gca()
    
    y_values = []
    for i,item in enumerate(legend): 
        #for i,bookname in enumerate(x_values_sorted):
        #legend_entry = legend_list_sorted[i]
        #Color = legend_entry[0]
        #Hatch = legend_entry[1]
        Bookname = item[0]
        minutes = SecToMin(item[1])
        y_values.append(minutes)
        Hatch = item[2]
        Color = item[3]
        Edgecolor = item[4]
        ax.bar(Bookname, minutes, edgecolor=Edgecolor, color=Color ,width=1,align='center', 
               fill=True, linestyle='--', snap=False, hatch=Hatch)    
    ax.axis('on')
    
    
    no_values = not legend
    max_value = max(y_values, default=0)
    
    # set y axis
    if no_values:
        ax.get_yaxis().set_visible(False)
    else:
        if len(y_values) == 1:
            ax.margins(x=0.75)
        #Set limit of Y axis: The max should be 10 Minutes unless it has been surpassed
        if max_value < 10:
            ax.set_ylim(top=10)
        else:
            ax.yaxis.set_major_locator(MaxNLocator(integer=True,steps=[1,1.5,2,5,10],nbins=7))
    
    yticks = ax.get_yticks().tolist()
    new_yticks = []
    double_digit_hour = len(str(int(max(yticks)/60))) > 1
    for tick in yticks:
        hours = int(tick/60)
        minutes = int(tick-hours*60)        
        if tick != 0:
            if double_digit_hour:
                # if you have 10 hrs, then the steps should not include 1h30m
                new_yticks.append(f"{hours}h")
            else:
                # if you have less than 10 hrs, then you may include the minutes
                if hours > 0 and minutes > 0:
                    new_yticks.append(f"{hours}h{minutes}m")
                elif hours > 0 and minutes == 0:
                    new_yticks.append(f"{hours}h")
                elif hours == 0:
                    new_yticks.append(f"{minutes}m")    
        else:
            # exclude origin tick
            new_yticks.append('')
    
    ax.set_yticklabels(new_yticks)
    ax.get_xaxis().set_visible(False)
    fig.subplots_adjust(left=0.3)
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    return PIL.Image.frombytes("RGB", size, raw_data, decoder_name='raw', )


def seconds_to_timestring(seconds): 
    """Convert nr Seconds to a string of one of the following formats: 
        if it contains Hours:   at least | '1Hours00Minutes'           | no seconds
        if it contains Minutes: at least | '1Minutes00Seconds'         |
        if it contains Seconds: at least | '1Seconds'                  |
        
        The variable Seconds will get subtracted unless we can no longer subtract [HOURS] and [MINUTES] and we know that the remainder is [SECONDS]
    """
    if seconds:
        txt = ""
        hours = int(seconds/3600)
        if hours > 0:
            txt += f"{hours}h"
            seconds = seconds - hours*3600 
        
        minutes = int(seconds/60)
        if minutes > 0 or hours != 0:
            if len(str(minutes)) == 1 and hours != 0:
                txt += f"0{minutes}m"
            else:
                txt += f"{minutes}m"
            seconds = seconds - minutes*60
            
        seconds = int(seconds) #round off
        if seconds >= 0 and hours == 0:
            if len(str(seconds)) == 1 and (minutes != 0 or hours != 0):
                txt += f"0{seconds}s"
            else:
                txt += f"{seconds}s"
        
        return txt
    else:
        return ''
def drawlegend(legend):
    
    
    labels = []
    handles = []
    # legend squares
    for item in legend:
        Book = item[0]
        Seconds = item[1]
        Hatch = item[2]
        Color = item[3]
        Edgecolor = item[4]
        handles.append(mpatches.Patch(edgecolor=Edgecolor,facecolor=Color,hatch=Hatch))
        if Seconds:
            labels.append(textwrap.fill(f"{Book} ({ seconds_to_timestring(Seconds)})",40))
        else:
            labels.append(textwrap.fill(f"",40))
    
    #handles = [mpatches.Patch(edgecolor='black',facecolor=c,hatch=next(hatch_it),label="hallo") for c in colors]
    
    #totalvalue_it  = iter(totalvalues)
    #labels = totalbooks
    #for item in legend
    #labels = [textwrap.fill(f"{x} ({ seconds_to_timestring(next(totalvalue_it))})",40) for x in totalbooks]
    legend = plt.legend( handles, labels, loc=2, framealpha=False, frameon=True, markerscale=3.6, markerfirst=True, fontsize=12 )
    
    fig = Figure( figsize=[4, 40], dpi=100 )
    fig = legend.figure
    fig.set_size_inches( 8, 30 )
    fig.tight_layout()
    fig.canvas.draw()
    ax = fig.gca()
    ax.axis('off')
    ax.get_xaxis().set_visible(False)
    fig.patch.set_facecolor( (254/255, 240/255, 231/255, 1) )
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    img = PIL.Image.frombytes("RGB", size, raw_data, decoder_name='raw', )
    #cut down image
    color = ( 254, 240, 231 )
    img = imop.cropimage(img, 0, backgroundcolor=color, border=5)
    img = imop.cropimage(img, 1, backgroundcolor=color, border=15)
    #img.show()
    return img

def sortsubdata(data):
    totalbooks = []
    totalvalues = []
    bookstoday = []
    valuestoday = []
    #first order FC entries, then FB then combine the two
    for book,value in zip(data[0],data[1]):
        if book not in totalbooks:
            totalbooks.append(book)
            totalvalues.append(value)
    
    
    books_it  = iter(totalbooks)
    values_it = iter(totalvalues)
    
    
    X2 = [(next(books_it),next(values_it)) for _ in totalbooks] #[('book1',t1) , ... , ('bookN',tN)]
    # sort list with 'key', this way we can sort the list by the second element: the amount of time spend
    X2.sort( key=takeSecond )
    
    bookstoday = []
    valuestoday = []
    #first order FC entries, then FB then combine the two
    for book,value in zip(data[2],data[3]):
        if book not in bookstoday:
            bookstoday.append(book)
            valuestoday.append(value)
    
    
    books_it  = iter(bookstoday)
    values_it = iter(valuestoday)
    
    
    X3 = [(next(books_it),next(values_it)) for _ in bookstoday] #[('book1',t1) , ... , ('bookN',tN)]
    # sort list with 'key', this way we can sort the list by the second element: the amount of time spend
    X3.sort( key=takeSecond )
    
    return X2,X3

def SecToMin(input_):  
    if type(input_) == list:
        return [round(seconds/60,1) for seconds in input_]
    if type(input_) == float or type(input_) == int:
        return round(input_/60,1)
def CreateGraph(self):
    DATE_THRESHOLD = self.GraphNdays
    
    #load data
    try:
        with open(str(Path(self.dirsettings,"timecount_flashbook.json")), 'r') as file:
            timedict_fb = json.load(file)
        file.close()
    except:
        timedict_fb = {}
    try:
        with open(str(Path(self.dirsettings,"timecount_flashcard.json")), 'r') as file2:
            timedict_fc = json.load(file2)
        file2.close()
    except:
        timedict_fc = {}
    
    #% COLLECT ALL DATA
    data_fb = GetValues(timedict_fb, DATE_THRESHOLD)
    data_fc = GetValues(timedict_fc, DATE_THRESHOLD)    
    totalbooks_fb = data_fb[0]
    totalbooks_fc = data_fc[0]
    
    # COMBINE DATA
    fb_sorted_total, fb_sorted_today = sortsubdata(data_fb) #(books,seconds) tuples ordered from small to large
    fc_sorted_total, fc_sorted_today = sortsubdata(data_fc) 
    print()
    print(f"sorted today = {fb_sorted_today}")
    unique_books = set(totalbooks_fb + totalbooks_fc)
    print(f"uniq = {unique_books}")
    
    """
    totalvalues = []
    totalbooks  = []
    for i,data in enumerate(sortedDATA):
        book = data[0]
        value = data[1]
        if book not in totalbooks:
            totalbooks.append(book)
            totalvalues.append(value)
    """     
    values_exist = fb_sorted_total + fc_sorted_total
    if values_exist:
        #Set Colormap
        lvlC = np.linspace(0.07, 0.97, len(unique_books)) #to exclude colors like Black from appearing in the legend
        colorlist = cm.nipy_spectral(lvlC)           
        
        #CREATE LEGEND: colors and hatches (pattern displayed on barplots)
        hatch_it = iter(["","/////","---","\\\\\\\\\\"]*len(unique_books)) # is superfluous but that is okay  
        
        color_it = iter(colorlist)
        
        
        seen = {}
        legend = []
        legend_graph_fb = []
        legend_graph_fb_today = []
        legend_graph_fc = []
        legend_graph_fc_today = []
        edgecolor = 'black'
        # first total
        for entry in fb_sorted_total:
            
            book, seconds = entry
            print(f"fb book = {book}")
            #make sure the same booktitles have the same colors and hatches
            if book in seen:
                dict_ = seen[book]
                hatch = dict_['hatch']
                color = dict_['color']
            else:
                hatch = next(hatch_it)
                color = next(color_it)
                seen[book] = {'hatch':hatch,'color':color}
            legend.append([book,seconds,hatch,color,edgecolor])
            legend_graph_fb.append([book,seconds,hatch,color,edgecolor])
        print(f"seen keys = {seen.keys()}")
        #separation between the two
        legend.append(['',None,None,(254/255, 240/255, 231/255, 1),None])
        
        for entry in fc_sorted_total:
            book, seconds = entry
            print(f"fc book = {book}")
            #make sure the same booktitles have the same colors and hatches
            if book in seen:
                dict_ = seen[book]
                hatch = dict_['hatch']
                color = dict_['color']
                print(f"book is in seen for {book}\n"*10)
            else:
                hatch = next(hatch_it)
                color = next(color_it)
                seen[book] = {'hatch':hatch,'color':color}
            legend.append([book,seconds,hatch,color,edgecolor])
            legend_graph_fc.append([book,seconds,hatch,color,edgecolor])
        # then today 
        for entry in fb_sorted_today:
            
            book, seconds = entry
            print(f"fb book = {book}")
            #make sure the same booktitles have the same colors and hatches
            if book in seen:
                dict_ = seen[book]
                hatch = dict_['hatch']
                color = dict_['color']
            else:
                print(f"error\n"*20)
                #hatch = next(hatch_it)
                #color = next(color_it)
                #seen[book] = {'hatch':hatch,'color':color}
            legend_graph_fb_today.append([book,seconds,hatch,color,edgecolor])
        for entry in fc_sorted_today:
            
            book, seconds = entry
            print(f"fb book = {book}")
            #make sure the same booktitles have the same colors and hatches
            if book in seen:
                dict_ = seen[book]
                hatch = dict_['hatch']
                color = dict_['color']
            else:
                print(f"error\n"*20)
                #hatch = next(hatch_it)
                #color = next(color_it)
                #seen[book] = {'hatch':hatch,'color':color}
            legend_graph_fc_today.append([book,seconds,hatch,color,edgecolor])
        print(f"seen keys = {seen.keys()}")
        
        
        print(f" seen = {seen}")    
        print("data = ")
        
        im5 = drawlegend(legend)
        
        
        
        
        
        
        #CREATE TEXT IMAGES
        # create columnlabels
        txt1 = textcard("Today",3.5,2)
        txt1 = imop.cropimage_wh(txt1, backgroundcolor=(254,240,231), border=5)
        txt2 = textcard(f"Last {DATE_THRESHOLD} days", 3,2)
        txt2 = imop.cropimage_wh(txt2, backgroundcolor=(254,240,231), border=5)
        # rowlabels
        txt3 = textcard("Flashbook",2,4).rotate(90, expand = 1)
        txt3 = imop.cropimage_wh(txt3, backgroundcolor=(254,240,231), border=5)
        txt4 = textcard("Flashcard",2,4).rotate(90, expand = 1)
        txt4 = imop.cropimage_wh(txt4, backgroundcolor=(254,240,231), border=5)
        
        
        #CREATE IMAGES
        if totalbooks_fb:
            im1 = drawcard(legend_graph_fb_today)
            im1 = imop.cropimage_wh(im1, backgroundcolor=(254,240,231), border=10)
            im2 = drawcard(legend_graph_fb)
            im2 = imop.cropimage_wh(im2, backgroundcolor=(254,240,231), border=10)            
            im1_w,im1_h = im1.size
            im2_w,im2_h = im2.size
        else:
            im1_w, im1_h, im2_w, im2_h = 0,0,0,0
            
        if totalbooks_fc:
            im3 = drawcard(legend_graph_fc_today)
            im3 = imop.cropimage_wh(im3, backgroundcolor=(254,240,231), border=10)
            im4 = drawcard(legend_graph_fc)
            im4 = imop.cropimage_wh(im4, backgroundcolor=(254,240,231), border=10)
            im3_w, im3_h = im3.size
            im4_w, im4_h = im4.size
        else:
            im3_w, im3_h, im4_w, im4_h = 0,0,0,0
        
        #im5 = drawlegend(totalbooks,totalvalues,legendbackup,hatchlist)
        im5_w, im5_h = im5.size
        
        
        TOTAL_WIDTH = max(txt3.width, txt4.width) + max(im1_w, im3_w) + max(im2_w, im4_w) + im5_w
        TOTAL_HEIGHT = max(txt1.height, txt2.height) + max(im1_h, im3_h) + max(im2_h, im4_h)
        COLUMN1_RIGHT = max(txt3.width, txt4.width) + max(im1_w, im3_w)
        COLUMN2_RIGHT = max(txt3.width, txt4.width) + max(im1_w, im3_w) + max(im2_w, im4_w)
        # COMBINE ALL IMAGES TO A MOZAIC        
        im_combined = PIL.Image.new('RGB', (TOTAL_WIDTH, TOTAL_HEIGHT), (254,240,231))
        
        
        try: #right align the images
            im_combined.paste(im1,  (COLUMN1_RIGHT - im1.width, max(txt1.height, txt2.height)))
            im_combined.paste(im2,  (COLUMN2_RIGHT - im2.width, max(txt1.height, txt2.height)))
        except: pass
        try:
            im_combined.paste(im3,  (COLUMN1_RIGHT - im3.width, max(txt1.height, txt2.height) + max(im1_h, im2_h))) #txt1.height+h1))
            im_combined.paste(im4,  (COLUMN2_RIGHT - im4.width, max(txt1.height, txt2.height) + max(im1_h, im2_h)))
        except: pass
        
        im_combined.paste(im5,  (COLUMN2_RIGHT , int(txt2.height)))
        # add headers
        
        im_combined.paste( txt1, (int(COLUMN1_RIGHT - max(im1_w, im3_w)/2 - txt1.width/2), 0))
        im_combined.paste( txt2, (int(COLUMN2_RIGHT - max(im2_w, im4_w)/2 - txt2.width/2), 0 ))
        
        
        if totalbooks_fb:
            center_row_1 = max(txt1.height, txt2.height) + max(im1_h, im2_h)/2
            im_combined.paste( txt3, (0 , int(center_row_1 - txt3.height/2)-5 ))
        
        if totalbooks_fc:
            center_row_2 = max(txt1.height, txt2.height) + max(im1_h, im2_h) + max(im3_h, im4_h)/2
            im_combined.paste( txt4, (0 , int(center_row_2 - txt4.height/2) - 5 ))
            
        
    else:
        im_combined = PIL.Image.new('RGB', (1, 1), (254, 240, 231))
    
    #resize horizontally
    try:
        VirtualWidth, VirtualHeight = self.m_panelGraph.GetVirtualSize()
        VirtualWidth  = int(VirtualWidth * 0.95)
        VirtualHeight = int(VirtualHeight * 0.95)
            
        #resize image if it is too large
        ImageWidth, ImageHeight = im_combined.size
        if ImageWidth > VirtualWidth:
            ImageHeight = int(ImageHeight/ImageWidth*VirtualWidth)
            ImageWidth = VirtualWidth
        if ImageHeight > VirtualHeight:
            ImageWidth = int(ImageWidth/ImageHeight*VirtualHeight)
            ImageHeight = VirtualHeight

        im_combined = im_combined.resize((ImageWidth, ImageHeight), PIL.Image.ANTIALIAS)
    except:#if testgraph is used
        w,h = 1207,270
    #output
    
    #new_im = new_im.resize((w, h), PIL.Image.ANTIALIAS)
    BOOL = len(values_exist) > 0
    return BOOL, im_combined

def DisplayGraph(self):
    if self.panel0.IsShown():
        if self.m_menuItemGraph.IsChecked(): 
            show_image, graph_image = CreateGraph(self)
            if show_image:
                self.m_panelGraph.Show()
                image_out = wx.Image( graph_image.size)
                image_out.SetData( graph_image.tobytes() )
                self.m_bitmapGraph.SetBitmap(wx.Bitmap(image_out))
            else:
                self.m_panelGraph.Hide()
        else:
            self.m_panelGraph.Hide()
        self.Layout()

    
def testmodule():
    
    N = 50
    totalbooks = [f"book{i}" for i in range(N)]
    totalvalues = [i for i in range(N)]
    
    lvlC = np.linspace(0.03,0.97,len(totalbooks))
    #random.shuffle(lvlC)
    color = cm.Paired(lvlC)
    color = cm.nipy_spectral(lvlC)           
    
    #CREATE LEGEND: colors and hatches (pattern displayed on barplots)
    hatch_it = iter(["","/////","---","\\\\\\\\\\"]*len(totalbooks))  
    hatchlist = []
    for _ in enumerate(totalbooks):
        hatchlist.append(next(hatch_it))
    legend = {}
    for i,book in enumerate(totalbooks):   
        legend[book] = tuple((color[i],hatchlist[i] ))
    
    legendbackup = legend    
    im = drawlegend(totalbooks,totalvalues,legendbackup,hatchlist)
    #im.show()
    
#testmodule()

class testgraph():
    def __init__(self):
        self.dirsettings = r"C:\Users\Anton\AppData\Local\Flashbook\settings"
        self.GraphNdays = 30
        boolean, im = CreateGraph(self)
        #im.show()
#test = testgraph()

