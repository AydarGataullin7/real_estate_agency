from django.db import migrations


def transfer_owners(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')

    for flat in Flat.objects.all().iterator():
        Owner.objects.get_or_create(
            name=flat.owner,
            defaults={
                'phonenumber': flat.owners_phonenumber,
                'pure_phone': flat.owner_pure_phone,
            }
        )


def reverse_transfer(apps, schema_editor):
    Owner = apps.get_model('property', 'Owner')
    Owner.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0011_owner_owner_pure_phone_owner_owners_phonenumber'),
    ]

    operations = [
        migrations.RunPython(transfer_owners, reverse_transfer),
    ]
