from docx import Document
from pathlib import Path
from typing import List, Dict, Any
import json
import hashlib
from datetime import datetime

class DocumentProcessor:
    def __init__(self, upload_dir: Path):
        self.upload_dir = upload_dir
        self.upload_dir.mkdir(exist_ok=True)

    def extract_text_from_word(self, file_path: str) -> str:
        """Extract text from Word document with enhanced error handling."""
        try:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            return text
        except Exception as e:
            raise ValueError(f"Error processing Word document: {str(e)}")

    def save_document(self, file_content: bytes, filename: str) -> Dict[str, str]:
        """Save document with metadata."""
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{self._sanitize_filename(filename)}"
            file_path = self.upload_dir / safe_filename
            
            # Save file
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            # Generate metadata
            metadata = {
                "original_filename": filename,
                "saved_filename": safe_filename,
                "upload_time": datetime.now().isoformat(),
                "file_size": len(file_content),
                "file_hash": self._calculate_hash(file_content)
            }
            
            # Save metadata
            meta_path = file_path.with_suffix('.meta.json')
            with open(meta_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            return metadata
        except Exception as e:
            raise ValueError(f"Error saving document: {str(e)}")

    def get_document_list(self) -> List[Dict[str, Any]]:
        """Get list of documents with metadata."""
        documents = []
        for meta_file in self.upload_dir.glob("*.meta.json"):
            try:
                with open(meta_file, 'r') as f:
                    metadata = json.load(f)
                doc_path = meta_file.with_suffix('').with_suffix('.docx')
                if doc_path.exists():
                    metadata["exists"] = True
                    metadata["path"] = str(doc_path)
                    documents.append(metadata)
            except Exception:
                continue
        return sorted(documents, key=lambda x: x["upload_time"], reverse=True)

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe storage."""
        return "".join(c for c in filename if c.isalnum() or c in "._- ")

    def _calculate_hash(self, content: bytes) -> str:
        """Calculate SHA-256 hash of file content."""
        return hashlib.sha256(content).hexdigest()

    def validate_file(self, filename: str, content: bytes) -> None:
        """Validate file before processing."""
        if not filename.lower().endswith(('.doc', '.docx')):
            raise ValueError("Only Word documents (.doc, .docx) are supported")
        
        if len(content) > 10 * 1024 * 1024:  # 10MB limit
            raise ValueError("File size exceeds maximum limit of 10MB")
