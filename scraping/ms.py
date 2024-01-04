# Importing module
import mysql.connector
import csv
import random
# Creating connection object
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "rootpass1",
    database = "bookstore"
)

# Printing the connection object
#print(mydb)

cursor = mydb.cursor()

#stmt = """insert into address(address_one, address_two, city, state, zip)
#values ('2779 George Blauer Pl', NULL, 'San Jose', 'CA', '95135');"""

#cursor.execute(stmt)
#print ("stmt executed")

with open("values.csv") as file:
    data = list(csv.reader(file, delimiter=','))
    print (data)
    prev = set()
    for d in data:
        publisher = d[2]
        address_id = random.randint(0,1)
        print (publisher, address_id)
        if publisher not in prev:
            prev.add(publisher)
            prev.add(publisher)
            stmt = f" insert into publisher(publisher_name, publisher_address_id) values ('{publisher}', '{address_id}')"
            cursor.execute(stmt)
            print ("stmt executed")
    for d in data:
        if d[5] not in prev:
            prev.add(d[5])
            if d[0] not in prev:
                prev.add(d[0])

                title = d[0]
                fname, lname = d[1].split(" ")
                publisher = d[2]
                price = d[3]
                length = d[4]
                isbn = d[5]
                #print (publisher)
                #stmt = f"SELECT publisher_id FROM PUBLISHER WHERE publisher_name = '{publisher}';"
                #cursor.execute(stmt)

                #result = cursor.fetchone()
                #publisher_id = result[0]

                #stmt = f"SELECT author_id FROM AUTHOR WHERE author_fname = '{fname}' AND author_lname = '{lname}'"
                #cursor.execute(stmt)

                #result = cursor.fetchone()
                #author_id = result[0]

                #stmt = f"SELECT author_nl FROM AUTHOR WHERE author_id = '{author_id}'"
                #cursor.execute(stmt)
                #result = cursor.fetchone()
                #print (result[0][0])
                #nl = int(result[0][0] == 49)
                #print (nl)

                #if isbn not in prev:
                    #stmt = f"""insert into book(book_name, book_author_id, book_publisher_id, book_price, book_isbn, book_nl)
                    #values ('{title}', '{author_id}', '{publisher_id}', '{price}', '{isbn}', '{nl}')"""

                    #cursor.execute(stmt)



                """
                print (prev)
                fname, lname = d[1].split(" ")
                address = random.randint(0,1)
                nl = int(random.randint(0,4) == 3)


                print (publisher)
                """




                #print ("stmt executed")

        mydb.commit()

mydb.close()
