# 📋 Ctrl+V 2 Disk

A simple Python utility that saves clipboard content (text or images) to disk. Supports Windows, macOS, and Linux.

---

## ✨ Features

- 📸 Captures images directly from your clipboard
- 📝 Saves text content from your clipboard
- 🗂️ Respects file extensions (.txt, .md, .png, .jpg, etc.)
- ⚙️ Configurable defaults via `config.json`
- 💾 "ASK" mode to show save dialog
- 🖥️ Cross-platform support (Windows, macOS, Linux)
- ⚡ Lightweight and easy to use

---

## 🚀 Installation

This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

### Prerequisites

- Python 3.8 or higher
- [UV](https://docs.astral.sh/uv/getting-started/installation/) installed
- Linux users: install `xclip`, `xsel`, or `wl-clipboard` for text support

### Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd ctrlv2disk
   ```

2. Install dependencies with UV:
   ```bash
   uv sync
   ```

### Installing as CLI Tool

You can install `ctrlv2disk` as a command-line tool available globally:

**Option 1: Install with UV (recommended)**
```bash
uv pip install -e .
```

**Option 2: Install with pip**
```bash
pip install -e .
```

After installation, you can use the command directly:
```bash
ctrlv2disk ./myfile.txt
ctrlv2disk ./screenshot.png
ctrlv2disk
```

---

## 🎯 Usage

### Basic Usage

**With UV (without installing):**
```bash
uv run python main.py ./myfile.txt
uv run python main.py ./screenshot.png
uv run python main.py ./notes.md
```

**As installed CLI tool:**
```bash
ctrlv2disk ./myfile.txt
ctrlv2disk ./screenshot.png
ctrlv2disk ./notes.md
```

Or run without arguments to use timestamped filename:

```bash
ctrlv2disk
```

### Configuration

Edit `config.json` to customize defaults:

```json
{
  "default_text_extension": ".txt",
  "default_image_extension": ".png",
  "path": "CURRENT_DIR"
}
```

**Options:**

- `default_text_extension`: Default extension for text files (default: `.txt`)
- `default_image_extension`: Default extension for images (default: `.png`)
- `path`: Where to save files
  - `"CURRENT_DIR"`: Save to current directory (default)
  - `"ASK"`: Show save dialog
  - `"/path/to/folder"`: Save to specific directory

### Examples

**Save text with specific name:**
```bash
uv run python main.py ./my-notes.md
```

**Save image as JPEG (auto-converts from RGBA):**
```bash
uv run python main.py ./photo.jpg
```

**Use save dialog (when `path` is set to `"ASK"`):**
```bash
uv run python main.py
# Shows native save dialog
```

**Auto-generate timestamped filename:**
```bash
uv run python main.py
# Creates: 20240115_143022.txt or 20240115_143022.png
```

---

## 🛠️ Development

To add or update dependencies:

```bash
uv add <package-name>
```

To run with specific Python version:

```bash
uv run --python 3.11 python main.py
```

---

## 📝 Supported Formats

**Images:** PNG, JPEG, GIF, BMP, TIFF (automatically detected from clipboard)
**Text:** Any text content with configurable extensions (.txt, .md, etc.)

---

## 💻 Platform Notes

- **macOS**: Uses `pbpaste` for text, PIL for images
- **Windows**: Uses PowerShell for text, PIL for images
- **Linux**: Uses `xclip`, `xsel`, or `wl-paste` for text, PIL for images

---

## 🔧 Troubleshooting

**Linux text not working?** Install clipboard utilities:
```bash
# X11
sudo apt-get install xclip
# or
sudo apt-get install xsel

# Wayland
sudo apt-get install wl-clipboard
```

**JPEG save fails?** The script automatically converts RGBA to RGB for JPEG compatibility.
