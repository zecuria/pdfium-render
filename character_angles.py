#!/usr/bin/env python3

import os
import math
import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c

def main():
    # Set the path to the local libpdfium.dylib
    pdfium_lib_path = os.path.abspath("./libpdfium.dylib")
    
    # Configure pypdfium2 to use the local library
    if os.path.exists(pdfium_lib_path):
        os.environ['PYPDFIUM2_BINARY'] = pdfium_lib_path
    else:
        print(f"Warning: libpdfium.dylib not found at {pdfium_lib_path}")
        print("Using default pypdfium2 binary")
    
    # Load the PDF document
    try:
        pdf = pdfium.PdfDocument("./test/rotated.pdf")
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return
    
    # Iterate through each page
    for page_index in range(len(pdf)):
        print(f"Page {page_index + 1}:")
        
        page = pdf[page_index]
        
        # Get text page for character extraction
        textpage = page.get_textpage()
        
        # Get all characters on the page
        char_count = textpage.count_chars()
        
        for char_index in range(char_count):
            # Get character
            char = chr(pdfium_c.FPDFText_GetUnicode(textpage, char_index))
            
            # Try to get character rotation using different approaches
            angle_radians = 0.0
            
            try:
                # Method 1: Try to use raw API to get character matrix
                # Get the raw textpage handle
                raw_textpage = textpage
                
                angle_radians = pdfium_c.FPDFText_GetCharAngle(raw_textpage, char_index)
                
            except Exception:
                print("Error getting character matrix")
                # Method 2: Fallback to character bounds analysis
                try:
                    left, top, right, bottom = textpage.get_charbox(char_index)
                    char_width = right - left
                    char_height = bottom - top
                    
                    # Simple heuristic based on character dimensions
                    if char_height > char_width * 2:
                        angle_radians = math.pi / 2  # 90 degrees
                    elif char_width > char_height * 2 and char_height < 5:
                        angle_radians = -math.pi / 2  # -90 degrees
                        
                except Exception:
                    angle_radians = 0.0
            
            print(f"{char}: {angle_radians}")
        
        textpage.close()
    
    pdf.close()

if __name__ == "__main__":
    main() 