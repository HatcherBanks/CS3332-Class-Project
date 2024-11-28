import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="",
        user="",
        password="",
        database=""
    )

class CatalogPage:
    def __init__(self, root, username=None, password=None):
        self.root = root
        self.root.title("Shopping Mall")
        self.root.geometry("1080x720+0+0")
        
        self.cart = []
        self.catalog_items = self.fetch_catalog_items()
        
        self.is_admin = self.check_admin_credentials(username, password)

        #content frame
        self.frame = tk.Frame(self.root, bg="black", padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")  

        #title
        title = tk.Label(self.frame, text="Store Catalog", font=("Arial", 16, "bold"), bg="black")
        title.pack(pady=10)
        
        #admin controls
        if self.is_admin:
            admin_frame = tk.Frame(self.root, bg="black")
            admin_frame.grid(row=0, column=0, pady=10)

            add_item_button = tk.Button(admin_frame, text="Add Item", command=self.add_item_window, bg="white", fg="black")
            modify_item_button = tk.Button(admin_frame, text="Modify Item", command=self.modify_item_window, bg="white", fg="black")
            delete_item_button = tk.Button(admin_frame, text="Delete Item", command=self.delete_item_window, bg="white", fg="black")

            add_item_button.grid(row=0, column=0, padx=10)
            modify_item_button.grid(row=0, column=1, padx=10)
            delete_item_button.grid(row=0, column=2, padx=10)

        #view cart button
        view_cart_button = tk.Button(
            self.frame, text="View Cart", bg="white", fg="black", font=("Arial", 12),
            command=self.view_cart
        )
        view_cart_button.pack(pady=10)
        
        self.display_catalog()
        
    def check_admin_credentials(self, username, password):
        try:
            admin_username = "admin"
            admin_password = "admin123"

            if username == admin_username and password == admin_password:
                return True
            return False
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False


    def display_catalog(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for item in self.catalog_items:
            item_frame = tk.Frame(self.frame, bg="black", pady=5)
            item_frame.pack(fill="x", pady=5)

            item_label = tk.Label(item_frame, text=f"{item['name']} - ${item['price']}", font=("Arial", 12), bg="black", fg="white")
            item_label.pack(side="left")

            buy_button = tk.Button(
                item_frame, text="Add to Wishlist", bg="white", fg="black",
                command=lambda item=item: self.add_to_cart(item)
            )
            buy_button.pack(side="right")
        
        self.item_frames = self.frame.winfo_children()

    #admin functionalities
    def add_item_window(self):
        self.show_item_form("Add Item", self.add_item)

    def modify_item_window(self):
        self.show_item_form("Modify Item", self.modify_item)

    def delete_item_window(self):
        self.show_item_form("Delete Item", self.delete_item, for_deletion=True)

    def show_item_form(self, title, action, for_deletion=False):
        form_window = tk.Toplevel(self.root)
        form_window.title(title)
        form_window.geometry("720x480")
        
        name_var = tk.StringVar()
        price_var = tk.StringVar()
        quantity_var = tk.StringVar()

        tk.Label(form_window, text="Item Name").pack(pady=5)
        tk.Entry(form_window, textvariable=name_var).pack(pady=5)

        if not for_deletion:
            tk.Label(form_window, text="Price").pack(pady=5)
            tk.Entry(form_window, textvariable=price_var).pack(pady=5)

            tk.Label(form_window, text="Quantity").pack(pady=5)
            tk.Entry(form_window, textvariable=quantity_var).pack(pady=5)

        submit_button = tk.Button(
            form_window, text="Submit", 
            command=lambda: action(name_var.get(), price_var.get(), quantity_var.get(), form_window)
        )
        submit_button.pack(pady=10)

    def add_item(self, name, price, quantity, window):
        if not name or not price or not quantity:
            messagebox.showerror("Error", "All fields are required.")
            return
        if int(quantity) < 0:
            messagebox.showerror("Error", "Quantity cannot be less than 0.")
            return
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("INSERT INTO catalog_items (name, price, quantity) VALUES (%s, %s, %s)", 
                (name, price, int(quantity)))
            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("Success", "Item added successfully!")
            window.destroy()
            self.display_catalog()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    def modify_item(self, name, price, quantity, window):
        if not name:
            messagebox.showerror("Error", "Item name is required.")
            return

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("UPDATE catalog_items SET price = %s, quantity = %s WHERE name = %s", 
                (price, int(quantity), name))
            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("Success", "Item modified successfully!")
            window.destroy()
            self.display_catalog()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    def delete_item(self, name, _, __, window):
        if not name:
            messagebox.showerror("Error", "Item name is required.")
            return

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("DELETE FROM catalog_items WHERE name = %s", (name,))
            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("Success", "Item deleted successfully!")
            window.destroy()
            self.display_catalog()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    #get from database
    def fetch_catalog_items(self):
        try:
            with get_db_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT name, price FROM catalog_items")
                return cursor.fetchall()
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
        cart_window.title("Shopping Mall")
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
            cart_window, text="Checkout", bg="white", fg="black",
            command=lambda: self.go_to_payment_page(cart_window)
        )
        checkout_button.pack(pady=20)

    def go_to_payment_page(self, cart_window):
        payment_window = tk.Toplevel(self.root)
        PaymentPage(payment_window, self.cart, cart_window)



class PaymentPage:
    #create window
    def __init__(self, root, cart, previous_window):
        self.root = root
        self.cart = cart
        previous_window.destroy()

        self.root.title("Shopping Mall")
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
            

        payment_label = tk.Label(frame, text="Please Enter Your Payment Details", font=("Arial", 10), bg="black", fg="white")
        payment_label.pack(pady=10)

        #card info input boxes
        self.cardNumber = StringVar()
        self.cardName = StringVar()
        self.cardExp = StringVar()
        self.cardSecCode = StringVar()
        
        form_frame = tk.Frame(frame, bg="black")
        form_frame.pack(pady=10)

        labels_and_entries = [
            ("Card Number", self.cardNumber),
            ("Name on Card", self.cardName),
            ("Expiration Date", self.cardExp),
            ("Security Code", self.cardSecCode),
        ]

        for row, (label_text, text_var) in enumerate(labels_and_entries):
            label = tk.Label(form_frame, text=label_text, font=("arial", 15, "bold"), fg="white", bg="black")
            label.grid(row=row, column=0, padx=10, pady=5, sticky="e")

            entry = ttk.Entry(form_frame, textvariable=text_var, font=("arial", 15, "bold"), width=30)
            entry.grid(row=row, column=1, padx=10, pady=5)
        
        #checkout button
        checkout_button = tk.Button(
            frame, text="Confirm Payment", bg="white", fg="black", font=("Arial", 12),
            command=self.confirm_payment
        )
        checkout_button.pack(pady=10)

    def confirm_payment(self):
        if not all([self.cardNumber.get(), self.cardName.get(), self.cardExp.get(), self.cardSecCode.get()]):
            messagebox.showerror("Error", "All fields are required.")
        else:
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

        headerLabel = Label(frame, text ="Sign in", font = ("arial", 20, "bold"), fg = "white", bg = "black")
        headerLabel.place(x=125, y=50)

        usernameLabel = Label(frame, text ="Username", font = ("arial", 15, "bold"), fg = "white", bg = "black")
        usernameLabel.place(x=70, y=155)
        self.userText = ttk.Entry(frame,textvariable=self.username,font = ("arial", 15, "bold"))
        self.userText.place(x=40, y=180, width = 270)

        passwordLabel = Label(frame, text ="Password", font = ("arial", 15, "bold"), fg = "white", bg = "black")
        passwordLabel.place(x=70, y=250)
        self.passText = ttk.Entry(frame,textvariable=self.password,font = ("arial", 15, "bold"))
        self.passText.place(x=40, y=275, width = 270)

        loginButt = Button(frame, command= self.login, text = "Login", font = ("arial", 15, "bold"))
        loginButt.place(x=150, y=320, height = 25)

        RegisterButt = Button(frame,command=self.register, text = "Sign Up", font = ("arial", 15, "bold"))
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
                self.app=CatalogPage(self.openCatalog, username=self.username.get(), password=self.password.get())
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

        headerLabel = Label(frame, text="Register", font=("arial", 20, "bold"), fg="white", bg="black")
        headerLabel.grid(row=0, column=0, columnspan=2, pady=20)

        firstnameLabel = Label(frame, text="First Name", font=("arial", 15, "bold"), fg="white", bg="black")
        firstnameLabel.grid(row=1, column=0, padx=20, pady=10, sticky="e")
        self.firstnameText = ttk.Entry(frame, textvariable=self.firstname, font=("arial", 15, "bold"), width=25)
        self.firstnameText.grid(row=1, column=1, padx=20, pady=10)

        lastnameLabel = Label(frame, text="Last Name", font=("arial", 15, "bold"), fg="white", bg="black")
        lastnameLabel.grid(row=2, column=0, padx=20, pady=10, sticky="e")
        self.lastnameText = ttk.Entry(frame, textvariable=self.lastname, font=("arial", 15, "bold"), width=25)
        self.lastnameText.grid(row=2, column=1, padx=20, pady=10)

        emailLabel = Label(frame, text="Email", font=("arial", 15, "bold"), fg="white", bg="black")
        emailLabel.grid(row=3, column=0, padx=20, pady=10, sticky="e")
        self.emailText = ttk.Entry(frame, textvariable=self.email, font=("arial", 15, "bold"), width=25)
        self.emailText.grid(row=3, column=1, padx=20, pady=10)

        usernameLabel = Label(frame, text="New Username", font=("arial", 15, "bold"), fg="white", bg="black")
        usernameLabel.grid(row=4, column=0, padx=20, pady=10, sticky="e")
        self.userText = ttk.Entry(frame, textvariable=self.username, font=("arial", 15, "bold"), width=25)
        self.userText.grid(row=4, column=1, padx=20, pady=10)

        passwordLabel = Label(frame, text="New Password", font=("arial", 15, "bold"), fg="white", bg="black")
        passwordLabel.grid(row=5, column=0, padx=20, pady=10, sticky="e")
        self.passText = ttk.Entry(frame, textvariable=self.password, font=("arial", 15, "bold"), width=25, show="*")
        self.passText.grid(row=5, column=1, padx=20, pady=10)

        passwordLabel2 = Label(frame, text="Confirm Password", font=("arial", 15, "bold"), fg="white", bg="black")
        passwordLabel2.grid(row=6, column=0, padx=20, pady=10, sticky="e")
        self.passText2 = ttk.Entry(frame, textvariable=self.passwordConfirm, font=("arial", 15, "bold"), width=25, show="*")
        self.passText2.grid(row=6, column=1, padx=20, pady=10)

        RegisterButt = Button(frame, command=self.register, text="Sign Up", font=("arial", 15, "bold"), width=25)
        RegisterButt.grid(row=7, column=0, columnspan=2, pady=20)
        
    def register(self):
        if not self.username.get() or self.password.get():
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
