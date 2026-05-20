import os
from weasyprint import HTML, CSS
from app.core.logging import logger

class PDFGenerationService:
    def __init__(self, templates_dir: str = "app/templates"):
        self.templates_dir = templates_dir

    def generate_pdf(self, html_content: str, output_path: str, css_file: str = "modern_resume.css"):
        """
        Converts rendered HTML into a professional PDF using WeasyPrint.
        """
        try:
            logger.info(f"Generating PDF to {output_path}")
            
            # Load CSS if it exists
            css_path = os.path.join(self.templates_dir, css_file)
            stylesheets = []
            if os.path.exists(css_path):
                stylesheets.append(CSS(filename=css_path))
                
            HTML(string=html_content).write_pdf(
                output_path,
                stylesheets=stylesheets,
                presentational_hints=True
            )
            logger.info(f"PDF generated successfully at {output_path}")
        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")
            raise
