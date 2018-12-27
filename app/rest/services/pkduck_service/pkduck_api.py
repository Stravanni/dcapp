import os
import json
import ctypes
from ctypes import c_double
from ctypes import c_char_p
from sys import platform
import shutil

SELF_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
if platform == "darwin":
    DYNAMIC_LIB = "libpkduck.dylib"
else:
    DYNAMIC_LIB = "libpkduck.so"

# columns are in the format of 1,3,4#5#2#4,7, meaning that 
# the 1st, 3rd and 4th columns of the first table are selected 
# the 5th column of the second table is selected, etc. 
# tau is the similarity threshold, between 0 and 1 (usually greater than 0.7)

########################################################################
#
#   New API (Oct. 2018)
#
########################################################################

'''
@author: giovnani@csail.mit.edu


TODO: this function will receive only params as input, which is a JSON with all the information stored there
The forllowing implementation is to be compieant with the old api
# def executeService(params):

'''

def executeService(source, out_path, columns, tau, params={}):
    dir_in = source['CSV']['dir']
    dir_out = out_path['CSV']['dir']

    dir_metadata = dir_in + "/metadata_pkduck/"
    out_path['CSV']['dir'] = dir_metadata  # the output is redirected to the metadata folder
    # The purpose is twofold:
    #   - we do not change old API
    #   - we keep the meta-data
    # TODO: this will be a paramenter passed though the JSON input file
    if not os.path.exists(dir_metadata):
        os.makedirs(dir_metadata)

    # format_headers(dir_in)

    execute_pkduck(source, out_path, columns, tau)

    transform_files_pkduck(dir_metadata, dir_out)


# def execute_pkduck(input_json, output_json, columns, tau):
def transform_files_pkduck(dir_in, dir_out):
    files_in = os.listdir(dir_in)
    files_in = list(filter(lambda x: len(x.split("updated_")) > 1, files_in))  # only updated_* files

    for file in files_in:
        file_in = dir_in + file
        new_filename = file.split("updated_")[1]
        file_out = dir_out + new_filename

        shutil.move(file_in, file_out)

########################################################################
#
#   Old APIs
#
########################################################################

def execute_pkduck(input_json, output_json, columns, tau):

    i = input_json['CSV']['dir'];
    input_dir = c_char_p(i.encode('utf-8'))
    o = output_json['CSV']['dir'] ;
    output_dir = c_char_p(o.encode('utf-8'))

    columns = c_char_p(columns.encode('utf-8'))

    tau = c_double(tau)
    pkduck = ctypes.cdll.LoadLibrary(SELF_DIR_PATH + "/code/" + DYNAMIC_LIB)
    pkduck.execute(input_dir, output_dir, columns, tau)


def execute_pkduck_file(input_json_file, output_json_file, columns, tau):
    with open(input_json_file, 'r') as f:
        input_json = json.load(f)
    with open(output_json_file, 'r') as f:
        output_json = json.load(f)

    i = input_json['CSV']['dir'];
    input_dir = c_char_p(i.encode('utf-8'))
    o = output_json['CSV']['dir'] ;
    output_dir = c_char_p(o.encode('utf-8'))

    columns = c_char_p(columns.encode('utf-8'))

    tau = c_double(tau)
    pkduck = ctypes.cdll.LoadLibrary(SELF_DIR_PATH + "/code/" + DYNAMIC_LIB)
    pkduck.execute(input_dir, output_dir, columns, tau)

if __name__ == '__main__':
    columns = "1#2"
    execute_pkduck_file("input.json", "output.json", columns, 0.8)
