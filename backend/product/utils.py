import random
from typing import Tuple


def generate_product_code() -> str:
    """
    Generate a random 5-digit product code.
    
    Returns:
        str: A 5-digit product code.
    """
    return str(random.randint(10000, 99999))  # 5 haneli rastgele sayı

def calculate_check_digit(code: str) -> int:
    """
    Calculate the check digit for UPC or EAN-13 codes.
    
    Args:
        code (str): The first 11 (UPC) or 12 (EAN-13) digits as a string.
        
    Returns:
        int: The calculated check digit.
    """

    odd_sum = sum(int(code[i]) for i in range(0, len(code), 2))
    even_sum = sum(int(code[i]) for i in range(1, len(code), 2)) * 3
    total_sum = odd_sum + even_sum

    check_digit = (10 - (total_sum % 10)) % 10
    
    return check_digit

def generate_upc_ean13(product_code: str, producer_code: str = '123456', country_code: str = '869') -> Tuple[str, str]:
    """
    Generate UPC and EAN-13 codes based on producer and product codes.
    
    Args:
        producer_code (str): The producer code (6 digits for UPC, 4-7 digits for EAN-13).
        product_code (str): The product code (5 digits).
        country_code (str): The country code (default is '869' for Turkey).
        
    Returns:
        Tuple[str, str]: A tuple containing the generated UPC and EAN-13 codes.
    """
    upc_code_without_check = f"{producer_code}{product_code}"
    ean13_code_without_check = f"{country_code}{producer_code}{product_code[:3]}"
    
    # Calculate check digit
    upc_check_digit = calculate_check_digit(upc_code_without_check)
    ean13_check_digit = calculate_check_digit(ean13_code_without_check)
    
    upc_code = f"{upc_code_without_check}{upc_check_digit}"
    ean13_code = f"{ean13_code_without_check}{ean13_check_digit}"
    
    return upc_code, ean13_code

def generate_upc_code(product_code:str, producer_code: str = '123456') -> str:
    """
    Generate UPC code based on producer and product codes.

    Args:
        producer_code (str): The producer code (6 digits).
        product_code (str): The product code (5 digits).

    Returns:
        str: A 12-digit UPC code.
    """
    upc_code_without_check = f"{producer_code}{product_code}"
    upc_check_digit = calculate_check_digit(upc_code_without_check)
    upc_code = f"{upc_code_without_check}{upc_check_digit}"

    return upc_code

def generate_ean13_code(product_code: str, producer_code: str = '123456', country_code: str = '869') -> str:
    """
    Generate EAN-13 code based on producer and product codes.

    Args:
        producer_code (str): The producer code (4-7 digits).
        product_code (str): The product code (5 digits).
        country_code (str): The country code (default is '869' for Turkey).
    
    Returns:
        str: A 13-digit EAN-13 code.
    """
    ean13_code_without_check = f"{country_code}{producer_code}{product_code[:3]}"
    ean13_check_digit = calculate_check_digit(ean13_code_without_check)
    ean13_code = f"{ean13_code_without_check}{ean13_check_digit}"

    return ean13_code

# upc, ean13 = generate_upc_ean13("78901")
# upc, ean13 = generate_upc_ean13("78901", "654321")