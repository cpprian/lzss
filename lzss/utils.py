from bitarray import bitarray
from typing import Final
import cv2 

DEFUALT_OUTPUT_PATH: Final[str] = "./result.lzss"
IMAGE_TYPE: Final[str] = "image"


def read_data(data_path: str, file_type: str = "text") -> bytes:
    try:
        if file_type == IMAGE_TYPE:
            img = cv2.imread(data_path)
            data = cv2.imencode(".png", img)[1].tobytes()
        else:
            with open(data_path, "rb") as f:
                data = f.read()
        return data
    except FileNotFoundError:
        print(f"Error: File '{data_path}' not found.")


def write_data(output_buffer: bitarray, output_path: str = None):
    try:
        if output_path is None:
            output_path = DEFUALT_OUTPUT_PATH

        with open(output_path, "wb") as f:
            output_buffer.tofile(f)
    except:
        print(f"Error: Can't create file {output_buffer}")
