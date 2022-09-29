#Made by Bharat , Bhavik and Ashwin

from tkinter import *
from hashlib import sha256
import pymysql

#Designing the window for user registration
 
def register():
    #Declaring global variables
    global register_screen
    global username
    global password
    global username_entry
    global password_entry
    register_screen = Toplevel(main_screen) #Puting the Main window above other windows
    register_screen.title("Registration Form") #Title of the Window
    register_screen.geometry("300x250") #Size of the window
    register_screen['background']='#212121'
    #These 2 lines make it such that while the registration/Login screen is Open
    #the user is unable to interact with the main window , stopping them from spamming
    #multiple windows.
    register_screen.focus_set() 
    register_screen.grab_set()
 
    username = StringVar() #Local variable for usename
    password = StringVar() #Local Variable for password

    Label(register_screen, text="",bg="#212121",fg='white').pack() #Spacer
    Label(register_screen, text="PLEASE ENTER A \n USERNAME AND PASSWORD BELOW", bg="#212121",fg='white',font=("Rubik",9,"bold")).pack() #Main Header/Label
    Label(register_screen, text="",bg="#212121",fg='white').pack() #spacer
    username_lable = Label(register_screen, text="USERNAME ", font=("Rubik",9),bg="#212121",fg='#ed4048') #Username input label
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username) #User entry space for username
    username_entry.pack()
    password_lable = Label(register_screen, text="PASSWORD", font=("Rubik",9),bg="#212121",fg='#ed4048') #Password input label
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*') #User entry space for password
    password_entry.pack()
    Label(register_screen, text="",bg="#212121",fg='white').pack() #Spacer
    Button(register_screen, text="SUBMIT", width=10, height=1, bg="white",font=("Rubik",9,"bold"), command = register_user).pack() #Submit button
 
# Designing window for login 

def login():
    global login_screen
    global username_verify
    global password_verify
    global username_login_entry
    global password_login_entry
    
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    login_screen['background']='#212121'
    login_screen.focus_set()
    login_screen.grab_set()

    Label(login_screen, text="",bg="#212121",fg='white').pack()
    Label(login_screen, text="ENTER DETAILS BELOW TO LOGIN", bg="#212121",fg='white',font=("Rubik",9,"bold")).pack()
    Label(login_screen, text="",bg="#212121",fg='white').pack()
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    Label(login_screen, text="USERNAME ", font=("Rubik",9),bg="#212121",fg='#ed4048').pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="PASSWORD ", font=("Rubik",9),bg="#212121",fg='#ed4048').pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="",bg="#212121",fg='white').pack()
    Button(login_screen, text="SUBMIT", width=10, height=1, bg="white",font=("Rubik",9,"bold"), command = login_verify).pack()
 
# Implementing event on register button
 
def register_user():
 
    username_info = username.get() #Gets the username from the GUI (user inputted)
    password_info = password.get() #Gets the password from the GUI (user inputted)

    mydb = pymysql.connect(host="localhost",user="root",password="",database="accounts") 
    cur = mydb.cursor() 
    query = "SELECT * FROM accounts WHERE username_info = %s"
    cur.execute(query,[(username_info)]) 
    user_db = len(list(cur)) 
    mydb.close()

    #We are using hashlib to hash our passwords, 
    #sha256 is a hashing algorithm, we will be using for all intents and purposes.
    #We begin by encoding the the password as ascii since you can't encode unicode strings with sha256
    #Then the password is hashed , and saved in a file for login verification.
    password_hash = sha256(password_info.encode('ascii')).hexdigest()

    if bool(username_info) == False or bool(password_info) == False:
        empty_field()

    elif user_db > 0 :
        user_exists()

    elif ' ' in password_info:
        invalid_password()

    elif len(username_info) > 32 or len(password_info) > 32:
        long_creds()

    else:
        if username_info.isalnum() == True:
            con = pymysql.connect(host="localhost",user="root",password="",database="accounts")
            cur = con.cursor()
            cur.execute("INSERT INTO accounts (username_info,password_hash) values(%s,%s)",
                (username_info,
                password_hash
                )) 
            con.commit()
            con.close()
            register_sucess()

        else:
            invalid_username()

    username_entry.delete(0, END)
    password_entry.delete(0, END)
 
# Implementing event on login button 
 
def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    password_hash = sha256(password1.encode('ascii')).hexdigest()

    mydb = pymysql.connect(host="localhost",user="root",password="",database="accounts") # Connects to the Database
    cur = mydb.cursor() # Creates the cursor
    query = "SELECT * FROM accounts WHERE username_info = %s AND password_hash = %s" # This query pulls all the usernames and passwords as a key pair
    cur.execute(query,[(username1),(password_hash)]) # Adding the variables to it
    password_db = len(list(cur)) # If password_word > 0 , then the key pair entered by the user exists , and results in a successful login.  This can't be greater than 1 since all usernames are unique.
    mydb.close() # Disconnects from the DB
    #print(password_db) #Use this to check the above mentioned explaintion in action. 

    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    if password_db > 0:
        login_sucess()
    else:
        user_not_found()

 
# Designing popup for login success
 
