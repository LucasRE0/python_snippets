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

### torchvision ver, save image
import torch
import torchvision
def save_gridimage(images_arr, save_path, nrow=2, padding=0):
    images_arr = (images_arr / 255.0).astype(np.float32)
    images_arr = np.transpose(images_arr, [0,3,1,2])
    images_tensor = torch.as_tensor(images_arr)
    torchvision.utils.save_image(
        images_tensor, 
        save_path,
        nrow=nrow, padding=padding)

#-------------------------
### PIL ver
def apply_mask(img, mask):
    masked = img * (mask > 0)
    return masked

def apply_mask_for_dir(img_dir, mask_dir):
    ### get img names
    img_names = sorted([f for f in os.listdir(img_dir) if f.endswith((".jpg", ".png"))])

    for img_name in img_names:
        img_path = os.path.join(img_dir, img_name)
        mask_path = os.path.join(mask_dir, img_name)

        img = np.array(Image.open(img_path))
        mask = np.array(Image.open(mask_path))
        masked = apply_mask(img, mask)

        save_path = os.path.join(mask_dir, img_name[:-4] + "_masked.png")
        Image.fromarray(masked).save(save_path)
