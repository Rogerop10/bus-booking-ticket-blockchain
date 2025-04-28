import hashlib
import json
from time import time
from datetime import datetime
import streamlit as st

# Blockchain implementation
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash='1', proof=100)  # Genesis block

    def new_block(self, proof, previous_hash=None):
        """
        Create a new block and add it to the chain
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, user, bus_number, seat_number, date):
        """
        Create a new transaction (ticket booking)
        """
        self.current_transactions.append({
            'user': user,
            'bus_number': bus_number,
            'seat_number': seat_number,
            'date': date
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        Simple proof of work algorithm:
        Find a number such that hash(last_proof + proof) starts with 0000
        """
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the proof
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Initialize Blockchain
blockchain = Blockchain()

# Streamlit UI
st.set_page_config(page_title="Bus Ticket Blockchain", layout="centered")
st.title("🚌 Bus Ticket Booking System with Blockchain")

st.write("Book your seat on a bus and watch the blockchain grow with each transaction.")

# Form Input
user_name = st.text_input("👤 Enter your name:")
bus_number = st.text_input("🚌 Enter Bus Number (e.g., B123):")
seat_number = st.text_input("💺 Enter Seat Number (e.g., A1):")
trip_date = st.date_input("📅 Select Trip Date:")

# Book Ticket
if st.button("Book Ticket"):
    if user_name and bus_number and seat_number:
        blockchain.new_transaction(user_name, bus_number, seat_number, trip_date.strftime("%Y-%m-%d"))
        last_proof = blockchain.last_block['proof']
        proof = blockchain.proof_of_work(last_proof)
        block = blockchain.new_block(proof)

        st.success(f"✅ Ticket booked successfully!")
        st.info(f"🔒 Block #{block['index']} added to the blockchain.")
    else:
        st.warning("⚠️ Please fill out all fields.")

# Show Blockchain
st.subheader("📦 Current Blockchain")
for block in blockchain.chain:
    st.write(f"### Block {block['index']}")
    st.write(f"- ⏱ Timestamp: {datetime.fromtimestamp(block['timestamp'])}")
    st.write(f"- 🔗 Previous Hash: `{block['previous_hash']}`")
    st.write(f"- 🔐 Proof: {block['proof']}")
    st.write(f"- 📄 Transactions:")
    for txn in block['transactions']:
        st.json(txn)
    st.write("---")
