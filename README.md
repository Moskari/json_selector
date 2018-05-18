# Python 3 package for accessing json fields

Enables accessing json properties by defining a graph

## Example
```python
import json
from json_selector.json_selector import get_fields, explore_fields, flatten, unroll_headers, create_headers

# For example:
headers = [
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
    ('sub_object_name', selector_function)]    

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


if __name__ == '__main__':
    json_path = 'data.json'
    
    f = open(json_path, 'r')
    # Data is a list of objects    
    data = f.read()
    f.close()
    
    paths = []
    unroll_headers(headers, paths)
    
    new_headers = []
    create_headers(headers, new_headers, '')       
    
    data = json.loads(data)
    
    parsed_json = [get_fields(d, paths) for d in data]

    # Results to
    # new_headers == [
    #     'example_bottom_lvl_field_name', 
    #     'second_bottom_lvl_field', 
    #     'sub_object_name_example_2nd_lvl_field_name', 
    #     'sub_object_name_second_example_2nd_lvl_field_name', 
    #     'sub_object_name_subsub_object_name_example_3nd_lvl_field_name',
    #     'sub_list_name_0',
    #     'sub_list_name_1',
    #     'sub_list_name_2',
    #     'sub_object_name_sum_of_two']
    
    # parsed_json holds data for each row
    # parsed_json == [[<element for each header>], [...], ..., [...]]

```



## License

The MIT License (MIT)

**Disclaimer**
The author disclaims all responsibility for possible damage to equipment and/or people. Use the software with your own risk.
