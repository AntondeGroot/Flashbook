
filename = "gui_flashbook.py"
filename2 = "gui_flashbook3.py"
output = open(filename2, 'w')
f = open(filename, 'r')
read = f.readlines()

Cpath = r'u"D:\\Anton\\Documents\\' 
#Cpath = r'u"C:\\Users\\Anton\\.spyder-py3\\flashbook\\fin\\Flashbook-master\\gui design\\'
# every first item will be replaced by the one following it.
org = [
       ".AddSpacer",'.Add',
       Cpath + 'path_min"','path_min',
       Cpath + 'path_add"','path_add',
       Cpath + 'path_switch"','path_switch',
       '.AddLabelTool','.AddTool',
       '.AppendItem','.Append',
       '.SetSizeHintsSz','.SetSizeHints',
       '50, 1, 100','data, 1, data',
       'SetToolTipString','SetToolTip',
       'def __init__( self, parent )','def __init__( self, parent, data )',
       'wx.ArtProvider.GetBitmap( wx.ART_HELP_FOLDER,  )','data[0]',
       'wx.ArtProvider.GetBitmap( wx.ART_REDO,  )','data[1]',
       'self.m_notebook.AddPage( self.m_panel40, u"a page", True )','self.m_notebook.AddPage( self.m_panel40, u"General", False )',
       'self.m_notebook.AddPage( self.m_panel41, u"a page", False )','self.m_notebook.AddPage( self.m_panel41, u"Flashbook", False )',
       'self.m_notebook.AddPage( self.m_panel42, u"a page", False )','self.m_notebook.AddPage( self.m_panel42, u"Flashcard", False )',
       'self.m_notebook.AddPage( self.m_panel43, u"a page", False )','self.m_notebook.AddPage( self.m_panel43, u"Synchronize", False )',
       'self.m_textCtrlDelBook = wx.TextCtrl( self.m_panel26, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )','self.m_textCtrlDelBook = wx.TextCtrl( self.m_panel26, wx.ID_ANY, data, wx.DefaultPosition, wx.DefaultSize, 0 )'
       ]
a = []
for i in read:  
    k = 0
    for j in range(int(len(org)/2)):
        # the string.replace() function don't do the change at place
        # it's return a new string with the new changes.
        
        i = i.replace(org[k],org[k+1])
        k += 2
    a.append(i)

for page in a:
    #print(page)
    output.write(page)
f.close()   
output.close()
import os
os.remove(filename)
os.rename(filename2, filename)
