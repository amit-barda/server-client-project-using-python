
import socket

HOST = "192.168.56.1"  # or localhost, should match the server's HOST
PORT = 42141 # should match the server's PORT

def send_request_and_receive_response(request):
    # Create a socket for the client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((HOST, PORT))

        # Send the request to the server
        client_socket.send(request.encode())

        # Receive and decode the response from the server
        response = client_socket.recv(1024).decode()
        print("Response from server:\n", response)

    except ConnectionRefusedError:
        print("Could not connect to the server.")
    finally:
        # Close the client socket
        client_socket.close()

while True:
    # Get user input for the command to send to the server
    command = input("Enter command (CREATE, STATUS, PAY, REFILL, CHANGE, or EXIT): ").upper()

    if command == 'EXIT':
        break

    if command not in ['CREATE', 'STATUS', 'PAY', 'REFILL', 'CHANGE']:
        print("Invalid command. Please try again.")
        continue

    # Prepare the request based on the command
    if command == 'CREATE':
        request = 'CREATE'
    elif command == 'STATUS':
        card_id = input("Enter card ID: ")
        request = f'STATUS,{card_id}'
    elif command == 'PAY':
        card_id = input("Enter card ID: ")
        region = input("Enter region (North, Center, or South): ")
        request = f'PAY,{card_id},{region}'
    elif command == 'REFILL':
        card_id = input("Enter card ID: ")
        amount = input("Enter refill amount (0-9999): ")
        request = f'REFILL,{card_id},{amount}'
    elif command == 'CHANGE':
        card_id = input("Enter card ID: ")
        new_contract = input("Enter new contract (North, Center, South, or None): ")
        request = f'CHANGE,{card_id},{new_contract}'

    # Send the request to the server and receive the response
    send_request_and_receive_response(request)
