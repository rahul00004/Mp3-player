import os
from tkinter import *  #importing tkinter
from pygame import mixer 
import tkinter.messagebox    #messagae imported from tkinter
from tkinter import filedialog #filedialog import from tkinter
from mutagen.mp3 import MP3
from tkinter import ttk

from tkinter import ttk  # Normal Tkinter.* widgets are not themed!
from ttkthemes import ThemedTk
import threading
import time
root = ThemedTk(theme="")   # making instance of tkinter as Tk()
mixer.init()     # initializing mixer

root.title("moody")    # setting title


root.iconbitmap(r'image/music.ico')   # setting icon
displayFileName  = ttk.Label(root,text="Welcome to my music player" ,font="arial 20 bold")     
displayFileName.pack()   # packing text
topframe = Frame(root)
topframe.pack(pady=10,padx=20)  
length_label  = ttk.Label(topframe,text="Total length --:--",font="verdena 10 bold")     # setting label in widget using Label()
length_label.grid(row=0,column=0,padx=20) 
current_time_label  = ttk.Label(topframe,text="Current time -  --:--",font="verdena 10 bold")     
current_time_label.grid(row=0,column=1) 
play= PhotoImage(file='image/play.png')   # setting image as Photoimage instance
stop=PhotoImage(file="image/stop.png")
pause=PhotoImage(file="image/pause.png")
rewind=PhotoImage(file='image/rewind.png')
muted=PhotoImage(file="image/muted.png")
unmute=PhotoImage(file='image/unmute.png')
add=PhotoImage(file="image/add.png")
subtract=PhotoImage(file="image/subtract.png")

#create menubar
menubar=Menu(root)
root.config(menu=menubar)

def browse_file():   # browse file option
     global filename_path
     filename_path=filedialog.askopenfilename()
     print(filename_path)
     add_to_playlist(filename_path)


#playlist give filename path 
# playlist just represnt filename in list     
playlist=[]     
def add_to_playlist(filename):
     filename=os.path.basename(filename)
     index=0
     playlistbox.insert(index,filename)  

     playlistbox.grid()
     playlist.insert(index,filename_path)

     index+=1    
def del_song():
     select_song=playlistbox.curselection()
     select_song=int(select_song[0])
     playlistbox.delete(select_song)
     playlist.pop(select_song)

#create submenu
subMenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=subMenu)
subMenu.add_command(label='Open', command=browse_file)
subMenu.add_command(label='Exit', command=root.destroy)


def about_us():
     tkinter.messagebox.showinfo('About Moody','This is a music player created by Rahul')


subMenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=subMenu)
subMenu.add_command(label='About us' ,command = about_us)



#listbox
listframe = Frame(root)
listframe.pack(pady=10)  

playlistbox=Listbox(listframe)

playlistbox.grid(row=0,column=1)
list_button_frame = Frame(root)
list_button_frame.pack(padx=20)  
add_song=ttk.Button(list_button_frame,image=add,command=browse_file)
add_song.grid(row=0,column=1,padx=10)
del_song=ttk.Button(list_button_frame,image=subtract,command=del_song)
del_song.grid(row=0,column=3)

def showDetail(play_song):
     displayFileName['text'] = "Playing" +"  "+ os.path.basename(play_song)  
     file_data = os.path.splitext(play_song)
     if file_data[1] == '.mp3':
          audio=MP3(play_song)
          total_length=audio.info.length
          print(total_length)
         
     else:     
          getFile=mixer.Sound(play_song)
          total_length = getFile.get_length
     min,sec =divmod(total_length,60)
     min =round(min)
     sec=round(sec)
     print(min)
     print(sec)
     timeformat='{:02d}:{:02d}'.format(min,sec)
     print(timeformat)
     length_label['text'] = "Playing" +"  "+ timeformat
     t1=threading.Thread(target=start_count,args=(total_length))
     t1.start()
def start_count(t):
     global paused
     #when music stops mixer.music.get_busy returns false and we exit of while loop
     current_time=0
     while current_time<=t and mixer.music.get_busy() :
          if paused:
               continue
               paused
          else:
               min,sec =divmod(current_time,60)
               min =round(min)
               sec=round(sec)
               timeformat='{:02d}:{:02d}'.format(min,sec)
               current_time_label['text']='Current time' + " - " +timeformat
               time.sleep(1)
               current_time+=1



def play_btn():   
     if paused:
           mixer.music.unpause()
           statusbar['text']="Music resume" +' - ' + os.path.basename(filename_path)     
     else:
          try:
               #stop_button()
               #time.sleep(1)
               select_song=playlistbox.curselection()
               select_song=int(select_song[0])
               play_it=playlist[select_song]
               mixer.music.load(play_it)       
               mixer.music.play()                #playing song in 
               showDetail(play_it)
               statusbar['text']="Music resume" +' - ' + os.path.basename(play_it)    
               print("Clicked")

          except :
               tkinter.messagebox.showerror('file not found','please select file')     

paused = False


def pause_btn(): 
     global paused
     paused = True                 
     mixer.music.pause()    
     statusbar['text']="Music Paused"   

def rewind_btn():                  
     play_btn()
     statusbar['text']="Music rewind"   
                    
     print("Clicked")  

def stop_btn():                  
     mixer.music.stop()    
     
                    
     print("Clicked")     
def set_vol(value):
     volume=int(value)/100
     mixer.music.set_volume(volume)
mute=False
def mute_btn():
     global mute
     if mute :
          mixer.music.set_volume(0.7)
          unmute_button.configure(image=unmute)
          scale.set(70)
          mute=False
     else :
          mixer.music.set_volume(0)
          unmute_button.configure(image=muted)
          scale.set(0)
          mute=True   

                    
middleframe = Frame(root)
middleframe.pack(pady=30,padx=30)  



Play_buttton=ttk.Button(middleframe,image=play,command=play_btn)
Play_buttton.grid(row=0,column=0,padx=10)   # packing button created above
pause_button=ttk.Button(middleframe,image=pause,command=pause_btn)
pause_button.grid(row=0,column=1,padx=10)
stop_button=ttk.Button(middleframe,image=stop,command=stop_btn)
stop_button.grid(row=0,column=2,padx=10)


bottomframe = Frame(root)
bottomframe.pack(pady=10)


rewind_button=ttk.Button(bottomframe,command=rewind_btn ,image=rewind)
rewind_button.grid(row=0,column=0,padx=30)
unmute_button=ttk.Button(bottomframe,command=mute_btn ,image=unmute)
unmute_button.grid(row=0,column=1)
scale=ttk.Scale(bottomframe,from_=0,to=100,orient=HORIZONTAL,command=set_vol)
scale.set(60)
scale.grid(row=0,column=2 ,padx=30)
statusbar = ttk.Label(root,text='Enjoy music' ,relief =SUNKEN,anchor=W,font='Times 16 bold')
statusbar.pack(side=BOTTOM,fill=X)

def on_closing():
     
     root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)      
root.mainloop()   # running root instance of tkinter
