from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub


def create_translator_hub() -> TranslatorHub:
    """
    Create an object of the TranslatorHub class
    :return:
    """
    translator_hub = TranslatorHub(
        locales_map={"ru": ("ru", "en"), "en": ("en", "ru"), "pl": ("pl", "ru")},
        translators=[
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru-RU", filenames=["locales/ru/LC_MESSAGES/txt.ftl"]
                ),
            ),
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_files(
                    locale="en-US", filenames=["locales/en/LC_MESSAGES/txt.ftl"]
                ),
            ),
            FluentTranslator(
                locale="pl",
                translator=FluentBundle.from_files(
                    locale="pl-PL", filenames=["locales/pl/LC_MESSAGES/txt.ftl"]
                ),
            ),
        ],
    )

    return translator_hub
