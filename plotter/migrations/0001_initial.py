# Generated by Django 4.0.4 on 2022-05-24 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('coordinates', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=100)),
                ('unit_price', models.FloatField()),
                ('category', models.CharField(choices=[('PL', 'Pole'), ('FO', 'Fibre optic'), ('DT', 'Duct'), ('MH', 'Man hole'), ('OL', 'OLT'), ('ON', 'ONU'), ('HH', 'Hand Hole'), ('ST', 'Support Tangent'), ('OR', 'Others')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start', models.CharField(blank=True, max_length=100, null=True)),
                ('distance', models.FloatField(blank=True, null=True)),
                ('pole_separation', models.FloatField(blank=True, null=True)),
                ('Extra_Fiber_Length_After', models.FloatField(blank=True, null=True)),
                ('Extra_Fiber_Length', models.FloatField(blank=True, null=True)),
                ('man_hole_separation', models.FloatField(blank=True, null=True)),
                ('hand_hole_separation', models.FloatField(blank=True, null=True)),
                ('connect_coordinate', models.TextField(blank=True, null=True)),
                ('Support_Tangent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='plot_support_tangent', to='plotter.item')),
                ('duct', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='plot_duct', to='plotter.item')),
                ('fibre_optic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='plot_fibre', to='plotter.item')),
                ('hand_hole', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='plot_hand_hole', to='plotter.item')),
                ('man_hole', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='plot_man_hole', to='plotter.item')),
                ('olt', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='plot_olt', to='plotter.item')),
                ('onu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='plot_onu', to='plotter.item')),
                ('pole', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='plot_pole', to='plotter.item')),
                ('set_start_point', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plot_set_start_point', to='plotter.coordinate')),
            ],
        ),
        migrations.AddField(
            model_name='coordinate',
            name='plot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plotter.plot'),
        ),
    ]
