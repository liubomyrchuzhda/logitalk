from customtkinter import *
from socket import socket, AF_INET, SOCK_STREAM
import threading


class MainWindow(CTk):
   def __init__(self):
       super().__init__()
       self.geometry('400x300')
       self.label = None

       self.username = "Liubchik"

       self.menu_frame= CTkFrame(self, width=30, height=300)
       self.menu_frame.pack_propagate(False)
       self.menu_frame.place(x=0, y=0)
       self.is_show_menu = False
       self.speed_animate_menu = -5
       self.btn = CTkButton(self, text='▶️', command=self.toggle_show_menu, width=30)
       self.btn.place(x=0, y=0)
       self.chat_field = CTkScrollableFrame(self)
       self.chat_field.place(x=0, y=0)
       self.message_entry = CTkEntry(self, placeholder_text='Введіть повідомлення:', height=40)
       self.message_entry.place(x=0, y=0)
       self.send_button = CTkButton(self, text='>', width=50, height=40)
       self.send_button.place(x=0, y=0)
       self.open_img_btn = CTkButton(self, text="File", width=50, height=40, command=self.open_image)
       self.open_img_btn.place(x=0, y=0)

       self.adaptive_ui()

       try:
           self.socket = socket(AF_INET, SOCK_STREAM)
           self.socket.connect(("localhost", 8080))

           hello = f"TEXT@{self.username}@[SYSTEM]{self.username} приєднався (-лась) до чату \n"
           self.socket.send(hello.encode("utf-8"))

           threading.Thread(target=self.recv_message, daemon=True).start()
       except Exception as e:
           print("Не вдалося підключитися до сервера")

   def recv_message(self):
       buffer = ""
       while True:
           try:
               chunk = self.socket.recv(4096)
               if not chunk:
                   break
               buffer += chunk.decode("utf-8", errors="ignore")
               while "\n" in buffer:
                   line, buffer = buffer.split("\n", 1)
           except:
               break
       socket.close()

   def toggle_show_menu(self):
       if self.is_show_menu:
           self.is_show_menu = False
           self.speed_animate_menu *= -1
           self.btn.configure(text='▶️')
           self.show_menu()
       else:
           self.is_show_menu = True
           self.speed_animate_menu *= -1
           self.btn.configure(text='◀️')
           self.show_menu()
           self.label = CTkLabel(self.menu_frame, text='Імʼя')
           self.label.pack(pady=30)
           self.entry = CTkEntry(self.menu_frame)
           self.entry.pack()


   def show_menu(self):
       self.menu_frame.configure(width=self.menu_frame.winfo_width() + self.speed_animate_menu)
       if not self.menu_frame.winfo_width() >= 200 and self.is_show_menu:
           self.after(10, self.show_menu)
       elif self.menu_frame.winfo_width() >= 40 and not self.is_show_menu:
           self.after(10, self.show_menu)
           if self.label and self.entry:
               self.label.destroy()
               self.entry.destroy()


   def adaptive_ui(self):
        self.menu_frame.configure(height=self.winfo_height())
        self.chat_field.place(x=self.menu_frame.winfo_width())
        self.chat_field.configure(width=self.winfo_width()-self.menu_frame.winfo_width() - 20,
                                 height=self.winfo_height()-40)
        self.send_button.place(x=self.winfo_width()-50, y=self.winfo_height()-40)
        self.message_entry.place(x=self.menu_frame.winfo_width(), y=self.send_button.winfo_y())
        self.message_entry.configure(width=self.winfo_width() - self.menu_frame.winfo_width() - self.send_button.winfo_width())


        self.after(50, self.adaptive_ui)


   def open_image(self):
        file_name = filedialog.askopenfilename()
        if not file_name:
            return
        try:
            with open(file_name, "rb") as f:
                raw =f.read()
            b64_data = base64.b64encode(raw).decode()
            short_name = os.path.basenname(file_name)
            data = f"IMAGE@{self.username}@{short_name}@{b64_data}\n"
        except Exception as e:
            print(e)
       
       


win = MainWindow()
win.mainloop()