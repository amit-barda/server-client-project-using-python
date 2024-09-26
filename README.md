# server client project

#  Automated Public Transportation System

This project implements an automated public transportation system  . It is built as a client-server system, where clients send requests to the server, and the server responds accordingly.

## Table of Contents
- [Project Overview](#project-overview)
- [System Requirements](#system-requirements)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Client Operations](#client-operations)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The **Lots-Of-Trips** system simulates a public transportation card system, where users can create new cards, check card statuses, pay for rides, refill wallets, and change contracts. Each card has a unique ID, a contract field (representing a region), and a wallet containing a balance. The server ensures each request is valid before responding.

## System Requirements
- Python 3.x
- SQL Database (e.g., SQLite, MySQL)
- Socket Programming Library for Client-Server Communication
- Optional: GUI framework (e.g., Tkinter or PyQt for extra credit)

## Features

### Cards and Contracts
- Each card has a **unique ID** (up to 4 digits), a **wallet**, and a **contract**.
- Contracts represent regions: `North`, `Center`, `South`, or `None`.

### Operations
Clients can perform the following operations:
1. **Create a New Card**: Generates a new card with an initial wallet balance of 0 and no contract.
2. **Check Card Status**: Displays the card’s ID, wallet balance, and contract.
3. **Pay for a Ride**: Allows a ride if the contract or wallet conditions are met.
4. **Refill the Wallet**: Adds a specified amount of money to the card’s wallet.
5. **Change Contract**: Updates the contract to a different region.

### Payment System
- The system allows free rides within the card’s contract region.
- For other regions, the ride cost is subtracted from the wallet based on the price list:
  - North: 25
  - Center: 40
  - South: 30

## Installation

1. **Clone the repository**:
   ```bash
   git clone git@github.com:amit-barda/server-client-project-using-python.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd server-client-project-using-python
   ```
3. **Install required libraries**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up the database**:
   - Create a SQL database and ensure it is connected to the server code.

5. **Run the server**:
   ```bash
   python server.py
   ```

6. **Run the client**:
   ```bash
   python client.py
   ```

## Usage

### Client Operations

1. **Create a New Card**: 
   - Sends a request to the server to generate a new card.
   - Example:
     ```
     Client: Create new card
     Server: Card ID: 1234, Wallet: 0, Contract: None
     ```

2. **Check Card Status**: 
   - Sends a request to check the card’s information.
   - Example:
     ```
     Client: Check card status for ID: 1234
     Server: Card ID: 1234, Wallet: 50, Contract: Center
     ```

3. **Pay for a Ride**:
   - Sends a ride request for a specific region.
   - Example:
     ```
     Client: Pay for a ride to North, Card ID: 1234
     Server: Done (or Fail if conditions aren’t met)
     ```

4. **Refill the Wallet**:
   - Sends a request to add money to the wallet.
   - Example:
     ```
     Client: Refill wallet with 100, Card ID: 1234
     Server: Done
     ```

5. **Change Contract**:
   - Sends a request to change the card’s contract.
   - Example:
     ```
     Client: Change contract to South, Card ID: 1234
     Server: Done
     ```

## Error Handling

- The server rejects any request for a non-existent card with a relevant error message.
- The system checks for illegal inputs (e.g., invalid card ID, incorrect region).
- If a network issue occurs, the server will handle potential disconnections gracefully.

## Contributing

If you'd like to contribute to the project, feel free to submit a pull request or raise issues. All contributions are welcome!
