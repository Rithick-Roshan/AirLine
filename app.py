from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = '88c644b9f9ee399c4413ee24e331ce1d'  # Replace with your secret key
bcrypt = Bcrypt(app)

# Define data structures for passengers and flights
passenger_list = [
    {"name": "John Doe", "phone": "1234567890", "city": "New York", "dob": "1990-01-01", "password": bcrypt.generate_password_hash("password1").decode('utf-8')},
    {"name": "Jane Smith", "phone": "0987654321", "city": "Los Angeles", "dob": "1985-05-15", "password": bcrypt.generate_password_hash("password2").decode('utf-8')},
    {"name": "Alice Johnson", "phone": "5551234567", "city": "Chicago", "dob": "1992-08-21", "password": bcrypt.generate_password_hash("password3").decode('utf-8')},
    {"name": "Bob Brown", "phone": "4449876543", "city": "Houston", "dob": "1988-12-12", "password": bcrypt.generate_password_hash("password4").decode('utf-8')},
    {"name": "Charlie Davis", "phone": "3335557777", "city": "Phoenix", "dob": "1995-07-07", "password": bcrypt.generate_password_hash("password5").decode('utf-8')},
    {"name": "Emily White", "phone": "2228889999", "city": "Miami", "dob": "1993-04-18", "password": bcrypt.generate_password_hash("password6").decode('utf-8')},
    {"name": "Michael Clark", "phone": "7774445555", "city": "Dallas", "dob": "1991-11-30", "password": bcrypt.generate_password_hash("password7").decode('utf-8')},
    {"name": "Olivia Green", "phone": "6661112222", "city": "Seattle", "dob": "1989-09-25", "password": bcrypt.generate_password_hash("password8").decode('utf-8')},
    {"name": "Sophia Martinez", "phone": "3330001111", "city": "San Francisco", "dob": "1994-02-14", "password": bcrypt.generate_password_hash("password9").decode('utf-8')},
    {"name": "William Lee", "phone": "9996663333", "city": "Atlanta", "dob": "1996-06-05", "password": bcrypt.generate_password_hash("password10").decode('utf-8')},
    {"name": "Ella Hall", "phone": "8883337777", "city": "Boston", "dob": "1997-03-12", "password": bcrypt.generate_password_hash("password11").decode('utf-8')},
    {"name": "James Anderson", "phone": "1112223333", "city": "Denver", "dob": "1990-10-20", "password": bcrypt.generate_password_hash("password12").decode('utf-8')},
    {"name": "Lily Wilson", "phone": "2223334444", "city": "Las Vegas", "dob": "1993-08-08", "password": bcrypt.generate_password_hash("password13").decode('utf-8')},
    {"name": "Henry Moore", "phone": "4445556666", "city": "Portland", "dob": "1987-12-29", "password": bcrypt.generate_password_hash("password14").decode('utf-8')},
    {"name": "Ava Taylor", "phone": "5556667777", "city": "Salt Lake City", "dob": "1995-05-04", "password": bcrypt.generate_password_hash("password15").decode('utf-8')},
    {"name": "Logan Harris", "phone": "6667778888", "city": "Philadelphia", "dob": "1992-01-15", "password": bcrypt.generate_password_hash("password16").decode('utf-8')},
    {"name": "Mia Walker", "phone": "7778889999", "city": "Detroit", "dob": "1991-04-03", "password": bcrypt.generate_password_hash("password17").decode('utf-8')},
    {"name": "Jackson King", "phone": "8889990000", "city": "Charlotte", "dob": "1988-07-22", "password": bcrypt.generate_password_hash("password18").decode('utf-8')},
    {"name": "Charlotte Hill", "phone": "9990001111", "city": "Orlando", "dob": "1994-11-11", "password": bcrypt.generate_password_hash("password19").decode('utf-8')},
    {"name": "Lucas Scott", "phone": "0001112222", "city": "Minneapolis", "dob": "1993-06-27", "password": bcrypt.generate_password_hash("password20").decode('utf-8')}
]

