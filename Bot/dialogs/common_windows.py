"""
Module for common and similar Window in dialogs
"""

from aiogram.fsm.state import State
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.input.text import OnSuccess, OnError
from aiogram_dialog.widgets.kbd import Next, Cancel
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.utils import GetterVariant

from dialogs.getters.getters import get_texts_finished, get_texts_input_email
from utils.data_checking import check_email


class WindowNoRows(Window):
    """
    Window in which it is checked whether there is
    the user has entries in UserData or
    Person. If not, then the dialogue is interrupted,
    if there is dialogue continues.
    """

    def __init__(
        self,
        state: State,
        getter: GetterVariant,
        txt: str,
        when_1: str,
        when_2: str,
        click=None,
        *args,
        **kwargs,
    ):
        self.txt = txt
        self.state = state
        self.getter = getter
        self.when_1 = when_1
        self.when_2 = when_2
        self.click = click
        super().__init__(
            Format(
                f"{self.txt}",
                when=self.when_1,
            ),
            Next(text=Format("{but_next}"), when=self.when_1, on_click=self.click),
            Cancel(
                Format("{but_cancel}"),
                when=self.when_1,
            ),
            Format(
                "{no_data}",
                when=self.when_2,
            ),
            Cancel(Format("{start}"), id="but_start", when=self.when_2),
            state=self.state,
            getter=self.getter,
        )


class WindowFinished(Window):
    """
    Final Window for dialogues.
    It informs you that the data has been saved
    or certain actions have been performed
    and it is suggested to go to start_dialog
    """

    def __init__(self, state: State, txt: str, *args, **kwargs):
        self.txt = txt
        self.state = state
        super().__init__(
            Format(f"{self.txt}"),
            Cancel(Format("{start}")),
            state=self.state,
            getter=get_texts_finished,
        )


class WindowInputEmail(Window):
    """
    Window for entering email. General
    for email_dialog and doctor_dialog
    """

    def __init__(
        self, state: State, success: OnSuccess, error: OnError, *args, **kwargs
    ):
        self.state = state
        self.success = success
        self.error = error
        super().__init__(
            Format(text="{input_email}"),
            TextInput(
                id="email",
                type_factory=check_email,
                on_success=self.success,
                on_error=self.error,
            ),
            Cancel(Format("{but_cancel}"), id="but_cancel"),
            state=self.state,
            getter=get_texts_input_email,
        )
