import sqlite3

##connect toi sqlite
connection=sqlite3.connect("student.db")

##cursor object to insert,etc.
cursor=connection.cursor()

table_info="""
create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT)
"""
cursor.execute(table_info)

cursor.execute('''Insert Into STUDENT values('Shubham','CSE','C',55)''')
cursor.execute('''Insert Into STUDENT values('Raj','CSE','B',58)''')
cursor.execute('''Insert Into STUDENT values('Ravi','ML','C',76)''')
cursor.execute('''Insert Into STUDENT values('Shivam','DS','A',45)''')

#display all the records
print("The inserted records are:\n")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

#commit changes in db
connection.commit()
connection.close()