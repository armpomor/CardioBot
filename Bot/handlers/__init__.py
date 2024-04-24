from aiogram import Router


def get_handlers() -> Router:
    from . import other_handlers, user_handlers

    router = Router()
    router.include_router(other_handlers.maintenance_router)
    router.include_router(user_handlers.router)

    return router
