import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd


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
            return False, "Username already exists."
        cls.user_database[username] = {
            "Name": name,
            "Phone Number": phone_number,
            "Password": password,
            "Role": "User",
        }
        return True, "Registration successful!"

    @classmethod
    def login(cls, username, password):
        if username in cls.user_database:
            if cls.user_database[username]["Password"] == password:
                return True, f"Welcome back, {username}!"
            return False, "Incorrect password."
        return False, "Username not found."


class Guest(Person):
    pass


class Staff(Person):
    pass



class Room:
    def __init__(self, room_number, room_type, price):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.availability = "Available"

    def book_room(self):
        if self.availability == "Available":
            self.availability = "Booked"
            return True, f"Room {self.room_number} booked successfully!"
        return False, "Room is already booked."

    def release_room(self):
        if self.availability == "Booked":
            self.availability = "Available"
            return True, f"Room {self.room_number} is now available!"
        return False, "Room is already available."


class Hotel:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def get_available_rooms(self):
        return [room for room in self.rooms if room.availability == "Available"]


class UserInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Hotel Booking System")
        self.window.geometry("600x400")

        # Sample Hotel Data
        self.hotel = Hotel("Sunset Hotel", "123 Ocean Drive")
        self.hotel.add_room(Room(101, "Deluxe", 200))
        self.hotel.add_room(Room(102, "Standard", 150))
        self.hotel.add_room(Room(103, "Suite", 300))

        self.active_user = None

        self.login_screen()
        self.window.mainloop()

    def login_screen(self):
        self.clear_window()

        tk.Label(self.window, text="Hotel Booking System", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.window, text="Username:").pack()
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        tk.Label(self.window, text="Password:").pack()
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        tk.Button(self.window, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.window, text="Register", command=self.register_screen).pack()

    def register_screen(self):
        self.clear_window()

        tk.Label(self.window, text="Register", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.window, text="Name:").pack()
        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack()

        tk.Label(self.window, text="Phone Number:").pack()
        self.phone_entry = tk.Entry(self.window)
        self.phone_entry.pack()

        tk.Label(self.window, text="Username:").pack()
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        tk.Label(self.window, text="Password:").pack()
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        tk.Button(self.window, text="Register", command=self.register).pack(pady=5)
        tk.Button(self.window, text="Back to Login", command=self.login_screen).pack()

    def user_dashboard(self):
        self.clear_window()

        tk.Label(self.window, text=f"Welcome {self.active_user}!", font=("Arial", 18)).pack(pady=10)

        tk.Button(self.window, text="Book Room", command=self.book_room_screen).pack(pady=5)
        tk.Button(self.window, text="View Rooms", command=self.view_rooms).pack(pady=5)
        tk.Button(self.window, text="Logout", command=self.logout).pack(pady=5)

    def book_room_screen(self):
        self.clear_window()

        tk.Label(self.window, text="Available Rooms", font=("Arial", 18)).pack(pady=10)

        available_rooms = self.hotel.get_available_rooms()
        if available_rooms:
            for room in available_rooms:
                tk.Button(
                    self.window,
                    text=f"Room {room.room_number} ({room.room_type}) - ${room.price}",
                    command=lambda r=room: self.book_room(r),
                ).pack(pady=5)
        else:
            tk.Label(self.window, text="No rooms available.").pack()

        tk.Button(self.window, text="Back", command=self.user_dashboard).pack(pady=10)

    def view_rooms(self):
        self.clear_window()

        tk.Label(self.window, text="Hotel Rooms", font=("Arial", 18)).pack(pady=10)

        for room in self.hotel.rooms:
            tk.Label(
                self.window,
                text=f"Room {room.room_number} ({room.room_type}) - ${room.price} [{room.availability}]",
            ).pack(pady=5)

        tk.Button(self.window, text="Back", command=self.user_dashboard).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = Person.login(username, password)

        if success:
            self.active_user = username
            self.user_dashboard()
        else:
            messagebox.showerror("Error", message)

    def register(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        success, message = Person.register(name, phone, username, password)
        if success:
            messagebox.showinfo("Success", message)
            self.login_screen()
        else:
            messagebox.showerror("Error", message)

    def book_room(self, room):
        success, message = room.book_room()
        if success:
            messagebox.showinfo("Success", message)
            self.user_dashboard()
        else:
            messagebox.showerror("Error", message)

    def logout(self):
        self.active_user = None
        self.login_screen()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    UserInterface()
