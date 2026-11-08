import os
from dotenv import load_dotenv

from reader import Reader
from analyzer import Analyzer
from fixer import Fixer

load_dotenv()

if __name__ == "__main__":
    api_key = os.getenv("GIGACHAT_CREDENTIALS")
    
    if not api_key:
        print("Ошибка: Ключ GIGACHAT_CREDENTIALS не найден в файле .env")
    else:
        reader = Reader(api_key=api_key)
        analyzer = Analyzer(api_key=api_key)
        fixer = Fixer(api_key=api_key)
        
        test_task = "Написать функцию сложения двух чисел"
        test_code = "def add(a, b):\n    return a - b"
        
        try:
            print("--- ЭТАП 1: READER ---")
            print("Анализируем условие задачи...")
            requirements = reader.read_task(test_task)
            print(f"✅ Reader понял задачу! Цель: {requirements.task_goal}")
            
            print("\n--- ЭТАП 2: ANALYZER ---")
            print("Ищем ошибки в коде...")
            analysis_result = analyzer.analyze_code(test_task, test_code)
            
            with open("analysis_result.json", "w", encoding="utf-8") as f:
                f.write(analysis_result.model_dump_json(indent=4))
                
            print(f"✅ Найдено ошибок: {len(analysis_result.errors)}")
            for err in analysis_result.errors:
                print(f"  - Строка {err.line}: {err.description}")
            
            print("\n--- ЭТАП 3: FIXER ---")
            print("Исправляем найденные ошибки...")
            
            issues_json = analysis_result.model_dump_json()
            fix_result = fixer.fix_code(test_task, test_code, issues_json)
            
            with open("fixed_result.json", "w", encoding="utf-8") as f:
                f.write(fix_result.model_dump_json(indent=4))
                
            print("✅ Исправление готово!")
            print(f"Объяснение: {fix_result.explanation}")
            print("\nИсправленный код:")
            print(fix_result.fixed_code)
            
        except Exception as e:
            print(f"\n❌ Произошла ошибка: {e}")