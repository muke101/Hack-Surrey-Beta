from tkinter import *

import test #change "test" with the nameof your py files 



def web_scrap(event):
   name =  str(entry.get())


   if (name == "Donald Trump"):
      res.configure(text = "Running web script on: " + name)
      
      #replace this with all your functions
      test.printFunc()

   else:
      res.configure(text = "Cannot run script on " + name)

    
w = Tk()

Label(w, text="Name:").pack()
entry = Entry(w)


entry.bind("<Return>", web_scrap)
entry.pack()

res = Label(w)
res.pack()

w.geometry("400x100")
w.mainloop()
