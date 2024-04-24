from aiogram import types
from database import get_schedule_for_group, get_schedules_for_teacher  # Импорт функций для работы с БД

# Обработчик инлайн-запросов
async def inline_query_handler(inline_query: types.InlineQuery):
    query_text = inline_query.query.strip().lower()
    if not query_text:
        return

    results = []

    if query_text.isdigit():
        # Поиск по номеру группы
        schedule = get_schedule_for_group(query_text)
        if schedule:
            results.append(
                types.InlineQueryResultArticle(
                    id=query_text,
                    title=f"Расписание группы {query_text}",
                    input_message_content=types.InputTextMessageContent(
                        message_text=schedule
                    )
                )
            )
    else:
        # Поиск по фамилии преподавателя
        teacher_schedules = get_schedules_for_teacher(query_text)
        if teacher_schedules:
            for schedule in teacher_schedules:
                results.append(
                    types.InlineQueryResultArticle(
                        id=schedule['id'],
                        title=f"Расписание преподавателя {query_text}",
                        input_message_content=types.InputTextMessageContent(
                            message_text=schedule['schedule']
                        )
                    )
                )

    await inline_query.answer(results)
