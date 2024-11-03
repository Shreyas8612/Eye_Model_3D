import bpy
import bmesh

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Lens with anatomical ratios
# Anterior (front) ratio = front radius/lens_thickness = 8.672/4.979 = 1.7417
# Posterior (back) ratio = back radius/lens_thickness = 6.328/4.979 = 1.2709
lens_thickness = 4.979
anterior_ratio = 1.7417
posterior_ratio = 1.2709


# Function to create the eye's retina (inner hemisphere)
def create_retina(name, radius, location):
    # Create retina as a UV sphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=radius, location=location)
    retina = bpy.context.object
    retina.name = name

    # Switch to Edit Mode for UV unwrapping for image imprinting
    bpy.ops.object.mode_set(mode='EDIT')

    # Select all vertices/faces in Edit Mode
    bpy.ops.mesh.select_all(action='SELECT')

    # Unwrap the UV map using Sphere Project for acurate projection on retina
    bpy.ops.uv.sphere_project()

    # Switch back to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create a material for the retina to etermine how light interacts with light
    mat = bpy.data.materials.new(name="Retina_Material")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Create a Diffuse BSDF shader node for the retina for a non reflecting surface
    bsdf = nodes.new("ShaderNodeBsdfDiffuse")

    # Create a texture image node for the fundus retinal image
    # Texture nodes handle the way textures (images patterns) are applied to materials.
    tex_image = nodes.new('ShaderNodeTexImage')
    tex_image.image = bpy.data.images.load("Fundas_Image.png")

    # Add a UV Map node to ensure correct texture placement
    uvmap_node = nodes.new('ShaderNodeTexCoord')

    # Connect the UV map node to the texture node
    links.new(uvmap_node.outputs['UV'], tex_image.inputs['Vector'])

    # Link texture to the BSDF (Diffuse shader)
    links.new(tex_image.outputs['Color'], bsdf.inputs['Color'])

    # Create the material output node
    material_output = nodes.get('Material Output')

    # Link the Diffuse BSDF to the material output
    # The final output of the node network, which determines the appearance of the material on the object.
    links.new(bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # Assign material to retina object created at the beginning
    retina.data.materials.append(mat)

    # Ensure backface culling is disabled
    mat.use_backface_culling = False  # This ensures both sides of the retina are visible

    # Cut the retina in half to create the hemisphere
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_outer=True)
    bpy.ops.object.mode_set(mode='OBJECT')

    return retina


