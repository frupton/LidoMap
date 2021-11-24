import folium
import webbrowser
import os
import pandas as pd
import sounds


def get_data():
    name, lats, longs = ([] for i in range(3))
    raw_data = pd.read_csv('Lidos.csv')
    # num_points = len(raw_data)

    lats += list(raw_data['latitude'])
    longs += list(raw_data['longitude'])
    name += list(raw_data['name'])

    return name, lats, longs


def get_swim_list(file):

    done = []
    raw_data = pd.read_csv(file)
    done += list(raw_data['name'])
    return done


def folium_func(lats, longs, name, types_list):
    """
        Adds route and markers onto a OSM map using Folium
            Parameters:
                lats (array) :  array of latitude points
                longs (array):  array of longitude points
                name (array of string values) :  Name will appear on each points popup marker
                types_list (array of string values): What type of icon will be displayes
            Returns:
                Saves map.html to the folder you are working in
        """

    # dictionary with keys = point type, values = icon
    icons_dict = {'Lido': 'tint', 'done': 'check'}
    colour_dict = {'Lido': 'blue', 'done': 'green'}

    # Folium Stuff - Make an empty map
    m = folium.Map(location=[54.5781, -3.4360], zoom_start=6, tiles='Mapbox Bright')

    #   add marker one by one on the map: makes it easier when we have multiple places of interest
    for i in range(0, len(name)):
        if types_list[i] != 'no':
            folium.Marker(
                location=[lats[i], longs[i]],
                popup=name[i], icon=folium.Icon(color=colour_dict[types_list[i]], icon=icons_dict[types_list[i]], prefix='fa')).add_to(m)

    # Saves the map to folder
    m.save("map.html")
    message = 'Folium route saved'
    return message


if __name__ == "__main__":
    swum_file = 'lidos_swam.csv'
    show = 'both'
    # options are 'done' to show the ones on the swam list, 'all' to show all lidos, 'both'

    type = []
    name, lats, longs = get_data()
    swum = get_swim_list(swum_file)

    if show == 'all':
        for i in range(len(name)):
            type.append('Lido')
    elif show == 'done':
        for i in range(len(name)):
            if name[i] in swum:
                type.append('done')
            else:
                type.append('no')
    elif show == 'both':
        for i in range(len(name)):
            if name[i] in swum:
                type.append('done')
            else:
                type.append('Lido')

    # Calling folium_func
    x = folium_func(lats, longs, name, type)
    print(x)


filename = 'file:///' + os.getcwd() + '/' + 'map.html'
webbrowser.open_new_tab(filename)


sounds.ding()

