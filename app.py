import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="11Buddy2003",
        database="cs3332_project"
    )

class CatalogPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping Mall")
        self.root.geometry("1080x720+0+0")
        
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
                item_frame, text="Add to Wishlist", bg="#007bff", fg="black",
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
            connection = get_db_connection()
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT name, price FROM catalog_items")
            items = cursor.fetchall()
            connection.close()
            return items
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []
        finally:
            if connection:
                connection.close()

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
        cart_window.geometry("720x480")
        
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
            command=lambda: self.go_to_payment_page(cart_window)
        )
        checkout_button.pack(pady=20)

    def go_to_payment_page(self, cart_window):
        cart_window.destroy()
        payment_window = tk.Toplevel(self.root)
        PaymentPage(payment_window, self.cart)


class PaymentPage:
    #create window
    def __init__(self, root, cart):
        self.root = root
        self.cart = cart

        self.root.title("Payment")
        self.root.geometry("1080x720+0+0")

        frame = tk.Frame(self.root, bg="black", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(frame, text="Payment", font=("Arial", 16, "bold"), bg="black", fg="white")
        title.pack(pady=10)

        #display items from cart
        for item in self.cart:
            item_label = tk.Label(
                frame, text=f"{item['name']} - {item['price']}", font=("Arial", 12), bg="black", fg="white"
            )
            item_label.pack(anchor="w", padx=10, pady=5)

        payment_label = tk.Label(frame, text="Payment Details", font=("Arial", 14), bg="black", fg="white")
        payment_label.pack(pady=20)

        #checkout button
        checkout_button = tk.Button(
            frame, text="Confirm Payment", bg="#28a745", fg="white", font=("Arial", 12),
            command=self.confirm_payment
        )
        checkout_button.pack(pady=10)

    def confirm_payment(self):
        messagebox.showinfo("Payment", "Payment successful! Thank you for your purchase.")
        self.root.destroy()


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Log In")
        self.root.geometry("1080x720+0+0")
        frame=Frame(self.root, bg="black")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=450)

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

        RegisterButt = Button(frame,command=self.register, text = "Sign Up", font = ("times new roman", 15, "bold"))
        RegisterButt.place(x=138, y=350, height = 25)

    def register(self):
        self.openRegister = Toplevel(self.root)
        self.app=RegisterPage(self.openRegister)


    def login(self):
        if self.userText.get() == "" or self.passText.get() == "":
            messagebox.showerror("Error", "All fields required")
        else:
            connection = get_db_connection()
            
            mycursor = connection.cursor()
            query = "SELECT * FROM Customer WHERE username = %s AND password = %s"
            params = (self.username.get(), self.password.get())
            mycursor.execute(query, params)

            row = mycursor.fetchone()
            if row is None:
                messagebox.showerror("Error", "Invalid username or password")
            else:
                messagebox.showinfo("Success", "Login successful!")

                self.openCatalog = Toplevel(self.root)
                self.app=CatalogPage(self.openCatalog)
            connection.commit()
            connection.close()


class RegisterPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("1080x720+0+0")
        
        frame = Frame(self.root, bg="black")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=450)

        self.firstname = StringVar()
        self.lastname = StringVar()
        self.email = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.passwordConfirm = StringVar()

        headerLabel = Label(frame, text="Register", font=("times new roman", 20, "bold"), fg="white", bg="black")
        headerLabel.grid(row=0, column=0, columnspan=2, pady=20)

        firstnameLabel = Label(frame, text="First Name", font=("times new roman", 15, "bold"), fg="white", bg="black")
        firstnameLabel.grid(row=1, column=0, padx=20, pady=10, sticky="e")
        self.firstnameText = ttk.Entry(frame, textvariable=self.firstname, font=("times new roman", 15, "bold"), width=25)
        self.firstnameText.grid(row=1, column=1, padx=20, pady=10)

        lastnameLabel = Label(frame, text="Last Name", font=("times new roman", 15, "bold"), fg="white", bg="black")
        lastnameLabel.grid(row=2, column=0, padx=20, pady=10, sticky="e")
        self.lastnameText = ttk.Entry(frame, textvariable=self.lastname, font=("times new roman", 15, "bold"), width=25)
        self.lastnameText.grid(row=2, column=1, padx=20, pady=10)

        emailLabel = Label(frame, text="Email", font=("times new roman", 15, "bold"), fg="white", bg="black")
        emailLabel.grid(row=3, column=0, padx=20, pady=10, sticky="e")
        self.emailText = ttk.Entry(frame, textvariable=self.email, font=("times new roman", 15, "bold"), width=25)
        self.emailText.grid(row=3, column=1, padx=20, pady=10)

        usernameLabel = Label(frame, text="New Username", font=("times new roman", 15, "bold"), fg="white", bg="black")
        usernameLabel.grid(row=4, column=0, padx=20, pady=10, sticky="e")
        self.userText = ttk.Entry(frame, textvariable=self.username, font=("times new roman", 15, "bold"), width=25)
        self.userText.grid(row=4, column=1, padx=20, pady=10)

        passwordLabel = Label(frame, text="New Password", font=("times new roman", 15, "bold"), fg="white", bg="black")
        passwordLabel.grid(row=5, column=0, padx=20, pady=10, sticky="e")
        self.passText = ttk.Entry(frame, textvariable=self.password, font=("times new roman", 15, "bold"), width=25, show="*")
        self.passText.grid(row=5, column=1, padx=20, pady=10)

        passwordLabel2 = Label(frame, text="Confirm Password", font=("times new roman", 15, "bold"), fg="white", bg="black")
        passwordLabel2.grid(row=6, column=0, padx=20, pady=10, sticky="e")
        self.passText2 = ttk.Entry(frame, textvariable=self.passwordConfirm, font=("times new roman", 15, "bold"), width=25, show="*")
        self.passText2.grid(row=6, column=1, padx=20, pady=10)

        RegisterButt = Button(frame, command=self.register, text="Sign Up", font=("times new roman", 15, "bold"), width=25)
        RegisterButt.grid(row=7, column=0, columnspan=2, pady=20)
        
    def register(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "All fields required")
        elif self.password.get() != self.passwordConfirm.get():
            messagebox.showerror("Error", "Passwords do not match")
        else:
            try:
                connection = get_db_connection()
                mycursor = connection.cursor()

                query = "SELECT * from Customer where username=%s"
                mycursor.execute(query, (self.username.get(),))
                row = mycursor.fetchone()

                if row != None:
                    messagebox.showerror("Error", "Account already exists")
                else:
                    mycursor.execute(
                        "INSERT INTO Customer (customerFirstName, customerLastName, email, username, password) VALUES (%s, %s, %s, %s, %s)",
                        (self.firstname.get(), self.lastname.get(), self.email.get(), self.username.get(), self.password.get())
                    )

                    connection.commit()
                    messagebox.showinfo("Registration Successful", "Account created successfully")
                    self.root.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                if connection:
                    connection.close()


root=Tk()
app=LoginPage(root)
root.mainloop()
