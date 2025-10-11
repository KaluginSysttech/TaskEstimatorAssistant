"""Тесты для LLM клиента."""

from pathlib import Path

import pytest

from llm.llm_client import LLMClient


def test_load_system_prompt_from_file(tmp_path: Path) -> None:
    """Тест загрузки системного промпта из файла."""
    # Arrange: создаем временный файл с промптом
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    prompt_file = prompts_dir / "system_prompt.txt"
    test_prompt = "Ты помощник по оценке задач."
    prompt_file.write_text(test_prompt, encoding="utf-8")

    # Act: создаем LLMClient с указанием пути к промпту
    client = LLMClient(
        api_key="test_key",
        model="test_model",
        timeout=30,
        system_prompt_path=str(prompt_file),
    )

    # Assert: проверяем что промпт загружен
    assert client.system_prompt == test_prompt


def test_load_system_prompt_file_not_found() -> None:
    """Тест ошибки при отсутствии файла с промптом."""
    # Arrange: несуществующий путь
    nonexistent_path = "prompts/nonexistent.txt"

    # Act & Assert: должна быть ошибка FileNotFoundError
    with pytest.raises(FileNotFoundError, match="System prompt file not found"):
        LLMClient(
            api_key="test_key",
            model="test_model",
            timeout=30,
            system_prompt_path=nonexistent_path,
        )


def test_load_system_prompt_empty_file(tmp_path: Path) -> None:
    """Тест ошибки при пустом файле промпта."""
    # Arrange: создаем пустой файл
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    prompt_file = prompts_dir / "system_prompt.txt"
    prompt_file.write_text("", encoding="utf-8")

    # Act & Assert: должна быть ошибка ValueError
    with pytest.raises(ValueError, match="System prompt file is empty"):
        LLMClient(
            api_key="test_key",
            model="test_model",
            timeout=30,
            system_prompt_path=str(prompt_file),
        )


def test_load_system_prompt_whitespace_only(tmp_path: Path) -> None:
    """Тест ошибки при файле содержащем только пробелы."""
    # Arrange: создаем файл с пробелами
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    prompt_file = prompts_dir / "system_prompt.txt"
    prompt_file.write_text("   \n\n  \t  ", encoding="utf-8")

    # Act & Assert: должна быть ошибка ValueError
    with pytest.raises(ValueError, match="System prompt file is empty"):
        LLMClient(
            api_key="test_key",
            model="test_model",
            timeout=30,
            system_prompt_path=str(prompt_file),
        )
