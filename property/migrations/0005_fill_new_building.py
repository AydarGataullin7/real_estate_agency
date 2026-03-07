from django.db import migrations


def fill_new_building(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')

    for flat in Flat.objects.all():
        if flat.construction_year:
            if flat.construction_year >= 2015:
                flat.new_building = True
            else:
                flat.new_building = False
            flat.save()


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_flat_new_building'),
    ]

    operations = [
        migrations.RunPython(fill_new_building),
    ]
