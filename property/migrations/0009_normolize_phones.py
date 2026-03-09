from django.db import migrations
import phonenumbers


def normalize_phone_numbers(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')

    for flat in Flat.objects.all():
        raw_phone = flat.owners_phonenumber
        if raw_phone:
            try:
                parsed = phonenumbers.parse(raw_phone, 'RU')

                if phonenumbers.is_valid_number(parsed):
                    normalized = phonenumbers.format_number(
                        parsed,
                        phonenumbers.PhoneNumberFormat.E164
                    )
                    flat.owner_pure_phone = normalized
                else:
                    flat.owner_pure_phone = None
            except phonenumbers.NumberParseException:
                flat.owner_pure_phone = None
        else:
            flat.owner_pure_phone = None

        flat.save()


def reverse_func(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    for flat in Flat.objects.all():
        flat.owner_pure_phone = None
        flat.save()


class Migration(migrations.Migration):
    dependencies = [
        ('property', '0008_flat_owner_pure_phone'),
    ]

    operations = [
        migrations.RunPython(normalize_phone_numbers, reverse_func),
    ]
