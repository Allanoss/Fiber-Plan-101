from django.db import models

# Create your models here.

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('PL', 'Pole'),
        ('FO', 'Fibre optic'),
        ('DT', 'Duct'),
        ('MH', 'Man hole'),
        ('OL', 'OLT'),
        ('ON', 'ONU'),
        ('HH', 'Hand Hole'),
        ('ST', 'Support Tangent'),
        ('OR', 'Others'),
    ]
    
    sku = models.CharField(max_length=100)
    unit_price = models.FloatField()
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.sku

class Plot(models.Model):
    name = models.CharField(max_length=100)
    start = models.CharField(max_length=100, null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    # items
    pole = models.ForeignKey(Item, related_name='plot_pole', on_delete=models.PROTECT, null=True, blank=True)
    pole_separation = models.FloatField(null=True, blank=True)
    fibre_optic = models.ForeignKey(Item, related_name='plot_fibre', on_delete=models.PROTECT, null=True, blank=True)
    Extra_Fiber_Length_After = models.FloatField(null=True, blank=True)
    Extra_Fiber_Length = models.FloatField(null=True, blank=True)
    duct = models.ForeignKey(Item, related_name='plot_duct', on_delete=models.PROTECT, null=True, blank=True)
    onu = models.ForeignKey(Item, related_name='plot_onu', on_delete=models.PROTECT, null=True, blank=True)
    olt = models.ForeignKey(Item, related_name='plot_olt', on_delete=models.PROTECT, null=True, blank=True)
    man_hole = models.ForeignKey(Item, related_name='plot_man_hole', on_delete=models.PROTECT, null=True, blank=True)
    man_hole_separation = models.FloatField(null=True, blank=True)
    hand_hole = models.ForeignKey(Item, related_name='plot_hand_hole', on_delete=models.PROTECT, null=True, blank=True)
    hand_hole_separation = models.FloatField(null=True, blank=True)
    Support_Tangent = models.ForeignKey(Item, related_name='plot_support_tangent', on_delete=models.PROTECT, null=True, blank=True)
    # others = models.ManyToManyField(Item)
    set_start_point=models.ForeignKey('Coordinate', on_delete=models.SET_NULL, null=True, blank=True, related_name='plot_set_start_point')
    # connect_plot = models.ForeignKey('Plot', on_delete=models.SET_NULL, null=True, blank=True)
    # connect_coordinate = models.ForeignKey('Coordinate', on_delete=models.SET_NULL, null=True, blank=True, related_name='plot_connect_coordinate')
    connect_coordinate = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Coordinate(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    coordinates = models.TextField()

    def __str__(self):
        return f'{self.name} {self.coordinates}'