from tkinter import *
from tkinter.colorchooser import *
import pygame
import os
from tkinter import filedialog
import PIL
from PIL import Image, ImageTk
import subprocess
import sys

#####################
screenBg = '#1a1a1a'

color_dark1 = '#1a1a1a'
color_dark2 = '#2d2d2d'
color_dark3 = '#494949'

color_white1 = '#e6e6e6'

color_blue1 = '#2d69ff'
color_blue2 = '#000037' #'#00142d'

color_font1 = '#1a1a1a'
color_font2 = '#e6e6e6'

color_pine1 = '#c28a2b'

color_selection =  "#ba0c0c" #"#ef9a03"
color_unselected = "#2d69ff"

#color_sceneObject = '#2d2d2d'
#color_engine = '#00142d'

border = 1
padSize = 1
#####################

root = Tk()
root.title('UDengine 2 - By Guilherme Teres Nunes')
#root.geometry('512x512')
root.state('zoomed')
root.configure(background=screenBg)

##################################################################
##                    GAME ENGINE PLAYER CALL                   ##
##################################################################
inGame = False
# need to fix!
def Call_engine():
    ## STANDALONE PLAY
    #os.spawn*
    #os.system("UDplayer.py")
    #subprocess.call("UDplayer.py", shell=True)
    #proc = subprocess.Popen([sys.executable,"UDplayer.py"])
    #subprocess.call([sys.executable, "UDplayer.py"])
    pass

##################################################################
##                  GAME ENGINE EDITOR INTERFACE                ##
##################################################################

##################################
topMenu = Menu(root, background='#000099', foreground='white', activebackground='#004c99', activeforeground='white')# background=color_dark1, activebackground=color_dark1)
topMenu.add_command(label='File')#, command=getColorHTML)
root.config(menu=topMenu)

# Default
m1 = PanedWindow(root, orient=VERTICAL,background=screenBg, borderwidth=border, sashpad=padSize) #, showhandle=True
m1.pack(fill=BOTH, expand=1)
#TOP
Paned_top = PanedWindow(m1,background=screenBg, borderwidth=border, sashpad=padSize)
m1.add(Paned_top)
#DOWN
Paned_down = PanedWindow(m1,background=screenBg, borderwidth=border, sashpad=padSize)
m1.add(Paned_down)

# CONFIGURATIONS
m1.paneconfig(Paned_top, minsize=64)
m1.paneconfig(Paned_down, minsize=64)

Pdown_objInfo = Frame(Paned_down)#Label(Paned_down, text='uee')
Pdown_objInfo.configure(bg=color_dark3)
Paned_down.add(Pdown_objInfo)

nodes = Canvas(Paned_down, background=color_blue2)
#nodes.create_rectangle(-100,-100,2512,2512,fill=color_blue1)
Paned_down.add(nodes)
Paned_down.paneconfig(Pdown_objInfo, minsize=256)
Paned_down.paneconfig(nodes, minsize=64)

#playGame = pygame.display.set_mode((512,512))

