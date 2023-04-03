from PIL import Image
from pylibdmtx.pylibdmtx import encode

def encoded_to_image(encoded):
    return Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)

def resize_image(image, size):
    return image.resize((size, size), Image.NEAREST)

def image_to_matrix(image):
    width, height = image.size
    matrix = []

    for y in range(2,height-2):
        row = []
        for x in range(2,width-2):
            pixel = image.getpixel((x, y))
            if pixel == (0,0,0):  # Black pixel
                row.append("1")
            else:  # White pixel
                row.append("0")
        matrix.append(row)

    return matrix



def replace_table_in_file(file_path, new_matrix):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    start_idx, end_idx = None, None

    for i, line in enumerate(lines):
        if "NR" in line and "F1" in line:
            start_idx = i + 1
        elif "[END]" in line:
            end_idx = i

    if start_idx is None or end_idx is None:
        raise ValueError("Table not found in the .TAB file")

    n = len(new_matrix) 
    header_elements = ["NR"] + [f"F{i}" for i in range(1, n + 1)]
    header = "\t".join(header_elements) + "\n"
    #formatted_matrix = [header]
    formatted_matrix = []
    for i, row in enumerate(new_matrix):
        row_str = f"{i + 1:<7}"
        row_str += '\t'.join(f"{cell:<7}" for cell in row)
        row_str += '\n'
        formatted_matrix.append(row_str)

    lines[start_idx :end_idx] = formatted_matrix

    with open(file_path, 'r') as file:
        new_file = file.readlines()
    
    with open("test.TAB", 'w') as file:
        file.writelines(lines)
    
    
    
# Generate the Data Matrix barcode image
data = 'XYZ1234'
encoded = encode(data.encode('utf8'))

# Convert the Encoded object to an image
barcode_image = encoded_to_image(encoded)

# Resize the image to 12x12
resized_image = resize_image(barcode_image, 16)
barcode_image.save('test.png')

# Convert the image to a binary matrix
binary_matrix = image_to_matrix(resized_image)

replace_table_in_file("template.TAB", binary_matrix)

#binary_matrix = as.character(binary_matrix)
print('\n')
for row in binary_matrix:
    print(row)
print('\n')
