from PIL import Image

def process_pixel(pixel):
    # Check if the pixel is black (0) or white (255)
    return 1 if pixel == 0 else 0

def analyze_image(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Convert the image to grayscale
        img = img.convert("L")
        # Get the pixel values as a list of lists
        pixel_values = list(img.getdata())
        # Reshape the list into a 2D array based on the image size
        width, height = img.size
        grid = [pixel_values[i:i+width] for i in range(0, len(pixel_values), width)]
        # Process each pixel to get the final array
        result = [[process_pixel(pixel) for pixel in row] for row in grid]
        return result

# Path to the input image
image_path = "scan_image2.png"

result = analyze_image(image_path)

# Print the result
for row in result:
    print(row)
