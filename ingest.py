import os
import pytesseract
from unstructured.partition.pdf import partition_pdf
from database import DatabaseManager

# --- CHECK PATH: Must match your installation ---
import shutil
# Check if we are on Windows (Laptop) or Linux (Cloud)
if os.name == 'nt': 
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# On Cloud (Linux), it finds Tesseract automatically.

class IngestEngine:
    def __init__(self):
        self.db = DatabaseManager()
        self.img_dir = "static/images"
        os.makedirs(self.img_dir, exist_ok=True)

    def process_pdf(self, file_path):
        filename = os.path.basename(file_path)
        print(f"Processing {filename}...")
        try:
            elements = partition_pdf(
                filename=file_path,
                strategy="hi_res",
                infer_table_structure=True,
                extract_images_in_pdf=True,
                extract_image_block_types=["Image"],
                image_output_dir_path=self.img_dir
            )

            current_chunk = ""
            for el in elements:
                text = str(el).strip()
                if not text: continue
                page = el.metadata.page_number
                el_type = el.category

                if el_type == "Table":
                    if current_chunk:
                        self.db.save_chunk(current_chunk, {"source": filename, "page": page, "type": "text"})
                        current_chunk = ""
                    self.db.save_table(el.metadata.text_as_html, text, filename, page)

                elif el_type == "Image":
                    if current_chunk:
                        self.db.save_chunk(current_chunk, {"source": filename, "page": page, "type": "text"})
                        current_chunk = ""
                    self.db.save_chunk(f"Image Figure: {text}", {
                        "source": filename, "page": page, "type": "image", 
                        "image_path": el.metadata.image_path
                    })

                else:
                    current_chunk += text + "\n"
                    if len(current_chunk) > 1000:
                        self.db.save_chunk(current_chunk, {"source": filename, "page": page, "type": "text"})
                        current_chunk = ""
            
            if current_chunk:
                self.db.save_chunk(current_chunk, {"source": filename, "page": 1, "type": "text"})

            return True, "Done!"
        except Exception as e:
            return False, str(e)