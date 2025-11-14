"""
Export service for PDF and ePub
"""
import logging
from typing import Dict
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

logger = logging.getLogger(__name__)

class ExportService:
    """Service for exporting books to different formats"""

    @staticmethod
    def export_to_pdf(book_data: Dict) -> bytes:
        """Export book to PDF"""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Title
            story.append(Paragraph(book_data["title"], styles['Title']))
            story.append(Spacer(1, 12))

            # Description
            if book_data.get("description"):
                story.append(Paragraph(book_data["description"], styles['Normal']))
                story.append(Spacer(1, 12))

            # Chapters
            for chapter in book_data.get("chapters", []):
                story.append(Paragraph(f"Chapter {chapter['number']}: {chapter.get('title', '')}", styles['Heading1']))
                story.append(Spacer(1, 12))

                for block in chapter.get("blocks", []):
                    if block.get("block_type") == "text":
                        story.append(Paragraph(block.get("content", ""), styles['Normal']))
                        story.append(Spacer(1, 6))

            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()

        except Exception as e:
            logger.error(f"Error exporting to PDF: {e}")
            raise

    @staticmethod
    def export_to_epub(book_data: Dict) -> bytes:
        """Export book to ePub (placeholder)"""
        # TODO: Implement ePub export using ebooklib
        logger.warning("ePub export not yet implemented")
        return b""

export_service = ExportService()
