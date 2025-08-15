from RSA_Encryption import generateKeys
import mysql.connector as sqltor

n1, n2, accuracy = 1024, 1040, 10
public_key, private_key = generateKeys(n1, n2, accuracy)

name = input("Enter your name: ")

private_key_str = ""
with open(f"{name}_private_key.txt", 'w') as private_key_file:
	private_key_str += str(private_key[0])
	private_key_str += ", "
	private_key_str += str(private_key[1])
	private_key_file.write(private_key_str)

mycon = sqltor.connect(host="localhost", user="root", passwd="", database="rsa")
try:
	cursor = mycon.cursor()
	cursor.execute(f"insert into keystable (name, pk1, pk2) values('{name}','{public_key[0]}','{public_key[1]}') on duplicate key update pk1='{public_key[0]}',pk2='{public_key[1]}';")
	mycon.commit()
	print(f"Public key successfully updated in table.")
	print(f"Private key successfully saved in file '{name}_private_key.txt'.")
	print(f"Public key - {public_key}\nPrivate key - {private_key}")
except mysql.connector.Error as err:
	print(f"Error {err}")
finally:
	cursor.close()

	mycon.close()
