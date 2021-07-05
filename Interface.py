import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter.messagebox import showinfo

root = tk.Tk()
a = ("Comic Sans MS", 15, "bold")
b = ("Comic Sans MS", 20, "bold")
root.geometry("800x600")
root.resizable(False, False)
img = ImageTk.PhotoImage(Image.open("books.jpg"))
imagelabel = tk.Label(root, image=img).grid(row=0, column=0,columnspan=2,rowspan=4)

# The HomePage
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

# u are given a list of decks
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
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)




        # create a scrollbar
        self.scrollbar = tk.Scrollbar(root, orient='vertical', command=self.listbox.yview)
        self.scrollbar.grid(row=1, column=1, sticky='wns')

        # create an Add deck button
        self.AddBtn = tk.Button(root, text='Add Deck', command= self.AddDeck, font=('Comic Sans MS', 18, "bold"), bg='pink')
        self.AddBtn.grid(row=0, column=0, sticky='es', ipady=5)

        # create a go back button
        self.BackBtn = tk.Button(root, text='↩ Back', command=self.BackBtn, font=('Comic Sans MS', 18, "bold"), bg = 'pink')
        self.BackBtn.grid(row=0, column=0, sticky='ws', ipady=5)

    def BackBtn(self):
        self.listbox.destroy()
        self.scrollbar.destroy()
        self.AddBtn.destroy()
        self.BackBtn.destroy()
        FirstPage(root)

    def AddDeck(self):
        self.listbox.destroy()
        self.scrollbar.destroy()
        self.AddBtn.destroy()
        self.BackBtn.destroy()
        ThirdPage(root)

        # handle event
    def items_selected(self, event):
            # get selected indices
            selected_indices = self.listbox.curselection()

            # get selected items
            selected_decks = ",".join([self.listbox.get(i) for i in selected_indices])

            self.listbox.destroy()
            self.scrollbar.destroy()
            self.AddBtn.destroy()
            self.BackBtn.destroy()
            FourthPage(root)

            print(f'You selected: {selected_decks}')




class ThirdPage(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.Widgets()

    def Widgets(self):
        self.Name_Label = tk.Label(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text="NAME DECK:", border="2px")
        self.Name_Label.grid(row=0, column=0, ipady=10, sticky='we')

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

class FourthPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.Widgets()

    def Widgets(self):
        self.EditBtn = tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text="Edit Deck", command=self.Edit_Deck)
        self.EditBtn.grid(row=1, column=0, pady=5, sticky="we")

        self.DeleteBtn = tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text="Delete Deck", command= self.Delete_Deck)
        self.DeleteBtn.grid(row=2, column=0, pady=25, sticky="we")

        self.PlayBtn = tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text="Play Deck", command=self.Play_Deck)
        self.PlayBtn.grid(row=3, column=0, pady=25, sticky="we")

    def Edit_Deck(self):
        self.EditBtn.destroy()
        self.DeleteBtn.destroy()
        self.PlayBtn.destroy()
        FifthPage(root)

    def Delete_Deck(self):
        self.EditBtn.destroy()
        self.DeleteBtn.destroy()
        self.PlayBtn.destroy()
        ThirdPage(root).Cancel_Func()

    def Play_Deck(self):
        pass


class FifthPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.Widgets()

    def Widgets(self):
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.Name_Label = tk.Label(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text="Name Of Deck:", border="2px")
        self.Name_Label.grid(row=0, column=0, ipady=10, sticky='we')

        self.Name_entry = tk.Entry(root, bg="white", font=('Comic Sans MS', 18, "bold"), justify='center', width=35)
        self.Name_entry.grid(row=0, column=1, ipady=10, sticky='we')

        self.Submit = tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text="SUBMIT")
        self.Submit.grid(row=1, column=0, sticky="w")

        self.Cancel = tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text="CANCEL")
        self.Cancel.grid(row=1, column=1, sticky="e")

        # create a list box
        self.langs = ('card1', 'card2', 'card3', 'card4', 'card5', 'card6', 'card7', 'card8', 'card9')

        self.langs_var = tk.StringVar(value=self.langs)

        self.listbox = tk.Listbox(root, listvariable=self.langs_var, height=10, font=('Comic Sans MS', 18), selectforeground ='White', selectmode='extended', bg="pink")
        self.listbox.grid(row=2, column=0, columnspan=2, sticky='we')

        self.scrollbar = tk.Scrollbar(root, orient='vertical', command=self.listbox.yview)
        self.scrollbar.grid(row=2, column=2, sticky='ns')


root.mainloop()
