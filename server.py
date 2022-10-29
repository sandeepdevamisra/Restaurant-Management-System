from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey'

database = "my_db"

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:12345678@localhost:3306/{database}"
db = SQLAlchemy(app)


class User(db.Model):
    '''
    Class for initialising the User table.

    Attributes:
        username(string): Name of the user.
        password(string): Password.
        is_chef(string): Define if the user is a chef.
        is_active(string): Define if the user is logged in.
    '''
    username = db.Column(db.String(80), primary_key=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_chef = db.Column(db.String(10), nullable=False)
    is_active = db.Column(db.String(10), nullable=False)

    def __init__(self, username, password, is_chef, is_active):
        '''
        Constructor for User class

        Parameters:
            username(string): Name of the user.
            password(string): Password.
            is_chef(string): Define if the user is a chef.
            is_active(string): Define if the user is logged in.
        '''
        self.username = username
        self.password = password
        self.is_chef = is_chef
        self.is_active = is_active


class Menu(db.Model):
    '''
    Class initialising the Menu table.

    Attributes:
        item_id(int): ID of the item.
        half_price(int): Price of half plate.
        full_price(int): Price of full plate.
    '''
    item_id = db.Column(db.Integer, primary_key=True, nullable=False)
    half_price = db.Column(db.Integer, nullable=False)
    full_price = db.Column(db.Integer, nullable=False)

    def __init__(self, item_id, half_price, full_price):
        '''
        Constructor for Menu class.

        Parameters:
            item_id(int): ID of the item.
            half_price(int): Price of half plate.
            full_price(int): Price of full plate.
        '''
        self.item_id = item_id
        self.half_price = half_price
        self.full_price = full_price


class Order(db.Model):
    '''
    Class for initialising the Order table.

    Attributes:
        username(string): Name of the user.
        order_id(int): ID of the order placed.
        item_id(int): ID of the item from the menu.
        plate(string): Defines half plate or full plate.
        qty(int): Defines the quantity of item.
        amt(int): Defines the total price of the item(s) ordered.
    '''
    username = db.Column(db.String(80), primary_key=True, nullable=False)
    order_id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_id = db.Column(db.Integer, primary_key=True, nullable=False)
    plate = db.Column(db.String(10), primary_key=True, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    amt = db.Column(db.Integer, nullable=False)

    def __init__(self, username, order_id, item_id, plate, qty, amt):
        '''
        Constructor for Order table.

        Parameters:
            username(string): Name of the user.
            order_id(int): ID of the order placed.
            item_id(int): ID of the item from the menu.
            plate(string): Defines half plate or full plate.
            qty(int): Defines the quantity of item.
            amt(int): Defines the total price of the item(s) ordered.
        '''
        self.username = username
        self.order_id = order_id
        self.item_id = item_id
        self.plate = plate
        self.qty = qty
        self.amt = amt


class Transaction(db.Model):
    '''
    Class for initialising the Transaction table.

    Attributes:
        username(string): Name of the user.
        transaction_id(int): ID of the transaction.
        total(float): Total amount of the bill including discount and tip.
        tip(int): Amount of tip included.
        discount(float): Amount of discount included.
        share(int): Number of persons shared the bill.
    '''
    username = db.Column(db.String(80), primary_key=True, nullable=False)
    transaction_id = db.Column(db.Integer, primary_key=True, nullable=False)
    total = db.Column(db.Float, nullable=False)
    tip = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    share = db.Column(db.Integer, nullable=False)

    def __init__(self, username, transaction_id, total, tip, discount, share):

        '''
        Constructor for Transaction class.

        Parameters:
            username(string): Name of the user.
            transaction_id(int): ID of the transaction.
            total(float): Total amount of the bill including discount and tip.
            tip(int): Amount of tip included.
            discount(float): Amount of discount included.
            share(int): Number of persons shared the bill.
        '''
        self.username = username
        self.transaction_id = transaction_id
        self.total = total
        self.tip = tip
        self.discount = discount
        self.share = share


@app.route('/signup', methods=['POST'])
def signup():
    '''
    Function to enable registration of the user.

    Parameters: 
        void
    
    Returns:
        string: Message for the client
    '''
    data = request.get_json()
    check_user = User.query.filter_by(username=data['username']).first()
    if check_user:
        return "User already exists. Try logging in."
    new_user = User(
        data['username'],
        data['password'],
        data['is_chef'],
        data['is_active'])
    db.session.add(new_user)
    db.session.commit()
    return "Registration completed successfully."


@app.route('/login', methods=['POST'])
def login():
    '''
    Function to enable login.

    Parameters:
        void
    
    Returns:
        string: Message for the client
    '''
    data = request.get_json()
    check_user = User.query.filter_by(username=data['username']).first()
    if check_user:
        if(check_user.password == data['password']):
            check_user.is_active = "1"
            db.session.commit()
            response = check_user.is_active + " " + check_user.is_chef
            return response
        else:
            return "Incorrect Password"
    else:
        return "No such user exists"


@app.route('/logout', methods=['POST'])
def logout():
    '''
    Function to enable logout.

    Parameters: 
        void

    Returns: 
        string: Message for the client
    '''
    data = request.get_json()
    check_user = User.query.filter_by(username=data['username']).first()
    check_user.is_active = "0"
    db.session.commit()
    return check_user.is_active


@app.route('/add_item', methods=['POST'])
def add_item():
    '''
    Function to add items to the Menu table

    Paramters:
        void

    Returns:
        string: Message for the client
    '''

    data = request.get_json()
    check_item = Menu.query.filter_by(item_id=data['item_id']).first()
    if check_item:
        return "Item ID already exists"
    new_item = Menu(data['item_id'], data['half_price'], data['full_price'])
    db.session.add(new_item)
    db.session.commit()
    return "Item successfully added"


@app.route('/view_menu', methods=['GET'])
def view_menu():
    '''
    Function to read/view the Menu table.

    Parameters:
        void

    Returns:
        string: Message for the client
    '''

    data = Menu.query.all()

    response = "Item\tHalf Plate\tFull Plate\n\n"

    for i in data:
        response += str(i.item_id) + "\t" + str(i.half_price) + \
            "\t\t" + str(i.full_price) + "\n"

    return response


@app.route('/order', methods=['POST'])
def order():
    '''
    Function to place order of food items.

    Paramters:
        void

    Returns:
        string: Message for the client
    '''
    data = request.get_json()
    order_i = Menu.query.filter_by(item_id=data['item_id']).first()
    if(data['plate'] == "half"):
        amt = (order_i.half_price) * (data['qty'])
    else:
        amt = (order_i.full_price) * (data['qty'])

    temp = Order.query.filter_by(
        username=data['username'],
        order_id=data['order_id'],
        item_id=data['item_id'],
        plate=data['plate']).first()
    if(temp):
        temp.amt = temp.amt + amt
        temp.qty = temp.qty + data['qty']
        db.session.commit()
        return "Order placed successfully"

    new_item = Order(data['username'], data['order_id'], data['item_id'],
                     data['plate'], data['qty'], amt)
    db.session.add(new_item)
    db.session.commit()

    return "Order placed successfully"


@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    '''
    Function to generate the bill and store in the Transaction table.

    Parameters:
        void

    Returns:
        string: Message for the client
    '''
    data = request.get_json()
    temp = Order.query.all()
    amount = 0
    for i in temp:
        if i.username == data['username'] and i.order_id == data['order_id']:
            amount += i.amt
    tip = float(data['tip'] * 0.01)
    total_amount = amount + amount * tip
    tip = int(tip * 100)

    random_number = data['random_number']

    if(random_number == 0):
        val = -0.5 * total_amount
        total_amount = total_amount - 0.5 * total_amount

    if(random_number == 1):
        val = -0.25 * total_amount
        total_amount = total_amount - 0.25 * total_amount

    if(random_number == 2):
        val = -0.1 * total_amount
        total_amount = total_amount - 0.1 * total_amount

    if(random_number == 3):
        total_amount = total_amount
        val = 0

    if(random_number == 4):
        val = 0.2 * total_amount
        total_amount = total_amount + 0.2 * total_amount

    new_item = Transaction(
        data['username'],
        data['order_id'],
        total_amount,
        tip,
        val,
        data['share'])
    db.session.add(new_item)
    db.session.commit()

    return "Bill Generated"


@app.route('/display_transaction', methods=['POST'])
def display_transaction():
    '''
    Function to display the Transaction table

    Parameters:
        void
    
    Returns:
        string: Message for the client
    '''
    data = request.get_json()
    response = "Transactions are:\n"
    data2 = Transaction.query.all()
    for i in data2:
        if i.username == data['username']:
            response = response + str(i.transaction_id) + '\n'
    return response


@app.route('/display_bill', methods=['POST'])
def display_bill():
    '''
    Function to display the bill for each transaction made

    Parameters: 
        void

    Returns:
        string: Message for the client
    '''
    data = request.get_json()
    transaction_query = Transaction.query.filter_by(
        username=data['username'],
        transaction_id=data['transaction_id']).first()

    order_query = Order.query.all()

    user = data['username']
    total = str(transaction_query.total)
    tip = str(transaction_query.tip)
    discount = str(transaction_query.discount)
    share = str(transaction_query.share)

    response = f"User: {user}\nTotal: {total}\nTip: {tip}\nDiscount: {discount}\nShare: {share}\n\n"

    for i in order_query:
        if i.username == data['username'] and i.order_id == data['transaction_id']:
            response += "Item " + \
                str(i.item_id) + " [" + i.plate + "] " + "[" + str(i.qty) + "]: " + str(i.amt) + "\n"

    return response


if __name__ == '__main__':
  
    db.create_all()
    app.run(port=8000, debug=True)
