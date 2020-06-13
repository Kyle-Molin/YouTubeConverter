#***************************************************************************************************#
#Title: YouTube Converter                                                                           #
#Author: Kyle Molin                                                                                 #
#Date: 6/13/2020                                                                                    #
#Purpose: Download and convert YouTube videos to either an MP4 or MP3 format via a user friendly GUI#
#***************************************************************************************************#
from pytube import YouTube
from tkinter import *
from PIL import ImageTk,Image
from moviepy.editor import *
import os
import time
import glob

def mp3_button():
    dl_button = Button(main_frame, text = "Download Audio", bg = "#444444", fg = "#9e9e9e", command =lambda: dl_convert(yt.streams.filter(subtype="mp4", progressive=True).order_by('resolution').desc()[0]))
    dl_button.place(relx = 0.86, rely = 0.79, relwidth = 0.08, relheight = 0.046)

def mp4_button():
    dl_button = Button(main_frame, text = "Download Video", bg = "#444444", fg = "#9e9e9e", command =lambda: dl(yt.streams.filter(subtype="mp4")[var.get()]))
    dl_button.place(relx = 0.86, rely = 0.79, relwidth = 0.08, relheight = 0.046)

def dl_convert(dl_type):
    global file_size                                                    #Make file_size global so it does not have to be passed with a function call to progress_function
    file_size = dl_type.filesize                                        #Sends filesize of download to progress_function to calculate when the download is done
    #info_label.config(text = "Converting: " + vid_title + " To MP3")   #Changes label message to tell the user it is converting the file, needs to be tweeked to print when active
    dl_type.download()                                                  #Downloads video specified by user
    time.sleep(3)                                                       #Sleep for 3 seconds so pytube has proper amout of time to process the title of the video
                                                                        #Sometimes if something accesses the folder pytube downloaded the video in too early pytube makes the title "YouTube" instead of the proper name
    #**********************************************************#
    #Title: How to get the latest file in a folder using python#
    #Author: Marlon Abeykoon, jmlarson                         #
    #Date: 6/8/2020                                            #
    #Availability: https://stackoverflow.com/a/39327156        #
    #**********************************************************#
    all_files = glob.glob('./*.mp4')                                    # * means all if need specific format then *.csv
    latest_file = max(all_files, key=os.path.getctime)                  #Grabs the name of the lastest file downloaded to the current folder (Should be the video just downloaded)
    latest_file_dirty = latest_file.split(".\\")[1]                     #Splits off .\\from beginning of string (video title)
    latest_file = latest_file_dirty.split(".mp4")[0]                    #Splits off the extension from the filename

    mp4_file = r""+latest_file+".mp4"                                   #Sets the name of the mp4 file to convert
    mp3_file = r""+latest_file+".mp3"                                   #Sets the name of what the mp3 file will be called after conversion

    video = VideoFileClip(mp4_file)                                     #Video clip to convert

    audioclip = video.audio
    audioclip.write_audiofile(mp3_file, verbose=False, logger=None)     #Converts the video clip into pure audio, verbose and logger set to false so the cli progress bar does not introduce lag

    audioclip.close()                                                   #Closes activity on audioclip
    video.close()                                                       #Closes activity on video
    os.remove(mp4_file)                                                 #Removes mp4 file so the user is only left with the mp3 clip
    info_label.config(text ="Done Converting: " + vid_title + " To MP3")#Changes label message to tell the user it is done converting the file
    
def dl(dl_type):
    global file_size
    file_size = dl_type.filesize
    dl_type.download()

def display_opts(link_entry):
    try:
        global vid_title                                                #So progress_function can print the name of the video without it being passed in a call
        global yt                                                       #So any function in the script can access the original youtube link
        yt = YouTube(link_entry, on_progress_callback=progress_function)
        vid_title = yt.title
        for i in range(len(yt.streams.filter(subtype="mp4"))):
            Radiobutton(main_frame, text = yt.streams.filter(subtype="mp4")[i], variable = var, value = i, command =lambda: mp4_button()).pack(anchor = W)
        Radiobutton(main_frame, text = "Audio only", variable = var, value = 70, command =lambda: mp3_button()).pack(anchor = W)
    except:
        #Prints this message if yt.streams returns an error
        info_label['text'] = "Error: Please make sure this is an active YouTube link"

def progress_function(self, chunk, bytes_remaining):
    #info_label.config(text = "Please Wait, Downloading: " + vid_title) Needs to be tweeked to actually print the message once active
    #******************************************************************************************************************************************#
    #Title: How to Create a Simple YouTube Download Program with a Progress Indicator in Python 3 with pytube                                  #
    #Author: Yagi                                                                                                                              #
    #Date: 3/11/2018                                                                                                                           #
    #Availability: https://yagisanatode.com/2018/03/11/how-to-create-a-simple-youtube-download-program-with-a-progress-in-python-3-with-pytube/#
    #******************************************************************************************************************************************#
    if ((100*(file_size - bytes_remaining))/file_size) == 100:          #Calculates percent remaining and waits till it reaches 100
        info_label.config(text = "Done downloading: " + vid_title)      #Once the download is 100% complete print message in info label

top = Tk()                                                              #Initializing root window
top.title("YouTube to MP4 | v0.7 BETA")                                 #Change window title
top.iconbitmap('LoneWolf.ico')                                          #Chance icon on window
var = IntVar()                                                          #Used to specify which radio button is pressed
var.set(0)                                                              #Set choice to 1ist option

canvas = Canvas(top, height = 800, width = 1200)                        #Size of application window
canvas.pack()

frame = Frame(top, bg = "#333333", bd = 5)                              #Grey frame that incases the input field and submit button
frame.place(relx = 0.5, relwidth = 1.0, relheight = 0.1, anchor = "n")

img = PhotoImage(file = "logo.gif")
logo = Label(frame, image = img, bg = "#333333")
logo.place(relx = 0.03, rely = 0.15)

link_entry = Entry(frame, font = 40, bg = "#232323", fg = "white")      #Input field for user to paste link
link_entry.insert(0, "Paste YouTube link here")                         #Place holder text in input field
link_entry.place(relx = 0.15, rely = 0.3, relwidth = 0.7, relheight = 0.5)

#Lambda is used so when the button is clicked the variable is redefined, giving you what is currently in the entry box.
link_button = Button(frame, text = "Submit", bg = "#444444", fg = "#9e9e9e", command =lambda: display_opts(link_entry.get()))
link_button.place(relx = 0.85, rely = 0.3, relwidth = 0.08, relheight = 0.5)

main_frame = Frame(top, bg = "#232323", bd = 10)
main_frame.place(relx = 0.5, rely = 0.100009, relwidth = 1.0, relheight = 1.0, anchor = "n")

info_label = Label(main_frame)
info_label.place(relwidth = 1.0, relheight = 1.0)

top.mainloop()
