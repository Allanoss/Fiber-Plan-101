from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages


from .models  import Item, Plot, Coordinate
from .forms import PointsForm, ItemForm, PlotForm, PlotConnectForm, QuoteItemsFrom
from .utility import plot as plot_network, item_count


# Create your views here.
@login_required
def index(request):
    plots = Plot.objects.filter(~Q(name='settings'))

    context = {'plots': plots}
    return render(request, 'plotter/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        name = request.POST['name']
        plot = Plot(name=name)
        plot.save()
        return redirect(reverse('plotter-populate', args=[plot.id]))

@login_required
def populate(request, id):
    plot = get_object_or_404(Plot, pk=id)
    if plot.pole_separation:
        form = PlotForm(instance=plot)
    else:
        settings_plot = Plot.objects.filter(name='settings').first()
        if settings_plot:
            form = PlotForm(instance=settings_plot)
        else:
            form = PlotForm(instance=plot)
        
    if request.method == 'POST':
        name = request.POST['name']
        coordinates = request.POST['coordinates']
        coordinates = Coordinate(plot=plot, name=name, coordinates=coordinates)
        coordinates.save()

    context = {
        'plot': plot,
        'coordinates': plot.coordinate_set.all(),
        'form': form,
        'title': f'Plot N0# {plot.id}'
        }
    return render(request, 'plotter/populate.html', context)

@login_required
def more_settings(request, id):
    plot = get_object_or_404(Plot, pk=id)
    form = PlotConnectForm(instance=plot)
        
    if request.method == 'POST':
        form = PlotConnectForm(request.POST, instance=plot)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings saved successfully')
            return redirect(reverse('plotter-more_settings', args=[plot.id]))

    context = {
        'plot': plot,
        'form': form,
        'title': f'Plot N0# {plot.id}'
        }
    return render(request, 'plotter/connect.html', context)

@login_required
def properties(request, id):
    plot = get_object_or_404(Plot, pk=id)
    if request.method == 'POST':
        form = PlotForm(request.POST, instance=plot)
        if form.is_valid():
            form.save()
            messages.success(request, 'Properties saved successfully')
        
        plot_settings = Plot.objects.filter(name='settings').first()
        form_settings = PlotForm(request.POST, instance=plot_settings)
        if form_settings.is_valid():
            form_settings.save()
        return redirect(reverse('plotter-populate', args=[plot.id]))

@login_required
def coordinate_delete(request, id):
    coordinate = get_object_or_404(Coordinate, pk=id)
    plot = coordinate.plot
    coordinate.delete()

    return redirect(reverse('plotter-populate', args=[plot.id]))

@login_required
def plot(request, id):
    plot = get_object_or_404(Plot, pk=id)
    coordinates = plot.coordinate_set.all()
    # ["36.8159, -1.2795", ...] "36.8159, -1.2795" "36.8159" 36.8159
    # ["36.8159, -1.2795", ...] "36.8159, -1.2795" "-1.2795" -1.2795
    # [[36.8159, -1.2795], ...]"
    array_of_names = []
    array_of_array = []
    for coordinate in coordinates:
        x_y = coordinate.coordinates
        x, y = x_y.split(',')
        x_y_array = [float(x), float(y)]
        array_of_array.append(x_y_array)
        array_of_names.append(coordinate.name)

    # points=[[36.8159, -1.2795], [36.8219,-1.2921],[36.8259, -1.2850], [36.8145, -1.2870], [36.8222, -1.2935]]
    points = array_of_array
    names = array_of_names
    map_name = 'media/'+plot.name+'.html'

    set_start = None
    if plot.set_start_point:
        x_y = plot.set_start_point.coordinates # "36.8159, -1.2795"
        x, y = x_y.split(',') # "36.8159" "-1.2795"
        x_y_array = [float(x), float(y)] # [36.8159 -1.2795]
        set_start = x_y_array

    connect_point = None
    if plot.connect_coordinate:
        x_y = plot.connect_coordinate # "36.8159, -1.2795"
        x, y = x_y.split(',') # "36.8159" "-1.2795"
        x_y_array = [float(x), float(y)] # [36.8159 -1.2795]
        connect_point = x_y_array

    MinTot, Start = plot_network(points, names, map_name, set_start, connect_point)

    plot.distance = MinTot
    plot.start = Start
    plot.save()
    
    return redirect(reverse('plotter-network', args=[plot.id]))

@login_required
def quote_item(request, id):
    plot = get_object_or_404(Plot, pk=id)
    form = QuoteItemsFrom(instance=plot)
    if request.method == 'POST':
        form = QuoteItemsFrom(request.POST, instance=plot)
        if form.is_valid():
            form.save()
            return redirect(reverse('plotter-quote_price', args=[plot.id]))

    context = {'form':form}
    return render(request, 'plotter/quote_items.html', context)

@login_required
def quote_price(request, id):
    plot = get_object_or_404(Plot, pk=id)
    poles, fibre_optic, man_holes, hand_holes = item_count(plot)
    
    fibre_optic_price = fibre_optic * plot.fibre_optic.unit_price

    poles_price = 0
    man_hole_price = 0
    hand_hole_price = 0
    support_tangent_price = 0
    olt_price = 0
    onu_price = 0

    onus = plot.coordinate_set.count()

    if plot.pole:
        poles_price = poles * plot.pole.unit_price
    if plot.man_hole:
        man_hole_price = man_holes * plot.man_hole.unit_price
    if plot.hand_hole:
        hand_hole_price = hand_holes * plot.hand_hole.unit_price
    if plot.Support_Tangent:
        support_tangent_price = poles * plot.Support_Tangent.unit_price
    if plot.olt:
        olt_price = plot.olt.unit_price
    if plot.onu:
        onu_price = plot.onu.unit_price * onus
    #tension_clamps_price = poles * plot.others.filter(sku='Tension clamp').first().unit_price
    total = poles_price + fibre_optic_price + man_hole_price + hand_hole_price + support_tangent_price + olt_price + onu_price
   
    context = {
        'plot':plot,
        'fibre_optic_price': fibre_optic_price,
        
        # quanity
        'poles': poles,
        'fibre_optic':fibre_optic,
        'man_holes':man_holes,
        'hand_holes':hand_holes,
        'onu': onus,
        'Support_Tangent':poles,

        # price
        'poles_price': poles_price,
        'man_hole_price': man_hole_price,
        'hand_hole_price': hand_hole_price,
        'support_tangent_price': support_tangent_price,
        'olt_price':  olt_price,
        'onu_price': onu_price,
        'total': total, 
    }

    return render(request, 'plotter/quote_price.html', context)

@login_required
def network(request, id):
    plot = get_object_or_404(Plot, pk=id)
    context = {
        'plot': plot,
    }
    return render(request, 'plotter/network.html', context)

@login_required
def plot_delete(request, id):
    plot = get_object_or_404(Plot, pk=id)
    plot.delete()

    return redirect(reverse('plotter-index'))

# items
@login_required
def item_list(request):
    items = Item.objects.all()
    context = {'items':items}
    return render(request, 'plotter/item/index.html', context)

@login_required
def item_create(request):
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('plotter-item_list'))

    context = {'form': form}
    return render(request, 'plotter/item/create_and_update.html', context)

@login_required
def item_update(request, id):
    item = get_object_or_404(Item, pk=id)
    form = ItemForm(instance=item)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse('plotter-item_list'))

    context = {'form': form}
    return render(request, 'plotter/item/create_and_update.html', context)

@login_required
def item_delete(request, id):
    item = get_object_or_404(Item, pk=id)
    try:
        item.delete()
    except:
        messages.warning(request, 'This action is not allowed')

    return redirect(reverse('plotter-item_list'))