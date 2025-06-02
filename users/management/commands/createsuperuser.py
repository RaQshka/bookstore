from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from BookStore.models import City


class Command(createsuperuser.Command):
    help = 'Create a superuser with a required City field'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--city',
            dest='city_id',
            type=int,
            help='ID of the city to assign to the superuser',
        )

    def handle(self, *args, **options):
        city_id = options.get('city_id')

        # If city_id is not provided, prompt for it
        if not city_id:
            try:
                # List available cities
                cities = City.objects.all()
                if not cities.exists():
                    raise CommandError('No cities exist in the database. Please create at least one city first.')

                self.stdout.write('Available cities:')
                for city in cities:
                    self.stdout.write(f'ID: {city.id}, Name: {city.name}')

                city_id = self.get_input_data('City ID', None)
                if not city_id:
                    raise CommandError('City ID is required.')

                city_id = int(city_id)
                if not City.objects.filter(id=city_id).exists():
                    raise CommandError(f'City with ID {city_id} does not exist.')
            except ValueError:
                raise CommandError('City ID must be a valid integer.')

        options['city'] = city_id
        super().handle(*args, **options)

    def get_input_data(self, field_name, default=None):
        """Prompt for input and return the entered value."""
        prompt = f'Enter {field_name}'
        if default is not None:
            prompt += f' [{default}]'
        prompt += ': '
        return input(prompt).strip() or default

    def create_user(self, username, email, password, **extra_fields):
        """Override to include city in user creation."""
        city_id = extra_fields.pop('city', None)
        if city_id:
            try:
                city = City.objects.get(id=city_id)
            except City.DoesNotExist:
                raise CommandError(f'City with ID {city_id} does not exist.')
        else:
            raise CommandError('City is required.')

        extra_fields['city'] = city
        return super().create_user(username, email, password, **extra_fields)