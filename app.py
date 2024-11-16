import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

connection = mysql.connector.connect (
    host =  "host",                 #replace with your own info
    user = "user",                  #replace with your own info
    password = "password",          #replace with your own info
    database = "database"           #replace with your own info
)

class CatalogPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping Mall")
        self.root.geometry("1550x800+0+0")
        
        self.cart = []

        self.catalog_items = self.fetch_catalog_items()

        #content frame
        frame = tk.Frame(self.root, bg="black", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")  

        #title
        title = tk.Label(frame, text="Store Catalog", font=("Arial", 16, "bold"), bg="black")
        title.pack(pady=10)

        #add items to the frame
        for item in self.catalog_items:
            item_frame = tk.Frame(frame, bg="black", pady=5)
            item_frame.pack(fill="x", pady=5)

            item_label = tk.Label(item_frame, text=f"{item['name']} - {item['price']}", font=("Arial", 12), bg="black")
            item_label.pack(side="left")

            buy_button = tk.Button(
                item_frame, text="Buy Now", bg="#007bff", fg="black",
                command=lambda item=item: self.add_to_cart(item)
            )
            buy_button.pack(side="right")

        #add view cart button
        view_cart_button = tk.Button(
            frame, text="View Cart", bg="#28a745", fg="black", font=("Arial", 12),
            command=self.view_cart
        )
        view_cart_button.pack(pady=10)

    #get from database
    def fetch_catalog_items(self):
        try:
            #connect to the database
            connection = mysql.connector.connect(
            host =  "host",                 #replace with your own info
            user = "user",                  #replace with your own info
            password = "password",          #replace with your own info
            database = "database"           #replace with your own info
            )
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT name, price FROM catalog_items")
            items = cursor.fetchall()
            connection.close()
            return items
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

    def add_to_cart(self, item):
        self.cart.append(item)
        messagebox.showinfo("Added to Cart", f"{item['name']} has been added to your cart!")

    def view_cart(self):
        if not self.cart:
            messagebox.showinfo("Cart", "Your cart is empty!")
            return
        
        #create new window for the cart
        cart_window = tk.Toplevel(self.root)
        cart_window.title("Your Cart")
        cart_window.geometry("400x400")
        
        #cart title
        title = tk.Label(cart_window, text="Your Cart", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        #display items in cart
        for item in self.cart:
            item_label = tk.Label(cart_window, text=f"{item['name']} - {item['price']}", font=("Arial", 12))
            item_label.pack(anchor="w", padx=10, pady=5)

        #add checkout button
        checkout_button = tk.Button(
            cart_window, text="Checkout", bg="#dc3545", fg="black",
            command=lambda: self.checkout(cart_window)
        )
        checkout_button.pack(pady=20)

    def checkout(self, cart_window):
        cart_window.destroy()
        messagebox.showinfo("Checkout", "Thank you for your purchase!")
        self.cart.clear()





class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Log In")
        self.root.geometry("1550x800+0+0")
        frame=Frame(self.root, bg="black")
        frame.place(x=610, y=170, width=340, height=450)

        self.username = StringVar()
        self.password = StringVar()

        headerLabel = Label(frame, text ="Sign in", font = ("times new roman", 20, "bold"), fg = "white", bg = "black")
        headerLabel.place(x=125, y=50)

        usernameLabel = Label(frame, text ="Username", font = ("times new roman", 15, "bold"), fg = "white", bg = "black")
        usernameLabel.place(x=70, y=155)
        self.userText = ttk.Entry(frame,textvariable=self.username,font = ("times new roman", 15, "bold"))
        self.userText.place(x=40, y=180, width = 270)

        passwordLabel = Label(frame, text ="Password", font = ("times new roman", 15, "bold"), fg = "white", bg = "black")
        passwordLabel.place(x=70, y=250)
        self.passText = ttk.Entry(frame,textvariable=self.password,font = ("times new roman", 15, "bold"))
        self.passText.place(x=40, y=275, width = 270)

        loginButt = Button(frame, command= self.login, text = "Login", font = ("times new roman", 15, "bold"))
        loginButt.place(x=150, y=320, height = 25)

        RegisterButt = Button(frame,command=self.register, text = "Register", font = ("times new roman", 15, "bold"))
        RegisterButt.place(x=138, y=350, height = 25)

    def register(self):
        self.openRegister = Toplevel(self.root)
        self.app=RegisterPage(self.openRegister)


    def login(self):
        if self.userText.get() == "" or self.passText.get() == "":
            messagebox.showerror("Error", "All fields required")
        else:
            conn=mysql.connector.connect(host="localhost",
            user="root", 
            password="root", 
            db="malldata")
            mycursor=conn.cursor()     
            mycursor.execute("select * from customerinfo where username=%s and password=%s",(
                self.username.get(),
                self.password.get()
            ))
            row=mycursor.fetchone()
            if row == None:
                messagebox.showerror("Error", "Invalid username or Password")
            else:
                #messagebox.showinfo("Success", "Login Successful")
                self.openCatalog = Toplevel(self.root)
                self.app=CatalogPage(self.openCatalog)
            conn.commit()
            conn.close()



class RegisterPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("960x720+0+0")
        frame=Frame(self.root, bg="black")
        frame.place(x=150, y=50, width=700, height=500)

        self.firstname = StringVar()
        self.lastname = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.passwordConfirm = StringVar()

        headerLabel = Label(frame, text ="Register", font = ("times new roman", 20, "bold"), fg = "white", bg = "black")
        headerLabel.place(x=300, y=50)

        firstnameLabel = Label(frame, text ="First Name", font = ("times new roman", 15, "bold"), fg = "white", bg = "black")
        firstnameLabel.place(x=60, y=155)
        self.firstnameText = ttk.Entry(frame,textvariable=self.firstname,font = ("times new roman", 15, "bold"))
        self.firstnameText.place(x=40, y=180, width = 270)

        lastnameLabel = Label(frame, text ="Last Name", font = ("times new roman", 15, "bold"), fg = "white", bg = "black")
        lastnameLabel.place(x=60, y=250)
        self.lastnameText = ttk.Entry(frame,textvariable=self.lastname,font = ("times new roman", 15, "bold"))
        self.lastnameText.place(x=40, y=275, width = 270)

        usernameLabel = Label(frame, text ="New Username", font = ("times new roman", 15, "bold"), fg = "white", bg = "black")
        usernameLabel.place(x=400, y=155)
        self.userText = ttk.Entry(frame,textvariable=self.username,font = ("times new roman", 15, "bold"))
        self.userText.place(x=380, y=180, width = 270)

        passwordLabel = Label(frame, text ="New Password", font = ("times new roman", 15, "bold"), fg = "white", bg = "black")
        passwordLabel.place(x=400, y=250)
        self.passText = ttk.Entry(frame,textvariable=self.password,font = ("times new roman", 15, "bold"))
        self.passText.place(x=380, y=275, width = 270)

        passwordLabel2 = Label(frame, text ="Confirm Password", font = ("times new roman", 15, "bold"), fg = "white", bg = "black")
        passwordLabel2.place(x=400, y=325)
        self.passText2 = ttk.Entry(frame,textvariable=self.passwordConfirm,font = ("times new roman", 15, "bold"))
        self.passText2.place(x=380, y=350, width = 270)

        RegisterButt = Button(frame, command=self.register, text = "Register", font = ("times new roman", 15, "bold"))
        RegisterButt.place(x=300, y=425, height = 35, width = 100)

    def register(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "All fields required")
        elif self.password.get() != self.passwordConfirm.get():
            messagebox.showerror("Error", "Passwords do not match")   
        elif self.userText.get() == "admin" and self.passText.get() == "admin123":
            messagebox.showinfo("Test","Registration Successful!")
        else:
            conn=mysql.connector.connect(host="localhost",
            user="root", 
            password="root", 
            db="malldata")
            mycursor=conn.cursor()
            query=("select * from customerinfo where username=%s")
            value=(self.username.get(),)
            mycursor.execute(query, value)
            row=mycursor.fetchone()
            if row != None:
                messagebox.showerror("Error", "Account already exists")
            else:
                mycursor.execute("insert into customerinfo values(%s,%s,%s,%s)",(
                self.firstname.get(),
                self.lastname.get(), 
                self.username.get(), 
                self.password.get() 
                ))
                conn.commit()
                conn.close()
                messagebox.showinfo("Registration Successful", "Account created successfully")

root=Tk()
app=CatalogPage(root)
root.mainloop()