# Function to create the cornea (front part)
def create_cornea(name, radius, location):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=radius, location=location)
    cornea = bpy.context.object
    cornea.name = name

    # Create a transparent material for the cornea (make it slightly visible and transparent)
    mat = bpy.data.materials.new(name="Cornea_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]

    # Adjust IOR, Base Color, and Roughness for better visibility and transparency
    # The value of Alpha ranges from 0.0 (All light rays will pass through, transparent) to 1.0 (blocks all light rays, opaque)
    # In real life, the cornea is fully transparent
    # Roughness determines how light is scattered off the surface
    # The value of roughness ranges from 0.0 (completely smooth, perfect mirror) to 1.0 (completely rough, scatters light in many directions)
    # Base color defines the main color of the material
    # This is the color in RGB format, setting all values to 1 means the cornea will be pure white
    # The alpha value here is fully opaque (though it is controlled separately via the Alpha input as described above)
    bsdf.inputs['IOR'].default_value = 1.376  # Cornea refractive index
    bsdf.inputs['Alpha'].default_value = 0.3  # Higher transparency (visible but slightly transparent)
    bsdf.inputs['Roughness'].default_value = 0.1  # Small roughness
    bsdf.inputs['Base Color'].default_value = (1, 1, 1, 1)  # White color for cornea

    # Assign material to cornea
    cornea.data.materials.append(mat)

    # Cut the cornea to create the front spherical segment
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bisect(plane_co=(9, 0, 0), plane_no=(-1, 0, 0), clear_outer=True)
    bpy.ops.object.mode_set(mode='OBJECT')

    return cornea


# Function to create a realistic human lens
def create_lens(name, lens_thickness, anterior_ratio, posterior_ratio, segments, rings, location):
    # The average radius of curvature for the lens by combining the contributions from both the anterior (front) and posterior (back) surfaces.
    radius = lens_thickness / (1 / anterior_ratio + 1 / posterior_ratio)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segments, v_segments=rings, radius=radius)

    # Scale to create anterior surface of lens (shallow curve)
    # The scaling is applied along the X-axis for the front
    bmesh.ops.scale(
        bm,
        vec=(1 / (lens_thickness * anterior_ratio), 1, 1),
        verts=bm.verts[:int(len(bm.verts) / 2)]  # Selects the front half of the vertices
    )

    # Scale to create posterior surface of lens (steeper curve)
    # The scaling is applied along the X-axis for the back
    bmesh.ops.scale(
        bm,
        verts=bm.verts[int(len(bm.verts) / 2):],  # Selects the back half of the vertices
        vec=(1 / (lens_thickness * posterior_ratio), 1, 1)
    )

    # Create mesh and object for the lens
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location

    # Create a realistic lens material (slightly transparent and refractive)
    mat = bpy.data.materials.new(name="Lens_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]

    # Adjust IOR, Base Color, and Roughness for better visibility and transparency
    # The value of Alpha ranges from 0.0 (All light rays will pass through, transparent) to 1.0 (blocks all light rays, opaque)
    # In real life, the cornea is fully transparent
    # Roughness determines how light is scattered off the surface
    # The value of roughness ranges from 0.0 (completely smooth, perfect mirror) to 1.0 (completely rough, scatters light in many directions)
    bsdf.inputs['IOR'].default_value = 1.406  # Lens refractive index
    bsdf.inputs['Alpha'].default_value = 0.2  # Transparent but visible
    bsdf.inputs['Roughness'].default_value = 0.1  # Small roughness for diffusion

    # Assign the material to the lens
    obj.data.materials.append(mat)

    return obj


# Function to create the sclera (outer shell of the eye)
def create_sclera(name, radius, location):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=radius, location=location)
    sclera = bpy.context.object
    sclera.name = name

    # Create a white material for the sclera
    # The sclera is opaque to prevent internal light scattering from affecting the image on the retina
    mat = bpy.data.materials.new(name="Sclera_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1)  # White color for the sclera

    # Assign material to sclera
    sclera.data.materials.append(mat)

    # Cut the sclera to match the reference image
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_outer=True)
    bpy.ops.object.mode_set(mode='OBJECT')

    return sclera


# Add lights to the scene
def add_lighting():
    # Add a sun lamp
    bpy.ops.object.light_add(type='SUN', location=(15, 0, 5))
    sun = bpy.context.object
    sun.data.energy = 3.0

    # Add a point light inside the eye to brighten up the interior
    bpy.ops.object.light_add(type='POINT', location=(0, 0, 0))
    point_light = bpy.context.object
    point_light.data.energy = 200.0


# Function to switch shading mode to 'MATERIAL' in the 3D Viewport
def set_viewport_shading(shading_type='MATERIAL'):
    for area in bpy.context.screen.areas:  # Iterate through all areas in the screen
        if area.type == 'VIEW_3D':  # If the area is a 3D Viewport
            for space in area.spaces:
                if space.type == 'VIEW_3D':  # Check if it's a 3D space
                    space.shading.type = shading_type  # Set the shading mode
            break  # Once found, no need to continue


# Create the eye components
sclera = create_sclera("Sclera", radius=12.0, location=(0, 0, 0))
retina = create_retina("Retina", radius=11.5, location=(0, 0, 0))  # Slightly smaller than sclera
cornea = create_cornea("Cornea", radius=7.259, location=(5, 0, 0))  # Position cornea closer to human anatomy
lens = create_lens("Lens", lens_thickness, anterior_ratio, posterior_ratio, segments=32, rings=16, location=(7.3, 0, 0))
lens.scale[0] = lens_thickness

# Add lighting to the scene
add_lighting()

# Switch to material view in the
set_viewport_shading('MATERIAL')
