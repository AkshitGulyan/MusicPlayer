from tkinter import *
from PIL import Image,ImageTk
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
pygame.mixer.init()
root = Tk()
root.title("Music Player")
root.iconbitmap(r"images n icons\play-button-arrowhead.ico")
root.geometry("700x450")


Text=Label(root,text="Music Player completely made in Python", font=("Helvettica"))
Text.pack()

global paused
paused = FALSE

global song_len

#Functions n Commands C:\Users\akshi\OneDrive\Desktop\codeclause projects\music\52 Bars.mp3
def addsongs():
    songs = filedialog.askopenfilenames(initialdir="music", title="Choose a song", filetypes=(("mp3 files", "*.mp3"), ))
    for song in songs:
        song=song.replace("music/", "")
        song= song.replace(".mp3","")
        playlist.insert(END,song)

def removesongs():
    playlist.delete(ANCHOR)
    pygame.mixer.music.stop()
    

def play():
    song=playlist.get(ACTIVE)
    song=f"music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_time()

    #slide_pos= int(song_len1)
    #my_slider.config(to=slide_pos,value=0)

def next_song():
    next_one=playlist.curselection()
    next_one=next_one[0]+1
    song=playlist.get(next_one)
    song=f"music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlist.selection_clear(0,END)
    playlist.activate(next_one)
    playlist.select_set(next_one,last=None)
    my_slider.config(value=0)


def prev_song():
    prev_one=playlist.curselection()
    prev_one=prev_one[0]-1
    song=playlist.get(prev_one)
    song=f"music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlist.selection_clear(0,END)
    playlist.activate(prev_one)
    playlist.select_set(prev_one,last=None)
    my_slider.config(value=0)



def stop():
    pygame.mixer.music.stop()
    status_bar.config(text="")
    playlist.selection_clear(0,END)
    my_slider.config(value=0)


def pause(is_paused):
    global paused
    paused=is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused=FALSE
    else:
        pygame.mixer.music.pause()
        paused=TRUE



def song_time():
    cur_time=pygame.mixer.music.get_pos()/1000
    cur_time1=cur_time
    
    #slider_label.config(text=f"slider: {int(my_slider.get())} and songpos: {int(cur_time1)}")
    cur_time=time.strftime("%M:%S", time.gmtime(cur_time))
    if cur_time=="59:59":
        cur_time="00:00"
    else:
        pass
    
    song=playlist.get(ACTIVE)
    song=f"music/{song}.mp3"
    song_info=MP3(song)
    global song_len1
    song_len=song_info.info.length
    song_len1=song_len
    song_len=time.strftime("%M:%S", time.gmtime(song_len))

    if int(my_slider.get())==int(song_len1):
        status_bar.config(text=f"{song_len} of {song_len}")

    elif int(my_slider.get())==int(cur_time1+1):
        slide_pos= int(song_len1) 
        my_slider.config(to=slide_pos,value=cur_time1+1)
    else:
        slide_pos= int(song_len1)
        my_slider.config(to=slide_pos,value=my_slider.get())
        cur_time=time.strftime("%M:%S", time.gmtime(int(my_slider.get())))
        status_bar.config(text=f"{cur_time} of {song_len}")
        my_slider.config(value=int(my_slider.get()+1))

    

    #update status bar
    status_bar.after(1000,song_time)


    
def slide(x):
    #slider_label.config(text=f'{my_slider.get()} of {int(song_len1)}')
    song=playlist.get(ACTIVE)
    song=f"music/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start=my_slider.get())

    my_slider.config(value=my_slider.get())




#Playlist_listbox defn.
playlist=Listbox(root,bg='Grey',fg='black', width=80, selectbackground="green", selectforeground="black")
playlist.pack(pady=20)


#Player control images desc
prev_img= (Image.open(r"images n icons\back.png"))
resized_image= prev_img.resize((50,50), Image.ANTIALIAS)
prev_img = ImageTk.PhotoImage(resized_image)

next_img= (Image.open(r"images n icons\next.png"))
resized_image= next_img.resize((50,50), Image.ANTIALIAS)
next_img = ImageTk.PhotoImage(resized_image)

pause_img= (Image.open(r"images n icons\pause.png"))
resized_image= pause_img.resize((50,50), Image.ANTIALIAS)
pause_img = ImageTk.PhotoImage(resized_image)

play_img= (Image.open(r"images n icons\play.png"))
resized_image= play_img.resize((50,50), Image.ANTIALIAS)
play_img = ImageTk.PhotoImage(resized_image)

stop_img= (Image.open(r"images n icons\stop.png"))
resized_image= stop_img.resize((50,50), Image.ANTIALIAS)
stop_img = ImageTk.PhotoImage(resized_image)



#Player control frames defn.
controls_frame=Frame(root)
controls_frame.pack()



#player control buttons
prev_btn=Button(controls_frame, image= prev_img, borderwidth=0, command=prev_song)
next_btn=Button(controls_frame, image=next_img, borderwidth=0, command=next_song)
play_btn=Button(controls_frame, image=play_img, borderwidth=0, command=play)
pause_btn=Button(controls_frame, image=pause_img, borderwidth=0, command=lambda:pause(paused))
stop_btn=Button(controls_frame, image=stop_img, borderwidth=0, command=stop)


prev_btn.grid(row=0, column=0, padx=10)
next_btn.grid(row=0, column=4, padx=10)
play_btn.grid(row=0, column=1, padx=10)
pause_btn.grid(row=0, column=2, padx=10)
stop_btn.grid(row=0, column=3, padx=10)


#menu
my_menu=Menu(root, background="Black", fg="green")
root.config(menu=my_menu)
#sub_menus
file_menu=Menu(my_menu, background="Blue", fg="yellow")
my_menu.add_cascade(label="FILE", menu=file_menu)
file_menu.add_command(label="Add the songs to the playlist!", command=addsongs)
file_menu.add_command(label="Remove the currently selected song", command=removesongs)

#exit Menu
exit_menu=Menu(my_menu,background="Blue",fg="Yellow")
my_menu.add_cascade(label="EXIT", menu=exit_menu)
exit_menu.add_command(label="Exit from the Music Player", command=root.destroy)





#time duration bar
status_bar=Label(root,text="",bd=1, relief=GROOVE, anchor=W)
status_bar.pack(fill=X,side=BOTTOM)


Text=Label(status_bar,text="Made By Akshit Gulyan")
Text.pack()

my_slider=ttk.Scale(root,from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=450)
my_slider.pack(pady=25)

#slider_label=Label(root,text='0')
#slider_label.pack()

root.mainloop()
