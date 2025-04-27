import streamlit as st
from wallet import generate_private_key, generate_public_key, generate_wallet_address
import qrcode
from cryptography.fernet import Fernet
import io

# Function to encrypt wallet data
def encrypt_wallet_data(data, password):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data, key

# Simulate a wallet database (In a real-world scenario, this would be a database)
wallet_db = {}

# Function to simulate adding funds to a wallet
def add_funds(wallet_address, amount):
    if wallet_address not in wallet_db:
        wallet_db[wallet_address] = 0
    wallet_db[wallet_address] += amount
    return wallet_db[wallet_address]

# Function to simulate transferring funds from one wallet to another
def transfer_funds(sender_wallet, receiver_wallet, amount):
    if sender_wallet not in wallet_db or wallet_db[sender_wallet] < amount:
        return False  # Insufficient funds or wallet not found
    wallet_db[sender_wallet] -= amount
    if receiver_wallet not in wallet_db:
        wallet_db[receiver_wallet] = 0
    wallet_db[receiver_wallet] += amount
    return True

# Streamlit UI
st.set_page_config(page_title="Crypto Wallet Generator", page_icon=":money_with_wings:", layout="centered")

st.title("🚀 Crypto Wallet Generator")

# Step 1: User login
login = st.sidebar.checkbox("Login to your wallet")

if login:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username and password:
            # Fake login verification (in a real-world app, this would involve checking the credentials)
            st.session_state.username = username
            st.session_state.logged_in = True
            st.success(f"Welcome, {username}!")
        else:
            st.error("Please enter both username and password.")
else:
    st.sidebar.info("Please log in to access wallet features.")

# After login, allow users to generate wallet and manage funds
if 'logged_in' in st.session_state and st.session_state.logged_in:

    # Step 2: Generate Wallet
    st.write(f"Welcome to your wallet, {st.session_state.username}!")
    
    if st.button("🔐 Generate Wallet"):
        private_key = generate_private_key()
        public_key = generate_public_key(private_key)
        wallet_address = generate_wallet_address(public_key)

        # Store the wallet in the session state
        st.session_state.wallet_address = wallet_address

        # Store the wallet in the "wallet database"
        if wallet_address not in wallet_db:
            wallet_db[wallet_address] = 0  # Initialize balance as 0

        # Display keys and address with copy-to-clipboard functionality
        st.subheader("🔑 Private Key")
        private_key_text = private_key.hex()
        st.text_area("Private Key", private_key_text, height=68)
        st.button("Copy Private Key to Clipboard", key="copy_private_key", help="Copy to clipboard")

        st.subheader("🔓 Public Key")
        public_key_text = public_key.hex()
        st.text_area("Public Key", public_key_text, height=68)
        st.button("Copy Public Key to Clipboard", key="copy_public_key", help="Copy to clipboard")

        st.subheader("🏦 Wallet Address")
        st.text_area("Wallet Address", wallet_address, height=68)
        st.button("Copy Wallet Address to Clipboard", key="copy_wallet_address", help="Copy to clipboard")

        # Generate and display QR code for wallet address
        qr_code_img = qrcode.make(wallet_address)

        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        qr_code_img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        st.subheader("📱 Wallet Address QR Code")
        st.image(img_byte_arr, use_container_width=True)

        # Encrypt and allow wallet data download with password protection
        password = st.text_input("🔒 Set a password for your wallet file (optional)", type="password")

        if password:
            wallet_data = f"""
Private Key: {private_key.hex()}
Public Key: {public_key.hex()}
Wallet Address: {wallet_address}
            """

            encrypted_wallet_data, encryption_key = encrypt_wallet_data(wallet_data, password)

            st.download_button(
                label="📥 Download Encrypted Wallet File",
                data=encrypted_wallet_data,
                file_name="wallet_encrypted.txt",
                mime="text/plain",
            )

    # Step 3: Add Funds to Wallet
    st.subheader("💰 Add Funds to Wallet")
    add_amount = st.number_input("Amount to Add to Wallet", min_value=0.0, step=0.1, format="%.2f")
    if st.button("Add Funds"):
        if 'wallet_address' in st.session_state:
            wallet_address = st.session_state.wallet_address
            if add_amount > 0:
                current_balance = add_funds(wallet_address, add_amount)
                st.success(f"{add_amount} BTC added to your wallet. Current balance: {current_balance} BTC")
            else:
                st.error("Please enter a valid amount to add.")
        else:
            st.error("Please generate a wallet first.")

    # Step 4: Transfer Funds between Wallets
    st.subheader("💸 Transfer Funds")
    recipient_wallet = st.text_input("Recipient Wallet Address", "")
    transfer_amount = st.number_input("Amount to Transfer", min_value=0.0, step=0.1, format="%.2f")

    if st.button("Transfer Funds"):
        if 'wallet_address' in st.session_state:
            sender_wallet = st.session_state.wallet_address
            if recipient_wallet and transfer_amount > 0:
                success = transfer_funds(sender_wallet, recipient_wallet, transfer_amount)
                if success:
                    st.success(f"{transfer_amount} BTC transferred successfully!")
                    st.write(f"Your current balance: {wallet_db[sender_wallet]} BTC")
                else:
                    st.error("Transaction failed! Insufficient funds or invalid recipient.")
            else:
                st.error("Please provide both recipient address and amount to transfer.")
        else:
            st.error("Please generate a wallet first.")

else:
    st.info("Log in to generate a wallet, add funds, and transfer.")

st.markdown("---")
st.caption("Made with ❤️ using Python and Streamlit")