## Tentativa de por Pygame aqui. INICIO:
res = Frame(Paned_top, width=256,height=256)
Paned_top.add(res)
os.environ['SDL_WINDOWID'] = str(res.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
#screen = pygame.display.set_mode((256,256))
## FIM

Paned_sceneObj = Frame(Paned_top)#Label(Paned_top, text='Objects')
Paned_sceneObj.configure(bg=color_dark2)
Paned_top.add(Paned_sceneObj)

bottom = Canvas(Paned_top)#Label(Paned_top, text="Painel lateral Superior")
bottom.configure(bg=color_dark3)
Paned_top.add(bottom)
bottom.create_rectangle(10,22+2,312,130,fill=color_dark1)
bottom.create_rectangle(10,22+130,312,130+200,fill=color_dark1)
bottom.create_rectangle(10,22+331,312,330+200,fill=color_dark1)


Paned_top.paneconfig(res, minsize=64)
Paned_top.paneconfig(bottom, minsize=64)
Paned_top.paneconfig(Paned_sceneObj,minsize=128)

##################################################################
##                  GAME ENGINE EDITOR MECHANICS                ##
##################################################################

####             GAME ENGINE VARIABLES!
game = {'screenSize':[512,512],
        'fps':60}

scenes = []
defaultScene = {'name':'Scene01',
                'objects':[],
                'gravity':[True, 9.8],
                'background':'#00142d',
                'cameraPos':[0.0,0.0],
                'logicNode':[],
                'wireframe':False,
                'textures':{}}

scenes.append(defaultScene)

defaultObject = {'name':'Block',
                 'collision':False,
                 'dynamic':False,
                 'objectClass':'',
                 'material':None,
                 'parent':None,
                 'color':'#e6e6e6',
                 'renderLayer':2,
                 'position':[128.0,128.0],
                 'scale':[256.0,256.0],
                 'rotation':[0.0]}
scenes[0]['objects'].append(defaultObject)

currentSceneName ='None'
currentScene = None
currentSceneId = None

def getCurrentScene():
    global currentScene, currentSceneName, currentSceneId

    currentSceneName = 'Scene01'
    TmpcurrentScene = [[obj, ind] for ind, obj in enumerate(scenes) if obj['name'] == currentSceneName]

    if len(TmpcurrentScene) > 0:
        currentScene = TmpcurrentScene[0][0]
        currentSceneId = TmpcurrentScene[0][1]
    else:
        currentScene = None
        currentSceneId = None

getCurrentScene()
####             INTERFACE VARIABLES!
selectedObject = None

##################################################################
##                       TAB CONFIGURATION                      ##
##################################################################

def getColorHTML(start,title,see=None):
    global scenes, currentSceneId
    if currentSceneId != None:
        start = scenes[currentSceneId]['background']

    if see == 'objColor': # scenes[currentSceneId]['objects'][selectedObject[1]]['color']
        try:
            gc = askcolor(initialcolor=scenes[currentSceneId]['objects'][selectedObject[1]]['color'], title=title)
        except:
            gc = askcolor(initialcolor=start, title=title)
    else:
        gc = askcolor(initialcolor=start, title=title)

    if see == None:
        ue = gc[1]
        #print(ue)
        return(ue)
    elif see == 'bg':
        ue = gc[1]
        if currentSceneId != None:
            scenes[currentSceneId]['background'] = ue
            return(ue)
    elif see == 'objColor':
        ue = gc[1]
        if currentScene != None:
            try:
                scenes[currentSceneId]['objects'][selectedObject[1]]['color'] = ue
            except:
                pass
            return(ue)

####   SCENE AND GAME TAB
sg_title_scene = Label(bottom, text='Scene', bg=color_dark3, fg=color_font2)
sg_title_scene.place(x=10,y=2)

defaultSpacer = 42

sg_title_items1 = Label(bottom,text='Scene Name',bg=color_dark1, fg=color_font2)
sg_title_items1.place(x=32,y=32)
sg_title_items2 = Label(bottom,text='Gravity (bool)',bg=color_dark1, fg=color_font2)
sg_title_items2.place(x=32+128+32,y=32)

sg_entry_sname = Entry(bottom,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
sg_entry_sname.place(x=32,y=54)
sg_entry_gravity = Entry(bottom,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
sg_entry_gravity.place(x=64+128,y=54)

sg_title_items3 = Label(bottom,text='Background',bg=color_dark1, fg=color_font2)
sg_title_items3.place(x=32,y=32+defaultSpacer)
sg_title_items4 = Label(bottom,text='Gravity Speed',bg=color_dark1, fg=color_font2)
sg_title_items4.place(x=32+128+32,y=32+defaultSpacer)

sg_entry_bg = Button(bottom, text='Change BG', width=13, command=lambda:getColorHTML('#ffffff','Change Scene BG','bg'))#Entry(bottom,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
sg_entry_bg.place(x=32,y=54+defaultSpacer)
sg_entry_gravitySpeed = Entry(bottom,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
sg_entry_gravitySpeed.place(x=64+128,y=54+defaultSpacer)

# Game
sg_title_game = Label(bottom, text='Game', bg=color_dark3, fg=color_font2)
sg_title_game.place(x=10,y=5+defaultSpacer*3)

sg_title_items3 = Label(bottom,text='Screen Size',bg=color_dark1, fg=color_font2)
sg_title_items3.place(x=32,y=32+defaultSpacer*3)
sg_title_items4 = Label(bottom,text='Max FPS',bg=color_dark1, fg=color_font2)
sg_title_items4.place(x=32+128+32,y=32+defaultSpacer*3)

sg_entry_sizeX = Entry(bottom,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
sg_entry_sizeX.place(x=32,y=54+defaultSpacer*3)
sg_entry_maxFPS = Entry(bottom,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
sg_entry_maxFPS.place(x=64+128,y=54+defaultSpacer*3)

sg_title_items5 = Label(bottom,text='x',bg=color_dark1, fg=color_font2)
sg_title_items5.place(x=16,y=54+defaultSpacer*3)
sg_title_items6 = Label(bottom,text='y',bg=color_dark1, fg=color_font2)
sg_title_items6.place(x=16,y=54+defaultSpacer*4-22)
sg_entry_sizeY = Entry(bottom,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
sg_entry_sizeY.place(x=32,y=54+defaultSpacer*4-22)

## Camera Pos
sg_title_items7 = Label(bottom,text='Camera Position',bg=color_dark1, fg=color_font2)
sg_title_items7.place(x=32,y=32+defaultSpacer*5)

sg_entry_posX = Entry(bottom,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
sg_entry_posX.place(x=32,y=54+defaultSpacer*5)
sg_entry_posY = Entry(bottom,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
sg_entry_posY.place(x=32,y=54+defaultSpacer*6-22)

sg_title_items515 = Label(bottom,text='Wireframe',bg=color_dark1, fg=color_font2)
sg_title_items515.place(x=64+128,y=32+defaultSpacer*5)

sg_entry_wire = Entry(bottom,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
sg_entry_wire.place(x=64+128,y=54+defaultSpacer*5)

sg_title_items8 = Label(bottom,text='x',bg=color_dark1, fg=color_font2)
sg_title_items8.place(x=16,y=54+defaultSpacer*5)
sg_title_items9 = Label(bottom,text='y',bg=color_dark1, fg=color_font2)
sg_title_items9.place(x=16,y=54+defaultSpacer*6-22)

####### LOAD TEXTURES
sg_title_game = Label(bottom, text='Texture Material', bg=color_dark3, fg=color_font2)
sg_title_game.place(x=10,y=38+defaultSpacer*7)

def mat_load():
    global scenes

    ftype = [("PNG Image","*.png"),("JPG Image","*.jpg")]
    dialog = filedialog.askopenfilename(filetypes=ftype)
    print("Image directory: ",dialog)
    if currentScene != None:
        textName = dialog.split('/')
        textName = textName[len(textName)-1]
        ImageName = textName.split('.')[0]
        imgLoad = Image.open(dialog)
        imgLoad = imgLoad.resize((256,256), PIL.Image.ANTIALIAS)
        format = '.tif'
        imgLoad.save(ImageName+format)
        toAdd = pygame.image.load(ImageName+format)#.convert_alpha() # dialog
        scenes[currentSceneId]['textures'][textName] = [toAdd, dialog]

def mat_remove():
    global scenes
    name = mat_entry_name.get()
    if currentScene != None:
        if name in scenes[currentSceneId]['textures']:
            del scenes[currentSceneId]['textures'][name]
            mat_entry_name.delete(0, END)
            print('removed!')

def mat_showPreview():
    name = mat_entry_name.get()
    if currentScene != None:
        if name in scenes[currentSceneId]['textures']:
            fname = scenes[currentSceneId]['textures'][name][1]
            img = Image.open(fname)#PhotoImage(file=fname)
            img = img.resize((96,96), PIL.Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            mat_label_img.config(image=photo)
            mat_label_img.image = photo
            #print(scenes[currentSceneId]['textures'][name])

mat_entry_name = Entry(bottom,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
mat_entry_name.place(x=64+128,y=74+defaultSpacer*7)
mat_button_remove = Button(bottom, text='Remove',bg=color_white1,fg=color_font1, width=13, command=mat_remove)
mat_button_remove.place(x=64+128,y=22+54+defaultSpacer*10)
mat_button_load = Button(bottom, text='Load New',bg=color_white1,fg=color_font1, width=13, command=mat_load)
mat_button_load.place(x=32,y=22+54+defaultSpacer*10)

bottom.create_rectangle(64+128,55+defaultSpacer*8,64+128+100,100+55+defaultSpacer*8, fill=color_dark2)
mat_label_img = Label(bottom, bg=color_dark2)
mat_label_img.place(x=64+128,y=55+defaultSpacer*8)

mat_scroll = Scrollbar(bottom)
mat_scroll.place(x=128, y=74+defaultSpacer*7)

mat_list_text = Listbox(bottom,bg=color_white1,fg=color_font1, width=16, height=7, yscrollcommand=mat_scroll.set )
mat_list_text.place(x=32, y=74+defaultSpacer*7)

mat_scroll.config(command=mat_list_text.yview,width=22)

def SceneGameUpdate():
    # .delete(0, END)
    # .insert(0, 'mimimi')
    if currentScene != None:
        # Adicionar texturas na lista
        mat_list_text.delete(0, END)
        mat_list_text.insert(END, ' #Material List:')
        for obj in currentScene['textures']:
            mat_list_text.insert(END, obj)
        mat_entry_name.delete(0,END)

        #print(str(currentScene['wireframe']))
        sg_entry_wire.delete(0,END)

        sg_entry_sname.delete(0, END)
        sg_entry_sname.insert(0, currentScene['name'])
        sg_entry_gravity.delete(0, END)
        sg_entry_gravity.insert(0, str(currentScene['gravity'][0]))
        sg_entry_gravitySpeed.delete(0, END)
        sg_entry_gravitySpeed.insert(0, str(currentScene['gravity'][1]))
        #sg_entry_bg.delete(0, END)
        #sg_entry_bg.insert(0, currentScene['background'])
        sg_entry_posX.delete(0, END)
        sg_entry_posX.insert(0, str(currentScene['cameraPos'][0]))
        sg_entry_posY.delete(0, END)
        sg_entry_posY.insert(0, str(currentScene['cameraPos'][1]))

        sg_entry_sizeX.delete(0, END)
        sg_entry_sizeX.insert(0, str(game['screenSize'][0]))
        sg_entry_sizeY.delete(0, END)
        sg_entry_sizeY.insert(0, str(game['screenSize'][1]))
        sg_entry_maxFPS.delete(0, END)
        sg_entry_maxFPS.insert(0, str(game['fps']))

def SceneGameSync():
    global scenes
    error = False

    scenes[currentSceneId]['name'] = str(sg_entry_sname.get())
    #scenes[currentSceneId]['background'] = str(sg_entry_bg.get())

    mat_showPreview()

    lst = mat_list_text.get(ACTIVE)
    if lst != ' #Material List:':
        mat_entry_name.delete(0, END)
        mat_entry_name.insert(END, lst)

    mat_list_text.delete(0, END)
    mat_list_text.insert(END, ' #Material List:')

    for obj in currentScene['textures']:
        mat_list_text.insert(END, obj)
    try:
        scenes[currentSceneId]['cameraPos'] = [float(sg_entry_posX.get()),float(sg_entry_posY.get())]
        scenes[currentSceneId]['gravity'][0] = bool(sg_entry_gravity.get())
        scenes[currentSceneId]['gravity'][1] = float(sg_entry_gravitySpeed.get())
        scenes[currentSceneId]['wireframe'] = bool(sg_entry_wire.get())
        game['screenSize'] = [float(sg_entry_sizeX.get()),float(sg_entry_sizeY.get())]
        game['fps'] = int(sg_entry_maxFPS.get())
    except:
        error = True
    if error:
        SceneGameUpdate()
        print('ops...')

##################################################################
##                          OBJECT TAB                          ##
##################################################################

####   SCENE AND GAME TAB
obj_title_ObjPanel = Label(Pdown_objInfo, text='Object Panel', bg=color_dark3, fg=color_font2)
obj_title_ObjPanel.place(x=0,y=0)

defaultSpacer = 42

tmpX,tmpY = 32, 32
obj_title_items1 = Label(Pdown_objInfo,text='Object Name',bg=color_dark3, fg=color_font1)
obj_title_items1.place(x=tmpX,y=tmpY)
obj_entry_oname = Entry(Pdown_objInfo,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
obj_entry_oname.place(x=tmpX,y=tmpY+22)

tmpX,tmpY = 32+120, 32
obj_title_items2 = Label(Pdown_objInfo,text='Collision (bool)',bg=color_dark3, fg=color_font1)
obj_title_items2.place(x=tmpX,y=tmpY)
obj_entry_col = Entry(Pdown_objInfo,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
obj_entry_col.place(x=tmpX,y=tmpY+22)

tmpX,tmpY = 32+120*2, 32
obj_title_items3 = Label(Pdown_objInfo,text='Dynamic (bool)',bg=color_dark3, fg=color_font1)
obj_title_items3.place(x=tmpX,y=tmpY)
obj_entry_dynamic = Entry(Pdown_objInfo,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
obj_entry_dynamic.place(x=tmpX,y=tmpY+22)

tmpX,tmpY = 32, 32+defaultSpacer
obj_title_items4 = Label(Pdown_objInfo,text="Obj Class(list,split=,)",bg=color_dark3, fg=color_font1)
obj_title_items4.place(x=tmpX,y=tmpY)
obj_entry_class = Entry(Pdown_objInfo,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
obj_entry_class.place(x=tmpX,y=tmpY+22)

tmpX,tmpY = 32+120, 32+defaultSpacer
obj_title_items5 = Label(Pdown_objInfo,text="Material",bg=color_dark3, fg=color_font1)
obj_title_items5.place(x=tmpX,y=tmpY)
obj_SelectedMat = StringVar()
obj_SelectedMat.set("None")
optionList = ["None"]
obj_entry_mat = OptionMenu(Pdown_objInfo, obj_SelectedMat, *optionList)#Entry(Pdown_objInfo,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
obj_entry_mat.config(height=1, width=9)
obj_entry_mat.place(x=tmpX,y=tmpY+22)

tmpX,tmpY = 32+120*2, 32+defaultSpacer
obj_title_items6 = Label(Pdown_objInfo,text="Parent Name",bg=color_dark3, fg=color_font1)
obj_title_items6.place(x=tmpX,y=tmpY)
obj_entry_par = Entry(Pdown_objInfo,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
obj_entry_par.place(x=tmpX,y=tmpY+22)

tmpX,tmpY = 32+120, 32+defaultSpacer*2
obj_title_items7 = Label(Pdown_objInfo,text="Color",bg=color_dark3, fg=color_font1)
#obj_title_items7.place(x=tmpX,y=tmpY)
obj_entry_color = Button(Pdown_objInfo, text='Change Color', width=13, command=lambda:getColorHTML('#ffffff','Change Object Color','objColor')) #Entry(Pdown_objInfo,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
obj_entry_color.place(x=tmpX,y=tmpY+22)

tmpX,tmpY = 32+120*2, 32+defaultSpacer*2
obj_title_items8 = Label(Pdown_objInfo,text="Render Layer",bg=color_dark3, fg=color_font1)
obj_title_items8.place(x=tmpX,y=tmpY)
obj_entry_rlayer = Entry(Pdown_objInfo,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
obj_entry_rlayer.place(x=tmpX,y=tmpY+22)

##
obj_title_ObjTPanel = Label(Pdown_objInfo, text='Object Transform Panel', bg=color_dark3, fg=color_font2)
obj_title_ObjTPanel.place(x=0,y=32+defaultSpacer*3)

tmpX,tmpY = 32, 64+defaultSpacer*3
obj_title_items9 = Label(Pdown_objInfo,text="Position",bg=color_dark3, fg=color_font1)
obj_title_items9.place(x=tmpX,y=tmpY)
obj_entry_posX = Entry(Pdown_objInfo,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
obj_entry_posX.place(x=tmpX,y=tmpY+22)
obj_entry_posY = Entry(Pdown_objInfo,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
obj_entry_posY.place(x=tmpX,y=tmpY+22+22)

tmpX,tmpY = 32+120, 64+defaultSpacer*3
obj_title_items10 = Label(Pdown_objInfo,text="Scale",bg=color_dark3, fg=color_font1)
obj_title_items10.place(x=tmpX,y=tmpY)
obj_entry_scaleX = Entry(Pdown_objInfo,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
obj_entry_scaleX.place(x=tmpX,y=tmpY+22)
obj_entry_scaleY = Entry(Pdown_objInfo,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
obj_entry_scaleY.place(x=tmpX,y=tmpY+22+22)

tmpX,tmpY = 32+120*2, 64+defaultSpacer*3
obj_title_items11 = Label(Pdown_objInfo,text="Rotation",bg=color_dark3, fg=color_font1)
obj_title_items11.place(x=tmpX,y=tmpY)
obj_entry_rot = Entry(Pdown_objInfo,bg=color_white1,fg=color_font1, justify=CENTER,width=16)
obj_entry_rot.place(x=tmpX,y=tmpY+22)


def ObjInfoUpdate():
    if currentScene != None and selectedObject != None:

        obj_entry_scaleX.delete(0, END)
        obj_entry_scaleX.insert(END, str(selectedObject[0]['scale'][0]))
        obj_entry_scaleY.delete(0, END)
        obj_entry_scaleY.insert(END, str(selectedObject[0]['scale'][1]))
        obj_entry_posX.delete(0, END)
        obj_entry_posX.insert(END, str(selectedObject[0]['position'][0]))
        obj_entry_posY.delete(0, END)
        obj_entry_posY.insert(END, str(selectedObject[0]['position'][1]))
        obj_entry_rot.delete(0, END)
        obj_entry_rot.insert(END, str(selectedObject[0]['rotation'][0]))

        obj_entry_oname.delete(0, END)
        obj_entry_oname.insert(END, str(selectedObject[0]['name']))
        obj_entry_col.delete(0, END)
        obj_entry_col.insert(END, str(selectedObject[0]['collision']))
        obj_entry_dynamic.delete(0, END)
        obj_entry_dynamic.insert(END, str(selectedObject[0]['dynamic']))

        #prepareClass = str(selectedObject[0]['objectClass'])
        #prepareClass.replace('[','')
        #prepareClass.replace(']','')
        obj_entry_class.delete(0, END)
        obj_entry_class.insert(END, str(selectedObject[0]['objectClass']))
        #obj_entry_mat.delete(0, END)
        #obj_entry_mat.insert(END, str(selectedObject[0]['material']))

        #obj_SelectedMat = StringVar()
        obj_SelectedMat.set(str(selectedObject[0]['material']))
        #optionList = ["None"]

        obj_entry_par.delete(0, END)
        obj_entry_par.insert(END, str(selectedObject[0]['parent']))
        #obj_entry_color.delete(0, END)
        #obj_entry_color.insert(END, str(selectedObject[0]['color']))
        obj_entry_rlayer.delete(0, END)
        obj_entry_rlayer.insert(END,str(selectedObject[0]['renderLayer']))

from tkinter import _setit

def ObjInfoSync():
    global optionList, obj_entry_mat
    global scenes
    try:
        #obj_SelectedMat = StringVar()
        #obj_SelectedMat.set(str(selectedObject[0]['material']))
        optionList = ["None"]# + scenes[currentSceneId]['textures']
        for obj in scenes[currentSceneId]['textures']:
            optionList.append(obj)
        #print(optionList)
        obj_entry_mat['menu'].delete(0,END)#.config(Pdown_objInfo, obj_SelectedMat, *optionList)
        for obj in optionList:
            obj_entry_mat['menu'].add_command(label=obj,command=_setit(obj_SelectedMat, obj))

        scenes[currentSceneId]['objects'][selectedObject[1]]['name']         = str(obj_entry_oname.get())
        scenes[currentSceneId]['objects'][selectedObject[1]]['collision']    = bool(obj_entry_col.get())
        scenes[currentSceneId]['objects'][selectedObject[1]]['dynamic']      = bool(obj_entry_dynamic.get())
        scenes[currentSceneId]['objects'][selectedObject[1]]['objectClass']  = obj_entry_class.get()
        scenes[currentSceneId]['objects'][selectedObject[1]]['material']     = str(obj_SelectedMat.get())#str(obj_entry_mat.get())
        #print(obj_SelectedMat.get())
        scenes[currentSceneId]['objects'][selectedObject[1]]['parent']       = str(obj_entry_par.get())
        #scenes[currentSceneId]['objects'][selectedObject[1]]['color']        = str(obj_entry_color.get())
        scenes[currentSceneId]['objects'][selectedObject[1]]['renderLayer']  = int(obj_entry_rlayer.get())
        scenes[currentSceneId]['objects'][selectedObject[1]]['position']     = [float(obj_entry_posX.get()),float(obj_entry_posY.get())]
        scenes[currentSceneId]['objects'][selectedObject[1]]['scale']        = [float(obj_entry_scaleX.get()),float(obj_entry_scaleY.get())]
        scenes[currentSceneId]['objects'][selectedObject[1]]['rotation']     = [float(obj_entry_rot.get())]
    except:
        pass#ObjInfoUpdate()

###########################################################
####   SCENE OBJECTS TAB
ot_title_sceneOb = Label(Paned_sceneObj, text='      Scene Objects:', bg=color_dark2, fg=color_font2)
ot_title_sceneOb.place(x=0,y=0)

ot_entry_selected = Entry(Paned_sceneObj,bg=color_white1,fg=color_font1, justify=CENTER,width=20)
ot_entry_selected.place(x=0, y=22)

def Command_NewObject():#(obName=str(ot_entry_selected.get())):
    global scenes, selectedObject
    obName = str(ot_entry_selected.get())
    if obName != '':
        repeater = True
        value = 0
        while repeater:
            if value > 0:
                try:
                    vesef = obName.split('.')
                    vesef = int(vesef[len(vesef)-1])
                    newName = obName.replace(str(vesef), '')
                    newName = newName+str(value+vesef)
                except:
                    newName = str(obName)+'.'+str(value)
            else:
                newName = str(obName)
            selLikeThis = [ [obj, num] for num, obj in enumerate(scenes[currentSceneId]['objects']) if obj['name'] == newName]
            if len(selLikeThis) > 0:
                value += 1
            else:
                repeater = False

        newObj = {'name':newName,
                 'collision':False,
                 'dynamic':False,
                 'objectClass':'',
                 'material':None,
                 'parent':None,
                 'color':'#e6e6e6',
                 'renderLayer':2,
                 'position':[128.0,128.0],
                 'scale':[256.0,256.0],
                 'rotation':[0.0]}
        #newObj = defaultObject
        #newObj['name'] = newName
        scenes[currentSceneId]['objects'].append(newObj)
        print('added')
        ot_entry_selected.delete(0, END)
        ot_entry_selected.insert(END, newName)

def Command_DeleteObject():
    global scenes, selectedObject
    obName = str(ot_entry_selected.get())
    if obName != '':
        selLikeThis = [ [obj, num] for num, obj in enumerate(scenes[currentSceneId]['objects']) if obj['name'] == obName]
        if len(selLikeThis) > 0:
            scenes[currentSceneId]['objects'].remove(selLikeThis[0][0])
            selectedObject = None
            print('removed')
        else:
            print('nothing to remove')

ot_button_add = Button(Paned_sceneObj, text='New', command=Command_NewObject, bg=color_dark1, fg=color_font2, width=16)
ot_button_add.place(x=0,y=42)

ot_button_delete = Button(Paned_sceneObj, text='Delete',command=Command_DeleteObject, bg=color_dark1, fg=color_font2, width=16)
ot_button_delete.place(x=0,y=68)

ot_list_obj = Listbox(Paned_sceneObj, bg=color_dark2, fg=color_font2, activestyle='none', borderwidth=0, height=128)
ot_list_obj.place(x=0,y=96)

def SceneObjectsUpdate():
    lst = ot_list_obj.get(ACTIVE)
    if lst != ' #Object List:':
        ot_entry_selected.delete(0, END)
        ot_entry_selected.insert(END, lst)
    ot_list_obj.delete(0, END)
    ot_list_obj.insert(END, ' #Object List:')
    if currentScene != None:
        for obj in currentScene['objects']:
            ot_list_obj.insert(END, obj['name'])

def SceneObjectsSync():
    global selectedObject, scenes

    if currentScene != None:
        selLikeThis = [ [obj, num] for num, obj in enumerate(scenes[currentSceneId]['objects']) if obj['name'] == str(ot_entry_selected.get())]
        if len(selLikeThis) > 0:
            selectedObject = selLikeThis[0]
        #else:
        #    #ot_entry_selected.delete(0, END)
        #    try:
        #        ot_entry_selected.insert(END, selectedObject[0]['name'])
        #    except:
        #        selectedObject = None

##################################################################
##                       LOGIC NODES GUI                        ##
##################################################################
nodeSizeX = 128
nodeSizeY = 32

nodeCam = [0,0]
nodeZoom = 1.0

nodeList = []
nodeLogic = [] # Sensors        |   Verify
nodeCont  = [] # Controllers    |   Confirm
nodeAct   = [] # Actuators      |   Action
nodeConnect = []

Type_Verify  = 'keyevent,mouseevent,mousepos,objpos,prop,ray'.split(',')
Type_Confirm = 'and,or,compare,not'.split(',')
Type_Action  = 'endobj,replace,move,scale,add,propmath,propset'.split(',')

mousePos = [0,0]
MMB_Click= False
RMB_Click= False
LCTRL_press = False

lastMousePos = [0,0]
MMB_on = False
DragNode = None
RMB_tap = False

#### NODE LINES:
lineInput = None
def Node_drawLine(line):
    global nodeLogic, nodeConnect

    # line = [entry1, entry2]
    obA = [ob for ob in [[obj for obj in nodeLogic if obj[0] == line[0]],
                         [obj for obj in nodeCont if obj[0] == line[0]],
                         [obj for obj in nodeAct if obj[0] == line[0]]] if len(ob) > 0]
    obB = [ob for ob in [[obj for obj in nodeLogic if obj[0] == line[1]],
                         [obj for obj in nodeCont if obj[0] == line[1]],
                         [obj for obj in nodeAct if obj[0] == line[1]]] if len(ob) > 0]
    if len(obA) > 0 and len(obB) > 0:
        obA = obA[0]
        obB = obB[0]
        if len(obA) > 0 and len(obB) > 0:
            obA = obA[0][5]
            obB = obB[0][5]
            if obA != obB:
                nodes.create_line((obA[0]+nodeSizeX)*nodeZoom,obA[1]*nodeZoom, obB[0]*nodeZoom, obB[1]*nodeZoom, fill=color_white1)
            else:
                nodeConnect.remove(line)

        else:
            print(nodeLogic)
            print('Node disconnected: ', line)
            nodeConnect.remove(line)
    else:
        print(nodeLogic)
        print('Node disconnected: ', line)
        nodeConnect.remove(line)

def Node_removeLine(entry):
    global nodeConnect

    for obj in nodeConnect:
        if entry in obj:
            nodeConnect.remove(obj)
    for obj in nodeCont:
        if entry in obj:
            nodeConnect.remove(obj)
    for obj in nodeAct:
        if entry in obj:
            nodeConnect.remove(obj)

#### NODE WINDOWS:
def ResetNode():
    nodes.delete(ALL)

def Node_addLogic(entry, type, input, output, extraType, posXY):
    # extratype = caso um node tenha mais de 1 objeto... pra poder diferenciar do tipo. Ex: mouse pos tem x e y...
    global nodeLogic
    toInput = None
    toOutput = None # add: if type = 'obj'
    if input == 'bool':
        toInput='bool'
    elif input == 'float':
        toInput='float'

    if output == 'bool':
        toOutput='bool'
    elif output == 'float':
        toOutput='float'

    toAdd = [entry, type, toInput, toOutput, extraType, posXY]

    if type in Type_Action:
        nodeAct.append(toAdd)
    elif type in Type_Confirm:
        nodeCont.append(toAdd)
    elif type in Type_Verify:
        nodeLogic.append(toAdd)

def Node_Primitivenew(posX, posY,type ,**kwargs):
    global nodeList

    if 'slots' in kwargs:
        extraScale = 1+kwargs['slots']
    else:
        extraScale = 2
    if 'title' in kwargs:
        windowName = kwargs['title']
    else:
        windowName = '  Empty'

    thisNode = {'pos':[posX,posY],'slots':extraScale,'title':windowName}

    #nodes.create_rectangle(posX+nodeCam[0], posY+nodeCam[1], posX+nodeSizeX+nodeCam[0], posY+nodeSizeY*extraScale+nodeCam[1], fill=color_dark3)
    #nodes.create_rectangle(posX+nodeCam[0], posY+nodeCam[1], posX+nodeSizeX+nodeCam[0], posY+nodeSizeY+nodeCam[1], fill=color_dark1)
    tmpTitle = Label(nodes, text=windowName, bg=color_dark1, fg=color_font2)
    #tmpTitle.place(x=posX+nodeCam[0]+6, y=posY+nodeCam[1]+6)
    thisNode['titleText'] = tmpTitle

    nodeList.append(thisNode)

def Node_new(posx, posy, type, **kwargs):
    global nodeList

    if 'slots' in kwargs:
        extraScale = 1+kwargs['slots']
    else:
        extraScale = 2
    if 'title' in kwargs:
        windowName = kwargs['title']
    else:
        windowName = '  Empty'

    thisNode = {'pos':[posx,posy],'slots':1,'title':'Empty','type':None,'entry':[],'titleText':None}

    #nodes.create_rectangle(posX+nodeCam[0], posY+nodeCam[1], posX+nodeSizeX+nodeCam[0], posY+nodeSizeY*extraScale+nodeCam[1], fill=color_dark3)
    #nodes.create_rectangle(posX+nodeCam[0], posY+nodeCam[1], posX+nodeSizeX+nodeCam[0], posY+nodeSizeY+nodeCam[1], fill=color_dark1)
    #tmpTitle = Label(nodes, text=windowName, bg=color_dark1, fg=color_font2)
    #tmpTitle.place(x=posX+nodeCam[0]+6, y=posY+nodeCam[1]+6)
    #thisNode['titleText'] = tmpTitle

    #nodeList.append(thisNode)

    if type == 'Empty':
        thisNode['title'] = 'Empty'
        thisNode['type'] = None

    elif type == 'keyevent':
        thisNode['title'] = 'Keyboard event'
        thisNode['type'] = type #'keyevent'
        thisNode['entry'] = []
        tmpEntry = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpEnt = [tmpEntry, [],['bool'],'ok']
        thisNode['entry'].append(tmpEnt)

    elif type == 'mouseevent':
        thisNode['title'] = 'Mouse event'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpEntry = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpEnt = [tmpEntry, [],['bool'],'ok']
        thisNode['entry'].append(tmpEnt)

    elif type == 'mousepos':
        thisNode['title'] = 'Mouse Position'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpX = Label(nodes,bg=color_dark3,fg=color_font2, text='Mouse X pos')
        tmpEntX = [tmpX, [],['float'],'x']
        tmpY = Label(nodes,bg=color_dark3,fg=color_font2, text='Mouse Y pos')
        tmpEntY = [tmpY, [],['float'],'y']
        thisNode['entry'].append(tmpEntX)
        thisNode['entry'].append(tmpEntY)

    elif type == 'objpos':
        thisNode['title'] = 'Object Position'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpObj = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpEntObj = [tmpObj, [],[],'ok']
        tmpX = Label(nodes,bg=color_dark3,fg=color_font2, text='Object X')
        tmpEntX = [tmpX, [],['float'],['x',tmpObj]]
        tmpY = Label(nodes,bg=color_dark3,fg=color_font2, text='Object Y')
        tmpEntY = [tmpY, [],['float'],['y',tmpObj]]
        thisNode['entry'].append(tmpEntObj)
        thisNode['entry'].append(tmpEntX)
        thisNode['entry'].append(tmpEntY)

    elif type == 'prop':
        thisNode['title'] = 'Float'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpEntry = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpEnt = [tmpEntry, [],['float'],'ok']
        thisNode['entry'].append(tmpEnt)

    elif type == 'ray':
        thisNode['title'] = 'Ray'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpX = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpEntX = [tmpX, [],[],'x']
        tmpY = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpEntY = [tmpY, [],[],'y']
        tmpObj = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpEntObj = [tmpObj, [],['bool'],['ok',tmpX,tmpY]]
        thisNode['entry'].append(tmpEntObj)
        thisNode['entry'].append(tmpEntX)
        thisNode['entry'].append(tmpEntY)

    ###############################################################################################################

    elif type == 'and':
        thisNode['title'] = 'AND'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpEntry = Label(nodes,bg=color_dark3,fg=color_font2, text=' ')
        tmpEnt = [tmpEntry, ['bool'],['bool'],'ok']
        thisNode['entry'].append(tmpEnt)

    elif type == 'or':
        thisNode['title'] = 'OR'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpEntry = Label(nodes,bg=color_dark3,fg=color_font2, text=' ')
        tmpEnt = [tmpEntry, ['bool'],['bool'],'ok']
        thisNode['entry'].append(tmpEnt)

    elif type == 'not':
        thisNode['title'] = 'NOT'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpEntry = Label(nodes,bg=color_dark3,fg=color_font2, text=' ')
        tmpEnt = [tmpEntry, ['bool'],['bool'],'ok']
        thisNode['entry'].append(tmpEnt)

    elif type == 'compare':
        thisNode['title'] = 'Compare'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpAddNum = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpNum = [tmpAddNum, ['float'],[],'x']
        tmpAddNumY = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpNumY = [tmpAddNumY, ['float'],[],'y']
        tmpEntry = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpEnt = [tmpEntry, [],['bool'],['ok',tmpAddNum, tmpAddNumY]]
        thisNode['entry'].append(tmpNum)
        thisNode['entry'].append(tmpEnt)
        thisNode['entry'].append(tmpNumY)

    ###############################################################################################################

    elif type == 'endobj':
        thisNode['title'] = 'End Object'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpEntry = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpEnt = [tmpEntry, ['bool'],[],'ok']
        thisNode['entry'].append(tmpEnt)

    elif type == 'replace':
        thisNode['title'] = 'Replace Mat'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpAddNum = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpNum = [tmpAddNum, [],[],'ok']
        tmpEntry = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpEnt = [tmpEntry, ['bool'],[],['ok',tmpAddNum]]
        thisNode['entry'].append(tmpEnt)
        thisNode['entry'].append(tmpNum)

    elif type == 'move':
        thisNode['title'] = 'Move Object'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpAddNum = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpNum = [tmpAddNum, [],[],'x']
        tmpAddNumY = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpNumY = [tmpAddNumY, [],[],'y']
        tmpEntry = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpEnt = [tmpEntry, ['bool'],[],['ok',tmpAddNum, tmpAddNumY]]
        thisNode['entry'].append(tmpEnt)
        thisNode['entry'].append(tmpNum)
        thisNode['entry'].append(tmpNumY)

    elif type == 'scale':
        thisNode['title'] = 'Set Scale'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpAddNum = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpNum = [tmpAddNum, [],[],'x']
        tmpAddNumY = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpNumY = [tmpAddNumY, [],[],'y']
        tmpEntry = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpEnt = [tmpEntry, ['bool'],[],['ok',tmpAddNum, tmpAddNumY]]
        thisNode['entry'].append(tmpEnt)
        thisNode['entry'].append(tmpNum)
        thisNode['entry'].append(tmpNumY)

    elif type == 'add':
        thisNode['title'] = 'Add Object'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpEntry = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpEnt = [tmpEntry, ['bool'],[],'ok']
        thisNode['entry'].append(tmpEnt)

    elif type == 'propmath':
        thisNode['title'] = 'Prop Math'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpAddNum = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpNum = [tmpAddNum, [],[],'ok']
        tmpEntry = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpEnt = [tmpEntry, ['bool'],[],['ok',tmpAddNum]]
        thisNode['entry'].append(tmpEnt)
        thisNode['entry'].append(tmpNum)

    elif type == 'propset':
        thisNode['title'] = 'Set Prop'
        thisNode['type'] = type
        thisNode['entry'] = []
        tmpAddNum = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpNum = [tmpAddNum, [],[],'ok']
        tmpEntry = Entry(nodes,bg=color_white1,fg=color_font1, justify=CENTER,width=19 )
        tmpEnt = [tmpEntry, ['bool'],[],['ok',tmpAddNum]]
        thisNode['entry'].append(tmpEnt)
        thisNode['entry'].append(tmpNum)

    a = thisNode['title']
    #print(a)
    tmpTitle = Label(nodes, text=a, bg=color_dark1, fg=color_font2)
    thisNode['titleText'] = tmpTitle

    nodeList.append(thisNode)

def Node_BasicDraw(node):
    global nodeList, lineInput, nodeConnect

    posX = node['pos'][0]
    posY = node['pos'][1]
    try:
        extraScale = len(node['entry'])+1
    except:
        extraScale = node['slots']+1
    tmpTitle = node['titleText']

    nodes.create_rectangle((posX+nodeCam[0])*nodeZoom,
                           (posY+nodeCam[1])*nodeZoom,
                            (posX+nodeSizeX+nodeCam[0])*nodeZoom,
                             (posY+nodeSizeY*extraScale+nodeCam[1])*nodeZoom, fill=color_dark3)
    nodes.create_rectangle((posX+nodeCam[0])*nodeZoom,
                           (posY+nodeCam[1])*nodeZoom,
                            (posX+nodeSizeX+nodeCam[0])*nodeZoom,
                             (posY+nodeSizeY+nodeCam[1])*nodeZoom, fill=color_dark1)
    #tmpTitle = Label(nodes, text=windowName, bg=color_dark1, fg=color_font2)
    tmpTitle.place(x=posX+nodeCam[0]+6, y=posY+nodeCam[1]+6)

    if node['type'] != None:
        for i, obj in enumerate(node['entry']):
            obj[0].place(x=posX+nodeCam[0]+6, y=posY+nodeCam[1]+nodeSizeY*(i+1)+6)
            if obj[1] != []:
                nodes.create_rectangle((posX+nodeCam[0]-4)*nodeZoom,  (posY+nodeCam[1]+nodeSizeY*(i+1)+8)*nodeZoom,
                                        (posX+nodeCam[0]+4)*nodeZoom,  (posY+nodeCam[1]+nodeSizeY*(i+1)+16)*nodeZoom,
                                       fill=color_pine1)
                # Verificar se esta sendo arrastada uma linha ate algum input
                if mousePos[0] > (posX+nodeCam[0]-4)*nodeZoom and mousePos[1] > (posY+nodeCam[1]+nodeSizeY*(i+1)+8)*nodeZoom:
                    if mousePos[0] < (posX+nodeCam[0]+4)*nodeZoom and mousePos[1] < (posY+nodeCam[1]+nodeSizeY*(i+1)+16)*nodeZoom:
                        if lineInput != None:
                            nodeConnect.append([lineInput, obj[0]])
                            print(nodeConnect)
                            lineInput = None
                        if RMB_Click and LCTRL_press:
                            Node_removeLine(obj[0])



                toaddA = obj[1][0]
            else:
                toaddA = None
            if obj[2] != []:
                nodes.create_rectangle((posX+nodeCam[0]-4+nodeSizeX)*nodeZoom,  (posY+nodeCam[1]+nodeSizeY*(i+1)+8)*nodeZoom,
                                        (posX+nodeCam[0]+4+nodeSizeX)*nodeZoom,  (posY+nodeCam[1]+nodeSizeY*(i+1)+16)*nodeZoom,
                                       fill=color_pine1)
                # Verificar se o mousle esta em cima
                if lineInput == None:
                    if mousePos[0] > (posX+nodeCam[0]-4+nodeSizeX)*nodeZoom and mousePos[1] > (posY+nodeCam[1]+nodeSizeY*(i+1)+8)*nodeZoom:
                        if mousePos[0] < (posX+nodeCam[0]+4+nodeSizeX)*nodeZoom and mousePos[1] < (posY+nodeCam[1]+nodeSizeY*(i+1)+16)*nodeZoom:
                            lineInput = obj[0] # Mouse esta em cima!
                toaddB = obj[2][0]
            else:
                toaddB = None

            # ADD NODE TO LOGIC HERE!
            #if not node['type'] in ['compare']:
            Node_addLogic(obj[0], node['type'], toaddA, toaddB, obj[3], [posX+nodeCam[0],  posY+nodeCam[1]+nodeSizeY*(i+1)+12])

def Node_RemoveNode(nod):
    global nodeList

    #nod['titleText'].grid(row=5,column=5)
    nod['titleText'].destroy()
    for obj in nod['entry']:
        obj[0].destroy()
        #obj.grid(row=5,column=5)
        #obj.pack_forget()
    nodeList.remove(nod)

def UpdateNode():
    global MMB_on, lastMousePos, nodeCam, MMB_Click, RMB_Click, DragNode, nodeList, RMB_tap, nodeLogic, nodeCont, nodeAct, lineInput

    # Limpar nodes pra desenhar de novo
    ResetNode()
    nodeLogic = []
    nodeCont = []
    nodeAct = []

    # Redesenhar todos os nodes
    for node in nodeList:
        Node_BasicDraw(node) # {'pos':[posX,posY],'slots':extraScale,'title':windowName}
        if RMB_Click:
            if DragNode == None and lineInput ==None:
                if mousePos[0] > node['pos'][0]+nodeCam[0] and mousePos[1] > node['pos'][1]+nodeCam[1]:
                    if mousePos[0] < node['pos'][0]+nodeCam[0]+nodeSizeX and mousePos[1] < node['pos'][1]+nodeCam[1]+nodeSizeY:
                        # Ta dentro do node!
                        if LCTRL_press:
                            Node_RemoveNode(node) # Delete Node!
                        else:
                            DragNode = node
                            lastMousePos = mousePos
                            #RMB_Click = False

    # Redesenha todas as linhas
    for line in nodeConnect:
        Node_drawLine(line)

    if not RMB_Click:
        DragNode = None

    if lineInput != None:
        if not RMB_Click:
            lineInput = None
            #print('rmb')
            #pass
        else:
            #print('ue')
            obA = [obj for obj in nodeLogic+nodeCont+nodeAct if obj[0] == lineInput]
            #obA = [ob for ob in [[obj for obj in nodeLogic if obj[0] == lineInput],
                                 #[obj for obj in nodeCont if obj[0] == lineInput],
                                 #[obj for obj in nodeAct if obj[0] == lineInput]] if len(ob) > 0]
            #print(lineInput,nodeLogic+nodeCont+nodeAct)
            try:
                obA = obA[0][5]
                nodes.create_line(obA[0]+nodeSizeX,obA[1], mousePos[0], mousePos[1], fill=color_white1)
                #print('ue')
            except:
                lineInput = None
                #print('closed')

    if DragNode == None:
        if MMB_Click and lineInput == None:
            if RMB_tap == False:
                lastMousePos = mousePos
                RMB_tap = True
            if lastMousePos[1] > 0 and lastMousePos[0]> 0: # Dentro do nodes
                newPos = mousePos
                somaX = lastMousePos[0]-newPos[0]
                somaY = lastMousePos[1]-newPos[1]

                nodeCam[0] -= somaX
                nodeCam[1] -= somaY
                lastMousePos = newPos
        else:
            RMB_tap = False
    else:
        newPos = mousePos
        somaX = lastMousePos[0]-newPos[0]
        somaY = lastMousePos[1]-newPos[1]

        nodeList.remove(DragNode)
        DragNode['pos'][0] -= somaX
        DragNode['pos'][1] -= somaY
        lastMousePos = newPos
        nodeList.append(DragNode)

def PopupAdd(item):
    Node_new(mousePos[0]-nodeCam[0], mousePos[1]-nodeCam[1], item)

nodeTypes = Type_Action+Type_Confirm+Type_Verify#['keyboard','mousepos','float','bool','mouseover','mouse','getpos',
             #'getscale','getrot','pointover','endobj','move','rotate','setscale',
             #'compare']

popMenu = Menu(nodes, tearoff=0)

Menu_Verify = Menu(popMenu, tearoff=0)
toeval = ""
for obj in Type_Verify:
    toeval +="Menu_Verify.add_command(label=str('"+obj+"'),command=lambda: PopupAdd(str('"+obj+"')))\n"
exec(toeval)

Menu_Confirm = Menu(popMenu, tearoff=0)
toeval = ""
for obj in Type_Confirm:
    toeval +="Menu_Confirm.add_command(label=str('"+obj+"'),command=lambda: PopupAdd(str('"+obj+"')))\n"
exec(toeval)

Menu_Action = Menu(popMenu, tearoff=0)
toeval = ""
for obj in Type_Action:
    toeval +="Menu_Action.add_command(label=str('"+obj+"'),command=lambda: PopupAdd(str('"+obj+"')))\n"
exec(toeval)

popMenu.add_cascade(label='Verify',menu=Menu_Verify)
popMenu.add_cascade(label='Confirm',menu=Menu_Confirm)
popMenu.add_cascade(label='Action',menu=Menu_Action)

def PopupCreateMenu(event):
    popMenu.post(event.x_root, event.y_root)

nodes.bind('<Button-3>', PopupCreateMenu)

#Node_new(10,10, 'keyboard')
#Node_new(300,20, 'compare')


def FmousePos(event):
    global mousePos
    x,y = event.x, event.y
    mousePos = [x,y]
nodes.bind('<Motion>', FmousePos)

def FMMB(event):
    global MMB_Click
    MMB_Click = True
nodes.bind("<Button-2>", FMMB)

def FRMB(event):
    global RMB_Click
    RMB_Click = True
nodes.bind("<Button-1>", FRMB)
# <ButtonRelease-1>

def FMMB_re(event):
    global MMB_Click
    MMB_Click = False
nodes.bind("<ButtonRelease-2>", FMMB_re)

def FRMB_re(event):
    global RMB_Click
    RMB_Click = False
nodes.bind("<ButtonRelease-1>", FRMB_re)

def LCTRL(event):
    global LCTRL_press
    LCTRL_press = True
nodes.bind("<Key-Control_L>",LCTRL)

def LCTRL_re(event):
    global LCTRL_press
    LCTRL_press = False
nodes.bind("<KeyRelease-Control_L>",LCTRL_re)
nodes.focus_set()

##################################################################
##                      ENGINE VIEW CONTROL                     ##
##################################################################
## Inicio em 06/06/2016
pygame.font.init()
font_default = pygame.font.SysFont('arial', 15)

wireframe = False
viewPos = [0,0]
Obj_Drag = False
Mouse_Last = [0,0]
View_Lmb = 2

def View_ConfigureObjects(): # pra evitar que o usuario coloque coisas erradas nas variaveis
    global wireframe, scenes, viewPos
    wireframe = currentScene['wireframe']

    if currentScene != None:
        viewPos = [-scenes[currentSceneId]['cameraPos'][0], -scenes[currentSceneId]['cameraPos'][1]]

        for obj in scenes[currentSceneId]['objects']:
            if not obj['renderLayer'] in [1,2,3,4]:
                if obj['renderLayer'] in '1234':
                    obj['renderLayer'] = int(obj['renderLayer'])
                else:
                    obj['renderLayer'] = 2
                print('changed Render Layer')

def View_HexToRGB(hex):
    """ convert #RRGGBB to an (R, G, B) tuple """
    try:
        colorstring = hex.strip()
        if colorstring[0] == '#': colorstring = colorstring[1:]
        #if len(colorstring) != 6:
        #    raise ValueError, "input #%s is not in #RRGGBB format" % hex
        r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
        r, g, b = [int(n, 16) for n in (r, g, b)]
        return (r, g, b)
    except:
        return(0,0,0)

def View_DrawDebug(fps):
    text = ''
    if inGame: # Game running
        text += '('+str(int(fps*10)/10)+' FPS)'+' Game Engine Running...'
        debugger = font_default.render(text, 1, (255,255,255))
        screen.blit(debugger, (10,10))
    else:
        text += '('+str(int(fps*10)/10)+' FPS)'+' Game Editor'
        debugger = font_default.render(text, 1, (255,255,255))
        screen.blit(debugger, (10,10))

def View_DrawGimbal(pos, scale):
    global Obj_Drag, Mouse_Last

    color = View_HexToRGB(color_selection)
    width = 4
    pygame.draw.polygon(screen, color    , [[pos[0]+viewPos[0]-width,pos[1]+viewPos[1]-width],
                                            [pos[0]+viewPos[0]+scale[0]+width,pos[1]+viewPos[1]-width],
                                            [pos[0]+viewPos[0]+scale[0]+width,pos[1]+viewPos[1]+scale[1]+width],
                                            [pos[0]+viewPos[0]-width,pos[1]+viewPos[1]+scale[1]+width]])

    gpos = pygame.mouse.get_pos()
    if Obj_Drag == False:
        if gpos[0] > pos[0]+viewPos[0]-width and gpos[1] > pos[1]+viewPos[1]-width:
            if gpos[0] < pos[0]+viewPos[0]+scale[0]+width and gpos[1] < pos[1]+viewPos[1]+scale[1]+width:
                Obj_Drag = True
                Mouse_Last = gpos

def View_DrawObject(pos, scale, rot, texture, fullobj):
    global ot_entry_selected

    noText = True

    if texture[0] == '#':
        color = View_HexToRGB(texture)
        color = (color[0],color[1],color[2],255)
        noText = True
    else:
        color = View_HexToRGB('#fe01fa')
        color = (color[0],color[1],color[2],255)
        noText = False

    # Se o objeto for o selecionado...
    if currentScene != None and selectedObject != None:
        if scenes[currentSceneId]['objects'][selectedObject[1]] == fullobj:
            View_DrawGimbal(pos, scale)

    if noText == False: # Renderizar textura
        try: ####################################################################################################################
             ## URGENTE: Criar uma opção pra CARREGAR TEXTURAS, pq carrega-las todos os frames deixa tudo lento demais.
            tempTexture = scenes[currentSceneId]['textures'][texture][0]#pygame.image.load(texture).convert_alpha()
            tempMat = pygame.transform.scale(tempTexture, (int(scale[0]), int(scale[1])))
            screen.blit(tempMat,(pos[0]+viewPos[0],pos[1]+viewPos[1]))
        except:
            noText = True

    if wireframe == True:
        #print(bool(scenes[currentSceneId]['wireframe']))
        wireColor = View_HexToRGB(color_unselected)
        pygame.draw.polygon(screen, wireColor,
                            [[pos[0]+viewPos[0], pos[1]+viewPos[1]], [pos[0]+viewPos[0],pos[1]+scale[1]+viewPos[1]],
                             [pos[0]+scale[0]+viewPos[0],pos[1]+scale[1]+viewPos[1]], [pos[0]+scale[0]+viewPos[0],pos[1]+viewPos[1]] ], 1)
        pygame.draw.aaline(screen, wireColor, [pos[0]+viewPos[0], pos[1]+viewPos[1]],
                           [pos[0]+scale[0]+viewPos[0],pos[1]+scale[1]+viewPos[1]])
    else:
        if noText:
            pygame.draw.polygon(screen, color,
                                [[pos[0]+viewPos[0], pos[1]+viewPos[1]], [pos[0]+viewPos[0],pos[1]+scale[1]+viewPos[1]],
                                 [pos[0]+scale[0]+viewPos[0],pos[1]+scale[1]+viewPos[1]], [pos[0]+scale[0]+viewPos[0],pos[1]+viewPos[1]]])

    # Selecionar objeto
        #print('ke')
        #if fullobj != scenes[currentSceneId]['objects'][selectedObject[1]]:
        mpos = pygame.mouse.get_pos()
        #print('wtf')
        if mpos[0] > pos[0]+viewPos[0] and mpos[1] > pos[1]+viewPos[1]:
            if mpos[0] < pos[0]+scale[0]+viewPos[0] and mpos[1] < pos[1]+scale[1]+viewPos[1]:
                if mc[2]:
                    ot_entry_selected.delete(0, END)
                    ot_entry_selected.insert(END, fullobj['name'])

def View_RenderObjlist(lista):

    layer_01 = [obj for obj in lista if obj['renderLayer'] == 1]
    layer_02 = [obj for obj in lista if obj['renderLayer'] == 2]
    layer_03 = [obj for obj in lista if obj['renderLayer'] == 3]
    layer_04 = [obj for obj in lista if obj['renderLayer'] == 4]

    for layers in [layer_01,layer_02,layer_03,layer_04]:
        for obj in layers:
            if obj['material'] in [None,'None','']:
                texture = obj['color']
            else:
                texture = obj['material']
                #print(obj['material'], type(obj['material']))
            View_DrawObject(obj['position'], obj['scale'], obj['rotation'], texture, obj )

def View_DragObject():
    global Obj_Drag, scenes, Mouse_Last

    if Obj_Drag:
        if View_Lmb < 2:
            gpos = pygame.mouse.get_pos()
            toAddX = Mouse_Last[0]- gpos[0]
            toAddY = Mouse_Last[1]- gpos[1]
            if currentScene != None and selectedObject != None:
                scenes[currentSceneId]['objects'][selectedObject[1]]['position'][0] -= toAddX
                scenes[currentSceneId]['objects'][selectedObject[1]]['position'][1] -= toAddY
                Mouse_Last = gpos
                ObjInfoUpdate()
            else:
                Obj_Drag = False
        else:
            Obj_Drag = False

##################################################################
##                       GAME ENGINE PLAYER                     ##
##################################################################
game_Info = None
game_scenes = []
game_active = None
game_camera = [0,0]
game_timer = 0

logic_sen  = []
logic_cont = []
logic_act  = []
logic_connection = []

TheLastKey = None
KeyList = {}

def UD_Draw(fullobj):
    haveTexture = False
    if not fullobj['material'] in [None,"None",""]:
        haveTexture = True
    #print(fullobj['name'])
    if haveTexture:
        try:
            tempTexture = game_scenes[game_active]['textures'][fullobj['material']][0]
            tempMat = pygame.transform.scale(tempTexture, (int(fullobj['scale'][0]), int(fullobj['scale'][1])))
            screen.blit(tempMat,(fullobj['position'][0]+game_camera[0],fullobj['position'][1]+game_camera[1]))
        except:
            haveTexture = False
    if haveTexture == False:
        color = View_HexToRGB(fullobj['color'])
        color = (color[0],color[1],color[2],255)
        pygame.draw.polygon(screen, color,
                            [[fullobj['position'][0]+game_camera[0],fullobj['position'][1]+game_camera[1]],
                             [fullobj['position'][0]+game_camera[0],fullobj['position'][1]+game_camera[1]+fullobj['scale'][1]],
                             [fullobj['position'][0]+game_camera[0]+fullobj['scale'][0],fullobj['position'][1]+game_camera[1]+fullobj['scale'][1]],
                             [fullobj['position'][0]+game_camera[0]+fullobj['scale'][0],fullobj['position'][1]+game_camera[1]]])

def UD_Render():
    #print('working')
    for obj in game_scenes[game_active]['objects']:
        UD_Draw(obj)

def UD_RunNode(n):
    global TheLastKey
    if n[1] == 'keyevent':
        pressed = False
        #for event in pygame.event.get():
        #    if event.type == pygame.KEYDOWN:
        #        print('parte 1', pygame.key.name(event.key), n[0].get())
        #        if str(pygame.key.name(event.key)) == n[0].get():
        #            print(str(pygame.key.name(event.key)), n[0].get())
        #            pressed = True
        #            break
        #print(TheLastKey)
        #if TheLastKey == n[0].get():
        #    pressed = True
        #    TheLastKey = None
        try:
            print('go')
            return(KeyList[n[0].get()][0])
        except:
            print(KeyList)
            return(pressed)
    elif n[1] == 'mouseevent':
        pressed = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if str(event.button) == str(n[0].get()):
                    pressed = True
                    break
        return(pressed)
    elif n[1] == 'mousepos':
        if n[4] == 'x':
            return(pygame.mouse.get_pos()[0])
        else:#elif n[4] == 'y':
            return(pygame.mouse.get_pos()[1])
    elif n[1] == 'objpos':
        if n[4][0] == 'x':
            entrada = n[4][1].get()
            objeto = [obj for obj in game_scenes[game_active]['objects'] if obj['name'] == entrada]
            if len(objeto) > 0: # Encontrou o objeto
                objeto = objeto[0]
                return(objeto['position'][0])
        else:#elif n[4][0] == 'y':
            entrada = n[4][1].get()
            objeto = [obj for obj in game_scenes[game_active]['objects'] if obj['name'] == entrada]
            if len(objeto) > 0: # Encontrou o objeto
                objeto = objeto[0]
                return(objeto['position'][1])

def UD_ExecNode(n):
    global game_scenes
    if n[1] == 'endobj':
        obName = n[0].get()
        objetos = [[num, obj] for num, obj in enumerate(game_scenes[game_active]['objects']) if obj['name'] == obName]
        if len(objetos) > 0:
            objetos = objetos[0]
            game_scenes[game_active]['objects'].remove(objetos[1])
            return(True)
        else:
            return(False)
    elif n[1] == 'move':
        obName = n[0].get()
        objetos = [[num, obj] for num, obj in enumerate(game_scenes[game_active]['objects']) if obj['name'] == obName]
        if len(objetos) > 0:
            objetos = objetos[0]
            try:
                game_scenes[game_active]['objects'][objetos[0]]['position'][0] += int(n[4][1].get())
                game_scenes[game_active]['objects'][objetos[0]]['position'][1] += int(n[4][2].get())
                return(True)
            except:
                return(False)
        else:
            return(False)
    elif n[1] == 'scale':
        obName = n[0].get()
        objetos = [[num, obj] for num, obj in enumerate(game_scenes[game_active]['objects']) if obj['name'] == obName]
        if len(objetos) > 0:
            objetos = objetos[0]
            try:
                game_scenes[game_active]['objects'][objetos[0]]['scale'][0] = int(n[4][1].get())
                game_scenes[game_active]['objects'][objetos[0]]['scale'][1] = int(n[4][2].get())
                return(True)
            except:
                return(False)
        else:
            return(False)

def UD_Logic():
    for obj in logic_cont: # CONTROLADORES
        # ENTRADAS:
        L_input = [ob[0] for ob in logic_connection if ob[1] == obj[0]]
        # SAIDAS:
        L_output = [ob[1] for ob in logic_connection if ob[0] == obj[0]]

        if len(L_input) > 0 and len(L_output) > 0: # Verificar se n é um nodes desnecessario

            if obj[1] == 'and':
                tmpNot = 0 # se no final do for, for 0, ele executa!
                for inp in L_input:
                    inpName = [o for o in logic_sen if o[0] == inp][0]
                    isTrue = UD_RunNode(inpName)
                    if isTrue == False:
                        tmpNot +=1
                if tmpNot == 0: # Agr so executar os outputs!!
                    for out in L_output:
                        outName = [o for o in logic_act if o[0] == out][0]
                        UD_ExecNode(outName)

            elif obj[1] == 'or':
                tmpNot = 0 # se no final do for, for 0, ele executa!
                for inp in L_input:
                    inpName = [o for o in logic_sen if o[0] == inp][0]
                    isTrue = UD_RunNode(inpName)
                    if isTrue == False:
                        tmpNot +=1
                if tmpNot < len(L_input): # Agr so executar os outputs!!
                    for out in L_output:
                        outName = [o for o in logic_act if o[0] == out][0]
                        UD_ExecNode(outName)
            elif obj[1] == 'not':
                tmpNot = 0 # se no final do for, for 0, ele executa!
                for inp in L_input:
                    inpName = [o for o in logic_sen if o[0] == inp][0]
                    isTrue = UD_RunNode(inpName)
                    if isTrue == True:
                        tmpNot +=1
                if tmpNot == 0: # Agr so executar os outputs!!
                    for out in L_output:
                        outName = [o for o in logic_act if o[0] == out][0]
                        UD_ExecNode(outName)

def UD_GameControl():
    global game_timer

    if game_active!= None:
        if game_timer >= 0: #100:
            UD_Render()
            UD_Logic()
        else:
            game_timer += 1

def UD_StartEngine():
    global inGame, game_timer, game_camera, game_active, game_scenes, game_Info, logic_act, logic_connection, logic_cont,logic_sen
    if not inGame: # Nao esta no modo jogo
        if currentSceneId != None:
            game_timer          = 0
            game_camera         = scenes[currentSceneId]['cameraPos']
            game_active         = currentSceneId
            game_scenes         = scenes
            game_Info           = game
            logic_act           = nodeAct
            logic_connection    = nodeConnect
            logic_cont          = nodeCont
            logic_sen           = nodeLogic

            inGame = True #ATIVA MOTOR
        else:
            print("Error: Empty Scene Slot")
    else:
        print("Cannot Open multi game Process.")

def UD_CloseEngine():
    global inGame

    try:
        if inGame:
            inGame = False
    except:
        pass

topMenu.add_command(label='Run...',command=UD_StartEngine)
topMenu.add_command(label='Stop...',command=UD_CloseEngine)
##################################################################
##################################################################
tap = 0
selectedObjectBackup = 'forceUpdate///'

c = pygame.time.Clock()
lastFps = 0

pygame.init()

mainLoop = True
while mainLoop:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            TheLastKey = str(pygame.key.name(event.key))
            KeyList[str(pygame.key.name(event.key))] = [True,event.key]
            print('ue',KeyList)

        if event.type == pygame.KEYUP:
            print(event.key)
            if KeyList[str(pygame.key.name(event.key))][1] == event.key:
                KeyList[str(pygame.key.name(event.key))] = [False,event.key]
                print('saiu',str(pygame.key.name(event.key)))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                View_Lmb = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                View_Lmb += 1
    #        mainLoop = False

    tc = pygame.key.get_pressed()
    mc = pygame.mouse.get_pressed()
    engineX = Paned_top.sash_coord(0)[0]
    engineY = m1.sash_coord(0)[1]
    nodesX = Paned_down.sash_coord(0)[0]
    #print(engineX,engineY)

    if tap < 2: # Change the Tab positions
        altura = root.winfo_height()
        largura = root.winfo_width()

        Paned_top.sash_place(0,int((largura/3)*2),800)
        m1.sash_place(0,0,int((altura/3)*2))
        Paned_down.sash_place(0, int((largura/3)), 800)
        tap += 1
        # Load scene
        SceneGameUpdate()
        # Load scene objects
        SceneObjectsUpdate()
    else: # Sync Interface to Database
        SceneGameSync()
        ObjInfoSync()
        SceneObjectsSync()
        SceneObjectsUpdate()
        #Node UPDATE
        UpdateNode()

    if selectedObject != selectedObjectBackup: # Update
        ObjInfoUpdate()
        selectedObjectBackup = selectedObject

    screen = pygame.display.set_mode((engineX,engineY))
    bgColor = View_HexToRGB(scenes[currentSceneId]['background'])
    screen.fill((bgColor[0],bgColor[1],bgColor[2],255))
    pygame.display.init()

    if inGame:
        UD_GameControl()
    else:
        View_ConfigureObjects()
        View_DragObject()

        if currentScene != None:
            View_RenderObjlist(scenes[currentSceneId]['objects'])

    # FPS = 30
    if int(game['fps']) > 30:
        c.tick(int(game['fps']))
    else:
        c.tick(30)
    View_DrawDebug(c.get_fps())
    if pygame.time.get_ticks() - lastFps > 1000:
        #print(c.get_fps())
        lastFps = pygame.time.get_ticks()

    pygame.display.update()

    root.update()
#mainloop()
