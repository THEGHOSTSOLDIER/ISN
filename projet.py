######################################

#            premier fichier à exécuter (nécessite test2

######################################

from tkinter import *
import pyaudio
import wave
import time
verif = 0
def clic():
    fenetre.destroy()
    import test2
#define stream chunk   
chunk = 1024  

#open a wav format music  
f = wave.open("test.wav","rb")  
#instantiate PyAudio  
p = pyaudio.PyAudio()  
#open stream  
stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)  
#read data  
data = f.readframes(chunk)  

#play stream  
while data:  
    stream.write(data)  
    data = f.readframes(chunk)  

#stop stream
stream.stop_stream()  
stream.close() 

#close PyAudio  
p.terminate()

fenetre = Tk()
fenetre.title("Jeu")
fenetre.iconbitmap("spyder.ico")
fenetre.geometry("512x545+550+200")

photo = PhotoImage(file = "ninja.png")
canvas = Canvas(fenetre, width = 512, height = 512)
canvas.create_image(255, 255, image = photo)
canvas.pack()
button = Button(fenetre, text= "Jouer", command = clic)
button.pack()
