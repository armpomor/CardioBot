from aiogram import Router


def get_dialogs() -> Router:
    from . import (
        delete_dialog,
        doctor_dialog,
        email_dialog,
        entry_dialog,
        send_dialog,
        start_dialog,
        statistics_dialog,
        table_output_dialog,
        table_widgets_dialog,
        timezone_dialog,
    )

    router = Router()
    router.include_router(delete_dialog.delete_dialog)
    router.include_router(doctor_dialog.doctor_dialog)
    router.include_router(email_dialog.email_dialog)
    router.include_router(entry_dialog.entry_dialog)
    router.include_router(send_dialog.send_dialog)
    router.include_router(start_dialog.start_dialog)
    router.include_router(statistics_dialog.statistics_dialog)
    router.include_router(table_output_dialog.table_output_dialog)
    router.include_router(table_widgets_dialog.table_widgets_dialog)
    router.include_router(timezone_dialog.timezone_dialog)

    return router
