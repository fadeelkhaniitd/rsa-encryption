from RSA_Encryption import Decrypt
import mysql.connector as sqltor

name = input("Enter your name: ")

with open(f"{name}_private_key.txt") as private_key_file:
	content = private_key_file.read()
	private_key_list = content.split(', ')
	for i, x in enumerate(private_key_list):
		private_key_list[i] = int(x)
	private_key = tuple(private_key_list)

mycon = sqltor.connect(host="localhost", user="root", passwd="", database="rsa")
try:
	cursor = mycon.cursor()
	cursor.execute("select * from cipher;")
	data = cursor.fetchall()
	pending = []
	for row in data:
		if row[1] == name:
			pending.append([row[0], row[2], row[3]])
	if pending == []:
		print("You have not received any messages yet.")
	else:
		cursor.execute(f"delete from cipher where receiver='{name}';")
		mycon.commit()
		for curr in pending:
			message = Decrypt(curr[1], curr[2], private_key)
			print(f"{curr[0]} sent '{message}'.")
except mysql.connector.Error as err:
	print(f"Error {err}")
finally:
	cursor.close()

	mycon.close()
