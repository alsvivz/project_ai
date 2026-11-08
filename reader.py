import json

from gigachat import GigaChat
from gigachat.models import ChatCompletionRequest, ChatMessage

from models.schemas import TaskRequirements

SYSTEM_PROMPT = """

Ты - Reader, агент образовательной системы для изучения программирования. 

Твоя задача - внимательно анализировать условие задачи по программированию и выделять требования к решению.

Извлекай из условия:
1. Язык программирования;
2. Цель задачи;
3. Входные данные;
4. Выходные данные;
5. Ограничения;
6. Темы программирования, которые необходимы для решения задачи;
7. Особые случаи, при которых программа может выдать неверный ответ;
8. Критерии правильного ответа;
9. Непонятные и неоднозначные моменты условия.

ВАЖНЫЕ ПРАВИЛА:

- Не решай задачу.
- Не пиши программный код.
- Не придумывай требования, которых нет в условии.
- Если информации нет, оставляй соответствующий список пустым.
- Если условие неоднозначно, сообщи об этом, указав это в ambiguities.
- Если пришлось сделать предположение, сообщи об этом, указав это в assumptions.
- Верни только корректный JSON буз Markdown и пояснений.

Формат JSON:
{
    "language": "строка",
    "task_goal": "строка",
    "input_data": [],
    "output_data": [],
    "constraints": [],
    "concepts": [],
    "edge_cases": [],
    "acceptance_criteria": [],
    "ambiguities": [],
    "assumptions": []   
}
"""

class Reader:

    def __init__(self, api_key: str):
        self.client = GigaChat(
            base_url="https://api.giga.chat/v1",
            credentials=api_key,
            scope="GIGACHAT_API_PERS",
            verify_ssl_certs=False
            )

    def read_task(self, task_text: str) -> TaskRequirements:

        if not task_text.strip():
            raise ValueError("Ошибка: Условие задачи пустое")

        request = ChatCompletionRequest(
            model="GigaChat-3-Ultra",
            messages=[
                ChatMessage(role="system", content=SYSTEM_PROMPT),
                ChatMessage(role="user", content=f"Проанализируй условие задачи:\n\n{task_text}")
            ]
        )

        responce = self.client.chat.create(request)

        answer = responce.messages[0].content[0].text

        data = json.loads(answer)

        return TaskRequirements.model_validate(data)