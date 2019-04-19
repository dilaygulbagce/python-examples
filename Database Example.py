
import sqlite3

con = sqlite3.connect("contacts.db", isolation_level = None)

con.execute("CREATE TABLE IF NOT EXISTS Contacts (PersonID INTEGER PRIMARY KEY, Name, Surname)")
con.execute("CREATE TABLE IF NOT EXISTS Numbers (Person INTEGER, Type, Number)")
cur = con.cursor()

while True:
    choice = input("1)Search by Name\n" +
                   "2)Search by Number\n" +
                   "3)Exit\n")

    if choice == '1':
        Name = input("Enter the name: ").title()
        Surname = input("Enter the surname: ").title()
        cur.execute("SELECT PersonID FROM Contacts WHERE Name = ? AND Surname = ?", (Name, Surname))
        PersonID = cur.fetchone()

        if PersonID:
            Person = str(PersonID[0])
            print("Contact numbers: ")

            cur.execute("SELECT Type, Number FROM Numbers WHERE Person = ?", str(Person[0]))
            a = cur.fetchall()

            for i in a:
                print(i)

            choice2 = input("   1)Change the name\n" +
                            "   2)Delete contact\n" +
                            "   3)Change the number\n" +
                            "   4)Delete the number\n" +
                            "   5)Add number\n" +
                            "   6)Exit\n ")

            if choice2 == '1':
                Name = input("New name: ").title()
                Surname = input("New surname: ").title()
                con.execute("UPDATE Contacts SET Name = ?, Surname = ? WHERE PersonID = ?", (Name, Surname, str(Person[0])))
                print("Name changed successfully!")

            if choice2 == '2':
                delete = input("Are you sure want to delete this? (Y/N): ").title()

                if delete == 'Y':
                    con.execute("DELETE FROM Contacts WHERE Name = ? AND Surname = ?", (Name, Surname))
                    con.execute("DELETE FROM Numbers WHERE Person = ?", str(Person[0]))
                    print("Deleted successfully!")

                if delete == 'N':
                    print("Deletion canceled!")

            if choice2 == '3':
                Type = input("Enter the number type that you want to be changed: ").title()
                Number = input("Enter the new number: ")
                con.execute("UPDATE Numbers SET Number = ? WHERE Type = ? AND Person = ?", (Number, Type, str(Person[0])))
                print("Number changed successfully!")

            if choice2 == '4':
                Type = input("Enter the number type that you want to be deleted: ").title()
                delete = input("Are you sure want to delete this? (Y/N): ").title()

                if delete == 'Y':
                    con.execute("DELETE FROM Numbers WHERE Type = ? AND Person = ?", (Type, str(Person[0])))
                    print("Deleted successfully!")

                if delete == 'N':
                    print("Deletion canceled!")

            if choice2 == '5':
                Type = input("Enter the number type that you want to be added: ").title()
                Number = input("Enter the number: ")
                con.execute("INSERT INTO Numbers VALUES (?, ?, ?)", (str(Person[0]), Type, Number))
                print("Number adding successfully!")

        else:
            add = input("Person not found. Do you want to add new contact? (Y/N): ").title()

            if add == 'Y':
                con.execute("INSERT INTO Contacts(Name, Surname) VALUES (?, ?)", (Name, Surname))

                cur.execute("SELECT PersonID FROM Contacts WHERE Name = ? AND Surname = ?", (Name, Surname))
                PersonID = cur.fetchone()
                PersonID = str(PersonID[0])

                Type = input("Enter the number type: ").title()
                Number = input("Enter the number: ")

                con.execute("INSERT INTO Numbers VALUES (?, ?, ?)", (PersonID, Type, Number))

                print("Added successfully!")

            if add == 'N':
                print("Adding canceled!")

    if choice == '2':
        TelNum = input("Enter phone number: ")
        
        cur.execute("SELECT Name, Surname, Type FROM Contacts, Numbers WHERE PersonID = Person AND Number = '"+TelNum+"'")
        a = cur.fetchone()

        if a:
            print(a[0] + ' ' + a[1] + ' - ' + a[2])
        
        else:
            save = input("Number not found. Do you want to add new contact? (Y/N): ").title()

            if save == 'Y':

                Type = input("Enter the number type: ").title()
                Number = TelNum
                Name = input("Enter the name: ").title()
                Surname = input("Enter the surname: ").title()

                cur.execute("INSERT INTO Contacts(Name, Surname) VALUES(?,?)", (Name, Surname))
                cur.execute("SELECT PersonID FROM Contacts WHERE Name = ? AND Surname = ?", (Name, Surname))
                PersonID = cur.fetchone()
                Person = (PersonID[0])

                con.execute("INSERT INTO Numbers(Person, Type, Number) VALUES (?, ?, ?)", (Person, Type, Number))
                print("Added successfully!")

            if save == 'N':
                print("Adding Canceled!")

    if choice == '3':
        break