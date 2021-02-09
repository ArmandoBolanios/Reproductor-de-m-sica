from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('Codemy.com MP3 Player')
root.geometry('500x450')

pygame.mixer.init()

#Grab Song Lenght time Info
def play_time():
    #check for double timing
    if stopped:
        return 
    #grab current song elapsed time
    current_time = pygame.mixer.music.get_pos() / 1000
    
    #throw up temp label to get data
    #slider_label.config(text=f'Slider: {int(my_slider.get())} and song position: {int(current_time)}')
    #convert to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    
    #get currently playing song
    #current_song = song_box.curselection()
    #grab song title from playlist
    song = song_box.get(ACTIVE)  
    #add directory structure and mp3 to song  title
    song = f'C:/Users/Hermann/Documents/python/GUI/audio/{song}.mp3'
    #load song with Mutagen
    song_mut = MP3(song)
    #Get song length
    global song_length
    song_length = song_mut.info.length
    #convert to time format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    
    #Increase current time by 1 second
    current_time +=1
    
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length} ')
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        #update slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
    else:
        #update slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        
        #convert to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
        
        #output time status bar
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length} ')

        #move this  thing along by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)
        
    #output time to status bar
    #status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length} ')
    
    #update slider position value to current song position
    #my_slider.config(value=int(current_time))
    
        
    #update time
    status_bar.after(1000, play_time)

#add song function
def add_song():
    song = filedialog.askopenfilename(initialdir='C:/Users/Hermann/Documents/python/GUI/audioaudio/', title="hose a song", filetypes=(("mp3 Files", "*.mp3"), ))
    
    #strip put the directory info and .mp3 extension from the song name
    song = song.replace("C:/Users/Hermann/Documents/python/GUI/audio/", "")
    song = song.replace(".mp3", "")
    
    #add song to listbox
    song_box.insert(END, song)

#Add many songs to playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='C:/Users/Hermann/Documents/python/GUI/audioaudio/', title="hose a song", filetypes=(("mp3 Files", "*.mp3"), ))
    
    # loop thru song list and replace directory info  and mp3
    for song in songs:
        song = song.replace("C:/Users/Hermann/Documents/python/GUI/audio/", "")
        song = song.replace(".mp3", "")
        #Insert into playlist
        song_box.insert(END, song)

#Play selected song
def play():
    #set stopped variable to false so song can play
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'C:/Users/Hermann/Documents/python/GUI/audio/{song}.mp3'
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    #call the play_time function to get  song  lenght
    play_time()
    
    #update slider to position
    #slider_position = int(song_length)
    #my_slider.config(to=slider_position, value=0)
    
    #Get current volume
    #current_volume = pygame.mixer.music.get_volume()
    #slider_label.config(text=current_volume * 100)
    
#Stop playing current song    
global stopped
stopped =  False
def stop():
    #Reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)
    #stop song from playing
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    
    #Clear the status bar
    status_bar.config(text='')
    
    #set stop variable to true
    global stopped
    stopped = True

#Play the next song in the playlist
def next_song():
    #Reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)
    
    #get the  current song tuple number
    next_one = song_box.curselection()
    #add one the current song number
    next_one = next_one[0]+1
    #grab song title from playlist
    song = song_box.get(next_one)
    
    #add directory structure and mp3 to song  title
    song = f'C:/Users/Hermann/Documents/python/GUI/audio/{song}.mp3'
    
    #load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    #Clear active bar in playlist listbox
    song_box.selection_clear(0, END)
    
    #Activate new sonf bar
    song_box.activate(next_one)
    
    #Set Active bar to next song
    song_box.selection_set(next_one, last=None)

#play previous song in Playlist
def previous_song():
    #Reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)
    
    #get the  current song tuple number
    next_one = song_box.curselection()
    #add one the current song number
    next_one = next_one[0]-1
    #grab song title from playlist
    song = song_box.get(next_one)
    #add directory structure and mp3 to song  title
    song = f'C:/Users/Hermann/Documents/python/GUI/audio/{song}.mp3'
    
    #load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    #Clear active bar in playlist listbox
    song_box.selection_clear(0, END)
    
    #Activate new sonf bar
    song_box.activate(next_one)
    
    #Set Active bar to next song
    song_box.selection_set(next_one, last=None)

#delete a song
def delete_song():
    stop()
    #delete currently selected song
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()
   
#delete all songs from playlist
def delete_all_songs():
    stop()
    #delete all songs
    song_box.delete(0, END)
    #stop music if it's playing
    pygame.mixer.music.stop()

#create global pause variable
global paused
paused = False

#Pause and Unpause the current song    
def pause(is_paused):
    global paused
    paused = is_paused
    
    if paused:
        #Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        #Pause
        pygame.mixer.music.pause()
        paused= True

#create slider function
def slide(x):
    #slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE)
    song = f'C:/Users/Hermann/Documents/python/GUI/audio/{song}.mp3'
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

# Create Volume function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    
    # Get current volume
    #current_volume = pygame.mixer.music.get_volume()
    #slider_label.config(text=current_volume * 100)

#Create Master Frame
master_frame = Frame(root)
master_frame.pack(pady=20)

#create playlist box
song_box = Listbox(master_frame, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
song_box.grid(row=0, column=0)

#Define player control buttons images
back_btn_img = PhotoImage(file='C:/Users/Hermann/Documents/python/GUI/back.PNG')
forward_btn_img = PhotoImage(file='C:/Users/Hermann/Documents/python/GUI/next.PNG')
play_btn_img = PhotoImage(file='C:/Users/Hermann/Documents/python/GUI/play.PNG')
pause_btn_img = PhotoImage(file='C:/Users/Hermann/Documents/python/GUI/pause.PNG')
stop_btn_img = PhotoImage(file='C:/Users/Hermann/Documents/python/GUI/stop.PNG')

#create player control frame
controls_frame =  Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)

#Create Volume label frame
volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

#create player control buttons
back_button = Button(controls_frame, image=back_btn_img,        borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image= forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_img,        borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img,      borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img,        borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

#create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="add one song to playlist", command=add_song)

# Add Many songs to playlist
add_song_menu.add_command(label="add many songs to playlist", command=add_many_songs)

#create delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu .add_command(label="Delete a song from playlist", command = delete_song)
remove_song_menu .add_command(label="Delete all songs from playlist", command = delete_all_songs)

#create starus var
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#create music position slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)

#Create volume slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)

#create temporary slider label
#slider_label =  Label(root, text="0")
#slider_label.pack(pady=10)

root.mainloop()
