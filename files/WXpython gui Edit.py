
versionnumber = '1.5.0'


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
       'wx.HyperlinkCtrl','wx.adv.HyperlinkCtrl',
       'wx.HL_DEFAULT_STYLE','wx.adv.HL_DEFAULT_STYLE',
       '50, 1, 100','data, 1, data',
       'SetToolTipString','SetToolTip',
       'def __init__( self, parent )','def __init__( self, parent, data )',
       'wx.ArtProvider.GetBitmap( wx.ART_HELP_FOLDER,  )','data[0]',
       'wx.ArtProvider.GetBitmap( wx.ART_REDO,  )','data[1]',
       'self.m_notebook.AddPage( self.m_panel40, u"a page", True )','self.m_notebook.AddPage( self.m_panel40, u"General", False )',
       'self.m_notebook.AddPage( self.m_panel41, u"a page", False )','self.m_notebook.AddPage( self.m_panel41, u"Flashbook", False )',
       'self.m_notebook.AddPage( self.m_panel42, u"a page", False )','self.m_notebook.AddPage( self.m_panel42, u"Flashcard", False )',
       'self.m_notebook.AddPage( self.m_panel43, u"a page", False )','self.m_notebook.AddPage( self.m_panel43, u"Synchronize", False )',
       'self.m_textCtrlDelBook = wx.TextCtrl( self.m_panel26, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )','self.m_textCtrlDelBook = wx.TextCtrl( self.m_panel26, wx.ID_ANY, data, wx.DefaultPosition, wx.DefaultSize, 0 )',
       'self.m_textCtrlComBooks = wx.TextCtrl( self.m_panel26, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,70 ), wx.TE_MULTILINE )','self.m_textCtrlComBooks = wx.TextCtrl( self.m_panel26, wx.ID_ANY, data[0], wx.DefaultPosition, wx.Size( -1,70 ), wx.TE_MULTILINE )',
       'self.m_textCtrlCombinedFileName = wx.TextCtrl( self.m_panel26, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 430,-1 ), 0 )','self.m_textCtrlCombinedFileName = wx.TextCtrl( self.m_panel26, wx.ID_ANY, data[1], wx.DefaultPosition, wx.Size( 430,-1 ), 0 )',
       'self.m_textCtrl51Score = wx.TextCtrl( self.m_panel64, wx.ID_ANY, u"Your score is 100%", wx.DefaultPosition, wx.Size( 200,-1 ), 0|wx.NO_BORDER )','self.m_textCtrl51Score = wx.TextCtrl( self.m_panel64, wx.ID_ANY, data, wx.DefaultPosition, wx.Size( 200,-1 ), 0|wx.NO_BORDER )',
       'self.m_bitmap6 = wx.StaticBitmap( self.m_panel29, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SIMPLE_BORDER )','self.m_bitmap6 = wx.StaticBitmap( self.m_panel29, wx.ID_ANY, data[0], wx.DefaultPosition, wx.Size( -1,-1 ), wx.SIMPLE_BORDER )',
	   'self.m_bitmap7 = wx.StaticBitmap( self.m_panel29, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SIMPLE_BORDER )','self.m_bitmap7 = wx.StaticBitmap( self.m_panel29, wx.ID_ANY, data[1], wx.DefaultPosition, wx.Size( -1,-1 ), wx.SIMPLE_BORDER )',
       'self.m_bitmap8 = wx.StaticBitmap( self.m_panel29, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SIMPLE_BORDER )','self.m_bitmap8 = wx.StaticBitmap( self.m_panel29, wx.ID_ANY, data, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SIMPLE_BORDER )',
       'wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Edit the cards", pos = wx.DefaultPosition, size = wx.Size( 527,188 ), style = wx.DEFAULT_DIALOG_STYLE )','wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = data[0], pos = wx.DefaultPosition, size = wx.Size( 527,188 ), style = wx.DEFAULT_DIALOG_STYLE )',
       'self.m_textCtrl24 = wx.TextCtrl( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )','self.m_textCtrl24 = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[1], wx.DefaultPosition, wx.DefaultSize, 0 )',
       'self.m_textCtrl25 = wx.TextCtrl( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )','self.m_textCtrl25 = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[2], wx.DefaultPosition, wx.DefaultSize, 0 )',
       'self.m_textCtrl30 = wx.TextCtrl( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )','self.m_textCtrl30 = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[3], wx.DefaultPosition, wx.DefaultSize, 0 )',
       'self.m_bitmapAbout = wx.StaticBitmap( self.m_panel33, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 100,100 ), 0 )','self.m_bitmapAbout = wx.StaticBitmap( self.m_panel33, wx.ID_ANY, data, wx.DefaultPosition, wx.Size( 100,100 ), 0 )',
       'self.m_bitmap13 = wx.StaticBitmap( self.m_panel32, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )','self.m_bitmap13 = wx.StaticBitmap( self.m_panel32, wx.ID_ANY, data[0], wx.DefaultPosition, wx.DefaultSize, 0 )',
       'self.m_bitmap14 = wx.StaticBitmap( self.m_panel32, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )','self.m_bitmap14 = wx.StaticBitmap( self.m_panel32, wx.ID_ANY, data[1], wx.DefaultPosition, wx.DefaultSize, 0 )',
       'self.m_textCtrlQtext = wx.TextCtrl( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )','self.m_textCtrlQtext = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[2], wx.DefaultPosition, wx.DefaultSize, 0 )',
       'self.m_textCtrlQpic = wx.TextCtrl( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )','self.m_textCtrlQpic = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[3], wx.DefaultPosition, wx.Size( -1,-1 ), 0 )',
       'self.m_textCtrlAtext = wx.TextCtrl( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )','self.m_textCtrlAtext = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[4], wx.DefaultPosition, wx.DefaultSize, 0 )',
       'self.m_textCtrlApic = wx.TextCtrl( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )','self.m_textCtrlApic = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[5], wx.DefaultPosition, wx.DefaultSize, 0 )',
       'self.m_textCtrlTopic = wx.TextCtrl( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )','self.m_textCtrlTopic = wx.TextCtrl( self.m_panel32, wx.ID_ANY, data[6], wx.DefaultPosition, wx.DefaultSize, 0 )'
       ]
# sometimes a variable can change for example the Version number, this variable is unknown but everything left and right of it IS known
# the following will replace it and update it
fragments = ['self.m_staticText59 = wx.StaticText( self.m_panel33, wx.ID_ANY, ',', wx.DefaultPosition, wx.DefaultSize, 0 )']
fragments_middle = [f"'Version {versionnumber}'"]

a = []
for string in read:  
    k = 0
    for j in range(int(len(org)/2)):
        # the string.replace() function don't do the change at place
        # it's return a new string with the new changes.
        
        string = string.replace(org[k],org[k+1])
        k += 2
       
    
    for j in range(int(len(fragments)/2)): 
        k = 0
        if fragments[j] in string and fragments[j+1] in string:
            # indices
            leftside = string.find(fragments[j])+len(fragments[j])
            rightside = string.find(fragments[j+1])
            # replace
            var = string[leftside:rightside]     
            string = string.replace(var,fragments_middle[j])
            
            
            k += 2
    
    a.append(string) 
for page in a:
    #print(page)
    output.write(page)
f.close()   
output.close()
import os
os.remove(filename)
os.rename(filename2, filename)
