import requests
import random
import csv
file_name = "Menu.csv"
status = "0"
user_name = ""
order_id = 1
chef = ""


rows = []
with open(file_name, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        rows.append(row)
for row in rows[1:]:
    data = {}
    data['item_id'] = row[0]
    data['half_price'] = row[1]
    data['full_price'] = row[2]
    response = requests.post(
        'http://localhost:8000/add_item',
        json=data).content

while(True):
    inp = input('''\n1. Signup
2. Login
3. Logout
4. Add items
5. Read menu
6. Order
7. Display Transaction
\n''')

    inp = int(inp)
    if(inp == 1):
        username = input("Username: ")
        password = input("Password: ")
        is_chef = input("For chef enter 1 / For customer enter 0: ")
        data = {}
        data['username'] = username
        data['password'] = password
        data['is_chef'] = is_chef
        data['is_active'] = "0"
        response = requests.post(
            'http://localhost:8000/signup',
            json=data).content
        print()
        print(response.decode('ascii'))
    elif(inp == 2):
        username = input("Username: ")
        password = input("Password: ")
        data = {}
        data['username'] = username
        data['password'] = password
        user_name = username
        response = requests.post(
            'http://localhost:8000/login',
            json=data).content
        if response.decode('ascii')[0] == "0" or response.decode('ascii')[0] == "1":
            status = response.decode('ascii')[0]
            chef = response.decode('ascii')[2]
            print("Logged in successfully")
        else:
            print(response.decode('ascii'))

    elif(inp == 3):
        data = {}
        data['username'] = user_name
        if(status == "1"):
            response = requests.post(
                'http://localhost:8000/logout',
                json=data).content
            if response.decode('ascii') == "0" or response.decode(
                    'ascii') == "1":
                status = response.decode('ascii')
                user_name = ""
                chef = "0"
                print("Logged out successfully")
            else:
                print(response.decode('ascii'))
        else:
            print("You are not logged in")

    elif(inp == 4):
        if status == "1":
            if chef == "1":
                n = int(input("No. of items: "))
                for i in range(0, n):
                    item_id = int(input("Item ID: "))
                    half_price = int(input("Half Price: "))
                    full_price = int(input("Full Price: "))
                    data = {}
                    data['item_id'] = item_id
                    data['half_price'] = half_price
                    data['full_price'] = full_price
                    response = requests.post(
                        'http://localhost:8000/add_item', json=data).content
                    print()
                    print(response.decode('ascii'))
            else:
                print("You are not authorised")
        else:
            print("You are not logged in")
    elif(inp == 5):
        if status == "1":
            response = requests.get('http://localhost:8000/view_menu').content
            print()
            print(response.decode('ascii'))
        else:
            print("You are not logged in")
    elif(inp == 6):
        if status == "1":
            while(True):
                print("Want to order something?\n", end="")
                resp = int(input("Enter 1 if yes, else enter 0: "))
                if(resp == 0):
                    break
                item_id = int(input("Item ID: "))
                plate = input("half / full: ")
                qty = int(input("Quantity: "))
                data = {}
                data['username'] = user_name
                data['order_id'] = order_id
                data['item_id'] = item_id
                data['plate'] = plate
                data['qty'] = qty
                response = requests.post(
                    'http://localhost:8000/order', json=data).content
                print()
                print(response.decode('ascii'))

            tip = int(input("% Tip -- 0 / 10 / 20: "))
            share = int(input("How many of you want to split the bill?: "))
            if share == 0:
                share = 1

            test_your_luck = int(
                input("Do you want to test you luck? If yes, enter 1, else enter 0: "))

            if(test_your_luck == 1):
                my_list = [0, 1, 2, 3, 4]
                dist = [0.05, 0.1, 0.15, 0.2, 0.5]
                random_number = random.choices(my_list, dist)[0]
            if(test_your_luck == 0):
                random_number = 3

            data = {}
            data['username'] = user_name
            data['order_id'] = order_id
            data['tip'] = tip
            data['share'] = share
            data['random_number'] = random_number

            order_id += 1

            response = requests.post(
                'http://localhost:8000/generate_bill',
                json=data).content
            print()
            print(response.decode('ascii'))

        else:
            print("You are not logged in")

    elif(inp == 7):
        if status == "1":
            data = {}
            data['username'] = user_name
            response = requests.post(
                'http://localhost:8000/display_transaction',
                json=data).content
            print()
            print(response.decode('ascii'))

            resp = int(
                input("Enter the transaction number to view the billing details: "))
            if resp > 0:
                data = {}
                data['username'] = user_name
                data['transaction_id'] = resp
                response = requests.post(
                    'http://localhost:8000/display_bill',
                    json=data).content
                print()
                print(response.decode('ascii'))
            else:
                print("No response")
        else:
            print("You are not logged in")
