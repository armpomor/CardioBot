from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    entry: Entry
    entries: Entries
    geting: Geting
    enter: Enter
    diary: Diary
    doctor: Doctor
    quest: Quest
    cancel: Cancel
    change: Change
    save: Save
    you: You
    systolic: Systolic
    diastolic: Diastolic
    edit: Edit
    but: But
    press: Press

    @staticmethod
    def hello(*, username) -> Literal["""Привет { $username }!"""]: ...

    @staticmethod
    def firstrow() -> Literal["""Это дневник контроля артериального давления."""]: ...

    @staticmethod
    def secondrow() -> Literal["""Он поможет отслеживать ваши давление, пульс и самочувствие."""]: ...

    @staticmethod
    def thirdrow() -> Literal["""Врачи рекомендуют заполнять такие дневники каждый день."""]: ...

    @staticmethod
    def fourthrow() -> Literal["""Врач получит более достоверную информацию о состоянии"""]: ...

    @staticmethod
    def fifthrow() -> Literal["""вашего здоровья и сможет отметить, в какое время вы находитесь в зоне риска,"""]: ...

    @staticmethod
    def sixthrow() -> Literal["""и когда вам лучше всего принимать необходимые препараты."""]: ...

    @staticmethod
    def seventhrow() -> Literal["""Немного о том как вести дневник."""]: ...

    @staticmethod
    def eighthrow() -> Literal["""Измерять давление лучше утром, в обед и вечером."""]: ...

    @staticmethod
    def ninthrow() -> Literal["""Желательно указывать общее самочувствие, какие лекарства были приняты."""]: ...

    @staticmethod
    def tenthrow() -> Literal["""Если вдруг бот сломается или вы захотите связаться со мной, напишите"""]: ...

    @staticmethod
    def eleventhrow() -> Literal["""Для того чтобы получить дневник по email, необходимо ввести ваш email-адрес."""]: ...

    @staticmethod
    def twelfthrow() -> Literal["""Необходимая формальность: отправляя email-адрес, вы соглашаетесь на обработку"""]: ...

    @staticmethod
    def thirteenthrow() -> Literal["""данных"""]: ...

    @staticmethod
    def fourteenthrow() -> Literal["""Пользуйтесь моими ботами:"""]: ...

    @staticmethod
    def fiveteenthrow() -> Literal["""Бот по проверке препаратов на наличие доказанной эффективности."""]: ...

    @staticmethod
    def sixteenthrow() -> Literal["""Справочник по лекарственным препаратам."""]: ...

    @staticmethod
    def seventeenthrow() -> Literal["""Справочник по лекарственным растениям."""]: ...

    @staticmethod
    def eighteenthrow() -> Literal["""Управлять ботом можно с помощью кнопок 👇"""]: ...

    @staticmethod
    def missed() -> Literal["""Записать данные в дневник за прошедшую дату"""]: ...

    @staticmethod
    def timezone() -> Literal["""Изменить часовой пояс"""]: ...

    @staticmethod
    def statistics() -> Literal["""Показать последние 45 записей в виде графика"""]: ...

    @staticmethod
    def deletion() -> Literal["""Удалить"""]: ...

    @staticmethod
    def pulse() -> Literal["""Пульс"""]: ...

    @staticmethod
    def arrhythmia() -> Literal["""Артимия"""]: ...

    @staticmethod
    def comment() -> Literal["""Комментарий"""]: ...

    @staticmethod
    def sending() -> Literal["""Отправить"""]: ...

    @staticmethod
    def sending_diary(*, email) -> Literal["""Чтобы отправить дневник на { $email }, нажмите кнопку &#34;Отправить&#34;"""]: ...

    @staticmethod
    def question_send(*, email) -> Literal["""Отправить дневник на адрес { $email }?"""]: ...

    @staticmethod
    def change_email() -> Literal["""Изменить email"""]: ...

    @staticmethod
    def no_email() -> Literal["""Чтобы отправить дневник, сначала необходимо ввести email."""]: ...

    @staticmethod
    def next_start() -> Literal["""Для продолжения работы с ботом нажмите кнопку &#34;Старт&#34;"""]: ...

    @staticmethod
    def start() -> Literal["""Старт"""]: ...

    @staticmethod
    def no_data() -> Literal["""Сначала необходимо сделать хотя бы одну запись в дневнике."""]: ...

    @staticmethod
    def but_next() -> Literal["""Далее"""]: ...

    @staticmethod
    def next_del_data() -> Literal["""Чтобы удалить все свои записи нажмите &#34;Далее&#34;"""]: ...

    @staticmethod
    def next_send_email() -> Literal["""Для отправки дневника по email нажмите &#34;Далее&#34;"""]: ...

    @staticmethod
    def show_or_cancel_graph() -> Literal["""Чтобы показать график, нажмите &#34;Показать график&#34;"""]: ...

    @staticmethod
    def three_diary_entries() -> Literal["""Для построения графика необходимо минимум три записи в дневнике."""]: ...

    @staticmethod
    def show_graph() -> Literal["""Показать график"""]: ...

    @staticmethod
    def next_table() -> Literal["""Чтобы получить дневник в виде таблицы нажмите &#34;Далее&#34;"""]: ...

    @staticmethod
    def receive_diary() -> Literal["""Чтобы получить дневник, нажмите &#34;Получить дневник&#34;"""]: ...

    @staticmethod
    def get_table() -> Literal["""Получить дневник"""]: ...

    @staticmethod
    def next_display_entry() -> Literal["""Чтобы вывести на экран последние 20 записей нажмите &#34;Далее&#34;"""]: ...

    @staticmethod
    def utc1() -> Literal["""UTC+1 - Лондон"""]: ...

    @staticmethod
    def utc2() -> Literal["""UTC+2 - Калининград"""]: ...

    @staticmethod
    def utc3() -> Literal["""UTC+3 - Москва"""]: ...

    @staticmethod
    def utc4() -> Literal["""UTC+4 - Самара"""]: ...

    @staticmethod
    def utc5() -> Literal["""UTC+5 - Екатеринбург"""]: ...

    @staticmethod
    def utc6() -> Literal["""UTC+6 - Омск"""]: ...

    @staticmethod
    def utc7() -> Literal["""UTC+7 - Томск"""]: ...

    @staticmethod
    def utc8() -> Literal["""UTC+8 - Иркутск"""]: ...

    @staticmethod
    def utc9() -> Literal["""UTC+9 - Якутск"""]: ...

    @staticmethod
    def utc10() -> Literal["""UTC+10 - Владивосток"""]: ...

    @staticmethod
    def utc11() -> Literal["""UTC+11 - Магадан"""]: ...

    @staticmethod
    def utc12() -> Literal["""UTC+12 - Петропавловск-Камчатский"""]: ...

    @staticmethod
    def select_timezone() -> Literal["""Выберете часовой пояс, чтобы время в вашем дневнике отображалось корректно."""]: ...

    @staticmethod
    def save_timezone() -> Literal["""Чтобы сохранить часовой пояс, нажмите кнопку &#34;Сохранить&#34;."""]: ...

    @staticmethod
    def confirm_delete() -> Literal["""Все ваши записи удалены."""]: ...

    @staticmethod
    def send_diary() -> Literal["""Дневник отправлен!"""]: ...

    @staticmethod
    def save_email() -> Literal["""Email сохранен!"""]: ...

    @staticmethod
    def save_result() -> Literal["""Данные сохранены!"""]: ...

    @staticmethod
    def update_save() -> Literal["""Данные обновлены и сохранены."""]: ...

    @staticmethod
    def saving_timezone() -> Literal["""Часовой пояс сохранен!"""]: ...

    @staticmethod
    def input_email() -> Literal["""Введите email, на который будет выслан ваш дневник"""]: ...

    @staticmethod
    def edit_cancel() -> Literal["""Отменить редактирование"""]: ...

    @staticmethod
    def date_selection() -> Literal["""Выберете дату когда были сделаны измерения"""]: ...

    @staticmethod
    def time_selection() -> Literal["""Выберете час когда были сделаны измерения"""]: ...

    @staticmethod
    def entry_systolic() -> Literal["""Введите показатель верхнего (систолического) давления"""]: ...

    @staticmethod
    def entry_diastolic() -> Literal["""Введите показатель нижнего (диастолического) давления"""]: ...

    @staticmethod
    def entry_pulse() -> Literal["""Bведите показатель вашего пульса."""]: ...

    @staticmethod
    def entry_zero() -> Literal["""Если вы пульс не измеряли, введите ноль."""]: ...

    @staticmethod
    def presence_arrhythmia() -> Literal["""Отметьте есть ли у вас, в данный момент аритмия"""]: ...

    @staticmethod
    def write_comment() -> Literal["""Напишите в сообщении комментарий о вашем самочувствии и какие были приняты лекарства"""]: ...

    @staticmethod
    def press_save() -> Literal["""Нажмите кнопку &#34;Сохранить&#34; для сохранения введенных данных"""]: ...

    @staticmethod
    def word_yes() -> Literal["""Да"""]: ...

    @staticmethod
    def word_no() -> Literal["""Нет"""]: ...

    @staticmethod
    def unknown() -> Literal["""Неизвестно"""]: ...

    @staticmethod
    def delete_edit_row(*, result) -> Literal["""Запись с датой { $result } удалить или редактировать?"""]: ...

    @staticmethod
    def delete_row(*, result) -> Literal["""Удалить запись с датой { $result }"""]: ...

    @staticmethod
    def edit_row(*, result) -> Literal["""Редактировать запись с датой { $result }"""]: ...

    @staticmethod
    def mark_row() -> Literal["""Отметьте запись, которую необходимо отредактировать или удалить 👇"""]: ...

    @staticmethod
    def word_was() -> Literal["""Было:"""]: ...

    @staticmethod
    def row_delete() -> Literal["""Запись удалена"""]: ...

    @staticmethod
    def incorrect_input() -> Literal["""Некорректный ввод. Попробуйте еще раз."""]: ...

    @staticmethod
    def cancel_input() -> Literal["""Если хотите отменить ввод, нажмите &#34;Отмена&#34;"""]: ...

    @staticmethod
    def long_comment() -> Literal["""Слишком длинный комментарий. Уменьшите количество символов до 50."""]: ...

    @staticmethod
    def text_email() -> Literal["""Привет! Это CardioBot. На это письмо не надо отвечать. Дневник артериального давления во вложении к этому письму."""]: ...

    @staticmethod
    def service_mode() -> Literal["""Бот в режиме обслуживания. Пожалуйста, подождите."""]: ...

    @staticmethod
    def you_banned() -> Literal["""Вас забанили в боте!"""]: ...


