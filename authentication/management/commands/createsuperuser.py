from django.contrib.auth.management.commands.createsuperuser import Command as CreateSuperUserCommand
from django.core.management import CommandError

class Command(CreateSuperUserCommand):
    def add_arguments(self, parser):
        # Add additional arguments if needed
        parser.add_argument('--phone_number', type=str, help='Phone number for the superuser')
        super().add_arguments(parser)
    
    def handle(self, *args, **options):
        phone_number = options.get('phone_number')

        if not phone_number:
            raise CommandError('You must provide a phone number using the --phone_number option.')

        # Proceed with superuser creation
        super().handle(*args, **options)

        # After the superuser is created, you can store or validate the phone number
        print(f"Superuser created with phone number: {phone_number}")
