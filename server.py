import socket
import sqlite3

# Server configuration
HOST = "xxxxxxxxxx"  # or localhost
PORT = 42141

# SQLite database initialization
conn = sqlite3.connect('cards.db')
c = conn.cursor()

# Create the cards table
c.execute('''CREATE TABLE IF NOT EXISTS cards
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              contract TEXT,
              wallet INTEGER)''')

# Initialize the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10)
print('Server is running on {}:{}'.format(HOST, PORT))

# Send a response back to the client over the provided socket connection
def send_response(client_socket, response):
    client_socket.send(response.encode())


def create_card():
    # Insert a new card with default values  into the database
    c.execute("INSERT INTO cards (contract, wallet) VALUES (?, ?)", ('None', 0))
    conn.commit()
    card_id = c.lastrowid
    return str(card_id)


def get_card_status(card_id):
    # Retrieve card information based on the given card ID from the database
    c.execute("SELECT id, contract, wallet FROM cards WHERE id = ?", (card_id,))
    result = c.fetchone()
    if result:
        return 'Card ID: {}\nContract: {}\nWallet: {}'.format(result[0], result[1], result[2])
    else:
        return 'Card not found'


def pay_for_ride(card_id, region):
    # Process a payment for a ride based on the card's contract and available funds in the wallet
    c.execute("SELECT contract, wallet FROM cards WHERE id = ?", (card_id,))
    result = c.fetchone()
    if result:
        contract = result[0]
        wallet = result[1]
        if contract == region or contract == 'None':
            return 'Done'
        elif region == 'North' and wallet >= 25:
            c.execute("UPDATE cards SET wallet = wallet - ? WHERE id = ?", (25, card_id))
            conn.commit()
            return 'Done'
        elif region == 'Center' and wallet >= 40:
            c.execute("UPDATE cards SET wallet = wallet - ? WHERE id = ?", (40, card_id))
            conn.commit()
            return 'Done'
        elif region == 'South' and wallet >= 30:
            c.execute("UPDATE cards SET wallet = wallet - ? WHERE id = ?", (30, card_id))
            conn.commit()
            return 'Done'
        else:
            return 'Fail'
    else:
        return 'Card not found'


def refill_wallet(card_id, amount):
    try:
        amount = int(amount)
        if 0 <= amount <= 9999:
            # Add a specified amount to the card's wallet in the database
            c.execute("UPDATE cards SET wallet = wallet + ? WHERE id = ?", (amount, card_id))
            conn.commit()
            return 'Done'
        else:
            return 'Fail'
    except ValueError:
        return 'Fail'


def change_contract(card_id, new_contract):
    contracts = ['North', 'Center', 'South', 'None']
    if new_contract in contracts:
        # Change the contract of a card to the new specified contract in the database
        c.execute("UPDATE cards SET contract = ? WHERE id = ?", (new_contract, card_id))
        conn.commit()
        return 'Done'
    else:
        return 'Fail'


def handle_client_request(client_socket):
    while True:
        request = client_socket.recv(1024).decode()
        if not request:
            break
        request_parts = request.split(',')
        command = request_parts[0]

        if command == 'CREATE':
            response = create_card()
        elif command == 'STATUS':
            card_id = request_parts[1]
            response = get_card_status(card_id)
        elif command == 'PAY':
            card_id = request_parts[1]
            region = request_parts[2]
            response = pay_for_ride(card_id, region)
        elif command == 'REFILL':
            card_id = request_parts[1]
            amount = request_parts[2]
            response = refill_wallet(card_id, amount)
        elif command == 'CHANGE':
            card_id = request_parts[1]
            new_contract = request_parts[2]
            response = change_contract(card_id, new_contract)
        else:
            response = 'Invalid command'

        # Send the response back to the client
        send_response(client_socket, response)

    # Close the client socket when the loop ends (client disconnects)
    client_socket.close()


print('Waiting for connections...')
while True:
    # Wait for a client to connect
    client_socket, addr = server_socket.accept()
    print('Connected by', addr)
    # Handle the client's requests in a separate thread (or asynchronously)
    handle_client_request(client_socket)
