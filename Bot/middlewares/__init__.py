from aiogram import Dispatcher


def register_middlewares(dp: Dispatcher) -> None:
    from .banned import ShadowBanMiddleware
    from .add_user import AddUserMiddleware
    from .throttling import ThrottlingMiddleware
    from .i18n import TranslatorRunnerMiddleware

    dp.message.middleware(ShadowBanMiddleware())
    dp.message.middleware(AddUserMiddleware())
    dp.message.middleware(ThrottlingMiddleware())
    dp.update.middleware(TranslatorRunnerMiddleware())
