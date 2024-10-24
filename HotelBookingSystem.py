import tkinter as tk
from tkinter import font
from tkinter.simpledialog import messagebox
import pandas as pd

def login_user():
    if login_failed:
        login_failed = False
        messagebox.showerror("Error", "Login failed. Please check your username and password.")
    else:
        messagebox.showerror("Login successfully", "Welcome")
        
df = pd.read_csv('data.csv')
print(df.head())
user_file = "data.csv"

class Person:
    user_database = {}

    def __init__(self, name, phone_number, username, password):
        self.name = name
        self.phone_number = phone_number
        self.username = username
        self.password = password

    @classmethod
    def register(cls, name, phone_number, username, password):
        if username in cls.user_database:
            print("Username already exists, please choose another.")
        else:
            cls.user_database[username] = {"Name": name, "Phone Number": phone_number, "Password": password}
            print(f"Account {username} registered successfully.")
            return True 

    @classmethod
    def login(cls, username, password):
        if username in cls.user_database and cls.user_database[username]["Password"] == password:
            print(f"Account {username} logged in successfully.")
            return True  
        else:
            print("Incorrect username or password.")
            return False

class UserInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("User Management System")
        self.window.geometry("1000x800")  
        
        name_label = tk.Label(self.window, text="Name:")
        name_entry = tk.Entry(self.window)
        password_label = tk.Label(self.window, text="Password:")
        password_entry = tk.Entry(self.window, show="*")  
        phone_number_label = tk.Label(self.window, text="Phone number:")
        phone_number_entry = tk.Entry(self.window)

        name_label.grid(row=0, column=0)
        name_entry.grid(row=0, column=1)
        password_label.grid(row=1, column=0)
        password_entry.grid(row=1, column=1)
        phone_number_label.grid(row = 2, column = 0)
        phone_number_entry.grid(row = 2, column = 1)
        
        register_button = tk.Button(self.window, text="Register")
        login_button = tk.Button(self.window, text="Login")

        register_button.grid(row=3, column=0)
        login_button.grid(row=3, column=1)

        self.window.mainloop()
      
    
    def register_user(self):
        name = self.name_entry.get()
        phone_number = self.phone_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if Person.register(name, phone_number, username, password):
            self.clear_fields()
            tk.messagebox.showinfo("Success", "Registration successful!")
        else:
            tk.messagebox.showerror("Error", "Registration failed. Please check your input.")

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        phone_number = self.phone_number_entry.get()

        if Person.login(username, password, phone_number):
            self.clear_fields()
            tk.messagebox.showinfo("Success", "Login successful!")
        else:
            tk.messagebox.showerror("Error", "Login failed. Please check your username and password.")

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

if __name__ == "__main__":
    ui = UserInterface()
    
    
class Guest(Person):
    def __init__(self, name, phone_number, username, password, guest_type="Primary"):
        super().__init__(name, phone_number, username, password)
        self.guest_type = guest_type
    @classmethod
    def register_guest(cls, name, phone_number, username, password, guest_type="Primary"):
        cls.register(name, phone_number, username, password)
        return Guest(name, phone_number, username, password, guest_type)
    def request_room(self, hotel):
        room = hotel.find_available_room()
        if room:
            print(f"Guest {self.name} is booking room {room.room_number}.")
            room.book_room()
        else:
            print("No available rooms at the moment.")
class Staff(Person):
    def __init__(self, name, phone_number, username, password, position):
        super().__init__(name, phone_number, username, password)
        self.position = position
    @classmethod
    def register_staff(cls, name, phone_number, username, password, position):
        cls.register(name, phone_number, username, password)
        return Staff(name, phone_number, username, password, position)
    def check_in_guest(self, guest, room):
        print(f"{guest.name} has checked into room {room.room_number}.")
    def check_out_guest(self, guest, room):
        room.release_room()
        print(f"{guest.name} has checked out from room {room.room_number}.")
class Room:
    def __init__(self, room_number, room_type, price, availability="Available"):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.availability = availability
    def book_room(self):
        if self.availability == "Available":
            self.availability = "Booked"
            print(f"Room {self.room_number} is now booked.")
        else:
            print(f"Room {self.room_number} is already booked.")
    def release_room(self):
        if self.availability == "Booked":
            self.availability = "Available"
            print(f"Room {self.room_number} is now available.")
        else:
            print(f"Room {self.room_number} is already available.")
class Booking:
    def __init__(self, booking_number, room, checkin_date, checkout_date):
        self.booking_number = booking_number
        self.room = room
        self.checkin_date = checkin_date
        self.checkout_date = checkout_date
        self.status = "Booked"
    def cancel_booking(self):
        self.status = "Cancelled"
        self.room.release_room()
        print(f"Booking {self.booking_number} is cancelled.")
class Hotel:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.rooms = []
    def add_room(self, room):
        self.rooms.append(room)
        print(f"Room {room.room_number} added to the hotel.")
    def find_available_room(self):
        for room in self.rooms:
            if room.availability == "Available":
                return room
        return None



hotel = Hotel(name="Sunset Hotel", address="123 Ocean Drive")


room1 = Room(room_number=101, room_type="High Quality", price=200)
room2 = Room(room_number=102, room_type="Primary Room", price=150)

hotel.add_room(room1)
hotel.add_room(room2)

guest1 = Guest.register_guest(name="John Doe", phone_number="123-456-7890", username="johndoe", password="password123", guest_type="VIP")


staff1 = Staff.register_staff(name="Alice", phone_number="987-654-3210", username="alice", password="alicepass", position="Receptionist")


if Guest.login(username="johndoe", password="password123"):
    
    guest1.request_room(hotel)

if Staff.login(username="alice", password="alicepass"):
    
    staff1.check_in_guest(guest1, room1)

   
    booking1 = Booking(booking_number="B123", room=room1, checkin_date="2023-10-10", checkout_date="2023-10-12")

    
    booking1.cancel_booking()

    staff1.check_out_guest(guest1, room1)
