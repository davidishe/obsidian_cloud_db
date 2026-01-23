#!/usr/bin/env python3
"""
Extract text from Shorts 6.docx file
"""
import zipfile
import re
from xml.etree import ElementTree as ET

def extract_text_from_docx(docx_path):
    """Extract text from a .docx file preserving structure"""
    try:
        with zipfile.ZipFile(docx_path, 'r') as z:
            # Read the main document XML
            xml_content = z.read('word/document.xml')
            
            # Parse XML
            tree = ET.fromstring(xml_content)
            
            # Define namespace
            namespaces = {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            }
            
            # Extract all text from paragraphs
            paragraphs = []
            for paragraph in tree.findall('.//w:p', namespaces):
                texts = []
                for text_elem in paragraph.findall('.//w:t', namespaces):
                    if text_elem.text:
                        texts.append(text_elem.text)
                
                para_text = ''.join(texts).strip()
                if para_text:
                    paragraphs.append(para_text)
            
            return '\n\n'.join(paragraphs)
            
    except Exception as e:
        print(f"Error extracting text: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    docx_path = "Контент-завод/Shorts 6.docx"
    
    print(f"Extracting text from: {docx_path}")
    text = extract_text_from_docx(docx_path)
    
    if text:
        output_file = "shorts_6_extracted.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"\n✅ Text extracted to: {output_file}")
        print(f"\n📄 Preview (first 500 chars):")
        print("=" * 60)
        print(text[:500])
        print("=" * 60)
    else:
        print("❌ Failed to extract text")
