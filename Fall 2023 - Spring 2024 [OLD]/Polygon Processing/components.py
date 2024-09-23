import cv2 as cv
import numpy as np

# Read the input image
src = inputImage = cv.imread('component2 copy.jpg')

# Convert image to gray and blur it
src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
src_gray = cv.blur(src_gray, (3, 3))

def draw_red_grid(img):

    line_color = (150, 0, 0)
    line_thickness = 1

    # Define the spacing between grid lines (in pixels) corresponding to 1 cm
    grid_spacing = 15  
    
    # Draw vertical grid lines
    for x in range(0, img.shape[1], grid_spacing):
        cv.line(img, (x, 0), (x, img.shape[0]), line_color, line_thickness)

    # Draw horizontal grid lines
    for y in range(0, img.shape[0], grid_spacing):
        cv.line(img, (0, y), (img.shape[1], y), line_color, line_thickness)

def thresh_callback(val):
    threshold = val
    # Detect edges using Canny
    canny_output = cv.Canny(src_gray, threshold, threshold * 2)

    # Find contours
    contours, _ = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Create a black image to draw polygons and grid
    drawing = np.zeros_like(src)

    # Draw polygons only for contours
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 300:
            epsilon = 0.01 * cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, epsilon, True)

            # Filter by aspect ratio - polygons can't be too thin
            x, y, w, h = cv.boundingRect(approx)
            aspect_ratio = float(w) / h

            # Filter by elongation = essentially get rid of the wire paths - I mainly use this to get rid of the horizontal and diagonal lines
            elongation_threshold = 1.53  # 1.54 is too high but with 1.53 - two square cannot be identified but that may just be created a bigger connector or making the boxes thicker
            if 0.1 < aspect_ratio < elongation_threshold:
                cv.drawContours(drawing, [approx], 0, (255, 255, 255), 2)

    # Draw red grid
    draw_red_grid(drawing)

    # Show the result
    cv.imshow('Polygons with Grid', drawing)
    cv.imwrite('processed.jpg', drawing)

# Create Window
source_window = 'Source'
cv.namedWindow(source_window)
cv.imshow(source_window, src)

max_thresh = 255
thresh = 100  # Lower initial threshold

thresh_callback(thresh)


cv.waitKey(0)
cv.destroyAllWindows()
