import cv2
import numpy as np

# Global variables to store clicked points
points = []

def click_event(event, x, y, flags, params, t):
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
                length_in_micrometers = length_in_pixels * (100/108)  # Convert to micrometers
                print(f"Length in pixels: {length_in_pixels:.2f}")
                print(f"Length in micrometers: {length_in_micrometers:.2f}")
                cv2.imshow('Image', image)

                # Calculate velocity and uncertainty
                dt = 0.5  # uncertainty in time (ms)
                dd = 2    # uncertainty in distance (μm)
                
                # Calculate velocity (μm/ms)
                velocity = length_in_micrometers / t 
                
                # Calculate uncertainty in velocity
                delta_v = np.sqrt((1/t * dd)**2 + ((-length_in_micrometers / t**2) * dt)**2)
                print(f"Velocity: {1000*velocity:.2f} ± {1000*delta_v:.2f} μm/s")

def line_length_analysis(image_path):
    global image, points
    # Extract time value from filename
    try:
        t = 78.4  # Gets '78.4' from 'smooth bend 78.4.tif'
    except (ValueError, IndexError):
        print("Error: Cannot parse time from filename. Expected format: 'name XX.X.tif'")
        return
        
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        return

    # Create window and set mouse callback
    cv2.imshow('Image', image)
    cv2.setMouseCallback('Image', lambda event, x, y, flags, params: 
                        click_event(event, x, y, flags, params, t))
    
    # Wait for key press
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    points = []  # Reset points for next use

# Example usage
image_path = 'smooth bend 78.4.tif'
line_length_analysis(image_path)
