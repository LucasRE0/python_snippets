import json

import numpy as np
import torch


class ExtendJSONEncoder(json.JSONEncoder):
    def default(self, value):
        if isinstance(value, np.ndarray):
            ### numpy array -> list
            return value.tolist()
        elif isinstance(value, torch.Tensor):
            ### torch tensor -> list
            return value.tolist()
        if isinstance(value, object) and hasattr(value, '__dict__'):
            ### original class -> dict
            return value.__dict__
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
    if isinstance(data, object) and hasattr(data, '__dict__'):
        ### original class -> dict
        data = data.__dict__
    assert isinstance(data, dict), "get_json_summary() got unexpected type data: {}".format(type(data))
    ret_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            summary_value = get_json_summary(value)
        else:
            if value is None or isinstance(value, (bool, int)):
                summary_value = value
            elif isinstance(value, str):
                summary_value = value if len(value) <= 32 else str(type(value))
            else:
                summary_value = str(type(value))
                if isinstance(value, (list, tuple)):
                    if all([isinstance(i, dict) for i in value]):
                        summary_value = [get_json_summary(i) for i in value]
                    else:
                        summary_value += " : len {}".format(len(value))
                elif isinstance(value, np.ndarray):
                    summary_value += " : shape {}".format(value.shape)
                elif isinstance(value, torch.Tensor):
                    summary_value += " : shape {}".format(value.shape)
                
        ret_data[key] = summary_value
    return ret_data
  

def save_json_summary_file(save_path, data):
    summary_data = get_json_summary(data)
    save_json_file(save_path, summary_data)

    
def print_json_sammary(data):
    summary_data = get_json_summary(data)
    print_json(summary_data)
