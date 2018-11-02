
filename = "gui_flashbook.py"
filename2 = "gui_flashbook3.py"
output = open(filename2, 'w')
f = open(filename, 'r')
read = f.readlines()

# every first item will be replaced by the one following it.
org = [
       ".AddSpacer",'.Add',
       'u"../../Flashbook Flashcard/Final/Flashbook-master/gui design/path_min"','path_min',
       'u"../../Flashbook Flashcard/Final/Flashbook-master/gui design/path_add"','path_add',
       'u"../../Flashbook Flashcard/Final/Flashbook-master/gui design/path_switch"','path_switch',
       '.AddLabelTool','.AddTool',
       '.AppendItem','.Append',
       '.SetSizeHintsSz','.SetSizeHints'
       ]

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