class Entry:
    @staticmethod
    def __call__() -> Literal["""Записать в дневник измеренные данные"""]: ...

    @staticmethod
    def cancel() -> Literal["""Отменить ввод данных"""]: ...


class Entries:
    @staticmethod
    def display() -> Literal["""Вывести на экран последние 20 записей"""]: ...


class Geting:
    @staticmethod
    def diary() -> Literal["""Получить дневник в виде таблицы Exel"""]: ...


class Deletion:
    @staticmethod
    def diary() -> Literal["""Удалить дневник со всеми записями"""]: ...


class Enter:
    @staticmethod
    def email() -> Literal["""Ввести или заменить email для отправки дневника"""]: ...


class Diary:
    @staticmethod
    def send() -> Literal["""Отправить на почту дневник в виде таблицы"""]: ...


class Doctor:
    @staticmethod
    def send() -> Literal["""Отправить дневник вашему врачу на почту"""]: ...


class Quest:
    @staticmethod
    def deletion() -> Literal["""Вы действительно хотите удалить все ваши записи?"""]: ...


class Cancel:
    @staticmethod
    def deletion() -> Literal["""Отменить удаление"""]: ...


class Change:
    @staticmethod
    def systolic() -> Literal["""Изменить систолическое давление"""]: ...

    @staticmethod
    def diastolic() -> Literal["""Изменить диастолическое давление"""]: ...

    @staticmethod
    def pulse() -> Literal["""Изменить пульс"""]: ...

    @staticmethod
    def arrhythmia() -> Literal["""Изменить наличие аритмии"""]: ...

    @staticmethod
    def comment() -> Literal["""Изменить комментарий"""]: ...


class Save:
    @staticmethod
    def data() -> Literal["""Сохранить данные"""]: ...

    @staticmethod
    def email() -> Literal["""Чтобы сохранить email, нажмите кнопку &#34;Сохранить&#34;."""]: ...


class You:
    @staticmethod
    def entered() -> Literal["""Вы ввели"""]: ...


class Systolic:
    @staticmethod
    def press() -> Literal["""Систолическое давление"""]: ...


class Diastolic:
    @staticmethod
    def press() -> Literal["""Диастолическое давление"""]: ...


class Edit:
    @staticmethod
    def cancel() -> Literal["""Отменить изменение данных"""]: ...


class But:
    @staticmethod
    def cancel() -> Literal["""Отмена"""]: ...


class Press:
    @staticmethod
    def cancel() -> Literal["""Для отмены нажмите &#34;Отмена&#34;"""]: ...

    @staticmethod
    def save() -> Literal["""Сохранить"""]: ...

