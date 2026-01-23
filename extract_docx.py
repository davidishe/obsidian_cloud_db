import os
import zipfile
import re
import sys

log_file = open('debug_log.txt', 'w')

def log(msg):
    log_file.write(str(msg) + '\n')
    print(msg)

def clean_xml(xml_content):
    # Very basic XML stripper
    text = re.sub('<[^>]+>', ' ', xml_content)
    text = re.sub('\s+', ' ', text).strip()
    return text

def extract_docx():
    try:
        current_dir = os.getcwd()
        log(f"CWD: {current_dir}")
        files = [f for f in os.listdir('.') if f.endswith('.docx')]
        log(f"Found docx files: {files}")
        
        if not files:
            log("No docx found")
            return

        docx_file = files[0]
        log(f"Processing {docx_file}")
        
        with zipfile.ZipFile(docx_file, 'r') as z:
            namelist = z.namelist()
            log(f"Zip content: {namelist[:5]}...")
            
            if 'word/document.xml' not in namelist:
                 log("word/document.xml not found!")
                 return

            xml_content = z.read('word/document.xml').decode('utf-8')
            text = clean_xml(xml_content)
            
            with open('extracted_text.md', 'w', encoding='utf-8') as f:
                f.write(text)
                log("Written to extracted_text.md")
                
    except Exception as e:
        log(f"Error: {e}")
        import traceback
        traceback.print_exc(file=log_file)
    finally:
        log_file.close()

if __name__ == "__main__":
    extract_docx()
