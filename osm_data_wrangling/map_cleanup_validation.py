import re

isint = re.compile('^[0-9]+$')
isfloat = re.compile('^[-+]?\d+\.?\d*$')
isbool = re.compile('^(true|false)$')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
iszip = re.compile('^[0-9]{5}(?:-[0-9]{4})?$')
isphone = re.compile('^[1-9]\d{2}-\d{3}-\d{4}')

problems = {'way':[], 'node':[], 'tag':[], 'wn': [], 'id':[], 'zip_code':[]}
zip_codes = []
node_id_list = []
way_id_list = []

def init_arrays():
    global zip_codes
    global node_id_list
    global node_id_list
    global way_id_list
    global invalid_ways
    global invalid_nodes
    global invalid_tags

    zip_codes = []
    node_id_list = []
    way_id_list = []
    invalid_ways = []
    invalid_nodes = []
    invalid_tags = []

# verify that attributes are present and valid
def validate_node(node):
    if isint.match(node.attrib['id']) \
        and isfloat.match(node.attrib['lat']) \
        and isfloat.match(node.attrib['lon']) \
        and node.attrib['user'] \
        and isint.match(node.attrib['uid']) \
        and isint.match(node.attrib['version']) \
        and isint.match(node.attrib['changeset']) \
        and node.attrib['timestamp']:
            return True
    problems['node'] = node
    return False

# verify that key/value is present
def validate_tags(tag):
    # has a key and value
    if tag.attrib['k'] and tag.attrib['v']:
        return True
    problems['tag'] = tag
    return False

# verify that attributes are present and valid
def validate_way(way):
    if isint.match(way.attrib['id']) \
        and way.attrib['user'] \
        and isint.match(way.attrib['uid']) \
        and isint.match(way.attrib['version']) \
        and isint.match(way.attrib['changeset']) \
        and way.attrib['timestamp']:
        return True
    problems['way'] = way
    return False

# zip code has 5 or 9 number format
# Atlanta zip codes start with a '3'
def validate_zip_code(zip_code):
    if zip_code not in zip_codes:
        zip_codes.append(zip_code)
        if not iszip.match(zip_code) and str(zip_code)[0] == '3':
            problems['zip_code'] = zip_code
            return False
    return True

# unique ids
def validate_id(this_id):
    # should not have duplicate id's
    if this_id in node_id_list:
        problems['id'] = this_id
        return False
    node_id_list.append(this_id)
    return True

# is phone number in ###-###-#### format
def validate_phone(phone_num):
    if isphone.match(phone_num):
        return True
    return False

# correct phone number to ###-###-#### format
def standardize_phone(phone_num):
    try:
        std_phone_num = [n for n in phone_num if n.isdigit()]
        if len(std_phone_num) > 10:
            # disregard country codes for now
            std_phone_num = std_phone_num[1:]
        std_phone_num.insert(3,'-')
        std_phone_num.insert(7,'-')
        std_phone_num = ''.join(std_phone_num)
        return std_phone_num
    except:
        pass
    return phone_num

def validate_waynodes(wn):
    if isint.match(wn.attrib['ref']):
        return True
    problems['wn'] = wn
    return False
