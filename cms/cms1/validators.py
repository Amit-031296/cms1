import re

def email_val(email):
    if not re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email):
        return None

def password_val(password):
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$',password):
        return '-'

def pincode_val(pincode):
    if not re.match(r'^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$',pincode):
        return '-'