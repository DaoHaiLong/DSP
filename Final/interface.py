from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
from LSBMethod import *
from PhaseCodingMethod import *
from abstracmethod import*

root = Tk()
root.geometry("755x700")

# create window using from in Tkinter
class Application(Frame):
    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)
        # reference to the master widget, which is the tk window
        self.master = master
        self.initUI()
    # Creation of init_window
    def initUI(self):
        # changing the title of our master widget
        self.master.title("Audio Steganography")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        self.interfaceEncoding()
        self.interfaceDencoding()
        self.infomation()
        
        
    def infomation(self):
        self.infor= StringVar()
        self.lblinfor = Label(root, textvariable=self.infor,font=('arial',30, "bold italic"))
        self.lblinfor.place(x=180, y=10)
        self.infor.set("Audio Steganography ")
        
        self.exit = Button(root, text="Exit", command=self.Exit)
        self.exit.place(x=310, y=560,height=50, width=150)

    def interfaceEncoding(self):
        # encode Label
        self.encoded= StringVar()
        self.lblencode = Label(root, textvariable=self.encoded,font=('arial',15, "bold italic"))
        self.lblencode.place(x=80, y=80)
        self.encoded.set("Encoding ")
        # select method
        self.optionencodeVar = StringVar()
        self.optionencodeVar.set("Least Significant Bit")  # default value

        self.Menu = OptionMenu(root,self.optionencodeVar, "Least Significant Bit", "Phase Coding",)
        self.Menu.place(x=10, y=150,height=30, width=245)
        # creating a button instance
        self.selectFiled = Button(self, text="Select File To Encode", command=self.selectFileEncode)
        self.selectFiled.place(x=10, y=200,height=30, width=245)

        # file location label
        self.location = StringVar()
        self.lbllocation = Entry(root,font=('arial', 13), textvariable=self.location )
        self.lbllocation.place(x=10, y=250,height=30,width=245)
        # placing the button on my window

        # entry box
        self.lblmess=Label(root, text='Enter Message',font=('arial',13, "bold italic"))
        self.lblmess.place(x=70,y=285)
        self.entryText = Entry(root)
        self.entryText.place(x=10, y=310,height=30,width=245)
        
        # encoded  location label
        self.lblmess=Label(root, text='Save Location',font=('arial',13, "bold italic"))
        self.lblmess.place(x=70,y=340)
    
        self.enocdedLocation = StringVar()
        self.locationOfEncodeFile = Entry(root, textvariable=self.enocdedLocation,font=('arial', 13))
        self.locationOfEncodeFile.place(x=10, y=370,height=30,width=245)
        
        self.encodeButton = Button(self, text="Encode", command=self.encode)
        self.encodeButton.place(x=230, y=500,height=50,width=150)

    def interfaceDencoding(self):
        # decode Label
        self.decodeVar = StringVar()
        self.decodelabel = Label(root, textvariable=self.decodeVar,font=('arial',15, "bold italic"))
        self.decodelabel.place(x=570, y=80)
        self.decodeVar.set("Decoding ")

        # select method
        self.decodeOptionsVar = StringVar()
        self.decodeOptionsVar.set("Least Significant Bit")  # default value

        self.decodingOptionsMenu = OptionMenu(root, self.decodeOptionsVar, "Least Significant Bit", "Phase Coding")
        self.decodingOptionsMenu.place(x=500, y=150,height=30, width=245)
        # creating a button instance
        self.selectFileDecodeButton = Button(self, text="Select  File To Decode ", command=self.selectFileDecode)
        self.selectFileDecodeButton.place(x=500, y=200,height=30, width=245)
        #
        # file location label
        self.locationdecode = StringVar()
        self.lbllocationdecode = Entry(root,font=('arial', 13), textvariable=self.locationdecode)
        self.lbllocationdecode.place(x=500, y=250,height=30, width=245)

        self.lblmess=Label(root, text='Decoding text ',font=('arial',13, "bold italic"))
        self.lblmess.place(x=570,y=340)
    
        self.denocdedLocation = StringVar()
        self.locationOfDencodeFile = Entry(root, textvariable=self.denocdedLocation)
        self.locationOfDencodeFile.place(x=500, y=370,height=30, width=245)
        
        self.dencodeButton = Button(root,text="Decode", command=self.decode)
        self.dencodeButton.place(x=400, y=500,height=50,width=150)


    def selectFileEncode(self):
        # file selection
        root.AudioName = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.wav"), ("all files", "*.*")))
        self.fileSelected = root.AudioName
        self.location.set(root.AudioName)

    def selectFileDecode(self):
        root.AudioName = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.wav"), ("all files", "*.*")))
        self.fileSelcetedForDecode = root.AudioName
        self.locationdecode.set(root.AudioName)

    def encode(self):
        # select method to encode
        if self.optionencodeVar.get() == "Least Significant Bit":
            method = LSB()
        else:
            method = PhaseCoding()
        result = method.encodeAudio(self.fileSelected, self.entryText.get())
        self.enocdedLocation.set(result)

    def decode(self):
        # select method to decode
        if self.decodeOptionsVar.get() == "Least Significant Bit":
            method = LSB()
        else:
            method = PhaseCoding()

        result = method.decodeAudio(self.fileSelcetedForDecode)
        self.denocdedLocation.set(result)
    
    def Exit(self):
        self.exit_program = messagebox.askyesno(
            title='Audio Steganography Application',
            message='Confirm if you want to exit program?')
        if self.exit_program > 0:
            root.destroy()
        else:
            return None

# creation of an instance of window
app = Application(root)

# mainloop
root.mainloop()