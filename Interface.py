import tkinter as tk
from PIL import ImageTk, Image
import sqlite3

root = tk.Tk()
a = ("Comic Sans MS", 15, "bold")
b = ("Comic Sans MS", 20, "bold")
root.geometry("800x600")
#root.resizable(False, False)
img = ImageTk.PhotoImage(Image.open("books.jpg"))
imagelabel = tk.Label(root, image=img).grid(row=0, column=0, columnspan=2, rowspan=4)


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

        conn = sqlite3.connect('DecksDB.db')
        cursor = conn.cursor()

        # CREATE A DECKTABLE;
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        decks = cursor.fetchall()

        # ADDING SEARCHES TO A LIST;
        self.deck_list = []
        for deck in decks:
            self.deck_list.append(str(deck[0]))
        # CLOSE CONNECTION;
        conn.commit()
        conn.close()

        # create a list box
        self.list_var = tk.StringVar(value=self.deck_list)

        self.listbox = tk.Listbox(root, listvariable=self.list_var, height=10, font=('Comic Sans MS', 18),
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
        root.columnconfigure(0, weight=0)
        root.rowconfigure(0, weight=0)
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
            self.selected_indices = self.listbox.curselection()

            # get selected items
            selected_decks = ",".join([self.listbox.get(i) for i in self.selected_indices])

            self.listbox.destroy()
            self.scrollbar.destroy()
            self.AddBtn.destroy()
            self.BackBtn.destroy()
            FourthPage(root,selected_decks)

            print(f'You selected: {selected_decks}')




class ThirdPage(tk.Frame):
    def __init__(self, master):
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
        self.deck = self.Name_entry.get()
        self.Add_Deck_to_database(self.deck)
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

    def Add_Deck_to_database(self, Deck):
        # CONNECT TO DATABASE;
        conn = sqlite3.connect('DecksDB.db')
        cursor = conn.cursor()

        # CREATE A DECKTABLE;

        cursor.execute(f'CREATE TABLE IF NOT EXISTS [{Deck}](Front NULL, Back NULL)')

        # CLEAR SEARCH BOX TO ENTER A NEW SEARCH;
        self.Name_entry.delete(0, tk.END)

        # CLOSE CONNECTION;
        conn.commit()
        conn.close()

class FourthPage(tk.Frame):
    def __init__(self, master,deck=None):
        super().__init__(master,deck=None)
        self.deck = deck
        self.Widgets()

    def Widgets(self):
        self.EditBtn = tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text=f"Edit {self.deck}", command=self.Edit_Deck)
        self.EditBtn.grid(row=1, column=0, pady=5, sticky="we")

        self.DeleteBtn = tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text=f"Delete {self.deck}", command= self.Delete_Deck)
        self.DeleteBtn.grid(row=2, column=0, pady=25, sticky="we")

        self.PlayBtn = tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text=f"Play {self.deck}", command=self.Play_Deck)
        self.PlayBtn.grid(row=3, column=0, pady=25, sticky="we")

    def Edit_Deck(self):
        self.EditBtn.destroy()
        self.DeleteBtn.destroy()
        self.PlayBtn.destroy()
        FifthPage(root,self.deck)

    def Delete_Deck(self):

        # delete deck from database
        conn = sqlite3.connect('DecksDB.db')
        cursor = conn.cursor()

        cursor.execute(f'DROP TABLE {self.deck} ;')
        # CLOSE CONNECTION;
        conn.commit()
        conn.close()

        self.EditBtn.destroy()
        self.DeleteBtn.destroy()
        self.PlayBtn.destroy()
        ThirdPage(root).Cancel_Func()





    def Play_Deck(self):
        pass


class FifthPage(tk.Frame):
    def __init__(self, master,deck=None):
        super().__init__(master,deck=None)
        self.deck = deck
        self.Widgets()

    def Widgets(self):
        root.columnconfigure(0, weight=0)
        root.rowconfigure(0, weight=0)

        self.EditName = tk.Button(root, text='Edit Name', command=self.EditName_func,
                                 font=('Comic Sans MS', 18, "bold"), bg='pink')
        self.EditName.grid(row=0, column=0, sticky='we', ipady=10, columnspan=1)

        self.EditCard = tk.Button(root, text='Edit Cards', command=self.EditCard_func,
                                  font=('Comic Sans MS', 18, "bold"), bg='pink')
        self.EditCard.grid(row=1, column=0, sticky='we', ipady=10, columnspan=1)

    def EditName_func(self):
        self.EditName.destroy()
        self.EditCard.destroy()
        self.Name_Label = tk.Label(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text=f"Name:", border="2px")
        self.Name_Label.grid(row=0, column=0, ipady=10, sticky='we')

        self.Name_entry = tk.Entry(root, bg="white", font=('Comic Sans MS', 18, "bold"), justify='center', width=35)
        self.Name_entry.grid(row=0, column=1, ipady=10, sticky='we')
        self.Name_entry.insert(0, self.deck)

        self.Submit = tk.Button(root, text='Submit', command=self.Submit_func, font=('Comic Sans MS', 18, "bold"), bg='pink')
        self.Submit.grid(row=1, column=0, sticky='we', columnspan=2)

        self.Back = tk.Button(root, text='↩ Back', command=self.Back_func, font=('Comic Sans MS', 18, "bold"),
                                bg='pink')
        self.Back.grid(row=2, column=0, sticky='we',columnspan=2)


    def Submit_func(self):
        self.New_Name = self.Name_entry.get()
        conn = sqlite3.connect('DecksDB.db')
        cursor = conn.cursor()

        cursor.execute(f"ALTER TABLE [{self.deck}] RENAME TO [{self.New_Name}];")
        # CLOSE CONNECTION;
        conn.commit()
        conn.close()

        self.Name_Label.destroy()
        self.Name_entry.destroy()
        self.Submit.destroy()
        self.Back.destroy()
        FourthPage(root, self.New_Name)

    def Back_func(self):
        self.Name_Label.destroy()
        self.Name_entry.destroy()
        self.Submit.destroy()
        self.Back.destroy()
        FourthPage(root,self.deck)

    def EditCard_func(self):
        self.EditName.destroy()
        self.EditCard.destroy()
        SixthPage(root,self.deck)

