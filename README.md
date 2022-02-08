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

I used geopy to find the coordinates of the place:

```python
from geopy.geocoders import Nominatim

loc = Nominatim(user_agent = "app_name").geocode(place_str)
```

Then the first function returns a list of lists, which contains the string of fims, year it was filmed, some additional info about it and a tupple of coorditanes of the place it was filmed at

```bash
[["#15SecondScare (2015) {It's Me Jessica (#1.5)}, Coventry, West Midlands, England, UK,", (52.4081812, -1.510477)]...]
```

## Creating a map

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
