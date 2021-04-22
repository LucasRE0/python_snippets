import os
from glob import glob


def get_file_names_w_exts(input_dir, exts):
    return sorted([f for f in os.listdir(input_dir) if f.endswith(exts)])


def get_file_pathes_w_exts(input_dir, exts, recursive=False):
    if recursive:
        if isinstance(exts, str):
            return sorted(glob(os.path.join(input_dir, "**", "*"+exts), recursive=True))
        elif isinstance(exts, (list, tuple)):
            ret_list = []
            for ext in exts:
                ret_list += sorted(glob(os.path.join(input_dir, "**", "*"+ext), recursive=True))
            return ret_list
    else:
        return sorted([os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(exts)])




