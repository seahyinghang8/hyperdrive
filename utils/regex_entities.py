import re
REGEX_ENTITIES = {
    'SSN': re.compile(r'^\d{3}-\d{2}-\d{4}$'),
    'EIN': re.compile(r'^[0-9]\d?-\d{7}$'),
    'DOLLAR_AMOUNT': re.compile(
        r'^\$?([1-9]{1}[0-9]{0,2}(\,[0-9]{3})*(\.[0-9]{0,2})?|[1-9]{1}[0-9]{0,}(\.[0-9]{0,2})?|0(\.[0-9]{0,2})?|(\.[0-9]{1,2})?)$'),
}