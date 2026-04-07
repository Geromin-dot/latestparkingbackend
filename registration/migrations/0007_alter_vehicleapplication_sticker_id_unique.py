from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_parkingreservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicleapplication',
            name='sticker_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]