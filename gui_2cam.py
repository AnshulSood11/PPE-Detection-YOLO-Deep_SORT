import tkinter as tk
import threading
from PIL import ImageTk, Image
import cv2


class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.start()

    def run(self):
        self.root = tk.Tk()
        self.root.title("Helmet Detection")
        self.root.geometry("1300x800")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        label1 = tk.Label(self.root, text="Persons with helmet = ").place(x=10, y=510)
        label2 = tk.Label(self.root, text="Persons without helmet = ").place(x=10, y=530)
        label3 = tk.Label(self.root, text="Persons with helmet = ").place(x=440, y=510)
        label4 = tk.Label(self.root, text="Persons without helmet = ").place(x=440, y=530)

        label5 = tk.Label(self.root, text="Messages Cam 1",relief = tk.RIDGE).place(x=170, y=490)
        label6 = tk.Label(self.root, text="Messages Cam 2",relief = tk.RIDGE).place(x=600, y=490)
        label7 = tk.Label(self.root, text="All Messages",relief = tk.RIDGE).place(x=1030, y=490)

        self.num_with_helmet1 = tk.StringVar()
        label_with_helmet1 = tk.Label(self.root, textvariable=self.num_with_helmet1).place(x=200, y=510)

        self.num_without_helmet1 = tk.StringVar()
        label_without_helmet1 = tk.Label(self.root, textvariable=self.num_without_helmet1).place(x=200, y=530)

        self.num_with_helmet2 = tk.StringVar()
        label_with_helmet2 = tk.Label(self.root, textvariable=self.num_with_helmet2).place(x=630, y=510)

        self.num_without_helmet2 = tk.StringVar()
        label_without_helmet2 = tk.Label(self.root, textvariable=self.num_without_helmet2).place(x=630, y=530)

        self.messages1 = tk.Text(self.root)
        self.messages1.place(x=0, y=550, width=425, height=180)

        self.messages2 = tk.Text(self.root)
        self.messages2.place(x=430, y=550, width=425, height=180)

        self.allmessages = tk.Text(self.root)
        self.allmessages.place(x=860, y=510, width=425, height=220)

        img = cv2.imread('no_signal.jpg', 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)

        self.panel1 = tk.Label(image=img)
        self.panel1.image = img
        self.panel1.place(x=0, y=0)
        self.panel1.configure(image=img)
        self.panel1.image = img

        self.panel2 = tk.Label(image=img)
        self.panel2.image = img
        self.panel2.place(x=650, y=0)
        self.panel2.configure(image=img)
        self.panel2.image = img

        quit_btn = tk.Button(self.root, text="Quit", command=self.root.quit,width = 10,height = 2)
        quit_btn.place(x=620, y=740)
        # quit_btn.place()

        self.root.mainloop()

    def callback(self):
        self.root.quit()

    def quit(self):
        # self.stop_event.set()
        self.root.destroy()

    def update(self, images, values, messages):
        img = cv2.cvtColor(images[0], cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        self.panel1.configure(image=img)
        self.panel1.image = img


        self.num_with_helmet1.set(values[0])
        self.num_without_helmet1.set(values[1])
        message = messages[0]
        if message != "":
            self.messages1.insert(tk.INSERT, message)
            self.allmessages.insert(tk.INSERT, "Cam 1: " + message)

        if len(images)>1:
            img = cv2.cvtColor(images[1], cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(image=img)
            self.panel2.configure(image=img)
            self.panel2.image = img

            self.num_with_helmet2.set(values[2])
            self.num_without_helmet2.set(values[3])

            message = messages[1]
            if message != "":
                self.messages2.insert(tk.INSERT, message)
                self.allmessages.insert(tk.INSERT, "Cam 2: " + message)