class SixthPage(tk.Frame):
    def __init__(self, master, deck=None):
        super().__init__(master, deck=None)
        self.deck = deck
        self.Widgets()

    def Widgets(self):
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        conn = sqlite3.connect('DecksDB.db')
        cursor = conn.cursor()

        # CREATE A DECKTABLE;

        cursor.execute("SELECT Front FROM "+ self.deck)
        cards = cursor.fetchall()

        # ADDING SEARCHES TO A LIST;
        self.card_list = []
        for card in cards:
            self.card_list.append(str(card[0]))
        print(self.card_list)

        # CLOSE CONNECTION;
        conn.commit()
        conn.close()

        # create a list box
        self.list_var = tk.StringVar(value=self.card_list)


        self.Back = tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text="↩ Back",command = self.Back_func)
        self.Back.grid(row=1, column=0, sticky="w")

        self.AddCard = tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text="Add Card",command= self.AddCard_func)
        self.AddCard.grid(row=1, column=1, sticky="e")


        self.listbox = tk.Listbox(root, listvariable=self.list_var, height=10, font=('Comic Sans MS', 18),
                                  selectforeground='White', selectmode='extended', bg="pink")
        self.listbox.grid(row=2, column=0, columnspan=2, sticky='we')

        self.scrollbar = tk.Scrollbar(root, orient='vertical', command=self.listbox.yview)
        self.scrollbar.grid(row=2, column=2, sticky='ns')


    def AddCard_func(self):
        self.Back.destroy()
        self.scrollbar.destroy()
        self.AddCard.destroy()
        self.listbox.destroy()

        root.columnconfigure(0, weight=0)
        root.rowconfigure(0, weight=0)

        # FRONT of flashcard
        self.Front_Label = tk.Label(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text=f"FRONT:",
                                   border="2px")
        self.Front_Label.grid(row=0, column=0, ipady=10, sticky='we')

        self.Front_entry = tk.Entry(root, bg="white", font=('Comic Sans MS', 18, "bold"), justify='center', width=35)
        self.Front_entry.grid(row=0, column=1, ipady=10, sticky='we')


        # BACK of flashcard
        self.BACK_Label = tk.Label(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text=f"BACK:",
                                   border="2px")
        self.BACK_Label.grid(row=1, column=0, ipady=10, sticky='we')

        self.BACK_entry = tk.Entry(root, bg="white", font=('Comic Sans MS', 18, "bold"), justify='center', width=35)
        self.BACK_entry.grid(row=1, column=1, ipady=10, sticky='we')


        self.Submit = tk.Button(root, text='Submit', font=('Comic Sans MS', 18, "bold"), bg='pink',command= self.Submit_func)
        self.Submit.grid(row=2, column=0, sticky='we', columnspan=2)

        self.Back = tk.Button(root, text='↩ Back', font=('Comic Sans MS', 18, "bold"), bg='pink',command= self.Back_func_2)
        self.Back.grid(row=3, column=0, sticky='we', columnspan=2)


    def Back_func(self):
        self.Back.destroy()
        self.scrollbar.destroy()
        self.AddCard.destroy()
        self.listbox.destroy()

        FourthPage(root, self.deck)

    def Back_func_2(self):
        self.Front_Label.destroy()
        self.Front_entry.destroy()
        self.BACK_entry.destroy()
        self.BACK_Label.destroy()
        self.Submit.destroy()
        self.Back.destroy()
        FifthPage(root,self.deck)

# function adds card to deck table.
    def Submit_func(self):
        # CONNECT TO DATABASE;
        conn = sqlite3.connect('DecksDB.db')
        cursor = conn.cursor()

        # INSERT CARD INTO DECKTABLE
        params = (self.Front_entry.get(),self.BACK_entry.get())
        cursor.execute("INSERT INTO "+ self.deck + " VALUES (?,?)",params)

        # CLEAR BOX TO ENTER A NEW CARD;
        self.Front_entry.delete(0, tk.END)
        self.BACK_entry.delete(0, tk.END)



        # CLOSE CONNECTION;
        conn.commit()
        conn.close()




root.mainloop()
