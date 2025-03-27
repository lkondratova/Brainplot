# Brainplot

## Overview

The brainplot script is designed to visualize brain templates and areas for various species using data from the Scalable Brain Atlas. It processes input data, generates visualizations, and saves the results in various formats.

## Requirements
Python 3.x

Required libraries: os, importlib, matplotlib, pandas, numpy, PIL

## Installation
Ensure you have the required libraries installed. You can install them using pip:
```
pip install matplotlib pandas numpy pillow
```
## Usage
Initialization:

The script first looks for an auto_input.txt file in the current directory.
If the file exists, it reads the species, templates, and areas from the file.
If the file does not exist, it prompts the user for manual input.

Input Data:

Species: Choose from macaque, mouse, mouse_allen, rat, human, ferret, opossum.

Templates: Enter slice numbers as shown on the Scalable Brain Atlas website (https://scalablebrainatlas.incf.org/).

Areas: Enter areas to be applied to the templates, separated by commas. Use $ to separate multiple areas for the same column.

Processing:

The script processes the input data, opens the templates, and sets up the areas.
It creates a matrix for visualization and converts areas to corresponding events.

Visualization:

The script generates visualizations for the templates and areas.
It saves the visualizations in the output folder.

Functions:

whole_colormap(colormap='viridis'): Generates a colormap visualization for the slice.
whole_one_color(color=[0, 255, 0]): Colors the templates using a single color.
two_sided_colormap(colormap='viridis'): Generates a colormap visualization for two-sided data.
two_sided_one_color(color1=[255, 120, 0], color2=[0, 0, 255]): Colors the templates using two different colors for each side.
create_label(color=(255, 0, 0, 255)): Creates custom labels on a transparent background.

## Output
The script saves the visualizations in the output folder.
It generates HTML files for descriptive statistics and visualizations.
It saves images in PNG format and combines them into PDF files.

## Example
To run the script with manual input:
```
import brainplot

brainplot.initialization()
brainplot.create_templ(animal, templates)
brainplot.areas_viz()
brainplot.identify_events()
brainplot.to_pixel_coordinates()
brainplot.whole_colormap('viridis')
```

## Notes
Ensure the auto_input.txt file is correctly formatted if using automatic input.
