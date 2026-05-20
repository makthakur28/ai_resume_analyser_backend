import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.schemas.resume import StructuredResume
from app.core.logging import logger

class TemplateService:
    def __init__(self, templates_dir: str = "app/templates"):
        self.templates_dir = templates_dir
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def render_resume(self, resume_data: StructuredResume, template_name: str = "modern_resume.html") -> str:
        """
        Renders the StructuredResume into HTML using Jinja2.
        """
        try:
            template = self.env.get_template(template_name)
            # Pass the pydantic model as dict
            html_content = template.render(resume=resume_data.model_dump())
            return html_content
        except Exception as e:
            logger.error(f"Failed to render template {template_name}: {e}")
            raise
