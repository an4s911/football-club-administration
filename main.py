import mysql.connector as mc
from getpass import getpass
from datetime import date
import re

# Database connection lines. Connecting to database fc_admin
db = mc.connect(
	host='localhost', 
	user='root',
	passwd='',
	auth_plugin='mysql_native_password'
	)
dbCursor = db.cursor()
Exec = dbCursor.execute

# Create database if it doesn't already exist
# creates requried tables with appropriate column names
Exec("create database if not exists fc_admin")
Exec("use fc_admin")
Exec("create table if not exists admins(name varchar(20), username varchar(20), password varchar(50), nationality varchar(20))")
Exec("create table if not exists events(sl_no int primary key not null auto_increment, date date, description varchar(70))")
Exec("create table if not exists transfers(sl_no int primary key not null auto_increment, date date, description varchar(20))")

# This is the variable that determines if the user is logged in or not
# It will be changed each time the user logs in or out to the values 
# True and False respectively
loggedIn = False

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
	"""
	Main function for the program. 
	"""

	# Checks if the user is already login in and if not then asks to login
	# or else the user can explore as guest

	global loggedIn
	
	print("Main Menu")

	if loggedIn:
		print("Admin Controls!")

		print("1. Members")
		print("2. Transfers")
		print("3. Events/ News")

		ch = int(fcInput("1/2/3/4:"))

		if ch == 1:
			show_admins()

		elif ch == 2:
			transfers()

		elif ch == 3:
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

		ch = int(fcInput("1/2/3:"))

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
	This function is for logging in the admin

	If the entered credentials are correct then the user will be 
	logged in and can special features like modify admin details, 
	post new events etc.
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
	"""
	This is the function that logs in the user as a guest.
	A guest can only view and cannot modify.
	"""

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
	This function is used to display the list of all
	the admins. And to delete or modify admins(for admins only)

	When an admin is deleted the current user is logged out 
	for security.

	Guest users can only see the names and details of each
	admin
	"""

	global loggedIn

	Exec('desc admins')
	colnames = [colname[0] for colname in dbCursor.fetchall()]

	Exec('select * from admins')
	admins = [dict(admin) for admin in [list(zip(colnames, admin)) for admin in dbCursor.fetchall()]]

	print("For more details on each admin, enter the number preceding the name.")

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

						print("You will be logged out and returned to Main Menu for security reasons")
						loggedIn = False

						main()

					else:
						continue

				elif ch == 2:
					for detail in admin_details:
						if detail != 'password':
							print(detail.capitalize(), '-->', admin_details[detail].capitalize())

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
		print("Invalid key")
		new_admin()


def events():
	"""
	This function is used for displaying and posting events(only for admins)

	It has 3 options (4 if admin):
		1. To show the upcoming events
		2. To show the past events
		3. To show all events
		4. (Admins only) To post new event.
	"""

	global loggedIn

	print("Events")
	print("1. Upcoming events")
	print("2. Past events")
	print("3. All events")
	
	if loggedIn: 
		print("4. Post new event")

	ch = int(fcInput(": "))

	if ch == 1:
		Exec("select date, description from events where DATE(date) >= CURDATE()")
		upcoming_events = dbCursor.fetchall()
		
		for event in upcoming_events:
			date, description = event
			print(f"{upcoming_events.index(event)+1}. {description} on {date}")

	elif ch == 2:
		Exec("select date, description from events where DATE(date) < CURDATE()")
		past_events = dbCursor.fetchall()
		
		for event in past_events:
			date, description = event
			print(f"{past_events.index(event)+1}. {description} on {date}")

	
	elif ch == 3:
		Exec("select date, description from events")
		all_events = dbCursor.fetchall()

		print("All Events")

		for event in all_events:
			date, description = event
			print(f"{all_events.index(event)+1}. {description} --> {date}")

	
	elif ch == 4 and loggedIn:
		print("Enter date in formats \nYear-YYYY, Month-MM, Day-DD")
		
		event_year = int(fcInput('Year: '))
		event_month = int(fcInput('Month: '))
		event_day = int(fcInput('Day: '))
		event_description = fcInput("Description: ")
		
		print("--- Posting Event details ---")
		
		print("--- Saving to Database ---")
		Exec(f"insert into events (date, description) values('{event_year}-{event_month}-{event_day}', '{event_description}')")
		db.commit()
		
		print("--- Database Successful ---")
		print("--- Event Posted ---")
		events()

	else:
		print("Invalid")
		events()

	events()


def transfers():
	"""
	This function is accessible by admins only

	It is used to display past, upcoming or all transfers

	Also new transfers can be added.
	"""

	global loggedIn

	if not loggedIn:
		print("You are not authorized")
		menu()

	print("Transfers")
	print("1. All Transfers")
	print("2. Past Transfers")
	print("3. Upcoming Transfers")
	print("4. New Transfer")

	ch = int(fcInput(": "))

	if ch == 1:
		Exec("select date, description from transfers")

		transfers_list = dbCursor.fetchall()

		for transfer in transfers_list:
			date, description = transfer

			print(f"{transfers_list.index(transfer)+1}. {description} on {date}")
	
	elif ch == 2:
		Exec("select date, description from transfers where DATE(date) < CURDATE()")

		transfers_list = dbCursor.fetchall()

		for transfer in transfers_list:
			date, description = transfer

			print(f"{transfers_list.index(transfer)+1}. {description} on {date}")

	elif ch == 3:
		Exec("select date, description from transfers where DATE(date) >= CURDATE()")

		transfers_list = dbCursor.fetchall()

		for transfer in transfers_list:
			date, description = transfer

			print(f"{transfers_list.index(transfer)+1}. {description} on {date}")


	elif ch == 4:
		print("New transfer. Enter the required information when prompted")

		print("Transfer date format -> Year-YYYY, Month-MM, Day-DD")
		transfer_year = int(fcInput("Year: "))
		transfer_month = int(fcInput("Month: "))
		transfer_day = int(fcInput("Day: "))

		print("Enter a bried description")
		transfer_description = fcInput("Description: ")
		
		print("--- Saving to Database ---")
		Exec(f"insert into transfers (date, description) values('{transfer_year}-{transfer_month}-{transfer_day}', '{transfer_description}')")
		db.commit()
		
		print("--- Database Successful ---")
		print("--- Transfer information Stored ---")

		transfers()

	else:
		print("Invalid")
		transfers()

	transfers()

if __name__=="__main__":
	instructions()