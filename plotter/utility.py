
import openrouteservice as ors
import folium
import math

from plotter.models import Coordinate

Client = ors.Client(key='5b3ce3597851110001cf624820c44dd22f3c4a128773998371409a6f')
# points=[[36.8159, -1.2795], [36.8219,-1.2921],[36.8259, -1.2850], [36.8145, -1.2870], [36.8222, -1.2935]]

def ors_route(coordinates, output='map'):
    route=Client.directions(coordinates=coordinates, 
                            profile='foot-walking',
                            optimized= False,
                            preference='shortest',
                            continue_straight=True,                        
                            format='geojson')
    if(output == 'map'):
        return route
        
    if(output == 'distance'):
        return route['features'][0]['properties']['segments'][0]['distance']

def find_start(points, connect_point):
    MinTot=999999999
    Start=list()
    for i in points: 
        Tdistance=0
        for y in points:
            now=[i,y]
            distance=ors_route(now, 'distance')
            Tdistance+=distance
            
        print(Tdistance) 
        if MinTot>Tdistance:
            MinTot=Tdistance
            Start=i
            #name_min=names[i]
    
    # Adding the distance between the start and connect point
    if connect_point:
        now=[Start, connect_point]
        distance=ors_route(now, 'distance')
        MinTot += distance

    return MinTot, Start


def min_tot_for_set_point(set_start, points, connect_point=None):
    Tdistance = 0
    for y in points:
        now=[set_start, y]
        distance=ors_route(now, 'distance')
        Tdistance+=distance

    if connect_point:
        now=[set_start, connect_point]
        distance=ors_route(now, 'distance')
        Tdistance+=distance

    return Tdistance, set_start

# def connect_integration(connect_point, points):
#     if set_start:
#         MinTot, Start = min_tot_for_set_point(set_start, points)
#     else:
#         MinTot, Start = find_start(points)   
#     integrate_distance = ors_route(connect_point, Start)

#     return integrate_distance

# SUSPENDED
# def Max_Tot(points):     #Point to provide alternative network link
#     MaxTot=0
#     Start=list()
#     for i in points: 
#         Tdistance=0
#         for y in points:
#             now=[i,y]
#             distance=ors_route(now, 'distance')
#             Tdistance+=distance
            
#         print(Tdistance) 
#         if MaxTot<Tdistance:
#             MaxTot=Tdistance
#             Altpoint=i
    
#     connect1 = [Altpoint, connect_point]
#     Altdistance1 = ors_route(connect1, 'distance') 
#     connect2 = [Altpoint, Start]
#     Altdistance2 = ors_route (connect2)
#     Altdistance = Altdistance1 + Altdistance2

    # return Altpoint, Altdistance  

def plot(points, names, map_name, set_start=None, connect_point=None):
    if set_start:
        MinTot, Start = min_tot_for_set_point(set_start, points, connect_point)
    else:
        MinTot, Start = find_start(points, connect_point)

    # Start=points[0]
    my_directions=folium.Map(location=[ Start[1], Start[0]], zoom_start=14)  
    for i in range(len(points)):
        
        now=[Start,points[i]]
        route = ors_route(now)
        folium.GeoJson(route, name='route').add_to(my_directions)

        folium.Marker(
            location=[points[i][1], points[i][0]],
            tooltip = names[i],
            icon=folium.Icon(icon="home"),
        ).add_to(my_directions)

    # SUSPENDED
    # connect_route=[Start, connect_point]
    # route = ors_route(connect_route)
    # folium.GeoJson(route, name='route').add_to(my_directions)

    # SUSPENDED
    # Altroute = [connect_point, Altpoint,Start]
    # route = ors_route(Altroute)
    # folium.GeoJson(route, name='route').add_to(my_directions)

    if connect_point:
        now=[Start, connect_point]
        route = ors_route(now)
        folium.GeoJson(route, name='route').add_to(my_directions)

        folium.Marker(
            location=[connect_point[1], connect_point[0]],
            tooltip = 'integration point',
            icon=folium.Icon(icon="home"),
        ).add_to(my_directions)

    folium.Marker(
            location=[Start[1], Start[0]],
            tooltip = 'Build Cabinet',
            icon=folium.Icon(icon="down", color='lightgreen'),
        ).add_to(my_directions)

    # SUSPENDED
    # folium.Marker(
    #         location=[connect_point[1], connect_point[0]],
    #         tooltip = 'Point of Network Integration',
    #         icon=folium.Icon(icon="down"),
    #     ).add_to(my_directions)    
    # # folium.LayerControl().add_to(my_directions)

    # SUSPENDED
    # folium.Marker(
    #         location=[Altpoint[1], Altpoint[0]],
    #         tooltip = 'Alternative Route Point',
    #         icon=folium.Icon(icon='down', color='lightgreen'),
    #     ).add_to(my_directions) 


    my_directions.save(map_name)
    #print (name_min)

    return MinTot, Start


def item_count(plot):

    total_fibre_excess = math.ceil(plot.distance / plot.Extra_Fiber_Length_After) *  plot.Extra_Fiber_Length
    
    poles = math.ceil(plot.distance / plot.pole_separation) + 1 
    fibre_optic = plot.distance + total_fibre_excess
    man_holes = math.floor(plot.distance / plot.man_hole_separation) + 1
    hand_holes = math.floor(plot.distance / plot.hand_hole_separation)
    

    return poles, fibre_optic, man_holes, hand_holes

