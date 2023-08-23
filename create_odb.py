# Abaqus python script to create an ODB file
# from existing odb file.

# import statements
from abaqus import *
from abaqusConstants import *
import odbAccess

mainodb_name = 'interference_fit.odb'
subodb_name = 'subodb.odb'

# Open main odb
odb = session.openOdb(name=mainodb_name)

# Create sub-odb object
subodb = session.Odb(name='data', path=subodb_name)

# Accessing instances of main odb
isn_names = odb.rootAssembly.instances.keys()

# Iterating through instance names
# ----------------------------------------------------
# Access instance
for isn_name in isn_names:
    isn1 = odb.rootAssembly.instances[isn_name]
    isn_space = isn1.embeddedSpace
    isn_type = isn1.type

    # read the data
    # Extract element information
    el_dict = dict()
    for element in isn1.elements:
        conn = element.connectivity
        label = element.label
        el_type = element.type
        if el_type not in el_dict:
            el_dict[el_type] = [ tuple([label, ] + list(conn)), ]
        else:
            el_dict[el_type].append(tuple([label, ] + list(conn)))
        

    # Extract node information
    nd_label, nd_coords = [], []
    for node in isn1.nodes:
        label = node.label
        coords = node.coordinates
        nd_label.append(label)
        nd_coords.append(tuple(coords))

    # write the data
    # create the part
    # space,  type, name
    mypart = subodb.Part(name=isn_name, embeddedSpace=isn_space,
                        type=isn_type)

    # Add node and elements
    mypart.addNodes(labels=tuple(nd_label), coordinates=tuple(nd_coords))

    for key,val in el_dict.items():
        mypart.addElements(elementData=tuple(val), type=key)

    # Create a instance from the part
    subodb.rootAssembly.Instance(name=isn_name, object=mypart)
# ----------------------------------------------------

# Update and save subodb
subodb.update()
subodb.save()
subodb.close()
subodb = session.openOdb(name=subodb_name)

print('yaaay, we created a subodb')

