import mysql.connector as mc
import getpass

# Database connection lines. Connecting to database fc_admin
db = mc.connect(
	host='localhost', 
	user='root', 
	auth_plugin='mysql_native_password', 
	database='fc_admin'
	)
dbCursor = db.cursor()
Exec = dbCursor.execute

# This is the variable that determines if the user is logged in or not
# It will be changed each time the user logs in or out to the values 
# True and False respectively
loggedIn = False
guest = False

user_info = {'guest': False, 'loggedIn': False}

def fcInput(prompt):
	"""
	This function is a custom input function which is gonna be used in this 
	program instead of the default input() function. 

	It will do some checks on the user's input and then returns the value 
	input by the user if conditions meet like if the input is 'q' then the 
	program quits and 'm' is used to go back to main menu.
	"""
	global loggedIn
	user_input = input(prompt).lower()

	if user_input in ['q', 'm', 'lo', 'help']:
		if user_input == 'q':
			quit_confirm_input = input("Are you sure you want to quit? y/n: ")
			if quit_confirm_input.lower() in ['y', 'yes']:
				quit()
			else: 
				main()
		elif user_input == 'm':
			main()
		elif user_input == 'lo':
			if loggedIn == True:
				loggedIn = False
				print("You have been logged out.")
				main()
			else:
				main()
		elif user_input == 'help':
			instructions()
	else:
		return user_input

def instructions():
	main()

def main():
	global loggedIn
	"""
	Main function for the program. 
	"""

	# Checks if the user is already loggin in and if not then asks to login
	# or else the user can explore as guest
	if loggedIn == False:
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

	# If user is logged in as an admin, then they can do jobs as listed:
	# Manage Members, Payments, Transfers, Events/ News
	else:
		print("Admin Controls!")
		print("1. Members")
		print("2. Payments")
		print("3. Transfers")
		print("4. Events/ News")

		ch = int(fcInput("1/2/3/4:"))

		if ch == 1:
			members()
		elif ch == 2:
			payments()
		elif ch == 3:
			transfers()
		elif ch == 4:
			events()
		else:
			print("Invalid")
			main(loggedIn)

def login():
	"""
	pass
	"""
	global loggedIn
	username = fcInput("Username: ")
	password = getpass.getpass("Password: ")

	Exec("select username, password from admins")
	userpass_admins = dbCursor.fetchall()
	for admin in userpass_admins:
		if username.lower() == admin[0].lower():
			if password == admin[1]:
				
				loggedIn = True
				print("You are now Logged In 😄")
				main()
			else:
				print("Incorrect Password😕. Try again!😌")
				login()
		else:
			print("Username not found.😐")
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
			print(admins[ch-1])
			if fcInput("Main menu? (y/n): ").lower() in ['y', 'yes']:
				main()
			else:
				continue
		except IndexError:
			print("Invalid!")

def new_admin():
	"""pass"""
	pass

def members():
	"""pass"""
	pass

def payments():
	"""pass"""
	pass

def events():
	"""pass"""
	pass

if __name__=="__main__":
	instructions()