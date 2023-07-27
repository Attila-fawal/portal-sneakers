import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_sneakers.settings')
django.setup()

from products.models import Size

# Men sizes
for size in range(40, 47):
    Size.objects.get_or_create(size=size, size_type='M')

# Women sizes
for size in range(36, 42):
    Size.objects.get_or_create(size=size, size_type='W')

# Kids sizes
for size in range(32, 35):
    Size.objects.get_or_create(size=size, size_type='K')
