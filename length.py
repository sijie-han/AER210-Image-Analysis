import cv2
import numpy as np

# Global variables to store clicked points
points = []

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 2:
            points.append((x, y))
            # Draw a circle at clicked point
            cv2.circle(image, (x, y), 3, (0, 255, 0), -1)
            cv2.imshow('Image', image)
            
            if len(points) == 2:
                # Draw line between points
                cv2.line(image, points[0], points[1], (0, 255, 0), 2)
                # Calculate length
                length_in_pixels = np.sqrt((points[1][0] - points[0][0])**2 + 
                                         (points[1][1] - points[0][1])**2)
                length_in_micrometers = length_in_pixels * (200/210)  # Convert to micrometers
                print(f"Length in pixels: {length_in_pixels:.2f}")
                print(f"Length in micrometers: {length_in_micrometers:.2f}")
                cv2.imshow('Image', image)

def line_length_analysis(image_path):
    global image, points
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        return

    # Create window and set mouse callback
    cv2.imshow('Image', image)
    cv2.setMouseCallback('Image', click_event)
    
    # Wait for key press
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    points = []  # Reset points for next use

# Example usage
image_path = 'MultiTime-Test/t_0001.tif'
line_length_analysis(image_path)
