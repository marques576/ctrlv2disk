import os
from PIL import ImageGrab
from datetime import datetime

def save_clipboard_image(folder="."):
    # Grab image from clipboard
    img = ImageGrab.grabclipboard()
    if img is None:
        print("No image in clipboard!")
        return False

    # Prompt user for file name
    user_input = input("Enter file name (without extension, leave empty for timestamp): ").strip()
    
    if not user_input:
        # If user leaves blank, use timestamp
        user_input = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{user_input}.png"
    path = os.path.join(folder, filename)

    try:
        img.save(path, "PNG")
        print(f"Image saved as: {path}")
        return True
    except Exception as e:
        print("Failed to save image:", e)
        return False

if __name__ == "__main__":
    save_clipboard_image()
