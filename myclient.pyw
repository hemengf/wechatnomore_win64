import thread
from ChatFns import *
import sys
from PIL import Image, ImageTk
import datetime

WindowTitle = ''
PORT = 8011
root = Tk()
#root.tk.call('tk', 'scaling',1.5 )
root.title(WindowTitle)
w,h=350,500
root.geometry("%dx%d"%(w,h))
root.resizable(width=FALSE, height=FALSE)
image = Image.open('transparent.png')
img = ImageTk.PhotoImage(image)
root.tk.call('wm','iconphoto',root._w,img)

#Chat window $ Entry box
ChatLog = Text(root, bd=0, bg="white", height="8", width="50", font=("Inconsolata",14))
ChatLog.insert(END, "Connecting to your partner..\n")
ChatLog.config(state=DISABLED)
EntryBox = Text(root, bd=0, bg="white",width="29", height="5", font=("Inconsolata",14))
ChatLog.place(x=0,y=6, height=h/1.5, width=w)
EntryBox.place(x=0, y=h/1.5, height=h-h/1.5, width=w)

def ConnectSocket(s,logfile):
    def PressAction(event):
            EntryBox.config(state=NORMAL)
            EntryText = FilteredMessage(EntryBox.get("0.0",END))
            LoadMyEntry(ChatLog, EntryText)

            #Scroll to the bottom of chat windows
            ChatLog.yview(END)

            #Erase previous message in Entry Box
            EntryBox.delete("0.0",END)
                    
            #Send my mesage to all others
            s.sendall(EntryText.encode('utf8'))
            logfile.write('You:')
            logfile.write(EntryText.encode('utf8'))
    def DisableEntry(event):
            EntryBox.config(state=DISABLED)
    EntryBox.bind("<Return>", DisableEntry)
    EntryBox.bind("<KeyRelease-Return>", PressAction)

def ReceiveData():
    i = 0
    logfile = open('./logfile','a+')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logfile.write('\n'+timestamp)
    while 1: #loop1: repeatedly getting data
        try: 
            data=''# make sure data doesn't remain the value read from previous iteration if the next s.recv() command won't succeed
            data = s.recv(1024)
        except:
            if i != 0:
                disconnect_msg = '\nYour partner is disconnected D;\n'
                LoadConnectionInfo(ChatLog, disconnect_msg)
                logfile.write(disconnect_msg)
                initMixer()
                playmusic('Blop.mp3')
            while 1: #loop2: repeatly try connecting
                try:
                    hostvalue = HOSTlist[i%len(HOSTlist)]
                    #print 'connecting to %s'%hostvalue
                    #sys.stdout.flush()

                    s = socket(AF_INET, SOCK_STREAM)
                    ConnectSocket(s,logfile)
                    s.connect((hostvalue, PORT))
                    connect_msg = '\nYour partner is connected ;D\n'
                    LoadConnectionInfo(ChatLog, connect_msg)
                    logfile.write(connect_msg+'\n')
                    initMixer()
                    playmusic('Atone.mp3')

                    try: #if got disconnected at this point, need to get out of loop2 in this way
                        data = s.recv(1024)
                    except:
                        break

                    break
                except Exception as e:
                    i += 1
                    pass
        if data != '':
            LoadOtherEntry(ChatLog, data)
            logfile.write('YourPartner:')
            logfile.write(data)
    logfile.close()

thread.start_new_thread(ReceiveData,())

root.mainloop()


