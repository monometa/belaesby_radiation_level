# Radiation situation around Belarusian NPP

This application is a pipeline for automating the collection and storage of data on the radiation situation in the sanitary protection zone and the observation zone of the Astravets Nuclear Power Plan. 

The data is collected from https://belaes.by and stored in a file [```radiation.csv```](./radiation.csv). Information about the situation is updated on the website belaes.by every half an hour.

The technical part is implemented by parsing data with a python script [parse_svg_data.py](./parse_svg_data.py) and a schedule using GitHub actions.