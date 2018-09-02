import mysql.connector as mycon

mydb = mycon.connect(
	host="localhost",
	user="brennan",
	passwd="admin",
	database="test"
)

cursor = mydb.cursor()

cursor.execute("describe vg_test")

result = cursor.fetchall()

for x in result:
 	print(x)