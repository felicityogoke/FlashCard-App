import tkinter as tk
from PIL import ImageTk, Image
import sqlite3
from tkinter.messagebox import showinfo

root = tk.Tk()
a = ("Comic Sans MS", 15, "bold")
b = ("Comic Sans MS", 20, "bold")
root.geometry("800x600")
root.resizable(False, False)
img = ImageTk.PhotoImage(Image.open("books.jpg"))
imagelabel = tk.Label(root, image=img).grid(row=0, column=0, columnspan=2, rowspan=4)


# THE HOME PAGE
class FirstPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.Widgets()

    # CONTAINS A BUTTON TO DIRECT TO A NEW PAGE CONTAINING LIST OF DECKS
    def Widgets(self):
        self.GoToDeckBtn = tk.Button(root, text='Go To Decks ➤', command=self.GoToDeckFunc,
                                     font=('Comic Sans MS', 18, "bold"), bg='pink')
        self.GoToDeckBtn.grid(row=1, column=0, sticky='we', ipady=15, columnspan=2)

    # FUNCTION FOR GoToDeckBtn BUTTON
    def GoToDeckFunc(self):
        self.GoToDeckBtn.destroy()
        SecondPage(root)


FirstPage(root)


# THE SECOND PAGE THAT CONTAINS A LIST OF DECKS
class SecondPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.deck_list = self.GetListOfDecks()
        self.Widgets()

    # FUNCTION TO GET ALL DECKS FROM DATABASE
    def GetListOfDecks(self):
        conn = sqlite3.connect('DecksDB.db')
        cursor = conn.cursor()

        # selects all decks from database;
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        decks = cursor.fetchall()

        # adding decks to list;
        self.deck_list = []
        for deck in decks:
            self.deck_list.append(str(deck[0]))

        # close connection;
        conn.commit()
        conn.close()
        return self.deck_list

    def Widgets(self):
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # A list box
        self.list_var = tk.StringVar(value=self.deck_list)

        self.listbox = tk.Listbox(root, listvariable=self.list_var, height=10, font=('Comic Sans MS', 18),
                                  selectforeground='White', selectmode='extended', bg="pink")
        self.listbox.grid(row=2, column=0, sticky='nwes')
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)

        # A scrollbar
        self.scrollbar = tk.Scrollbar(root, orient='vertical', command=self.listbox.yview)
        self.scrollbar.grid(row=2, column=1, sticky='wns')

        # A button that returns to the previous page
        self.BackBtn = tk.Button(root, text='↩Back', command=self.BackBtnFunc, font=('Comic Sans MS', 18, "bold"),
                                 bg='pink')
        self.BackBtn.grid(row=0, column=0, sticky='nw', ipady=5)

        # A button to add decks to list
        self.AddDeckBtn = tk.Button(root, text='Add Deck', command=self.AddDeckFunc, font=('Comic Sans MS', 18, "bold"),
                                    bg='pink')
        self.AddDeckBtn.grid(row=1, column=0, sticky='we', ipady=5, columnspan=2)

    # FUNCTION FOR BackBtn BUTTON
    def BackBtnFunc(self):
        self.listbox.destroy()
        self.scrollbar.destroy()
        self.AddDeckBtn.destroy()
        self.BackBtn.destroy()
        root.columnconfigure(0, weight=0)
        root.rowconfigure(0, weight=0)
        FirstPage(root)

    # FUNCTION FOR AddDeckBtn BUTTON
    def AddDeckFunc(self):
        self.listbox.destroy()
        self.scrollbar.destroy()
        self.AddDeckBtn.destroy()
        self.BackBtn.destroy()
        ThirdPage(root)

    # FUNCTION WHEN ITEM IS SELECTED FROM DECKS LIST.
    def items_selected(self, event):
        # get selected indices
        self.selected_indices = self.listbox.curselection()

        # get selected items
        selected_decks = ",".join([self.listbox.get(i) for i in self.selected_indices])

        self.listbox.destroy()
        self.scrollbar.destroy()
        self.AddDeckBtn.destroy()
        self.BackBtn.destroy()
        FourthPage(root, selected_decks)

        print(f'You selected: {selected_decks}')


# THIRD PAGE THAT SHOWS ENTRY BOX WHERE USER ENTERS NAME OF NEW DECK, A SUBMIT BUTTON AND A BACK BUTTON
class ThirdPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.Widgets()


    def Widgets(self):
        root.columnconfigure(0, weight=0)
        root.rowconfigure(0, weight=0)
        # A button to return to previous page.
        self.BackBtn = tk.Button(root, text='↩Back', command=self.BackBtnFunc, font=('Comic Sans MS', 18, "bold"),
                                 bg='pink')
        self.BackBtn.grid(row=0, column=0, sticky='nw', ipady=5)

        self.NameLabel = tk.Label(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text="NAME DECK:", border="2px")
        self.NameLabel.grid(row=1, column=0, ipady=10, sticky='we')

        self.NameEntry = tk.Entry(root, bg="white", font=('Comic Sans MS', 18, "bold"), justify='center', width=35)
        self.NameEntry.grid(row=1, column=1, ipady=10, sticky='we')

        self.SubmitBtn = tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text="SUBMIT",
                                   command=self.SubmitDeckFunc)
        self.SubmitBtn.grid(row=3, column=0, columnspan=2, sticky="we")

    # FUNCTION FOR SubmitBtn BUTTON
    # IT CREATES A NEW DECK TABLE IN DATABASE WHEN THE SubmitBtn BUTTON IS CLICKED
    def SubmitDeckFunc(self):
        Deck = self.NameEntry.get()
        # Connect to database;
        conn = sqlite3.connect('DecksDB.db')
        cursor = conn.cursor()

        # Create a deck table;
        cursor.execute(f'CREATE TABLE IF NOT EXISTS [{Deck}](Front NULL, Back NULL)')

        # Close connection;
        conn.commit()
        conn.close()

        # Clear search box to enter new word;
        self.NameEntry.delete(0, tk.END)

    # FUNCTION FOR BackBtn BUTTON
    def BackBtnFunc(self):
        self.BackBtn.destroy()
        self.NameLabel.destroy()
        self.NameEntry.destroy()
        self.SubmitBtn.destroy()
        SecondPage(root)


