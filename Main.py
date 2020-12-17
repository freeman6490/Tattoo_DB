import mysql.connector
from mysql.connector import errorcode

try:
    cm_connection = mysql.connector.connect(
        user='tattoo_user',
        password='180860#Ja',
        host='127.0.0.1',
        database="tattoo"
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Invalid credentials")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database not found")
    else:
        print("Something went wrong", err)

else:
    print("Success")
    customer_cursor = cm_connection.cursor()
    artist_cursor = cm_connection.cursor()
    print("Select a choice: ")
    print("1. Display list of all Customers")
    print("2. Display list of all Artists")
    print("3. Display artists in certain price range")
    print("4. Add data")
    print("5. Edit data")
    print("6. Delete data")
    val = input("Select a choice: ")

    if (val == "1"):
        customer_query = ("SELECT * FROM customer")
        customer_cursor.execute(customer_query)

        for row in customer_cursor.fetchall():
            print("{} has a price range of {} dollars".format(row[0],row[2]))

        customer_cursor.close()
    elif (val == "2"):
        artist_query = ("SELECT * FROM artist")
        artist_cursor.execute(artist_query)

        for row in artist_cursor.fetchall():
            print("{} specializes in {} and has an hourly rate of {} dollars".format(row[1],row[2],row[3]))

        artist_cursor.close()
    elif (val == "3"):
        print("1. Under 100")
        print("2. Under 200")
        print("3. Under 300")
        option = input("Select a choice: ")
        if (option == "1"):
            artist_query = ("SELECT name FROM artist WHERE hourly_rate < 100")
            artist_cursor.execute(artist_query)

            for row in artist_cursor.fetchall():
                print("{}", row[0])

            artist_cursor.close()
        elif (option == "2"):
            artist_query = ("SELECT name FROM artist WHERE hourly_rate < 200")
            artist_cursor.execute(artist_query)

            for row in artist_cursor.fetchall():
                print(row[0])

            artist_cursor.close()
        else:
            artist_query = ("SELECT name FROM artist WHERE hourly_rate <3100")
            artist_cursor.execute(artist_query)

            for row in artist_cursor.fetchall():
                print(row[0])

            artist_cursor.close()
    elif (val == "4"):
        print("1. Add an artist")
        print("2. Add a customer")
        numbers = input("Select a choice: ")
        if (numbers == "1"):
            artist_id = input("Enter id: ")
            name = input("Enter name: ")
            specialty = input("Enter specialty: ")
            artist_hourly = input("Enter hourly rate: ")

            artist_insert_query = ("Insert into artist "
                                   "(artist_id, name, specialty, hourly_rate) "
                                   "VALUES (%s, %s, %s, %s)")
            artist_data = (artist_id, str(name), str(specialty), artist_hourly)

            try:
                artist_cursor = cm_connection.cursor()
                artist_cursor.execute(artist_insert_query, artist_data)
                cm_connection.commit()
                print("Added an artist")
                artist_cursor.close()
            except mysql.connector.Error as err:
                print("Artist not added")
                print(err)
            cm_connection.close()

        else:
            name = input("Enter customer name: ")
            customer_id = input("Enter customer ID: ")
            price_range = input("Enter price range: ")

            customer_insert_query = ("Insert into customer "
                                     "(customer_id, name, price_range) "
                                     "VALUES (%s, %s, %s)")
            customer_data = (customer_id, str(name), price_range)

            try:
                customer_cursor = cm_connection.cursor()
                customer_cursor.execute(customer_insert_query, customer_data)
                cm_connection.commit()
                print("Added a customer")
                customer_cursor.close()
            except mysql.connector.Error as err:
                print("Customer not added")
                print(err)
            cm_connection.close()


    elif (val == "5"):
        selection = input("Select 1 to update artist, 2 to update customer: ")
        if selection == "1":
            artist_search_id = input("Enter artist id: ")
            column = input("Enter what column to update (name, artist_id, hourly_rate, specialty): ")
            prompt = input("Enter new value for {} ".format(column))
            if column == "name" or "specialty":
                artist_query = (" Update artist "
                                "SET " + str(column) + "= %s "
                                "WHERE artist_id = %s")
                artist_data = (prompt, artist_search_id)
            else:
                prompt = input("Enter new value for {} ".format(column))
                artist_query = (" Update artist "
                                "SET " + column + "= %s "
                                "WHERE artist_id = %s")
                artist_data = (prompt, artist_search_id)

            try:
                artist_cursor = cm_connection.cursor()
                artist_cursor.execute(artist_query, artist_data)
                cm_connection.commit()
                print("Updated artist")
                artist_cursor.close()
            except mysql.connector.Error as err:
                print("Was not able to update artist")
                print(err)
                cm_connection.close()
        else:
            customer_search_id = input("Enter customer id: ")
            column = input("Enter what column to update (name, customer_id, price_range): ")
            prompt = input("Enter new value for {} ".format(column))
            if column == "name":
                customer_query = (" Update customer "
                                "SET " + str(column) + "= %s "
                                                       "WHERE customer_id = %s")
                customer_data = (prompt, customer_search_id)
            else:
                prompt = input("Enter new value for {} ".format(column))
                customer_query = (" Update customer "
                                "SET " + column + "= %s "
                                                  "WHERE customer_id = %s")
                customer_data = (prompt, customer_search_id)

            try:
                customer_cursor = cm_connection.cursor()
                customer_cursor.execute(customer_query, customer_data)
                cm_connection.commit()
                print("Updated customer")
                artist_cursor.close()
            except mysql.connector.Error as err:
                print("Was not able to update customer")
                print(err)
                cm_connection.close()
    else:
        selection = input("1 to delete customer, 2 to delete artist: ")
        if selection == "1":
            customer_delete_key = input("Enter customer id to delete: ")
            customer_query = ("DELETE FROM customer "
                              "WHERE customer_id = %s")
            customer_data = (customer_delete_key, )

            try:
                customer_cursor = cm_connection.cursor()
                customer_cursor.execute(customer_query, customer_data)
                cm_connection.commit()
                print("Deleted customer")
                customer_cursor.close()
            except mysql.connector.Error as err:
                print("Not able to delete customer")
                print(err)
        else:
            artist_delete_key = input("Enter artist id to delete: ")
            artist_query = ("DELETE FROM artist "
                              "WHERE artist_id = %s")
            artist_data = (artist_delete_key, )

            try:
                artist_cursor = cm_connection.cursor()
                artist_cursor.execute(artist_query, artist_data)
                cm_connection.commit()
                print("Deleted artist")
                customer_cursor.close()
            except mysql.connector.Error as err:
                print("Not able to delete artist")
                print(err)
    cm_connection.close()
