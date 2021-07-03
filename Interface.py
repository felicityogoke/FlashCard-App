import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

# create the root window
root = tk.Tk()
a = ("Comic Sans MS", 15, "bold")
b = ("Comic Sans MS", 20, "bold")
root.geometry("430x430")
root.configure(bg='white')
root.resizable(False, False)

class FirstPage(tk.Frame):
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

        self.listbox = tk.Listbox(root, listvariable=self.langs_var, height=10, font=('Comic Sans MS', 18), selectforeground= 'White', selectmode='extended',bg="white")
        self.listbox.grid(row=1,column=0,  sticky= 'nwes')
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)


        # create a scrollbar
        self.scrollbar = tk.Scrollbar(root, orient='vertical', command=self.listbox.yview)
        self.scrollbar.grid(row=1, column=1, sticky='nsw')

        # create an Add deck button
        self.AddBtn = tk.Button(root,text='Add Deck', command=self.AddDeck, font=('Comic Sans MS', 12, "bold"), bg='white')
        self.AddBtn.grid(row=0, column=1, sticky='w', ipady=10)

    def AddDeck(self):
        pass



FirstPage(root)
root.mainloop()
