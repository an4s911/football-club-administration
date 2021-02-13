import mysql.connector as mc
from getpass import getpass

# Database connection lines. Connecting to database fc_admin
db = mc.connect(
	host='localhost', 
	user='root',
	passwd='',
	auth_plugin='mysql_native_password'
	)
dbCursor = db.cursor()
Exec = dbCursor.execute

Exec("create database if not exists fc_admin")
Exec("use fc_admin")
Exec("create table if not exists admins(name varchar(20), username varchar(20), password varchar(50), nationality varchar(20))")

# This is the variable that determines if the user is logged in or not
# It will be changed each time the user logs in or out to the values 
# True and False respectively
loggedIn = False
guest = False

user_info = {'guest': False, 'loggedIn': False, 'username': None}

def fcInput(prompt):
	"""
	This function is a custom input function which is gonna be used in this 
	program instead of the default input() function. 

	It will do some checks on the user's input and then returns the value 
	input by the user if conditions meet like if the input is 'q' then the 
	program quits and 'm' is used to go back to main menu.
	"""
	global loggedIn
	user_input = input(prompt)

	copy_user_input = user_input.lower()

	if copy_user_input in ['q', 'm', 'lo', 'help']:
		if copy_user_input == 'q':
			quit_confirm_input = input("Are you sure you want to quit? y/n: ")
			if quit_confirm_input.lower() in ['y', 'yes']:
				quit()
			else: 
				main()
		elif copy_user_input == 'm':
			main()
		elif copy_user_input == 'lo':
			if loggedIn == True:
				loggedIn = False
				print("You have been logged out.")
				main()
			else:
				main()
		elif copy_user_input == 'help':
			instructions()
	elif not copy_user_input:
		print("Invalid Input! Going back to the main menu")
		main()
	else:
		return user_input

def instructions():
	print("""------------------------------
Instructions on How to use this software.
In any input space you can use the following characters to do the respective task.
q - To quit the program (asks for confirmation)
m - Go back to the main menu
lo - Logout out of your account
help - To show this instructions
------------------------------""")
	main()

def main():
	global loggedIn
	"""
	Main function for the program. 
	"""

	# Checks if the user is already loggin in and if not then asks to login
	# or else the user can explore as guest
	print("Main Menu")
	if loggedIn:
		print("Admin Controls!")
		print("1. Members")
		print("2. Payments")
		print("3. Transfers")
		print("4. Events/ News")

		ch = int(fcInput("1/2/3/4:"))

		if ch == 1:
			show_admins()
		elif ch == 2:
			payments()
		elif ch == 3:
			transfers()
		elif ch == 4:
			events()
		else:
			print("Invalid")
			main(loggedIn)

	# If user is logged in as an admin, then they can do jobs as listed:
	# Manage Members, Payments, Transfers, Events/ News
	else:
		print("You are not logged in")
		print("Select one of the below")
		print("1. Login")
		print("2. Guest")
		print("3. New Admin")
		ch = int(fcInput("1/2:"))

		if ch == 1:
			login()
		elif ch == 2:
			guest()
		elif ch == 3:
			new_admin()
		else:
			print("Invalid Input!")
			main(loggedIn)

def login():
	"""
	The login Function
	"""
	global loggedIn
	username = fcInput("Username: ")
	password = getpass("Password: ")

	Exec("select username, password from admins")
	userpass_admins = dbCursor.fetchall()
	for admin in userpass_admins:
		if username.lower() == admin[0].lower():
			if password == admin[1]:
				
				loggedIn = True
				print("You are now Logged In")
				main()
				break
			else:
				print("Incorrect Password. Try again!")
				login()
				break
	else:
		print("Username not found.")
		login()

def guest():
	global loggedIn
	print("You are on guest mode!")
	print("1. View events")
	print("2. Show Admins")
	ch = int(fcInput("1/2: "))

	if ch == 1:
		events()
	elif ch == 2:
		show_admins()
	else:
		print("Invalid")
		guest()


def show_admins():
	"""
	show_admins()
	"""
	global loggedIn
	Exec('desc admins')
	colnames = [colname[0] for colname in dbCursor.fetchall()]
	Exec('select * from admins')
	admins = [dict(admin) for admin in [list(zip(colnames, admin)) for admin in dbCursor.fetchall()]]

	print("For more details on each admin, enter the number preceeding the name.")
	while True:
		for admin in admins:
			print(f"{admins.index(admin)+1}.", admin['name'])

		ch = int(fcInput(': '))
		try:
			admin_details = admins[ch-1]

			if loggedIn:
				print("Options available on member:")
				print("1. Delete Member")
				print("2. Show details")
				print("3. Modify details")

				ch = int(fcInput(": "))

				if ch == 1:
					confirmation = fcInput("Are you sure to delete (y/n): ")
					if confirmation.lower() in ['y', 'yes']:
						username = admin_details['username']
						print("--- Deleting Account ---")
						print("--- Removing from database ---")
						Exec(f"delete from admins where username='{username}'")
						db.commit()
						print("--- Removed account details from Database ---")
						print(f"--- Deleted admin account for {username} ---")
						print()
						print("You will be logged out and returned to Main Menu for security reasons")
						loggedIn = False
						main()

					else:
						continue
			else:
				for detail in admin_details:
					if detail != 'password':
						print(detail.capitalize(), '-->', admin_details[detail].capitalize())

			if fcInput("Main menu? (y/n): ").lower() in ['y', 'yes']:
				main()
			else:
				continue
		except IndexError:
			print("Invalid!")

def new_admin():
	"""
	To create a new admin account.

	It takes no arguments

	The user can create an admin account only if authorized, 
	and to verify the user must input an Admin Key which is
	mandatory.

	This function returns --> None
	"""
	print("For creating a new admin account, the admin key is required")
	admin_key_input = fcInput("Admin Key: ") 
	admin_key = open('admin_key.txt').read() # The admin key is "ADMIN"
	if admin_key_input == admin_key:
		print("That is the valid key. Fill the following details.")
		name = fcInput("Name: ")
		username = fcInput("Username: ")
		password = getpass("Password: ")
		nationality = fcInput("Nationality: ")
		Exec(f"insert into admins values('{name}', '{username}', '{password}', '{nationality}')")
		db.commit()
		print("... Signing Up....")
		print("Successfully Registered")
		main()

	else:
		print("Invaild key")
		new_admin()

def payments():
	"""pass"""
	pass

def events():
	"""pass"""
	pass

if __name__=="__main__":
	instructions()