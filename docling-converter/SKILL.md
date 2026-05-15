name: docling-converter
description: Use when converting various document formats (DjVu, PDF, DOCX, PPTX, etc.) to structured Markdown using Docling with high-fidelity OCR and layout analysis.
metadata:
  category: technique
  triggers: convert djvu to markdown, docling ocr, extract images from pdf, docx to markdown, convert pptx to markdown, scanned document to markdown
---

# Docling Document Converter

High-fidelity conversion of various document formats to structured Markdown using the Docling engine.

## When to Use
- Converting DjVu (via PDF), PDF, DOCX, or PPTX files to Markdown for Obsidian/Logseq.
- Extracting text and structure from scanned documents or complex office files.
- Automating high-quality OCR and image extraction pipelines.

## Requirements
- **System**: `djvulibre-bin`, `poppler-utils` (for PDF/DjVu).
- **Python**: Dedicated virtual environment (e.g., `ocr`) with `docling` and `torch+cpu` installed.

## Core Capabilities
- **Multi-format Support**: Native support for PDF, DOCX, PPTX, XLSX, HTML, Images, and more.
- **Layout Analysis**: Recognizes document structure (headers, paragraphs, tables).
- **OCR Integration**: Uses RapidOCR (CPU-optimized) for scanned images.
- **Image Extraction**: Automatically identifies and saves figures/pictures.
- **Markdown Export**: Generates clean Markdown with relative links to images.

## Usage

### Using the Dedicated Script
The skill includes a `djvu_converter.py` script (located in `scripts/`). It must be run using the `ocr` virtual environment.

```bash
# Path to script in skill folder
SKILL_SCRIPT="~/.gemini/antigravity/skills/docling-converter/scripts/djvu_converter.py"

# Convert full document using the 'ocr' venv
./ocr/bin/python $SKILL_SCRIPT "document.djvu"

# Convert specific page range
./ocr/bin/python $SKILL_SCRIPT "document.djvu" --pages 1-10
```

### Environment Setup (One-time)
```bash
python3 -m venv ocr
./ocr/bin/pip install docling torch --index-url https://download.pytorch.org/whl/cpu
```

### Manual Configuration (Python)
If modifying the pipeline, use the following Docling setup:

```python
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

options = PdfPipelineOptions()
options.generate_picture_images = True  # Enable image extraction
options.images_scale = 2.0              # High quality images

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=options)
    }
)
```

## Best Practices
- **Space Handling**: The script automatically URL-encodes image paths (replaces spaces with `%20`) to ensure Markdown previews work correctly.
- **CPU Optimization**: All dependencies are installed for CPU usage to avoid CUDA overhead.
- **Relative Links**: Images are saved in a `{filename}_images` folder. Keep this folder next to the `.md` file.

## Troubleshooting
- **Missing images in preview**: Ensure image paths are URL-encoded if filenames contain spaces.
- **Low OCR quality**: Increase `options.images_scale` (default is 2.0).
- **ddjvu not found**: Install system dependencies: `sudo apt-get install djvulibre-bin`.
