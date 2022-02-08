# The web-map project

The main goal was to create a mobule that generates a HTML file, which contains a map with at least three different layers. The user enteres a year, coordinates of the location(films are found using it) and a file where to get information from. The programm calculates ten closest filming possitions and makes Markers out of it

# Problems I dealt with

## Reading a file

At first, I used a function with argparcing to get the info user entered, and returned four variables

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

## Calculating distance and getting the ten films 

## Creating a map

# Conclusion

```python
import math
```

Hello

<h5>Heloooooo</h5>