flight_list = [
    {"airline_number": "AA123", "name": "American Airlines", "from_city": "New York", "to_city": "Los Angeles", "price_single": 300, "price_round": 550},
    {"airline_number": "DL456", "name": "Delta Airlines", "from_city": "Chicago", "to_city": "Houston", "price_single": 200, "price_round": 350},
    {"airline_number": "UA789", "name": "United Airlines", "from_city": "Phoenix", "to_city": "New York", "price_single": 250, "price_round": 450},
    {"airline_number": "SW123", "name": "Southwest Airlines", "from_city": "Los Angeles", "to_city": "Chicago", "price_single": 280, "price_round": 500},
    {"airline_number": "JB456", "name": "JetBlue Airways", "from_city": "Miami", "to_city": "San Francisco", "price_single": 320, "price_round": 600},
    {"airline_number": "AA789", "name": "American Airlines", "from_city": "Atlanta", "to_city": "Denver", "price_single": 270, "price_round": 480},
    {"airline_number": "DL321", "name": "Delta Airlines", "from_city": "Boston", "to_city": "Las Vegas", "price_single": 310, "price_round": 580},
    {"airline_number": "UA654", "name": "United Airlines", "from_city": "Portland", "to_city": "Salt Lake City", "price_single": 290, "price_round": 520},
    {"airline_number": "SW987", "name": "Southwest Airlines", "from_city": "Philadelphia", "to_city": "Detroit", "price_single": 260, "price_round": 470},
    {"airline_number": "JB654", "name": "JetBlue Airways", "from_city": "Charlotte", "to_city": "Orlando", "price_single": 300, "price_round": 550}
]


def find_passenger_by_username_or_phone(username=None, phone=None):
    for passenger in passenger_list:
        if passenger["name"] == username or passenger["phone"] == phone:
            return passenger
    return None

def register_new_passenger(name, phone, city, dob, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_passenger = {"name": name, "phone": phone, "city": city, "dob": dob, "password": hashed_password}
    passenger_list.append(new_passenger)
    return new_passenger

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passenger = find_passenger_by_username_or_phone(username=username, phone=username)
        if passenger and bcrypt.check_password_hash(passenger['password'], password):
            session['username'] = passenger['name']
            return jsonify({"success": True, "redirect_url": url_for('show_flights')})
        else:
            return jsonify({"success": False, "error": "Invalid username or password"})
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        city = request.form['city']
        dob = request.form['dob']
        password = request.form['password']
        register_new_passenger(name, phone, city, dob, password)
        return jsonify({"success": True, "redirect_url": url_for('login')})
    return render_template('signup.html')

@app.route('/show_flights')
def show_flights():
    if 'username' in session:
        return render_template('flights.html', flights=flight_list)
    else:
        return redirect(url_for('login'))

@app.route('/booking', methods=['POST'])
def booking():
    airline_number = request.form.get('airline_number')
    trip_choice = request.form.get('trip_choice')
    payment_method = request.form.get('payment_method')
    flight = next(f for f in flight_list if f['airline_number'] == airline_number)
    price = flight['price_single'] if trip_choice == 'single' else flight['price_round']
    
    if payment_method == 'cash':
        return render_template('success.html', message="Booking completed successfully.")
    elif payment_method == 'internet':
        return redirect(url_for('payment', price=price))

@app.route('/payment')
def payment():
    price = request.args.get('price')
    return render_template('payment.html', price=price)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    account_number = request.form.get('account_number')
    amount = float(request.form.get('amount'))
    if check_bank_balance(account_number) >= amount:
        return render_template('success.html', message="Transaction successful. Booking completed.")
    else:
        return render_template('success.html', message="Insufficient balance. Transaction failed.")

def check_bank_balance(account_number):
    # Simulate bank balance check
    bank_accounts = {
        "123456": 1000,
        "654321": 500,
        "111111": 750,
        "222222": 1200,
        "333333": 850,
        "444444": 1100,
        "555555": 950,
        "666666": 800,
        "777777": 1050,
        "888888": 900
    }
    return bank_accounts.get(account_number, 0)

if __name__ == "__main__":
    app.run(debug=True)
