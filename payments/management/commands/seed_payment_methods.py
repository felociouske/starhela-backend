from django.core.management.base import BaseCommand
from payments.models import PaymentMethod


class Command(BaseCommand):
    help = "Seed payment methods for all supported countries"

    def handle(self, *args, **options):
        payment_methods = [
            {
                "country": "KE",
                "method_name": "M-Pesa",
                "account_name": "Starhela",
                "account_number": "254750518501",
                "payment_link": "",
                "required_amount": 550,
                "instructions": "Send KES 550 to:\n\n1. Go to M-Pesa on your phone\n2. Tap 'Lipa na M-Pesa Online'\n3. Select 'Business' or 'Buy Goods & Services'\n4. Enter our Till/Paybill and amount\n5. Complete the payment\n\nOr click the green button below to initiate auto payment.",
                "is_active": True,
                "display_order": 1,
            },
            {
                "country": "UG",
                "method_name": "Safaricom Transfer",
                "account_name": "Starhela",
                "account_number": "0750518501",
                "payment_link": "",
                "required_amount": 15000,
                "instructions": "Send UGX 15,000 via Safaricom Mobile Money:\n\n1. Dial *165# on your Safaricom line\n2. Select 'Send Money'\n3. Enter receiver: +256750518501\n4. Enter amount: 15,000 UGX\n5. Confirm and complete payment",
                "is_active": True,
                "display_order": 1,
            },
            {
                "country": "TZ",
                "method_name": "Safaricom Transfer",
                "account_name": "Starhela",
                "account_number": "0750518501",
                "payment_link": "",
                "required_amount": 125,
                "instructions": "Send TZS 125 via Safaricom Mobile Money:\n\n1. Dial *165# on your Safaricom line\n2. Select 'Send Money'\n3. Enter receiver: +255750518501\n4. Enter amount: 125 TZS\n5. Confirm and complete payment",
                "is_active": True,
                "display_order": 1,
            },
            {
                "country": "NG",
                "method_name": "Eversend Transfer",
                "account_name": "Starhela",
                "account_number": "starhela@eversend",
                "payment_link": "https://eversend.co",
                "required_amount": 50,
                "instructions": "Send NGN 50 via Eversend:\n\n1. Go to Eversend website or app\n2. Select Nigeria and NGN currency\n3. Enter amount: 50 NGN\n4. Follow the payment process\n5. Get your transaction code and paste it below",
                "is_active": True,
                "display_order": 1,
            },
            {
                "country": "GH",
                "method_name": "Eversend Transfer",
                "account_name": "Starhela",
                "account_number": "starhela@eversend",
                "payment_link": "https://eversend.co",
                "required_amount": 50,
                "instructions": "Send GHS 50 via Eversend:\n\n1. Go to Eversend website or app\n2. Select Ghana and GHS currency\n3. Enter amount: 50 GHS\n4. Follow the payment process\n5. Get your transaction code and paste it below",
                "is_active": True,
                "display_order": 1,
            },
        ]

        for method_data in payment_methods:
            method, created = PaymentMethod.objects.update_or_create(
                country=method_data["country"],
                method_name=method_data["method_name"],
                defaults={
                    "account_name": method_data["account_name"],
                    "account_number": method_data["account_number"],
                    "payment_link": method_data["payment_link"],
                    "required_amount": method_data["required_amount"],
                    "instructions": method_data["instructions"],
                    "is_active": method_data["is_active"],
                    "display_order": method_data["display_order"],
                },
            )
            status = "Created" if created else "Updated"
            self.stdout.write(
                self.style.SUCCESS(f"{status}: {method_data['country']} - {method_data['method_name']}")
            )

        self.stdout.write(
            self.style.SUCCESS("✓ Payment methods seeded successfully!")
        )
