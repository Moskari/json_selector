# -*- coding: utf-8 -*-
"""
Created on Wed May 16 14:38:18 2018

@author: Samuli Rahkonen
"""


def explore_fields(obj, fields):    
    ''' 
    Explores given json obj according to given `fields` header list.
    Returns a list hierarchy of found values according to the fields structure.
    May include None values for not found values and skips subbranches of 
    field hierarchy if parent fields are not found. Use i.e.
    flatten function to make the result a 1D list.
    '''
    if not isinstance(fields, list):
        raise Exception(
            'Fields should be list, was %s, %s' % (
                str(type(fields)), str(fields)))
    result = []
    for field in fields:
        if isinstance(field, str):
            if field in obj:
                result.append(obj[field])
            else:
                result.append(None)

        elif isinstance(field, int):
            if len(obj) >= field + 1:
                result.append(obj[field])
            else:
                result.append(None)

        elif isinstance(field, list):                    
            result.append([explore_fields(obj, [f]) for f in field])
        
        elif isinstance(field, tuple):
            parent, subfields = field
            if callable(subfields): # TODO
                _, tmp = subfields(obj[parent])
                result.append(tmp)
            elif isinstance(parent, str) and parent in obj:
                result.append(explore_fields(obj[parent], subfields))
            elif isinstance(parent, int) and len(obj) >= parent + 1:
                result.append(explore_fields(obj[parent], subfields))
            else:
                result.append(None)
        else:
            raise Exception('Unknown field %s' % str(field))
    return result


def flatten(l, curr=None):
    ''' Flattens arbitrary depth list of lists '''
    if curr is None:
        current_list = []
    else:
        current_list = curr
    if isinstance(l, list):
        for val in l:
            flatten(val, current_list)
        return current_list
    else:
        current_list.append(l)


def create_headers(fields, hdrs, path=[]):
    ''' Creates human readable headers for given headers '''
    if callable(fields):
        field, _ = fields()
        hdrs.append('_'.join([path, field]))
        return
    for field in fields:
        if isinstance(field, tuple):
            parent, subfields = field
            create_headers(subfields, hdrs, '_'.join([path, str(parent)]))
            
        if isinstance(field, (str, int)):
            hdrs.append('_'.join([path, str(field)]))
      
def unroll_headers(fields, paths, path=[]):
    ''' 
    Unrolls given fields to absolute json paths. `paths`  param is the
    return value (list of strings and/or ints).
    '''
    if callable(fields):
        new_path = path.copy()
        new_path.append(fields)
        paths.append(new_path)
        return
    for field in fields:
        if isinstance(field, tuple):
            parent, subfields = field
            new_path = path.copy()
            new_path.append(parent)
            unroll_headers(subfields, paths, new_path)
            
        if isinstance(field, (str, int)):
            new_path = path.copy()
            new_path.append(field)
            paths.append(new_path)
      
def get_fields(obj, json_paths):
    ''' 
    Takes json obj and list of unrolled json paths and returns list of rows
    which have values corresponding to json paths or None
    '''
    result = []
    for path in json_paths:
        curr_obj_branch = obj
        for field in path:
            if callable(field):
                _, data = field(curr_obj_branch)
                curr_obj_branch = data
                break
            else:
                try:
                    curr_obj_branch = curr_obj_branch[field]
                except:
                    curr_obj_branch = None
                    break
        result.append(curr_obj_branch)
    return result

def get_data(json_data, headers, return_many=False):
    '''
    Takes json object and header path list which defines what data will
    be returned from the `json_data`. Optional `return_many` is used if the
    function is applied to list of objects. Setting `return_many` to True if
    more efficient than calling this function multiple times.
    
    Returns tuple (<new header names>, <values corresponding to headers>)
    
    The given headers must be in the following form:
    
    # For example:
    [
    'example_bottom_lvl_field_name',
    'second_bottom_lvl_field',
    ('sub_object_name', [
        'example_2nd_lvl_field_name', 
        'second_example_2nd_lvl_field_name']),
    ('sub_object_name', [
        ('subsub_object_name', [
            'example_3nd_lvl_field_name'])]),
    ('sub_list_name', [0, 1, 2]), # Takes three first list elements
    # Custom function for returning something from `sub_object_name`
    ('sub_object_name', selector_function) 
    ]    
    
    # Custom function could be i.e. following    
    

    def selector_function(obj):
        # Gets an json object, selects a subobject and its list. 
        # Then sums together 2 first object property values
        # If there are not 2 values, then return one value or 0
        # Returns tuple(str(name_of_result), some_value)
        skills = flatten(explore_fields(obj, [('sub_object_name', [
            (0, ['some_field']),
            (1, ['some_field'])])]))
        return 'sum_of_two', sum(list(filter(lambda x: x is not None, skills)))
    '''
    paths = []
    unroll_headers(headers, paths)
    new_headers = []
    create_headers(headers, new_headers, '')
    
    if return_many:
        result = [get_fields(d, paths) for d in json_data]
    else:
        result = get_fields(json_data, paths)
    return new_headers, result