# FOURTH PAGE; WHEN DECK IS SELECTED THEY ARE TAKEN TO FOURTH PAGE
# THERE THEY ARE GIVEN 2 OPTIONS; PLAY OR DELETE
class FourthPage(tk.Frame):
    def __init__(self, master, deck=None):
        super().__init__(master, deck=None)
        self.deck = deck
        self.Widgets()

    def Widgets(self):
        # A button to return to previous page.
        self.BackBtn = tk.Button(root, text='↩Back', command=self.BackBtnFunc, font=('Comic Sans MS', 18, "bold"),bg='pink')
        self.BackBtn.grid(row=0, column=0, sticky='nw', ipady=5)

        # A button to play Deck.
        self.PlayBtn = tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text=f"Play {self.deck}", command= self.PlayDeckFunc)
        self.PlayBtn.grid(row=1, column=0, sticky="we", pady=50)

        # A button to play Deck.
        self.DeleteDeckBtn = tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text=f"Delete {self.deck}", command= self.DeleteDeckFunc)
        self.DeleteDeckBtn.grid(row=3, column=0, sticky="we", pady=50)

    # FUNCTION FOR BackBtn BUTTON
    def BackBtnFunc(self):
        self.BackBtn.destroy()
        self.PlayBtn.destroy()
        self.DeleteDeckBtn.destroy()
        SecondPage(root)

    # FUNCTION FOR PlayBtn BUTTON
    def PlayDeckFunc(self):
        self.BackBtn.destroy()
        self.PlayBtn.destroy()
        self.DeleteDeckBtn.destroy()
        FifthPage(root, self.deck)

    # FUNCTION FOR DeleteDeckBtn BUTTON
    def DeleteDeckFunc(self):
        # Connect to db
        conn = sqlite3.connect('DecksDB.db')
        cursor = conn.cursor()

        # delete deck from db
        cursor.execute(f'DROP TABLE {self.deck} ;')

        # Close connection;
        conn.commit()
        conn.close()



# FIFTH PAGE; OPENS WHEN PLAY OPTION IS CLICKED,
class FifthPage(tk.Frame):
    def __init__(self, master, deck=None):
        super().__init__(master, deck=None)
        self.deck = deck
        self.Widgets()

    # FUNCTION THAT RETURNS LISTS OF CARDS SAVED IN SPECIFIED DECK
    def GetListOfCards(self):
        conn = sqlite3.connect('DecksDB.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM " + self.deck)
        self.cards = cursor.fetchall()

        # CLOSE CONNECTION;
        conn.commit()
        conn.close()

        return self.cards

    # CONTAINS FLIPPABLE CARD, BACK BUTTON AND NEXT BUTTON
    def Widgets(self):
        try:
            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=1)

            self.cards = self.GetListOfCards()

            self.myiter = iter(self.cards)
            self.next_item = (next(self.myiter))


            # A button to return to previous Page
            self.BackBtn = tk.Button(root, text='↩ Back', command=self.BackBtnFunc, font=('Comic Sans MS', 18, "bold"),
                                     bg='pink')
            self.BackBtn.grid(row=0, column=0, sticky='nw', ipady=5)

            # A button for the current card
            self.CardBtn = tk.Button(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text=self.next_item[0],
                                     command=self.FlipCardFunc)
            self.CardBtn.grid(row=1, column=0, pady=50, ipady=150, sticky="ewsn", rowspan=2, padx=300, ipadx=80)

            # A button for the next Card
            self.NextBtn = tk.Button(root, text='Next >', command=self.NextBtnFunc, font=('Comic Sans MS', 18, "bold"),
                                     bg='pink')
            self.NextBtn.grid(row=3, column=0, sticky='se', ipady=5)
            self.EndOfDeckLabel = tk.Label(root, bg="pink", font=('Comic Sans MS', 18, "bold"), text=f"END OF DECK :)",
                                           border="2px")

        except:
            FourthPage(root, self.deck)
            msg = f'{self.deck} Is Empty :('

            showinfo(
                title='Information',
                message=msg)

    # FUNCTION FOR BackBtn BUTTON
    def BackBtnFunc(self):
        self.BackBtn.destroy()
        self.CardBtn.destroy()
        self.NextBtn.destroy()
        self.EndOfDeckLabel.destroy()
        FourthPage(root, self.deck)

    # FUNCTION FOR CardBtn BUTTON
    def FlipCardFunc(self):
        if self.CardBtn['text'] == self.next_item[0]:
            self.CardBtn.config(text=self.next_item[1])
        elif self.CardBtn['text'] == self.next_item[1]:
            self.CardBtn.config(text=self.next_item[0])

    # FUNCTION FOR NextBtn BUTTON
    def NextBtnFunc(self):
        try:
            self.next_item = (next(self.myiter))
            self.CardBtn.config(text=self.next_item[0])
        except StopIteration:
            self.CardBtn.destroy()
            self.NextBtn.destroy()
            self.EndOfDeckLabel.grid(row=1, column=0, pady=180, padx=80, sticky='enw')

root.mainloop()
