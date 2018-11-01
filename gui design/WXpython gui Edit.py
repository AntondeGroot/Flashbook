
filename = "gui_flashbook.py"
filename2 = "gui_flashbook3.py"
output = open(filename2, 'w')
f = open(filename, 'r')
read = f.readlines()


org = [".AddSpacer",'u"../../Flashbook Flashcard/Final/Flashbook-master/gui design/path_min"',
       'u"../../Flashbook Flashcard/Final/Flashbook-master/gui design/path_add"','u"../../Flashbook Flashcard/Final/Flashbook-master/gui design/path_switch"']
rep = ['.Add','path_min','path_add','path_switch']

a = []

for i in read:  
    for j in range(len(org)):
        print(i)
        # the string.replace() function don't do the change at place
        # it's return a new string with the new changes.
        
        i = i.replace(org[j],rep[j])
    a.append(i)

for page in a:
    print(page)
    output.write(page)
f.close()   
output.close()
import os
os.remove(filename)
os.rename(filename2, filename)
