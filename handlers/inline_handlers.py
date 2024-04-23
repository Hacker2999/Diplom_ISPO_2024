from aiogram import types

from database import get_schedule_for_group, get_schedules_for_teacher
from main import dp, bot
from utils import format_schedule  # Assuming you have a utility function for formatting


@dp.inline_handler()
async def inline_query_handler(inline_query: types.InlineQuery):
    query_text = inline_query.query.strip().lower()
    if not query_text:
        return

    # Implement search logic based on query text
    results = []
    if query_text.isdigit():
        # Search by group number
        schedule = get_schedule_for_group(query_text)  # Replace with your implementation
        if schedule:
            results.append(
                types.InlineQueryResultArticle(
                    id=f"group_{query_text}",
                    title=f"Group {query_text} Schedule",
                    input_message_content=types.InputTextMessageContent(
                        message_text=format_schedule(schedule)
                    )
                )
            )
    else:
        # Search by teacher name (you can extend this for other search options)
        teacher_schedules = get_schedules_for_teacher(query_text)  # Replace with your implementation
        if teacher_schedules:
            for schedule in teacher_schedules:
                results.append(
                    types.InlineQueryResultArticle(
                        id=f"teacher_{schedule['teacher_name']}",
                        title=f"{schedule['teacher_name']} Schedule",
                        input_message_content=types.InputTextMessageContent(
                            message_text=format_schedule(schedule)
                        )
                    )
                )

    await bot.answer_inline_query(inline_query.id, results)
