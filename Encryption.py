from RSA_Encryption import Encrypt
import mysql.connector as sqltor

sender = input("Enter your name (sender): ")
receiver = input("Enter receiver's name: ")

mycon = sqltor.connect(host="localhost", user="root", passwd="Fadeel@2006", database="rsa")
try:
	cursor = mycon.cursor()
	cursor.execute("select * from keystable;")
	data = cursor.fetchall()
	public_key = None
	for row in data:
		if row[0] == receiver:
			public_key = tuple([int(row[1]), int(row[2])])
			break
	if public_key == None:
		print("The receiver has not generated keys yet.")
	else:
		message = input("Enter message here: ")
		block_size = int(input("Enter block size (typically 10): "))
		cipher = Encrypt(message, block_size, public_key)

		cursor.execute(f"insert into cipher values('{sender}','{receiver}','{cipher}',{block_size});")
		mycon.commit()
except mysql.connector.Error as err:
	print(f"Error {err}")
finally:
	cursor.close()
	mycon.close()