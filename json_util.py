import json

import numpy as np


class ExtendJSONEncoder(json.JSONEncoder):
    def default(self, value):
        if isinstance(value, np.ndarray):
            ### numpy array -> list
            return value.tolist()
        else:
            return super(ExtendJSONEncoder, self).default(value)
 

def load_json_file(load_path):
    with open(load_path, "r") as f:
        data = json.load(f)
    return data

  
def save_json_file(save_path, data):
    with open(save_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, cls=ExtendJSONEncoder)

        
def print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=4, cls=ExtendJSONEncoder))
        
      
def get_json_summary(data):
    assert isinstance(data, dict), "get_json_summary() got unexpected type data: {}".formata(type(data))
    ret_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            summary_value = get_json_summary(value)
        else:
            summary_value = str(type(value))
            if isinstance(value, list):
                summary_value += " : len {}".format(len(value))
            elif isinstance(value, np.ndarray):
                summary_value += " : shape {}".format(value.shape)
                
        ret_data[key] = summary_value
    return ret_data
  

def save_json_summary_file(save_path, data):
    summary_data = get_json_summary(data)
    save_json_file(save_path, summary_data)

    
def print_json_sammary(data):
    summary_data = get_json_summary(data)
    print_json(summary_data)
