use pdfium_render::prelude::*;

fn main() -> Result<(), PdfiumError> {
    let pdfium = Pdfium::default();
    let document = pdfium.load_pdf_from_file("test/rotated.pdf", None)?;

    for (page_index, page) in document.pages().iter().enumerate() {
        println!("Page {}:", page_index + 1);
        
        let text = page.text()?;
        let chars = text.chars();

        for character in chars.iter() {
            let char_str = character.unicode_string()
                .unwrap_or_else(|| "[?]".to_string());
            let angle_radians = character.angle_radians().unwrap_or(0.0);
            
            println!("{}: {}", char_str, angle_radians);
        }
    }
    
    Ok(())
} 