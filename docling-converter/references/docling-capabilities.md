# Docling Capabilities Reference

Docling is a multi-format document parsing and conversion engine.

## Supported Input Formats
Docling can natively process the following formats:
- **Documents**: PDF, DOCX, XLSX, PPTX, HTML, AsciiDoc, Markdown.
- **Images**: PNG, JPEG, TIFF, BMP (via OCR).
- **Data**: CSV, JSON (Docling native).
- **Specialized**: XML (USPTO, JATS, XBRL), METS.
- **Experimental**: Audio, VTT, LaTeX.

> [!NOTE]
> For **DjVu** files, we use a two-step process: first converting to PDF using `ddjvu`, then processing with Docling.

## 1. Advanced Layout Analysis
Docling identifies and classifies document elements beyond simple text:
- **Headers**: Maintains hierarchy (H1, H2, H3).
- **Paragraphs**: Detects text blocks and flow.
- **Lists**: Correctly identifies bulleted and numbered lists.
- **Footnotes**: Recognizes and often links footnotes.

## 2. Table Understanding
One of Docling's strongest features is its ability to reconstruct tables:
- Converts complex PDF/scanned tables into native Markdown tables.
- Handles cell spanning and alignment in many cases.

## 3. Image and Figure Extraction
Docling can identify and crop visual elements:
- **Figures**: Extracts diagrams, charts, and drawings.
- **Captions**: Often associates figures with their textual descriptions.
- **Referencing**: Provides absolute or relative paths to extracted artifacts.

## 4. OCR (Optical Character Recognition)
When no text layer is present (scanned documents):
- Uses **RapidOCR** by default.
- Supports high-resolution rendering for improved accuracy.
- Can be configured for CPU-only or GPU acceleration.

## 5. Mathematical Formula Support
Docling includes experimental support for recognizing mathematical formulas and converting them to LaTeX/Markdown compatible formats.

## 6. Pipeline Customization
You can tweak the engine behavior:
- `generate_picture_images`: Toggle figure extraction.
- `images_scale`: Adjust resolution of extracted images and OCR rendering.
- `do_table_structure`: Enable/disable advanced table parsing.

## 7. Export Formats
- **Markdown**: Optimized for LLM ingestion and Obsidian usage.
- **JSON**: Full structural metadata for programmatic processing.
- **HTML**: For web-ready document representation.
- **DocSet**: Internal high-level representation used by Docling Core.

## Project Context
In this workspace, Docling is integrated via `djvu_converter.py`, which uses `ddjvu` as a high-quality pre-processor to convert DjVu files into standard PDFs that Docling can parse with maximum accuracy.
