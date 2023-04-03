from pylibdmtx.pylibdmtx import encode, decode
from PIL import Image

def code_to_matrix(code: str) -> list:
    # Encode the input code as a DataMatrix
    encoded_data = encode(code.encode('utf8'))
    # Create an image from the encoded data
    image = Image.frombytes('L', (encoded_data.width, encoded_data.height), encoded_data.pixels, 'raw')
    image.save("test.png")
    # Crop the image to 12x12
    cropped_image = image.crop((0, 0, 12, 12))

    # Convert the image to a 12x12 binary matrix
    matrix = []
    for row in range(cropped_image.height):
        matrix_row = []
        for col in range(cropped_image.width):
            pixel = cropped_image.getpixel((col, row))
            print(pixel)
            matrix_row.append('1' if pixel == 255 else '0')
        matrix.append(matrix_row)

    return encoded_data

matrix = code_to_matrix("ABC1234")
print(matrix)
#for row in matrix:
#    print(row)
    
encoded = encode('ABC1234'.encode('utf8'))
img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
img.save('dmtx.png')
print(decode(Image.open('dmtx.png')))

