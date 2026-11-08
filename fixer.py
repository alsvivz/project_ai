import json
import os

from gigachat import GigaChat
from gigachat.models import ChatCompletionRequest, ChatMessage
from pydantic import BaseModel, Field

class FixedResult(BaseModel):
  fixed_code: str = Field(description="Исправленный код")
  explanation: str = Field(description="Объяснение изменений")

SYSTEM_PROMPT = """
Ты - Fixer, агент образовательной системы для изучения программирования.

Твоя задача - исправить ошибки в коде на основе списка проблем, найденных Analyzer.

ВАЖНЫЕ ПРАВИЛА:
1. Исправляй ТОЛЬКО те ошибки, которые есть в списке.
2. Минимально меняй код. Не переписывай всё решение, если можно изменить пару строк.
3. Если в списке ошибок пусто, верни исходный код без изменений.
4. Верни ответ СТРОГО в формате JSON без Markdown и пояснений.

Формат JSON:
{
  "fixed_code": "текст исправленного кода",
  "explanation": "краткое описание того, что было изменено"
}
"""

class Fixer:

  def __init__(self, api_key: str):
    self.client = GigaChat(
      base_url="https://api.giga.chat/v1",
      credentials=api_key,
      scope="GIGACHAT_API_PERS",
      verify_ssl_certs=False
      )

  def fix_code(self, task_text: str, code_text: str, issues_json: str) -> FixedResult:

    if not code_text.strip():
      raise ValueError("Ошибка: Код пустой")

    request = ChatCompletionRequest(
      model="GigaChat-3-Ultra",
      messages=[
        ChatMessage(role="system", content=SYSTEM_PROMPT),
        ChatMessage(role="user", content=f"Условие задачи:\n{task_text}\n\nИсходный код:\n{code_text}\n\nНайденные ошибки:\n{issues_json}")
      ]
    )

    response = self.client.chat.create(request)

    answer = response.messages[0].content[0].text
    answer = answer.replace("```json", "").replace("```", "").strip()

    data = json.loads(answer)

    return FixedResult.model_validate(data)