
filename = "gui_flashbook.py"
filename2 = "gui_flashbook3.py"
output = open(filename2, 'w')
f = open(filename, 'r')
read = f.readlines()

# every first item will be replaced by the one following it.
org = [
       ".AddSpacer",'.Add',
       r'u"D:\\Anton\\Documents\\path_min"','path_min',
       r'u"D:\\Anton\\Documents\\path_add"','path_add',
       r'u"D:\\Anton\\Documents\\path_switch"','path_switch',
       '.AddLabelTool','.AddTool',
       '.AppendItem','.Append',
       '.SetSizeHintsSz','.SetSizeHints',
       '50, 1, 100','data, 1, data',
       'SetToolTipString','SetToolTip',
       'def __init__( self, parent )','def __init__( self, parent, data )'
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
