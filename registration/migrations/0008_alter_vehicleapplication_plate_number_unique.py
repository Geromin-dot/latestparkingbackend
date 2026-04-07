from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0007_alter_vehicleapplication_sticker_id_unique'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicleapplication',
            name='plate_number',
            field=models.TextField(unique=True),
        ),
    ]