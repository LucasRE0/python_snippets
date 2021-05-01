import numpy
from PIL import Image
import cv2

#-------------------------
### PIL ver
def make_square(im, min_size=256, fill_color=(0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

### cv2 ver
def make_square(arr, min_size=256, fill_color=(0, 0, 0)):
    x, y, ch = arr.shape
    size = max(min_size, x, y)
    x_st, y_st = int((size -x) / 2), int((size -y) /2)
    new_arr = np.array([[fill_color for _ in range(size)] for _ in range(size)])
    new_arr[x_st : x_st + x, y_st : y_st+y, :] = arr
    return new_arr.astype(np.uint8)

#-------------------------
### cv2 ver, all same size
def make_grid(arr_list):
    if not isinstance(arr_list[0], list):
        arr_list = [arr_list]
    max_n_row = max([len(row) for row in arr_list])
    fill_arr = np.zeros_like(arr_list[0][0])
    ret_arr = []
    for row in arr_list:
        if len(row) < max_n_row:
            row += [fill_arr] * (max_n_row - len(row))
        ret_arr += [np.hstack(row)]
    ret_arr = np.vstack(ret_arr)
    return ret_arr

### cv2 ver, square padding
def make_grid(arr_list):
    if not isinstance(arr_list[0], list):
        arr_list = [arr_list]
    max_n_row = max([len(row) for row in arr_list])
    max_res = max([max([max(arr.shape[:2]) for arr in row]) for row in arr_list])
    fill_arr = np.zeros((max_res, max_res, 3))
    ret_arr = []
    for row in arr_list:
        row = [make_square(x, min_size=max_res) for x in row]
        if len(row) < max_n_row:
            row += [fill_arr] * (max_n_row - len(row))
        ret_arr += [np.hstack(row)]
    ret_arr = np.vstack(ret_arr)
    return ret_arr



