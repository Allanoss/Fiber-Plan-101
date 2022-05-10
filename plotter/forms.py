from django import forms
from django.forms import ModelForm
from django.db.models import Q

from plotter.models import Coordinate, Plot, Item

class PointsForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    # points = forms.CharField(widget=forms.Textarea)

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['sku', 'unit_price', 'category']

class PlotForm(ModelForm):
    class Meta:
        model = Plot
        fields = ['pole_separation', 'Extra_Fiber_Length_After', 'Extra_Fiber_Length', 'man_hole_separation', 'hand_hole_separation']

class PlotConnectForm(ModelForm):
    class Meta:
        model = Plot
        # fields = ['set_start_point', 'connect_plot', 'connect_coordinate']
        fields = ['set_start_point', 'connect_coordinate']

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.fields['set_start_point'].queryset = Coordinate.objects.filter(plot=self.instance)
        # self.fields['connect_plot'].queryset = Plot.objects.filter(~Q(name='settings'))
        # if self.instance.connect_plot:
        #     self.fields['connect_coordinate'].queryset = Coordinate.objects.filter(plot=self.instance.connect_plot)
        # else:
        #     self.fields['connect_coordinate'].queryset = Coordinate.objects.none()

class QuoteItemsFrom(ModelForm):
    class Meta:
        model = Plot
        fields = ['pole', 'fibre_optic', 'duct', 'man_hole', 'hand_hole', 'Support_Tangent', 'onu', 'olt']

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.fields['pole'].queryset = Item.objects.filter(category='PL')
        self.fields['fibre_optic'].queryset = Item.objects.filter(category='FO')
        self.fields['duct'].queryset = Item.objects.filter(category='DT')
        self.fields['hand_hole'].queryset = Item.objects.filter(category='HH')
        self.fields['Support_Tangent'].queryset = Item.objects.filter(category='ST')
        self.fields['onu'].queryset = Item.objects.filter(category='ON')
        self.fields['olt'].queryset = Item.objects.filter(category='OL')
        # self.fields['others'].queryset = Item.objects.filter(category='OR')