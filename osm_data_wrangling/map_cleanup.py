import xml.etree.cElementTree as ET
import csv
import map_cleanup_db
import map_cleanup_validation as audit
import os

OSM_FILE = 'data/map'
SAMPLE_OSM_FILE = "data/sample"
osm_xml = open(OSM_FILE,'r')

nodes = []
node_tags = []
ways = []
way_tags = []
way_nodes = []

csv_filepath = ''

tag_type_list = ['amenity', 'tourism', 'shop', 'landuse', 'highway', \
    'leisure', 'place', 'gnis:feature_type', 'aeroway', 'railway',
    'waterway', 'natural']

node_fields = ['id', 'lat', 'lon', 'user',
    'uid', 'version', 'changeset', 'timestamp']
tag_fields = ['id', 'key', 'value', 'type']
way_fields = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
way_node_fields = ['id', 'node_id', 'position']

def init_arrays():
    audit.init_arrays()
    global nodes
    global node_tags
    global ways
    global way_tags
    global way_nodes

    nodes = []
    node_tags = []
    ways = []
    way_tags = []
    way_nodes = []

# Retrieve root elements from osm_file xml
def get_element(input_file, tags=('node', 'way')):
    context = ET.iterparse(input_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

# Create a sample xml file from the file
def create_sample_file(k=10):
    with open(SAMPLE_OSM_FILE, 'wb') as output:
        output.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write(b'<osm>\n  ')

        print('creating sample file...')
        # Write every kth top level element
        for i, element in enumerate(get_element(osm_xml)):
            if i % k == 0:
                output.write(ET.tostring(element, encoding='utf-8'))

        output.write(b'</osm>\n ')
    print("done!")

# Group all node, way, and relation elements into respective lists
def group_elements(input_file):
    print('grouping root elements...')
    context = ET.iterparse(input_file, events=('start', 'end'))

    for event, element in context:
        # Only focus on top-level node or way elements
        if event == 'end' and (element.tag == 'node' or element.tag == 'way'):
            process_element(element)

    print('done!')

def process_element(element, parent=None):
    # process each top-level elements
    if element.tag == 'node':
        if audit.validate_node(element):
            # node is valid
            #audit.validate_id(element.attrib['id'])
            nodes.append(element)
        else:
            # node is not valid
            return None
        # process tag children, if they exist
        tags = element.findall('tag')
        process_tags(tags, element)
    elif element.tag == 'way':
        if audit.validate_way(element):
            # way is valid
            #audit.validate_id(element.attrib['id'])
            ways.append(element)
        else:
            # way is not valid
            return None
        tags = element.findall('tag')
        nds = element.findall('nd')
        process_tags(tags, element)
        process_nds(nds, element)

    else:
        print('element not recognized: ', element.tag)

def process_tags(tags, parent):
    if len(tags) > 0:
        tag_type = get_tag_type(parent)
        for tag in tags:
            if parent == None:
                print("parent element not found")
                return None
            if audit.validate_tags(tag):
                # tag is valid
                zip_code = ''
                this_id = ''
                if parent.tag == 'node':
                    if tag.attrib['k'] == 'addr:postcode':
                        # zip code validation for node tags
                        zip_code = tag.attrib['v']
                    elif tag.attrib['k'] == 'phone':
                        # phone number validation for node tags
                        if not audit.validate_phone(tag.attrib['v']):
                            tag.attrib['v'] = audit.standardize_phone(tag.attrib['v'])
                    node_tags.append({'id':parent.attrib['id'],
                        'key':tag.attrib['k'], 'value':tag.attrib['v'],
                        'type':tag_type
                    })
                elif parent.tag == 'way':
                    if tag.attrib['k'] == 'tiger:zip_left':
                        # zip code validation for way tags
                        zip_code = tag.attrib['v']
                    elif tag.attrib['k'] == 'phone':
                        # phone number validation for way tags
                        if not audit.validate_phone(tag.attrib['v']):
                            tag.attrib['v'] = audit.standardize_phone(tag.attrib['v'])

                    if ';' in tag.attrib['v']:
                        # this way crosses two counties -- split into two
                        values = tag.attrib['v'].split(';')
                        for v in values:
                            way_tags.append({'id':parent.attrib['id'],
                                'key':tag.attrib['k'], 'value':v.strip(),
                                'type':tag_type
                            })
                    else:
                        way_tags.append({'id':parent.attrib['id'],
                            'key':tag.attrib['k'], 'value':tag.attrib['v'],
                            'type':tag_type
                        })

                if zip_code:
                    if not audit.validate_zip_code(zip_code):
                        pass
            else:
                # tag is not valid
                return None

def process_nds(nds, parent):
    if len(nds) > 0:
        pos = 1
        for nd in nds:
            if audit.validate_waynodes(nd):
                way_nodes.append({'id':parent.attrib['id'],
                    'node_id':nd.attrib['ref'], 'position':pos
                })
            else:
                return None
            pos += 1

# find relevant tags for a given top-level element
def get_tag_type(parent):
    try:
        # set the value of the element as the type for specific keys
        tag_type = [tag.attrib['v'] for tag in parent \
            if tag.tag == 'tag' and tag.attrib['k'] in tag_type_list]
        if len(tag_type) > 0:
            return tag_type[0].strip().replace('_',' ')
    except Exception as e:
        print('problem retreiving tag type')
    return ''

def convert_to_csv(file_name, fieldnames, element_list):
    if not element_list or len(element_list) == 0:
        print("element list is empty")
        return None

    print("creating ", file_name, "...")

    if not os.path.exists('csv/'):
        os.makedirs('csv/')
    else:
        # delete the file if it exists and rewrite
        if os.path.exists('csv/' + file_name):
            print('     rewriting...')
            os.remove('csv/' + file_name)

    csv_filepath = os.path.join('csv/', file_name)

    with open(csv_filepath, 'w') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        for element in element_list:
            row = {}
            for field in fieldnames:
                try:
                    row[field] = element.attrib[field]
                except:
                    row[field] = element[field]
            writer.writerow(row)
    print("done!")
