# The web-map project

The main goal was to create a mobule that generates a HTML file, which contains a map with at least three different layers. The user enteres a year, coordinates of the location(films are found using it) and a file where to get information from. The programm calculates ten closest filming possitions and makes Markers out of it

# Problems I dealt with

## Reading a file

At first, I used a function with argparcing to get the info user entered, and returned four variables:

```python
def get_info():
    parser = ArgumentParser()
    parser.add_argument("year", help='Year of the films')
    parser.add_argument("latitude", help='Latitude of your position')
    parser.add_argument("longtitude", help="Longtitude of your position")
    parser.add_argument("url", help="File url to get info from")
    arguments = parser.parse_args()
    return arguments.year, arguments.latitude, arguments.longtitude, arguments.url
``` 

Then, using the variables, I read the file line by line, user regular expressions to get the year the film was created:

```python
year = int(findall("[(]{1}\d\d\d\d[)]{1}", line[0])[0][1:-1])
```

I did it to choose only the places of the year we need to display in order to not find coordinates of the places of different year, this made the programm faster as finding coordinates of one place takes some time

## Calculating distance and getting the ten films 

I used geopy.geocoders to find the coordinates of the place:

```python
from geopy.geocoders import Nominatim

loc = Nominatim(user_agent = "app_name").geocode(place_str)
```

Then the first function returns a list of lists, which contains the string of fims, year it was filmed, some additional info about it and a tupple of coorditanes of the place it was filmed at

```bash
[["#15SecondScare (2015) {It's Me Jessica (#1.5)}, Coventry, West Midlands, England, UK", (52.4081812, -1.510477)]...]
```

Using geopy.distance I calculated a distance between two places, then added it as a new allament to already existing lish and sorted it using lambda function, and returned ten closest places of filming:

```python
for place in working_films:
    distance = geodesic(point_1, point_2).kilometers
    place.append(distance)
working_films.sort(key = lambda x: x[-1])
working_films = working_films[:11]
```

When the coordinates of places match, I unite them into one element using ' and '

## Creating a map

I used folium to create a map

At first, a main map was created, where the start coordinates were the ones user entered:

```python
main_map = Map(location = [latitude, longtitude], zoom_start = 3, control_scale = True)
```

Then I created three additional layers: a layer of markers that contain only information about what film was filmed there; a layer that contains full info about a film; and a marker cluster layer. By default only marker cluster layer displays. I used IFrame for both first and second layers:

```python
markers_group = FeatureGroup(name = "Markers of films", show = False)
iframe_group = FeatureGroup(name = "Full info about films", show = False)
marker_cluster = MarkerCluster(locations, name = "Marker Cluster")
```

```python
iframe_small = (IFrame(small_text, width = 75, height = 125))
iframe_big = (IFrame(to_place_points[place][1], width = 300, height = 100))
markers_group.add_child(Marker(location = [place[0], place[1]], popup = Popup(iframe_small), icon = Icon(color = 'green')))
iframe_group.add_child(Marker(location = [place[0], place[1]], popup = Popup(iframe_big), icon = Icon(color = 'red')))
```

In the end, a one line of code generates everything into one map, named "map.html":

```python
main_map.save('map.html')
```

# Conclusion

I ran all my function using main function

```python
def main():
    year, latitude, longtitude, url = get_info()
    latitude = int(latitude)
    longtitude = int(longtitude)
    year = int(year)

    dictinary = read_fil(url, year)
    to_place_points = calculate_top_ten(dictinary, latitude, longtitude)
    buid_map(to_place_points, latitude, longtitude)

main()
```

After all, map generates properly and all the layers do so too
