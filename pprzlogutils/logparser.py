"""
pprzlogutils - A Python library for parsing and processing Paparazzi UAV log files.

logparser provides functions to parse Paparazzi UAV log files and extract telemetry data. 
It also includes utilities to convert the extracted data into numpy arrays for further analysis.

Author: Pelochus
Date: July 2024
"""

import numpy
import os

from collections import namedtuple
from lxml import etree

# Constants
MESSAGES_BLOCK = 'protocol/msg_class'
TELEMETRY_OUTPUT_FILENAME = 'telemetry_messages.xml'
DATALINK_OUTPUT_FILENAME = 'datalink_messages.xml'
DATA_OUTPUT_FILENAME = 'data_log.txt'
OUTPUT_DIR = './output'
TMP_DIR = './tmp'

MESSAGES_TYPES = {} # Data structures (named tuples) for each message
DATA_DICT = {} # Data dictionary, with up to N (number of UAVs, IDs) MESSAGE_TYPES

'''
    Clean and format the XML, removing comments and recovering from errors
'''
def clean_and_format_xml(xml):
    parser = etree.XMLParser(remove_comments=True, recover=True, remove_blank_text=True)
    root = etree.fromstring(xml, parser)

    formatted_xml = etree.tostring(root, pretty_print=True, encoding='unicode')
    
    return formatted_xml

'''
    Simplify the .log file to a file which only contains the telemetry block
    This file will make easier to extract the vars for each message
'''
def make_messages_xml(logfile):
    parser = etree.XMLParser(remove_comments=True, recover=True)
    root = etree.fromstring(logfile, parser)

    # Find msg_class NAME = telemetry and ID = 1
    telemetry_xml = ''
    for msg_class in root.findall(MESSAGES_BLOCK):
        if msg_class.get('NAME') == 'telemetry' and msg_class.get('ID') == '1':
            telemetry_xml = etree.tostring(msg_class, encoding='unicode')
        elif msg_class.get('NAME') == 'datalink' and msg_class.get('ID') == '2':
            datalink_xml = etree.tostring(msg_class, encoding='unicode')

    telemetry_xml = clean_and_format_xml(telemetry_xml)
    datalink_xml = clean_and_format_xml(datalink_xml)
        
    # Save the msg_class block in a file
    output_file = os.path.join(TMP_DIR, TELEMETRY_OUTPUT_FILENAME)
    if telemetry_xml:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(telemetry_xml)
        
    # Save the msg_class block in a file
    output_file = os.path.join(TMP_DIR, DATALINK_OUTPUT_FILENAME)
    if datalink_xml:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(datalink_xml)

'''
    Create data structures for each message
    
    Examples:
    INS(timestamp, x, y, z, vx, vy, vz, ax, ay, az)
    GVF(timestamp, error, traj, s, ke, p)
'''
def create_structs(messages_type):
    with open(os.path.join(TMP_DIR, messages_type), 'r', encoding='utf-8') as f:
        parser = etree.XMLParser(remove_comments=True, recover=True)
        root = etree.fromstring(f.read(), parser)

        for msg in root.findall('message'):
            msg_name = msg.get('NAME')
            # msg_id = msg.get('ID')
            msg_vars = msg.findall('field')

            # Create a named tuple for each message
            fields = ['TIMESTAMP'] # To differentiate from a possible timestamp field inside the message
            for var in msg_vars:
                # Fix for some messages with a field named 'class'
                if var.get('NAME') != 'class':
                    fields.append(var.get('NAME'))

            # Create and save globally the named tuple
            MESSAGES_TYPES[msg_name] = namedtuple(msg_name, fields)

'''
    Parse the datafile, saving the data in the DATA_DICT dictionary
    Proposed data structure:

    DATA_DICT[id] = inner_dict[name][n].(timestamp, var1, var2...)

    (Suppose INS freq = 0.1 s, 10 Hz)
    Example for id = 2, field INS:

    DATA_DICT[2] -> inner_dict[INS][0] -> (0.1, x, y, z, vx, vy, vz, ax, ay, az)
    DATA_DICT[2] -> inner_dict[INS][1] -> (0.2, x, y, z, vx, vy, vz, ax, ay, az)
    ...
    DATA_DICT[2] -> inner_dict[INS][11] -> (1.2, x, y, z, vx, vy, vz, ax, ay, az)
'''
def parse_datafile(datafile, verbose=False):
    for line in datafile:
        # Split by spaces
        parts = line.split()
        
        # Extract data
        timestamp = float(parts[0])
        id = int(parts[1])
        name = parts[2]
        data = parts[3:]

        # Create the inner data dictionary for the id
        if id not in DATA_DICT:
            DATA_DICT[id] = {}
        
        # Create the inner array for the inner dict
        if name not in DATA_DICT[id]:
            DATA_DICT[id][name] = []
         
        # Save using the id and name. Previously check if name is saved (if it's a telemetry message)
        if name in MESSAGES_TYPES:
            linedata = MESSAGES_TYPES[name](timestamp, *data)
            DATA_DICT[id][name].append(linedata)

            if verbose:
                output_file = os.path.join(TMP_DIR, DATA_OUTPUT_FILENAME)
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(str(linedata))
                    f.write('\n')

#####################################################################
#####################################################################
# Numpy section
# Related and useful Links:
# https://numpy.org/doc/stable/reference/generated/numpy.array.html
# https://numpy.org/doc/stable/reference/generated/numpy.savetxt.html
#####################################################################
#####################################################################

'''
    Convert a certain message (for example, position messages) to a numpy array
    Only for a certain ID. Convert the array of messages
    This will assume float values only
'''
def convert_message_to_numpy(id, message):
    for var in MESSAGES_TYPES[message]._fields:
        convert_var_to_numpy(id, message, var)

'''
    Convert a certain variable (say, x position from position messages) to a numpy array
    This will assume float values only

    Returns the numpy array, too
'''
def convert_var_to_numpy(id, message, var):
    array = []
    for i in range(len(DATA_DICT[id][message])):
        array.append(float(getattr(DATA_DICT[id][message][i], var)))

    nparray = numpy.array(array)

    message_dir = OUTPUT_DIR + '/' + message
    os.makedirs(message_dir, exist_ok=True)
    
    filename = os.path.join(message_dir, var + '.npy')
    numpy.savetxt(filename, nparray) # Save to txt for later processing

    return nparray