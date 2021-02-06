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
dbExec = dbCursor.execute

# This is the variable that determines if the user is logged in or not
# It will be changed each time the user logs in or out to the values 
# True and False respectively
loggedIn = False 

def main(loggedIn=False):
	"""
	Main function for the program. 
	It takes in 1 argument 'loggedIn' and the default value if False
	"""

	# Checks if the user is already loggin in and if not then asks to login
	# or else the user can explore as guest
	if loggedIn == False:
		print("1. Login")
		print("2. Guest")
		print("na. New Admin")
		ch = int(input("1/2\n:"))

		if ch == 1:
			login()
		elif ch == 2:
			guest()
		elif ch.lower() == 'na':
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

		ch = int(input("1/2/3/4\n:"))

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
	username = input("Username: ")
	password = getpass.getpass("Password: ")

	dbExec("select username, password from admins")
	userpass_admins = dbCursor.fetchall()
	for admin in userpass_admins:
		if username.lower() == admin[0].lower():
			if password == admin[1]:
				loggedIn = True

def guest():
	"""pass"""
	pass

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