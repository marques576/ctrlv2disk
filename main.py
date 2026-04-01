import os
import sys
import json
import subprocess
import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab
from datetime import datetime
from pathlib import Path

# Platform detection
IS_WINDOWS = sys.platform == 'win32'
IS_MACOS = sys.platform == 'darwin'
IS_LINUX = sys.platform.startswith('linux')

CONFIG_PATH = Path(__file__).parent / "config.json"

def load_config():
    """Load configuration from config file."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {"default_text_extension": ".txt", "default_image_extension": ".png", "path": "CURRENT_DIR"}

def get_clipboard_text():
    """Get text from clipboard using platform-specific methods."""
    try:
        if IS_MACOS:
            # macOS
            result = subprocess.run(['pbpaste'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
        elif IS_WINDOWS:
            # Windows - using PowerShell
            result = subprocess.run(
                ['powershell', '-command', 'Get-Clipboard'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return result.stdout
        elif IS_LINUX:
            # Linux - try xclip or xsel
            # Try xclip first
            try:
                result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'],
                                       capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout
            except FileNotFoundError:
                pass
            # Try xsel as fallback
            try:
                result = subprocess.run(['xsel', '--clipboard', '--output'],
                                       capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout
            except FileNotFoundError:
                pass
            # Try wl-copy (Wayland)
            try:
                result = subprocess.run(['wl-paste'],
                                       capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout
            except FileNotFoundError:
                pass
    except Exception:
        pass
    return None

def show_save_dialog(is_image=False, default_filename="", default_ext=".txt"):
    """Show a save file dialog using tkinter."""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    if is_image:
        filetypes = [
            ('PNG files', '*.png'),
            ('JPEG files', '*.jpg *.jpeg'),
            ('GIF files', '*.gif'),
            ('BMP files', '*.bmp'),
            ('All files', '*.*')
        ]
        default_ext = ".png"
    else:
        filetypes = [
            ('Text files', '*.txt'),
            ('Markdown files', '*.md'),
            ('All files', '*.*')
        ]

    filepath = filedialog.asksaveasfilename(
        defaultextension=default_ext,
        filetypes=filetypes,
        initialfile=default_filename,
        title="Save clipboard content as"
    )

    root.destroy()
    return filepath

def save_clipboard_content(location):
    """Save clipboard content (text or image) to the specified location."""
    config = load_config()
    default_text_ext = config.get("default_text_extension", ".txt")
    default_image_ext = config.get("default_image_extension", ".png")
    save_path = config.get("path", "CURRENT_DIR")

    # Check if we need to ask the user for location
    if save_path == "ASK":
        # First, detect what type of content is in clipboard
        clipboard_content = ImageGrab.grabclipboard()
        is_image = clipboard_content is not None and not isinstance(clipboard_content, list)

        # Use provided location as default filename, or generate timestamp
        if location:
            location_path = Path(location)
            # If location is a directory, use it as destination with timestamp filename
            if location_path.is_dir():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                if is_image:
                    location_path = location_path / (timestamp + default_image_ext)
                else:
                    location_path = location_path / (timestamp + default_text_ext)
            else:
                default_filename = location_path.stem
                if is_image:
                    # Show dialog for image
                    chosen_path = show_save_dialog(is_image=True, default_filename=default_filename)
                    if not chosen_path:
                        print("Save cancelled by user.")
                        return False
                    location_path = Path(chosen_path)
                else:
                    # Show dialog for text
                    chosen_path = show_save_dialog(is_image=False, default_filename=default_filename, default_ext=default_text_ext)
                    if not chosen_path:
                        print("Save cancelled by user.")
                        return False
                    location_path = Path(chosen_path)
        else:
            default_filename = datetime.now().strftime("%Y%m%d_%H%M%S")
            if is_image:
                # Show dialog for image
                chosen_path = show_save_dialog(is_image=True, default_filename=default_filename)
                if not chosen_path:
                    print("Save cancelled by user.")
                    return False
                location_path = Path(chosen_path)
            else:
                # Show dialog for text
                chosen_path = show_save_dialog(is_image=False, default_filename=default_filename, default_ext=default_text_ext)
                if not chosen_path:
                    print("Save cancelled by user.")
                    return False
                location_path = Path(chosen_path)
    else:
        location_path = Path(location)

        # If location is a directory, use it as destination with timestamp filename
        if location_path.is_dir():
            # Need to detect content type first
            clipboard_content = ImageGrab.grabclipboard()
            is_image = clipboard_content is not None and not isinstance(clipboard_content, list)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if is_image:
                location_path = location_path / (timestamp + default_image_ext)
            else:
                location_path = location_path / (timestamp + default_text_ext)
        # If save_path is not CURRENT_DIR or ASK and no specific path provided in location,
        elif location_path.parent == Path('.') and save_path not in ["CURRENT_DIR", "ASK"]:
            location_path = Path(save_path) / location_path

    # Ensure parent directory exists
    location_path.parent.mkdir(parents=True, exist_ok=True)

    # Try to get image from clipboard first
    clipboard_content = ImageGrab.grabclipboard()

    # Add default extension if none provided (before we check content type)
    if not location_path.suffix:
        is_image = clipboard_content is not None and not isinstance(clipboard_content, list)
        if is_image:
            location_path = location_path.with_suffix(default_image_ext)
        else:
            location_path = location_path.with_suffix(default_text_ext)

    if clipboard_content is not None and not isinstance(clipboard_content, list):
        # Handle image save
        # If extension is not an image format, use default
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}
        if not location_path.suffix:
            location_path = location_path.with_suffix(default_image_ext)
        elif location_path.suffix.lower() not in image_extensions:
            location_path = location_path.with_suffix(default_image_ext)

        try:
            # Convert to RGB if saving as JPEG (JPEG doesn't support RGBA)
            if location_path.suffix.lower() in {'.jpg', '.jpeg'} and clipboard_content.mode == 'RGBA':
                rgb_img = clipboard_content.convert('RGB')
                rgb_img.save(location_path)
            else:
                clipboard_content.save(location_path)
            print(f"Image saved to: {location_path}")
            return True
        except Exception as e:
            print(f"Failed to save image: {e}")
            return False
    else:
        # Try to get text from clipboard
        text = get_clipboard_text()

        if text:
            try:
                with open(location_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Text saved to: {location_path}")
                return True
            except Exception as e:
                print(f"Failed to save text: {e}")
                return False
        else:
            print("No content in clipboard!")
            return False

def main():
    """Main entry point for the CLI."""
    if len(sys.argv) >= 2:
        location = sys.argv[1]
    else:
        # Generate timestamped filename in current directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        location = timestamp

    save_clipboard_content(location)

if __name__ == "__main__":
    main()
