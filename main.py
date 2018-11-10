#setup the database
#we must setup transactions--which will include the amount(positive or negative), the account, the description.
#the user must be able to add and remove Accounts--as well as get a clear view of the chart of accounts...
#the user should be able to get reports based on accounts--and on time schedules (such as 'within the last month' etc)
import os
import sqlite3
import random
import readline

def setup_newfile ():
	def use_presets():

		new_db_connection = sqlite3.connect(str(new_file_name) + '.db')
		c = new_db_connection.cursor()

		c.execute("""CREATE TABLE accounts (
					ID integer,
		            name text,
		            normal text,
		            balance integer
		            )""")
		for i in range (0, rec_accounts_length):
			c.execute("INSERT INTO accounts VALUES (?, ?, 'Debit', 0)", (i, rec_accounts[i],))
		new_db_connection.commit()

		master_db_exists = os.path.isfile('master_db.db')
		if master_db_exists:
			#file exists, open normal menu
			db_list_conn = sqlite3.connect('master_db.db')
			master_db = db_list_conn.cursor()
			# master_db.execute("""CREATE TABLE files (
			#             name text,
			#             )""")
			master_db.execute("INSERT INTO files VALUES (?)", (new_file_name,))
			db_list_conn.commit()
		else:
			db_list_conn = sqlite3.connect('master_db.db')
			master_db = db_list_conn.cursor()
			master_db_exists = os.path.isfile('master_db.db')

			master_db.execute("""CREATE TABLE files (
						name text
						)""")
			master_db.execute("INSERT INTO files VALUES (?)", (new_file_name,))
			db_list_conn.commit()

		# print("Raw DB is as follows")
		# print_coa()

	def enter_accounts():
		def setup_user_coa():
			new_db_connection = sqlite3.connect(new_file_name, '.db')
			c = new_db_connection.cursor()

			c.execute("""CREATE TABLE accounts (
					ID integer,
		            name text,
		            normal text,
		            balance integer
		            )""")
			user_coa_len = len(user_coa) - 1
			for i in range (0, user_coa_len):
				c.execute("INSERT INTO accounts VALUES (?, 'Debit', 0)", (user_coa[i],))
			new_db_connection.commit()

			print("Raw DB is as follows")
			print_coa()


		print("Please enter your accounts one at a time. When finished, press 'q' to quit.")
		user_coa = []
		while True:
			entry = raw_input(': ')
			if entry.lower() == 'q':
				break
	    	user_coa.append(entry)

		ays = raw_input("Are you sure you want to use the accounts you entered? (Y/N)")
		if (ays == "Y"):
			setup_user_coa()
		else:
			enter_accounts()
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Welcome to BookTerm setup. To begin, enter a name for your file.")
	new_file_name = raw_input(": ")

	os.system('cls' if os.name == 'nt' else 'clear')
	print("Now let's setup the chart of accounts.")


	print("Here are the recommended accounts for personal use:")

	rec_accounts = ["Gas, Fuel, Oil", "Eating Out", "Gaming", "Misc Expense"]
	rec_accounts_length = (len(rec_accounts) - 1)
	print("")
	for i in range (0, rec_accounts_length):
		print(rec_accounts[i])

	print("")
	print("Would you like to (1. Use the recommended) or (2. Setup your own accounts?) (1/2)")
	print("Note that you can add or remove accounts later")
	coa_setup_response = raw_input(": ")

	response = {'1' : use_presets, '2' : enter_accounts}

	response[coa_setup_response]()

def open_file(file):
	print("Opening " + str(file))
	term_file = sqlite3.connect(str(file) + '.db')

	c = term_file.cursor()
	c.execute("SELECT * FROM accounts WHERE normal='Debit'")
	print(c.fetchall())



def bookterm_startup():
	def db_exists_startup():
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Welcome Back!\n\n")
		print("BookTerm Files:")
		print("<><><><><><><><><><><>")

		db_list_conn = sqlite3.connect('master_db.db')
		master_db = db_list_conn.cursor()

		db_list_conn.text_factory = str

		file_list = master_db.execute('select name from files').fetchall()

		master_db.execute("SELECT max(rowid) from files")
		rows_number = (master_db.fetchone()[0])

		files_to_open = []

		for i in range (0, rows_number):
			file_name = file_list[i][0]
			print (file_name)
			files_to_open.append(file_name)
		print("<><><><><><><><><><><>")
		

		def complete(text, state):
			for cmd in files_to_open:
				if cmd.startswith(text):
					if not state:
						return cmd
					else:
						state -= 1

		readline.parse_and_bind("tab: complete")
		readline.set_completer(complete)
		file_opening = raw_input('Open File: ')
		print("1 for New File")

		if (str(file_opening) != "1"):
			open_file(file_opening)
		else:
			setup_newfile()


	def db_noexists_startup():
		#Database not found...would you like to setup?
		print("It appears the database file for BookTerm is not present, would you like to create a new file?")
		create_new_file = raw_input("(Y/N): ")

		if (create_new_file == "Y"):
			setup_newfile()
		else:
			bookterm_startup()

	db_exists = os.path.isfile('master_db.db')
	if db_exists:
		db_exists_startup()
	else:
		db_noexists_startup()

bookterm_startup()



def print_coa():
	new_db_connection = sqlite3.connect('bookterm.db')

	c = new_db_connection.cursor()
	c.execute("SELECT * FROM accounts WHERE normal='Debit'")
	print(c.fetchall())
