'''Lab 1.2'''
from csv import reader
from re import findall, search
from argparse import ArgumentParser
from folium import FeatureGroup, Map, Marker, IFrame, Icon, Popup, LayerControl
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster
from geopy.distance import geodesic

def get_info():
    '''
    Reads the info entered by user using argparse and returns it ti the main function
    '''
    parser = ArgumentParser()
    parser.add_argument("year", help='Year of the films')
    parser.add_argument("latitude", help='Latitude of your position')
    parser.add_argument("longtitude", help="Longtitude of your position")
    parser.add_argument("url", help="File url to get info from")
    arguments = parser.parse_args()
    return arguments.year, arguments.latitude, \
           arguments.longtitude, arguments.url

def read_fil(path, needed_year):
    '''
    Reads a file in a proper way, avoiding all unnecessary info,
    returns a list with the entered by user year and calculated
    geographic coordinates

    Uses cashe_list to avoid calculating the same coordinate twice
    >>> read_fil('l.list', 2016) #doctest: +ELLIPSIS
    [['#ActorsLife (2016), New York City, New York, USA,',...
    >>> read_fil('l.list', 2010) #doctest: +ELLIPSIS
    [['$#*! My Dad Says (2010), Warner Brothers Burbank Studios...
    '''
    cashe_list = {}
    return_list = []
    with open(path, 'rt', encoding="unicode_escape") as file:
        is_found = False
        for line in reader(file):
            # Checks for a line of ==== where the actual file starts
            try:
                if "=" in line[0]:
                    is_found = True
                    continue
                if is_found is False:
                    continue
            except:
                continue

            # checks the year needed
            try:
                year = int(findall("[(]{1}\d\d\d\d[)]{1}", line[0])[0][1:-1])
                if year != needed_year:
                    continue
            except IndexError:
                continue

            # parcing all necessary info
            text = ""
            all_places = []
            split_line = line[0].split("\t")
            try:
                if "(" not in split_line[-1]:
                    city = split_line[-1]
                else:
                    city = split_line[-2]
            except:
                continue
            if city == '':
                continue
            all_places.append(city)
            for i in range(1, len(line)):
                all_places.append(line[i])

            text += split_line[0] + ", "

            sup_text = ''
            u_check = 0
            two = False
            try:
                if '\t' in all_places[-2]:
                    u_check = 2
                    two = True
                    country = all_places[-2].split("\t")[0]
                    sup_text += country
                    sup_text += "; additional info: "
                    sup_text += all_places[-2].split("\t")[1]
                    sup_text += ","
                    sup_text += all_places[-1]
                    all_places.remove(all_places[-2])
                    all_places.remove(all_places[-1])
                    all_places.append(country)
            except IndexError:
                pass
            if "\t" in all_places[-1]:
                u_check = 2 if two else 1
                country = all_places[-1].split("\t")[0]
                sup_text += country
                sup_text += "; additional info: "
                sup_text += all_places[-1].split("\t")[1][1:-1]
                all_places.remove(all_places[-1])
                all_places.append(country)
            for i in range(len(all_places) - u_check):
                text += all_places[i]
                text += ","
            text += sup_text

            # if we already calculated coordinates, use calculated ones
            # don't calculate again
            loc = None
            i = 0

            try:
                while loc is None:
                    place_str = all_places[i]
                    for j in range(1 + i, len(all_places)):
                        place_str += ', ' + all_places[j]
                    if place_str in cashe_list:
                        loc = cashe_list[place_str]
                        break
                    loc = Nominatim(user_agent = "app_name").geocode(place_str)
                    if loc is not None:
                        cashe_list[place_str] = loc
                        break
                    all_places = place_str.split(",")
                    i += 1
            except IndexError:
                continue

            return_list.append([text, (loc.latitude, loc.longitude)])
    return return_list

