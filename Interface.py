import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

root = tk.Tk()
a = ("Comic Sans MS", 15, "bold")
b = ("Comic Sans MS", 20, "bold")
root.geometry("800x600")
root.resizable(False, False)
img = ImageTk.PhotoImage(Image.open("books.jpg"))
imagelabel = tk.Label(root, image=img).grid(row=0, column=0,columnspan=2,rowspan=3)


class FirstPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.Widgets()

    def Widgets(self):
        self.DeckBtn = tk.Button(root, text='Go To Decks ➤', command=self.GoToDeckFunc,
                                 font=('Comic Sans MS', 18, "bold"), bg='pink')
        self.DeckBtn.grid(row=1, column=0, sticky='we', ipady=15,columnspan=2)

    # function for going to deck page
    def GoToDeckFunc(self):
        self.DeckBtn.destroy()
        SecondPage(root)


FirstPage(root)


class SecondPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.Widgets()

    def Widgets(self):
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        # create a list box
        self.langs = ('deck1', 'deck2', 'deck3', 'deck4', 'deck5',
                      'deck6', 'deck7', 'deck8', 'deck9')

        self.langs_var = tk.StringVar(value=self.langs)

        self.listbox = tk.Listbox(root, listvariable=self.langs_var, height=10, font=('Comic Sans MS', 18),
                                  selectforeground='White', selectmode='extended', bg="pink")
        self.listbox.grid(row=1, column=0, sticky='nwes')
        # self.listbox.bind('<<ListboxSelect>>', self.items_selected)

        # create a scrollbar
        self.scrollbar = tk.Scrollbar(root, orient='vertical', command=self.listbox.yview)
        self.scrollbar.grid(row=1, column=1, sticky='wns')

        # create an Add deck button
        self.AddBtn = tk.Button(root, text='Add Deck', command=self.AddDeck, font=('Comic Sans MS', 18, "bold"),
                                bg='pink')
        self.AddBtn.grid(row=0, column=0, sticky='we', ipady=15,columnspan=2)

    def AddDeck(self):
        self.listbox.destroy()
        self.scrollbar.destroy()
        self.AddBtn.destroy()
        ThirdPage(root)

class ThirdPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.Widgets()

    def Widgets(self):
        self.Name_Label = tk.Label(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text="NAME DECK:", border="2px")
        self.Name_Label.grid(row=0, column=0,ipady=10, sticky='we')

        self.Name_entry = tk.Entry(root, bg="white", font=('Comic Sans MS', 18, "bold"), justify='center', width=35)
        self.Name_entry.grid(row=0, column=1, ipady=10, sticky='we')

        self.Submit= tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text="SUBMIT",command=self.Submit_Deck)
        self.Submit.grid(row=1, column=0, columnspan=2, sticky="we")

        self.Cancel= tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text="CANCEL",command= self.Cancel_Func)
        self.Cancel.grid(row=2, column=0, columnspan=2, pady=100, sticky="we")



    def Submit_Deck(self):
        self.Name_Label.destroy()
        self.Name_entry.destroy()
        self.Submit.destroy()
        self.Cancel.destroy()
        SecondPage(root)

    def Cancel_Func(self):
        self.Name_Label.destroy()
        self.Name_entry.destroy()
        self.Submit.destroy()
        self.Cancel.destroy()
        SecondPage(root)


root.mainloop()
