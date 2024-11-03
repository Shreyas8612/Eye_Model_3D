# **Blender Human Eye Model with Anatomical Features**

This project creates a detailed human eye model in Blender using Python scripting (Blender's built-in `bpy` module). The model includes anatomical components such as the sclera, retina, cornea, and lens, with materials and lighting to enhance realism.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Functions Explained](#functions-explained)
- [Acknowledgements](#acknowledgements)

## Overview

This script leverages Blender's Python API to create a realistic human eye model. It defines each anatomical part of the eye, assigns materials for realistic rendering, and sets up appropriate lighting for visualization.

- Models the sclera, retina, cornea, and lens.
- Adds realistic materials to each part to simulate transparency, refraction, and other optical properties.
- Configures scene lighting for better visualization of the eye model.

## Features

- **Eye Component Modeling**: Creates anatomical parts of the eye including sclera, retina, cornea, and lens.
- **Material Assignments**: Uses Blender's shader nodes to apply realistic materials to each component.
- **Scene Lighting**: Adds a sun lamp and point light for better visualization.
- **UV Mapping**: Unwraps the retina to allow for texture mapping (e.g., applying a fundus image).
- **Python Scripted Automation**: Automates the entire process in Blender.

## Requirements

- Blender 2.8 or higher
- Python 3 (comes with Blender)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/blender-eye-model.git
   cd blender-eye-model
   ```

2. **Open Blender and Run the Script**

   - Launch Blender.
   - Open the scripting workspace.
   - Load the Python script (`eye_model_script.py`) into the text editor.
   - Press `Run Script` to generate the eye model.

## Usage

1. **Ensure You Are in Blender's Scripting Workspace**

   - Open the script in Blender's scripting workspace.
   - Make sure to clear the default scene if necessary.

2. **Run the Script**

   - Click the `Run Script` button to create the eye model in the scene.

3. **View the Output**

   - The eye model will appear in the Blender viewport with all the components.
   - You can rotate, zoom, and inspect each part in detail.

## Project Structure

- **`eye_model_script.py`**: The main Python script that creates the human eye model using Blender's `bpy` module.

## Functions Explained

### In `eye_model_script.py`

- **`create_retina(name, radius, location)`**

  - Creates the retina as a UV sphere and applies texture mapping.
  - **Parameters**:
    - `name`: Name of the object.
    - `radius`: Radius of the retina.
    - `location`: Location of the retina.
  - **Returns**: The created retina object.

- **`create_cornea(name, radius, location)`**

  - Creates the cornea as a spherical segment and assigns a transparent material.
  - **Parameters**:
    - `name`: Name of the object.
    - `radius`: Radius of the cornea.
    - `location`: Location of the cornea.
  - **Returns**: The created cornea object.

- **`create_lens(name, lens_thickness, anterior_ratio, posterior_ratio, segments, rings, location)`**

  - Creates a realistic human lens using Blender's `bmesh` operations.
  - **Parameters**:
    - `name`: Name of the lens object.
    - `lens_thickness`: Thickness of the lens.
    - `anterior_ratio`: Ratio for the anterior (front) surface curvature.
    - `posterior_ratio`: Ratio for the posterior (back) surface curvature.
    - `segments`, `rings`: Number of segments and rings for the UV sphere.
    - `location`: Location of the lens.
  - **Returns**: The created lens object.

- **`create_sclera(name, radius, location)`**

  - Creates the sclera as a UV sphere and assigns an opaque white material.
  - **Parameters**:
    - `name`: Name of the object.
    - `radius`: Radius of the sclera.
    - `location`: Location of the sclera.
  - **Returns**: The created sclera object.

- **`add_lighting()`**

  - Adds a sun lamp and point light to the scene to illuminate the eye model.
  - **Parameters**: None
  - **Returns**: None

- **`set_viewport_shading(shading_type='MATERIAL')`**

  - Sets the Blender viewport shading mode to visualize materials.
  - **Parameters**:
    - `shading_type`: Type of shading (`MATERIAL` by default).
  - **Returns**: None

## Acknowledgements

This project uses Blender's Python API (`bpy`) to model and render the human eye. It is inspired by anatomical studies of the eye and aims to provide a visually accurate representation for educational purposes.

---

Feel free to modify the script to explore different anatomical variations or to adjust the materials for enhanced visualization.

