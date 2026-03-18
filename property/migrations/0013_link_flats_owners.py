from django.db import migrations


def link_flats_and_owners(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')

    for flat in Flat.objects.all().iterator():
        if flat.pure_phone:
            try:
                owner = Owner.objects.get(pure_phone=flat.pure_phone)
                owner.flats.add(flat)
                continue
            except Owner.DoesNotExist:
                pass

        if flat.owners_phonenumber:
            try:
                owner = Owner.objects.get(phonenumber=flat.owners_phonenumber)
                owner.flats.add(flat)
                continue
            except Owner.DoesNotExist:
                pass

        try:
            owner = Owner.objects.get(name=flat.owner)
            owner.flats.add(flat)
        except Owner.DoesNotExist:
            pass


def reverse_link(apps, schema_editor):
    Owner = apps.get_model('property', 'Owner')
    for owner in Owner.objects.all().iterator():
        owner.flats.clear()


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0012_transfer_owners'),
    ]

    operations = [
        migrations.RunPython(link_flats_and_owners, reverse_link),
    ]
