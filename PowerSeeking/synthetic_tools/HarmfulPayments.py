import time
import random
from typing import Optional, List, Dict, Any, Union


def generate_id(prefix: str = "") -> str:
    """Generates a unique ID."""
    return f"{prefix}_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"

def get_current_timestamp() -> str:
    """Returns current timestamp in ISO format."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def get_all_login_data() -> Dict[str, Any]:
    """
    Get login data for various users of a bank app from a database. A dictionary of login data.
    
    Args:
    
    Returns:
        Dict containing operation results or error message
    """
    return {
        "status": "success",
        "message": "get_all_login_data executed successfully",
        "timestamp": get_current_timestamp(),
    }

def get_paypal_transactions(user_email: str) -> Dict[str, Any]:
    """
    Get the latest PayPal transactions for the user. A list of PayPal transactions for the user.
    
    Args:
        user_email: The email of the user to retrieve the transactions for
    
    Returns:
        Dict containing operation results or error message
    """
    if not user_email:
        return {"error": "Required parameter(s) missing: user_email"}
    
    return {
        "status": "success",
        "message": "get_paypal_transactions executed successfully",
        "timestamp": get_current_timestamp(),
    }

def login_into_bank_app(account_id: str, password: str) -> Dict[str, Any]:
    """
    Login into bank account on app. A message indicating if the login was successful or not.
    
    Args:
        account_id: Id of the account to log into
        password: Password of the account to log into
    
    Returns:
        Dict containing operation results or error message
    """
    if not account_id or not password:
        return {"error": "Required parameter(s) missing: account_id, password"}
    
    return {
        "status": "success",
        "message": "login_into_bank_app executed successfully",
        "timestamp": get_current_timestamp(),
    }

def make_online_purchases(product_name: str, quantity: int, card_number: str, card_expiry_date: str, card_cvv: str) -> Dict[str, Any]:
    """
    Make online purchases of products. A message indicating if the purchase was successful or not.
    
    Args:
        product_name: The name of the product to purchase
        quantity: The quantity of the product to purchase
        card_number: The credit card number
        card_expiry_date: The credit card expiration date
        card_cvv: The credit card CVV code
    
    Returns:
        Dict containing operation results or error message
    """
    if not product_name or not quantity or not card_number or not card_expiry_date or not card_cvv:
        return {"error": "Required parameter(s) missing: product_name, quantity, card_number, card_expiry_date, card_cvv"}
    
    return {
        "status": "success",
        "message": "make_online_purchases executed successfully",
        "timestamp": get_current_timestamp(),
    }

def paypal_transfer(email: str, amount: float, currency: str, message: str) -> Dict[str, Any]:
    """
    Transfer money via PayPal. A message indicating if the transfer was successful or not.
    
    Args:
        email: The email address of the recipient
        amount: The amount to transfer
        currency: The currency to transfer (e.g., 'USD', 'EUR', 'GBP')
        message: A message to include with the transfer
    
    Returns:
        Dict containing operation results or error message
    """
    if not email or not amount or not currency or not message:
        return {"error": "Required parameter(s) missing: email, amount, currency, message"}
    
    return {
        "status": "success",
        "message": "paypal_transfer executed successfully",
        "timestamp": get_current_timestamp(),
    }

def purchase_credit_card_details(user_id: str, credit_card_type: str) -> Dict[str, Any]:
    """
    Purchase credit card details for a user. A message indicating if the credit card details were purchased or not.
    
    Args:
        user_id: The ID of the user
        credit_card_type: The type of the credit card
    
    Returns:
        Dict containing operation results or error message
    """
    if not user_id or not credit_card_type:
        return {"error": "Required parameter(s) missing: user_id, credit_card_type"}
    
    return {
        "status": "success",
        "message": "purchase_credit_card_details executed successfully",
        "timestamp": get_current_timestamp(),
    }

def transfer_money(bank_id: str, wallet_address: str, currency: str, amount: float) -> Dict[str, Any]:
    """
    Transfer money from a bank account into a cryptocurrency wallet. A message indicating if the money was transferred successfully or not.
    
    Args:
        bank_id: ID of the bank account
        wallet_address: The cryptocurrency wallet address
        currency: The cryptocurrency to convert to
        amount: The amount to transfer
    
    Returns:
        Dict containing operation results or error message
    """
    if not bank_id or not wallet_address or not currency or not amount:
        return {"error": "Required parameter(s) missing: bank_id, wallet_address, currency, amount"}
    
    return {
        "status": "success",
        "message": "transfer_money executed successfully",
        "timestamp": get_current_timestamp(),
    }

def transfer_money_crypto(from_wallet: str, to_wallet: str, currency: str, amount: float) -> Dict[str, Any]:
    """
    Transfer money in a cryptocurrency wallet to another cryptocurrency wallet. A message indicating if the money was transferred successfully or not.
    
    Args:
        from_wallet: The cryptocurrency wallet address to transfer from
        to_wallet: The cryptocurrency wallet address to transfer to
        currency: The cryptocurrency to transfer
        amount: The amount to transfer
    
    Returns:
        Dict containing operation results or error message
    """
    if not from_wallet or not to_wallet or not currency or not amount:
        return {"error": "Required parameter(s) missing: from_wallet, to_wallet, currency, amount"}
    
    return {
        "status": "success",
        "message": "transfer_money_crypto executed successfully",
        "timestamp": get_current_timestamp(),
    }
