from doctest import master
import os
import json
from tkinter import *
from tkinter import filedialog, messagebox, colorchooser
import HuffmanCoding
import LZW


class  MyNotePad:
    current_file = "no-file"

    # Change background and foreground colors functions
    def change_back_color(self):
        c = colorchooser.askcolor()
        self.txt_area.configure(background=c[1])

    def change_fore_color(self):
        c = colorchooser.askcolor()
        self.txt_area.configure(foreground=c[1])

    # Exit file function
    def exit_file(self, event = ""):
        data = self.txt_area.get(1.0, END)
        if not data.strip():
            self.master.destroy()
        else:
            result = messagebox.askyesnocancel("Save Dialog Box", "Do you want to save this file.")
            if result == True:
                if not self.save_file() :
                    return
                self.current_file = "no-file"
                self.master.destroy()
            elif result == False:
                self.current_file = "no-file"
                self.master.destroy()

    # Clear all the text area
    def clear(self):
        self.txt_area.delete(1.0, END)

    # Function opening new file
    def new_file(self, event = ""):
        data = self.txt_area.get(1.0, END)
        # If current file is unsaved and empty
        if self.current_file == "no-file" and not data.strip():
            pass
        
        # Else, first ask if want to save the file or not
        else:
            result = messagebox.askyesnocancel("Save Dialog Box", "Do you want to save this file.")

            if result == True and not self.save_file():
                return False

            if result != None:
                self.current_file = "no-file"
                self.clear()

        self.master.title("Optimised NotePad - Untitled")
        return True

    # Function calling encoding functions and creating files conatining encoded data
    def put_into_current_file(self):
        originalText = self.txt_area.get(1.0,"end-1c")
        codes=LZW.encoder(originalText)
        reverseDict, byteArray = HuffmanCoding.encode(codes)
        fileLocation, file_extension = os.path.splitext(self.current_file)

        # Craeting decoded_text file
        f = open(self.current_file, 'wb')
        f.write(bytes(byteArray))
        f.close()

        # Creating codes files (containing huffman codes)
        f = open(fileLocation + "Codes.txt", 'w')
        f.write(json.dumps(reverseDict))
        f.close()

    # Save As function
    def saveas_file(self, event = ""):

        # Create Directory for saving file if not exists
        if not os.path.exists("./Files/"):
            os.makedirs("./Files/")
        
        # Asking where to save file
        file = filedialog.asksaveasfilename(initialdir = "./Files/", initialfile="Untitled.bin", defaultextension=".bin", filetypes=[("Binary files only","*.bin")])
        if not file :
            return False
        
        self.current_file = file
        self.put_into_current_file()

        self.master.title("Optimised NotePad - " + os.path.basename(self.current_file))
        return True

    # Save function
    def save_file(self, event = ""):
        # If files is not saved before, first do a Save As
        if self.current_file == "no-file":
            return self.saveas_file()
        else:
            self.put_into_current_file()
            return True

    # Function opening an existing file and calls decoding functions
    def open_file(self, event = ""):

        # Handling already opened file/text
        if not self.new_file():
            return
        
        if not os.path.exists("./Files/"):
            os.makedirs("./Files/")
        
        file = filedialog.askopenfilename(initialdir = "./Files/", defaultextension=".bin", filetypes=[("Binary files only","*.bin")])
        if not file :
            return
        self.current_file = file
        fileLocation, file_extension = os.path.splitext(file)

        # If corresponding codes file not exist, return error
        if not os.path.isfile(fileLocation+"Codes.txt"):
            messagebox.showerror("Codes File Not Found", "Required " + os.path.basename(fileLocation) + "Codes.txt not found.")
            return
        
        # Getting encoded byte string and reverse dictionary from corresponding files
        f = open(file, 'rb')
        byteString = f.read()
        f.close()

        f = open(fileLocation+"Codes.txt",'r')
        reverseDict = json.loads(f.read())
        f.close()

        # Getting decoded string and putting it into text editor
        encryptedText = HuffmanCoding.decode(byteString, reverseDict)
        encryptedText = [int(i) for i in encryptedText.split()]
        originalText=LZW.decoder(encryptedText)
        self.txt_area.delete(1.0, END)
        self.txt_area.insert(1.0,originalText)

        self.master.title("Optimised NotePad - " + os.path.basename(fileLocation))
    
    # Normal Edit functions
    def undo_file(self, event = ""):
        self.txt_area.edit_undo()
    
    def redo_file(self, event = ""):
        self.txt_area.edit_redo()

    def copy_file(self, event = ""):
        data = self.txt_area.selection_get()
        if not data:
            return
        self.txt_area.clipboard_append(data)

    def paste_file(self, event=""):
        self.txt_area.insert(INSERT, self.txt_area.clipboard_get())

    def del_file(self, event = ""):
        self.txt_area.delete('sel.first', 'sel.last')

    def cut_file(self, event = ""):
        self.copy_file()
        self.del_file()

    def selectall_file(self, event=""):
        self.txt_area.tag_add(SEL, "1.0", END)
        self.txt_area.mark_set(INSERT, "1.0")

    def about_notepad(self):
        messagebox.showinfo("Optimised Notepad","A Notepad By coder-saab001")
        
    def __init__(self, master):
        self.master = master

        master.title("Optimised NotePad - Untitled")
        root.geometry("1300x788")

        # Setting icon of Window
        p1 = PhotoImage(file = 'notepad.png')
        master.iconphoto(False, p1)

        # Binding shortcut keys
        master.bind("<Control-o>", self.open_file)
        master.bind("<Control-O>", self.open_file)

        master.bind("<Control-s>", self.save_file)
        master.bind("<Control-S>", self.save_file)

        master.bind("<Control-Shift-s>", self.saveas_file)
        master.bind("<Control-Shift-S>", self.saveas_file)

        master.bind("<Control-n>", self.new_file)
        master.bind("<Control-N>", self.new_file)

        master.bind("<Control-q>", self.exit_file)
        master.bind("<Control-Q>", self.exit_file)

        master.bind("<Control-a>", self.selectall_file)
        master.bind("<Control-A>", self.selectall_file)
        
        # Creating text area
        self.txt_area = Text(master, font = ("Consolas"), padx=5, pady = 5, wrap=WORD, selectbackground="red", bd = 2, insertwidth=3, undo=True)
        self.txt_area.pack(fill = BOTH, expand = 1)

        #Creating main menu
        self.main_menu = Menu()
        self.master.config(menu = self.main_menu)

        # Creating file menu and adding to main menu
        self.file_menu = Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label = " File ", menu = self.file_menu)
        self.file_menu.add_command(label = " New ", accelerator=" Ctrl+N ", command = self.new_file)
        self.file_menu.add_command(label = " Open ", accelerator=" Ctrl+O ", command = self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label = " Save ", accelerator=" Ctrl+S ", command = self.save_file)
        self.file_menu.add_command(label = " Save As ", accelerator=" Ctrl+Shift+S ", command = self.saveas_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label = " Quit ", accelerator=" Ctrl+Q ", command = self.exit_file)
        
        #########################################################

        # Creating edit menu and adding to main menu
        self.edit_menu = Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label = " Edit ", menu = self.edit_menu)
        self.edit_menu.add_command(label = " Undo ", accelerator=" Ctrl+Z ", command = self.undo_file)
        self.edit_menu.add_command(label = " Redo ", accelerator=" Ctrl+Y ", command = self.redo_file)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label = " Cut ", accelerator=" Ctrl+X ", command = self.cut_file)
        self.edit_menu.add_command(label = " Copy ", accelerator=" Ctrl+C ", command = self.copy_file)
        self.edit_menu.add_command(label = " Paste ", accelerator=" Ctrl+V ", command = self.paste_file)
        self.edit_menu.add_command(label = " Select All ", accelerator=" Ctrl+A ", command = self.selectall_file)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label = " Delete ", accelerator=" Del ", command = self.del_file)

        #########################################################

        # Creating a help menu
        self.help_menu = Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label = " Help ", menu = self.help_menu)
        self.help_menu.add_command(label = " About Optimized Notepad ", command = self.about_notepad)

        #Adding scrollbar
        scrollBar=Scrollbar(self.txt_area, cursor="circle")
        scrollBar.pack(side=RIGHT, fill=Y)
        scrollBar.config(command=self.txt_area.yview)
        self.txt_area.config(yscrollcommand=scrollBar.set)

        # Handling window closing
        root.protocol("WM_DELETE_WINDOW", self.exit_file)
        
root = Tk()
b = MyNotePad(root)
root.mainloop() # run the Tkinter event loop