def calculate_top_ten(working_films, latitude, longtitude):
    '''
    Calculates the ten closest films to a location entered
    >>> calculate_top_ten([['#ActorsLife (2016)', (40.7127281, -74.0060152)], \
    ['#Fuga (2016)', (-22.9979553, -43.37311472822825)], \
    ['#KillTorrey (2016)', (34.1816482, -118.3258554)], \
    ['#LoveMyRoomie (2016)', (40.7127281, -74.0060152)], \
    ['#LoveMyRoomie (2016) ', (40.6526006, -73.9497211)], \
    ['#MyCurrentSituation: Atlanta (2016)', (33.7489924, -84.3902644)], \
    ['#MyCurrentSituation: Atlanta (2016)', (35.1490215, -90.0516285)], \
    ['#SmurTv (2016)', (37.270973, -79.9414313)], \
    ['#SmurTv (2016)', (35.2272086, -80.8430827)], \
    ['#SmurTv (2016)', (33.7489924, -84.3902644)]], -40, 70) #doctest: +ELLIPSIS
    {(-22.9979553, -43.37311472822825): [10207.976489480665, '#Fuga (2016)'], (40.6526006, -73.9497211):...
    >>> calculate_top_ten([['#ActorsLife (2016)', (40.7127281, -74.0060152)], \
    ['#Fuga (2016)', (-22.9979553, -43.37311472822825)], \
    ['#KillTorrey (2016)', (34.1816482, -118.3258554)], \
    ['#LoveMyRoomie (2016)', (40.7127281, -74.0060152)], \
    ['#LoveMyRoomie (2016) ', (40.6526006, -73.9497211)], \
    ['#MyCurrentSituation: Atlanta (2016)', (33.7489924, -84.3902644)], \
    ['#MyCurrentSituation: Atlanta (2016)', (35.1490215, -90.0516285)], \
    ['#SmurTv (2016)', (37.270973, -79.9414313)], \
    ['#SmurTv (2016)', (35.2272086, -80.8430827)], \
    ['#SmurTv (2016)', (33.7489924, -84.3902644)]], -70, 30) #doctest: +ELLIPSIS
    {(-22.9979553, -43.37311472822825): [6988.995927487033, '#Fuga (2016)'], (33.7489924, -84.3902644):...
    '''
    return_dict = {}

    # finds distance, sorts list from closest to farthest and gets ten closest
    for place in working_films:
        point_1 = str(latitude) + ',' + str(longtitude)
        point_2 = str(place[1][0]) + ',' + str(place[1][1])
        distance = geodesic(point_1, point_2).kilometers
        place.append(distance)
    working_films.sort(key = lambda x: x[-1])
    working_films = working_films[:10]

    # combines films that were shot in the same place into one element
    for elem in working_films:
        if elem[1] in return_dict.keys():
            if elem[0] not in return_dict[elem[1]][1]:
                return_dict[elem[1]][1] += ' and '
                return_dict[elem[1]][1] += elem[0]
        else:
            return_dict[elem[1]] = [elem[2], elem[0]]

    return return_dict

def buid_map(to_place_points, latitude, longtitude):
    '''
    Builds a map using the coordinates given by user
    Places Markers of 10 closest films to that point
    '''
    main_map = Map(location = [latitude, longtitude], zoom_start = 3, control_scale = True)

    # creating a list with coordinates for marker cluster
    locations = [[place[0], place[1]] for place in to_place_points]

    # creating groups for markers and for a marker cluster
    markers_group = FeatureGroup(name = "Markers of films", show = False)
    iframe_group = FeatureGroup(name = "Full info about films", show = False)
    marker_cluster = MarkerCluster(locations, name = "Marker Cluster")
    main_map.add_child(markers_group)
    main_map.add_child(iframe_group)
    main_map.add_child(marker_cluster)

    for place in to_place_points:
        text = to_place_points[place][1]
        small_text = ''

        # making a small marker, cutting original full text
        numbers_poss = search('[(]{1}\d\d\d\d[)]{1}', text)
        text_to_add = text[:numbers_poss.end()]
        text = text[numbers_poss.end():]
        small_text += text_to_add
        while True:
            numbers_poss = search('[(]{1}\d\d\d\d[)]{1}', text)
            if numbers_poss is None:
                break
            and_find = text.find(' and ')
            if and_find == -1 or and_find > numbers_poss.end():
                continue
            text_to_add = text[and_find:numbers_poss.end()]
            text = text[numbers_poss.end() - 1:]
            if text_to_add[5:] in small_text:
                continue
            small_text += text_to_add

        # Creating the markers
        iframe_small = (IFrame(small_text, width = 75, height = 125))
        iframe_big = (IFrame(to_place_points[place][1], width = 300, height = 100))
        markers_group.add_child(Marker(location = [place[0], place[1]], popup = \
                                Popup(iframe_small), icon = Icon(color = 'green')))
        iframe_group.add_child(Marker(location = [place[0], place[1]], popup = \
                                Popup(iframe_big), icon = Icon(color = 'red')))

    main_map.add_child(LayerControl())
    main_map.save('map.html')

def main():
    '''
    Runs the whole program
    '''
    year, latitude, longtitude, url = get_info()
    latitude = int(latitude)
    longtitude = int(longtitude)
    year = int(year)

    dictinary = read_fil(url, year)
    to_place_points = calculate_top_ten(dictinary, latitude, longtitude)
    buid_map(to_place_points, latitude, longtitude)

main()
