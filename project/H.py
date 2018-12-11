from tkinter import*

window = Tk()
window.title("Chatbot")
window.configure(background="black")
photo1 = PhotoImage(file="mop.gif")
Label  (window, image=photo1, bg="black") .grid(row=0, column=0, sticky=E)
window.mainloop()
