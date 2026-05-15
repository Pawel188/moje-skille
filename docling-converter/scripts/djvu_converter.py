#!/usr/bin/env python3
import subprocess
import os
import sys
import time
import argparse
import urllib.parse
from pathlib import Path

def check_dependencies():
    """Sprawdza czy ddjvu jest zainstalowane w systemie."""
    try:
        subprocess.run(["ddjvu", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        print("[!] Błąd: Narzędzie 'ddjvu' nie jest zainstalowane.")
        print("Zainstaluj je: sudo apt-get install djvulibre-bin")
        return False

def convert_djvu_to_pdf(input_path, output_path, pages=None):
    """Konwertuje DjVu (lub jego fragment) do wysokiej jakości PDF."""
    cmd = ["ddjvu", "-format=pdf"]
    if pages:
        cmd.append(f"-page={pages}")
        print(f"[*] Krok 1: Konwersja stron {pages} z DjVu do PDF...")
    else:
        print(f"[*] Krok 1: Konwersja całego DjVu do PDF: {input_path}")
    
    cmd.extend([input_path, output_path])
    
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Błąd ddjvu: {e}")
        return False

def convert_pdf_to_md(pdf_path, md_path):
    """Używa Docling do konwersji PDF na Markdown (OCR + Layout + Obrazy)."""
    print(f"[*] Krok 2: Uruchamianie Docling dla pliku: {pdf_path}")
    start_time = time.time()
    
    md_file_path = Path(md_path)
    image_dir = md_file_path.parent / f"{md_file_path.stem}_images"
    
    if not image_dir.exists():
        image_dir.mkdir(parents=True, exist_ok=True)
        
    try:
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling_core.types.doc import ImageRefMode
        
        # Konfiguracja opcji - włączamy ryciny
        pipeline_options = PdfPipelineOptions()
        pipeline_options.generate_picture_images = True
        pipeline_options.images_scale = 2.0
        
        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        
        result = converter.convert(pdf_path)
        
        # Eksport do MD z referencjami do obrazów
        # Kodujemy spacje w nazwie folderu dla Markdown (np. %20)
        image_dir_quoted = urllib.parse.quote(image_dir.name)
        
        result.document.save_as_markdown(
            filename=md_path,
            artifacts_dir=image_dir,
            image_mode=ImageRefMode.REFERENCED
        )
        
        # Docling v2 save_as_markdown może nie kodować spacji w ścieżkach wewnątrz pliku MD.
        # Naprawiamy to ręcznie po zapisie, jeśli nazwa folderu zawiera spacje.
        if " " in image_dir.name:
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
            new_content = content.replace(image_dir.name, image_dir_quoted)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            
        elapsed = time.time() - start_time
        print(f"[+] Sukces! Konwersja MD i obrazów zajęła {elapsed:.2f}s")
        print(f"[*] Obrazy zapisano w: {image_dir}")
        return True
    except ImportError as e:
        print(f"[!] Błąd: Brak bibliotek Docling: {e}")
        return False
    except Exception as e:
        print(f"[!] Błąd Docling: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(description="Konwerter DjVu do Markdown z obrazami.")
    parser.add_argument("input", help="Plik wejściowy .djvu")
    parser.add_argument("output", nargs="?", help="Plik wyjściowy .md (opcjonalnie)")
    parser.add_argument("--pages", help="Zakres stron, np. '1-5'")
    
    args = parser.parse_args()
    
    input_file = args.input
    output_file = args.output if args.output else os.path.splitext(input_file)[0] + ".md"
    
    if not os.path.exists(input_file):
        print(f"[!] Plik nie istnieje: {input_file}")
        sys.exit(1)
        
    if not check_dependencies():
        sys.exit(1)
        
    temp_pdf = f"temp_processing_{int(time.time())}.pdf"
    
    try:
        if convert_djvu_to_pdf(input_file, temp_pdf, args.pages):
            if convert_pdf_to_md(temp_pdf, output_file):
                print(f"[OK] Gotowe! Plik: {output_file}")
            else:
                print("[!] Błąd podczas konwersji do MD.")
        else:
            print("[!] Błąd podczas konwersji do PDF.")
    finally:
        if os.path.exists(temp_pdf):
            os.remove(temp_pdf)

if __name__ == "__main__":
    main()
