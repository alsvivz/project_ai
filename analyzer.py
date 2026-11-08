import json

from gigachat import GigaChat
from gigachat.models import ChatCompletionRequest, ChatMessage
from pydantic import BaseModel, Field
from typing import List

class CodeIssue(BaseModel):
 line: int = Field(description="Номер строки с ошибкой")
 description: str = Field(description="Описание ошибки")

class AnalysisResult(BaseModel):
 errors: List[CodeIssue] = Field(description="Список найденных ошибок")

SYSTEM_PROMPT = """
Ты - Analyzer, агент образовательной системы для изучения программирования.

Твоя задача - проверить предоставленный код на соответствие условию задачи и найти в нем ошибки.

Анализируй:
1. Синтаксические ошибки;
2. Логические ошибки;
3. Несоответствия требованиям задачи (входные/выходные данные);
4. Возможные баги (например, деление на ноль, выход за границы массива);
5. Проблемы с производительностью.

ВАЖНЫЕ ПРАВИЛА:
- Не исправляй код. Ты только ищешь проблемы.
- Не пиши программный код в ответе.
- Если ошибок нет, верни пустой список errors.
- Верни только корректный JSON без Markdown и пояснений.

Формат JSON:
{
 "errors": [
  {
   "line": 5,
   "description": "Описание того, что не так"
  }
 ]
}
"""

class Analyzer:

 def __init__(self, api_key: str):
  self.client = GigaChat(
   base_url="https://api.giga.chat/v1",
   credentials=api_key,
   scope="GIGACHAT_API_PERS",
   verify_ssl_certs=False
   )

 def analyze_code(self, task_text: str, code_text: str) -> AnalysisResult:

  if not code_text.strip():
   raise ValueError("Ошибка: Код пустой")

  request = ChatCompletionRequest(
   model="GigaChat-3-Ultra",
   messages=[
    ChatMessage(role="system", content=SYSTEM_PROMPT),
    ChatMessage(role="user", content=f"Условие задачи:\n{task_text}\n\nКод для анализа:\n{code_text}")
   ]
  )

  response = self.client.chat.create(request)

  answer = response.messages[0].content[0].text

  answer = answer.replace("```json", "").replace("```", "").strip()

  data = json.loads(answer)

  return AnalysisResult.model_validate(data)