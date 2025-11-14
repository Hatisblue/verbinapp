"""
Google Gemini AI service
"""
import os
import logging
from typing import Dict, List, Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-pro")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    logger.warning("GEMINI_API_KEY not set. Gemini service will not work.")


class GeminiService:
    """Service for interacting with Google Gemini AI"""

    def __init__(self):
        self.model = genai.GenerativeModel(GEMINI_MODEL)

    async def generate_book(
        self,
        plot: str,
        language: str = "ru",
        age_group: str = "7-12",
        pages: int = 10,
        style: str = "сказка",
        system_prompt: Optional[str] = None
    ) -> Dict:
        """
        Generate a book using Gemini AI

        Args:
            plot: User's plot description
            language: Book language
            age_group: Target age group
            pages: Number of pages to generate
            style: Book style (e.g., сказка, приключение)
            system_prompt: Optional system prompt override

        Returns:
            Dictionary with book data (title, description, chapters)
        """
        try:
            # Build the prompt
            if not system_prompt:
                system_prompt = (
                    "Вы - искусственный интеллект BookCreator AI, специализирующийся на создании детских книг. "
                    "Ваша задача - создать увлекательную, образовательную и безопасную книгу для детей. "
                    "Используйте простой язык, яркие образы и позитивные сюжеты."
                )

            user_prompt = f"""
Создайте детскую книгу со следующими параметрами:

Сюжет: {plot}
Язык: {language}
Возрастная группа: {age_group} лет
Стиль: {style}
Количество страниц: {pages}

Требования:
1. Создайте привлекательное название книги
2. Напишите краткое описание (синопсис) в 2-3 предложениях
3. Создайте {pages} страниц с интересным содержанием
4. Каждая страница должна содержать 3-5 абзацев текста
5. Адаптируйте сложность текста для возраста {age_group} лет
6. Используйте позитивные темы и безопасный контент
7. Добавьте описания для иллюстраций к каждой странице

Верните результат в следующем JSON формате:
{{
    "title": "Название книги",
    "description": "Краткое описание книги",
    "chapters": [
        {{
            "number": 1,
            "title": "Название главы",
            "content": "Текст главы",
            "illustration_prompt": "Описание иллюстрации для генерации"
        }},
        ...
    ]
}}
"""

            # Generate content
            logger.info(f"Generating book with Gemini: {GEMINI_MODEL}")
            response = self.model.generate_content(
                [system_prompt, user_prompt],
                generation_config=genai.GenerationConfig(
                    temperature=0.9,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=8192,
                )
            )

            # Parse response
            import json
            text = response.text.strip()

            # Try to extract JSON from markdown code blocks if present
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()

            book_data = json.loads(text)

            logger.info(f"Successfully generated book: {book_data.get('title')}")
            return book_data

        except Exception as e:
            logger.error(f"Error generating book with Gemini: {e}")
            raise

    async def moderate_content(self, text: str) -> Dict[str, any]:
        """
        Moderate content for inappropriate material

        Args:
            text: Content to moderate

        Returns:
            Dictionary with moderation results
        """
        try:
            prompt = f"""
Проверьте следующий текст на наличие неприемлемого содержания для детской книги:
- Нецензурная лексика
- Насилие
- Сексуальный контент
- Дискриминация
- Другой вредный контент

Текст: {text}

Верните результат в JSON формате:
{{
    "is_safe": true/false,
    "issues": ["список проблем, если есть"],
    "severity": "none/low/medium/high"
}}
"""

            response = self.model.generate_content(prompt)
            import json
            text = response.text.strip()

            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()

            result = json.loads(text)
            return result

        except Exception as e:
            logger.error(f"Error moderating content: {e}")
            # If moderation fails, be cautious and mark as unsafe
            return {"is_safe": False, "issues": ["Moderation service error"], "severity": "high"}

    async def improve_text(self, text: str, action: str = "improve") -> str:
        """
        Improve or modify text

        Args:
            text: Text to improve
            action: Action to perform (improve, simplify, expand)

        Returns:
            Improved text
        """
        try:
            prompts = {
                "improve": "Улучшите следующий текст, сделав его более интересным и литературным:",
                "simplify": "Упростите следующий текст для детей 7-9 лет:",
                "expand": "Расширьте следующий текст, добавив больше деталей и описаний:"
            }

            prompt = f"{prompts.get(action, prompts['improve'])}\n\n{text}"
            response = self.model.generate_content(prompt)

            return response.text.strip()

        except Exception as e:
            logger.error(f"Error improving text: {e}")
            return text  # Return original text on error


# Singleton instance
gemini_service = GeminiService()