def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("125x50")
    login_success_screen.focus_set()
    login_success_screen.grab_set()
    Label(login_success_screen, text="Login Success" , font=("Rubik",9)).pack()
    Button(login_success_screen, text="OK" ,width=10, height=1, bg="white",font=("Rubik",9,"bold"), command=delete_login_success).pack()

# Designing popup for login success
 
def empty_field():
    global empty_field_screen
    empty_field_screen = Toplevel(register_screen)
    empty_field_screen.title("Error")
    empty_field_screen.geometry("275x50")
    empty_field_screen.focus_set()
    empty_field_screen.grab_set()
    Label(empty_field_screen, text="Username/Password Cannot be empty" , font=("Rubik",9)).pack()
    Button(empty_field_screen, text="OK" ,width=10, height=1, bg="white",font=("Rubik",9,"bold"), command=delete_empty_field).pack()

# Designing popup for login success
 
def long_creds():
    global long_creds_screen
    long_creds_screen = Toplevel(register_screen)
    long_creds_screen.title("Error")
    long_creds_screen.geometry("275x50")
    long_creds_screen.focus_set()
    long_creds_screen.grab_set()
    Label(long_creds_screen, text="Username/Password Cannot be longer than 32 Characters" , font=("Rubik",9)).pack()
    Button(long_creds_screen, text="OK" ,width=10, height=1, bg="white",font=("Rubik",9,"bold"), command=delete_long_creds).pack()

# Designing popup for login success
 
def user_exists():
    global user_exists_screen
    user_exists_screen = Toplevel(register_screen)
    user_exists_screen.title("Error")
    user_exists_screen.geometry("125x50")
    user_exists_screen.focus_set()
    user_exists_screen.grab_set()
    Label(user_exists_screen, text="User Already Exists" , font=("Rubik",9)).pack()
    Button(user_exists_screen, text="OK" ,width=10, height=1, bg="white",font=("Rubik",9,"bold"), command=delete_user_exists).pack()

# Designing popup for registration success

def register_sucess():
    global register_success_screen
    register_success_screen = Toplevel(register_screen)
    register_success_screen.title("Success")
    register_success_screen.geometry("155x50")
    register_success_screen.focus_set()
    register_success_screen.grab_set()
    Label(register_success_screen, text="Registration Success" , font=("Rubik",9)).pack()
    Button(register_success_screen, text="OK" ,width=10, height=1, bg="white",font=("Rubik",9,"bold"), command=delete_register_success).pack()

# Designing popup for invalid Username

def invalid_username():
    global invalid_username_screen
    invalid_username_screen = Toplevel(register_screen)
    invalid_username_screen.title("Invalid Username")
    invalid_username_screen.geometry("325x50")
    invalid_username_screen.focus_set()
    invalid_username_screen.grab_set()
    Label(invalid_username_screen, text="Username can only contain Numbers and Letters." , font=("Rubik",9)).pack()
    Button(invalid_username_screen, text="OK" ,width=10, height=1, bg="white",font=("Rubik",9,"bold"), command=delete_invalid_username).pack()

# Designing popup for invalid password

def invalid_password():
    global invalid_password_screen
    invalid_password_screen = Toplevel(register_screen)
    invalid_password_screen.title("Invalid Password")
    invalid_password_screen.geometry("255x50")
    invalid_password_screen.focus_set()
    invalid_password_screen.grab_set()
    Label(invalid_password_screen, text="Password should not contain spaces." , font=("Rubik",9)).pack()
    Button(invalid_password_screen, text="OK" ,width=10, height=1, bg="white",font=("Rubik",9,"bold"), command=delete_invalid_password).pack()
 
# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Error")
    user_not_found_screen.geometry("125x50")
    user_not_found_screen.focus_set()
    user_not_found_screen.grab_set()
    Label(user_not_found_screen, text="Invalid Credentials" , font=("Rubik",9)).pack()
    Button(user_not_found_screen, text="OK",width=10, height=1, bg="white",font=("Rubik",9,"bold"), command=delete_user_not_found_screen).pack()
 
# Deleting popups
 
def delete_login_success():
    login_success_screen.destroy()

def delete_empty_field():
    empty_field_screen.destroy()

def delete_long_creds():
    long_creds_screen.destroy()

def delete_invalid_password():
    invalid_password_screen.destroy()

def delete_register_success():
    register_success_screen.destroy()

def delete_invalid_username():
    invalid_username_screen.destroy()

def delete_user_exists():
    user_exists_screen.destroy() 
 
def delete_user_not_found_screen():
    user_not_found_screen.destroy()
 
 
# Designing Main(first) window
 
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Sign up Or Login")
    main_screen['background']='#212121'

    Label(main_screen, text="",bg="#212121",fg='white').pack()
    Label(text="pyAuthenticator", bg="#212121",fg='white', width="300", height="2", font=("Rubik", 13, "bold")).pack(padx=10,pady=10)
    Label(main_screen, text="",bg="#212121",fg='white').pack()
    Button(text="LOGIN", height="2", width="20",bg="white",font=("Rubik",10,"bold") ,  command = login).pack()
    Label(main_screen, text="",bg="#212121",fg='white').pack()
    Button(text="REGISTER", height="2", width="20",bg="white",font=("Rubik",10,"bold") , command = register).pack()
 
    main_screen.mainloop()
 
 
main_account_screen()