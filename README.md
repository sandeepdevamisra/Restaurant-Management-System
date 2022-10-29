# Restaurant-Management-System
- This a CLI based Restaurant Management System where there are 2 types of users - customer and a chef.
- A customer can perform the following activities: 
1. Signup, Login, Logout
2. Read the latest menu stored in the database
3. Order food items 
4. Generate bill. Once the bill is generated, this transaction is complete and incoming order requests will contribute to the next transaction. 
5. View previous bill statements. Initially a list of transactions pertaining to that customer will be displayed. When the customer selects one of the transactions, the entire bill for that transaction will be displayed.
- A chef can perform all the activities that a customer can with the addition of adding new items to the menu along with its cost. These changes are reflected in the database.
- REST API is created and for Flask is used. 
- MySQL is used for database. 
## Running Instructions
- Open a terminal and go to the directory where the python scripts reside.
- run `python3`
- Inside it, run:
  - `from server import db`
  - `db.create_all()`
  - `quit()`
- In the same terminal run: `python3 server.py`
- Open another terminal and run `python3 client.py`
- In the client side, input can be given through the terminal
