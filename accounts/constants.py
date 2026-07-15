COUNTRY_CHOICES = [
    ("UG", "Uganda"),
    ("KE", "Kenya"),
    ("TZ", "Tanzania"),
    ("NG", "Nigeria"),
    ("GH", "Ghana"),
    ("OTHER", "Other"),
]

COUNTRY_CURRENCY = {
    "UG": "UGX",
    "KE": "KES",
    "TZ": "TZS",
    "NG": "NGN",
    "GH": "GHS",
    "OTHER": "USD",
}


def get_currency_for_country(country_code):
    return COUNTRY_CURRENCY.get(country_code, "USD")