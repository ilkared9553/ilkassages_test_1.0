
================================================================================
MESSENGER APPLICATION ilkassages — ПОЛНАЯ ИСПРАВЛЕННАЯ ВЕРСИЯ
================================================================================
ИНСТРУКЦИЯ ПО ЗАПУСКУ
1. pip install -r requirements.txt
2. python main.py

ИНСТРУКЦИЯ ДЛЯ СБОРКИ В APK (BUILDOZER)
buildozer -v android debug
================================================================================


import os
import sys
import re
import hashlib
import sqlite3
from datetime import datetime

# Настройка конфигурации Kivy перед импортом основных модулей
from kivy.config import Config

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', 'False')

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import TwoLineAvatarIconListItem, ImageLeftWidget, OneLineListItem
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast

# Постоянная ссылка на дефолтную аватарку для предотвращения падений из-за отсутствия файлов
DEFAULT_AVATAR = httpscdn-icons-png.flaticon.com512149149071.png


### SECTION Safe Path Cleaner (Фикс бага AsyncImage) ###
def clean_secure_path(path_str)
    Удаляет управляющие символы типа x14 и нормализует слэши для кроссплатформенности Kivy.
    if not path_str
        return 
    cleaned = re.sub(r'[x00-x1fx7f-x9f]', '', path_str)
    return cleaned.replace('', '')


### SECTION Database Management ###

class DatabaseManager
    def __init__(self, db_name=ilkassages.db)
        self.db_name = db_name
        self.init_db()

    def get_connection(self)
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self)
        with self.get_connection() as conn
            cursor = conn.cursor()
            cursor.execute(
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    display_name TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    avatar_path TEXT NOT NULL
                )
            )
            cursor.execute(
                CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    username TEXT UNIQUE,
                    avatar_path TEXT NOT NULL,
                    creator_id INTEGER NOT NULL
                )
            )
            cursor.execute(
                CREATE TABLE IF NOT EXISTS chat_members (
                    chat_id INTEGER,
                    user_id INTEGER,
                    PRIMARY KEY (chat_id, user_id)
                )
            )
            cursor.execute(
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    sender_id INTEGER,
                    text TEXT,
                    file_path TEXT,
                    timestamp TEXT,
                    is_read INTEGER DEFAULT 0
                )
            )
            cursor.execute(
                CREATE TABLE IF NOT EXISTS contacts (
                    user_id INTEGER,
                    contact_user_id INTEGER,
                    local_name TEXT,
                    PRIMARY KEY (user_id, contact_user_id)
                )
            )
            conn.commit()

    @staticmethod
    def hash_password(password str) - str
        salt = ilkassages_secure_salt_2026_
        return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()


db = DatabaseManager()

### SECTION UI Design Layout (KV) ###

KV_STR = f
ScreenManager
    LoginRegisterScreen
    MainChatsScreen
    ChatScreen
    SettingsScreen

LoginRegisterScreen
    name 'login_register'
    md_bg_color app.theme_cls.bg_normal

    MDBoxLayout
        orientation 'vertical'
        padding dp(24)
        spacing dp(16)
        adaptive_height True
        pos_hint {{center_x 0.5, center_y 0.5}}

        MDLabel
            text ilkassages
            font_style H4
            halign center
            theme_text_color Custom
            text_color 0.14, 0.50, 0.80, 1
            bold True

        MDLabel
            id form_title
            text Вход в аккаунт
            font_style Subtitle1
            halign center
            theme_text_color Secondary

        MDTextField
            id username_input
            hint_text Юзернейм (username)
            helper_text Только латиница и цифры
            helper_text_mode on_focus
            icon_right account
            on_text root.validate_username_realtime(self.text)

        MDTextField
            id display_name_input
            hint_text Отображаемое имя
            icon_right account-card-details
            opacity 0
            disabled True

        MDTextField
            id password_input
            hint_text Пароль
            password True
            icon_right eye-off

        MDRaisedButton
            id submit_btn
            text Войти
            pos_hint {{center_x 0.5}}
            size_hint_x 1
            md_bg_color 0.14, 0.50, 0.80, 1
            on_release root.process_auth()

        MDFlatButton
            id toggle_mode_btn
            text Нет аккаунта Зарегистрироваться
            pos_hint {{center_x 0.5}}
            theme_text_color Custom
            text_color 0.14, 0.50, 0.80, 1
            on_release root.toggle_mode()

MainChatsScreen
    name 'main_chats'
    on_enter root.load_chats()

    MDBoxLayout
        orientation 'vertical'

        MDTopAppBar
            title ilkassages
            elevation 4
            md_bg_color 0.14, 0.50, 0.80, 1
            left_action_items [[menu, lambda x root.open_settings()]]
            right_action_items [[brightness-4, lambda x app.toggle_theme()]]

        MDBoxLayout
            orientation 'horizontal'
            size_hint_y None
            height dp(56)
            padding [dp(12), dp(4), dp(12), dp(4)]
            spacing dp(8)

            MDTextField
                id search_input
                hint_text Поиск @имя (люди) или название (каналы)
                mode rectangle
                size_hint_x 0.85
                on_text_validate root.perform_search()

            MDIconButton
                icon magnify
                pos_hint {{center_y 0.5}}
                on_release root.perform_search()

        ScrollView
            MDList
                id chats_list

    MDFloatingActionButton
        icon plus
        md_bg_color 0.14, 0.50, 0.80, 1
        pos_hint {{right 0.95, bottom 0.05}}
        on_release root.show_plus_menu(self)

ChatScreen
    name 'chat'
    on_enter root.on_screen_enter()

    MDBoxLayout
        orientation 'vertical'

        MDTopAppBar
            id chat_toolbar
            title Чат
            elevation 4
            md_bg_color 0.14, 0.50, 0.80, 1
            left_action_items [[arrow-left, lambda x root.back_to_main()]]
            right_action_items [[pencil, lambda x root.show_rename_dialog()]]

        ScrollView
            id messages_scroll
            MDBoxLayout
                id messages_container
                orientation 'vertical'
                spacing dp(10)
                padding dp(12)
                adaptive_height True

        MDBoxLayout
            orientation 'horizontal'
            size_hint_y None
            height dp(60)
            padding dp(8)
            spacing dp(8)
            md_bg_color app.theme_cls.bg_light

            MDIconButton
                icon paperclip
                pos_hint {{center_y 0.5}}
                on_release root.open_file_manager()

            MDTextField
                id message_input
                hint_text Сообщение...
                multiline False
                pos_hint {{center_y 0.5}}

            MDIconButton
                icon send
                pos_hint {{center_y 0.5}}
                theme_text_color Custom
                text_color 0.14, 0.50, 0.80, 1
                on_release root.send_text_message()

SettingsScreen
    name 'settings'
    on_enter root.load_user_data()

    MDBoxLayout
        orientation 'vertical'

        MDTopAppBar
            title Настройки
            elevation 4
            md_bg_color 0.14, 0.50, 0.80, 1
            left_action_items [[arrow-left, lambda x root.back_to_main()]]

        ScrollView
            MDBoxLayout
                orientation 'vertical'
                padding dp(16)
                spacing dp(20)
                adaptive_height True

                BoxLayout
                    orientation 'vertical'
                    size_hint_y None
                    height dp(120)
                    pos_hint {{center_x 0.5}}
                    spacing dp(8)

                    AsyncImage
                        id avatar_img
                        source {DEFAULT_AVATAR}
                        size_hint (None, None)
                        size (dp(80), dp(80))
                        pos_hint {{center_x 0.5}}
                        allow_stretch True
                        keep_ratio False

                    MDFlatButton
                        text Изменить аватарку
                        pos_hint {{center_x 0.5}}
                        theme_text_color Custom
                        text_color 0.14, 0.50, 0.80, 1
                        on_release root.change_avatar()

                MDTextField
                    id current_username
                    hint_text Ваш юзернейм (Только чтение)
                    readonly True

                MDTextField
                    id edit_display_name
                    hint_text Отображаемое имя

                MDTextField
                    id edit_username
                    hint_text Новый юзернейм

                MDTextField
                    id edit_password
                    hint_text Новый пароль
                    password True

                MDRaisedButton
                    text Сохранить настройки
                    size_hint_x 1
                    md_bg_color 0.14, 0.50, 0.80, 1
                    on_release root.save_settings()

                MDRectangleFlatButton
                    text Выйти из аккаунта
                    size_hint_x 1
                    text_color 1, 0.2, 0.2, 1
                    line_color 1, 0.2, 0.2, 1
                    on_release root.logout()



### SECTION Screens Logic Class Definitions ###

class LoginRegisterScreen(MDScreen)
    is_register_mode = BooleanProperty(False)

    def toggle_mode(self)
        self.is_register_mode = not self.is_register_mode
        if self.is_register_mode
            self.ids.form_title.text = Создание нового профиля
            self.ids.display_name_input.opacity = 1
            self.ids.display_name_input.disabled = False
            self.ids.submit_btn.text = Зарегистрироваться
            self.ids.toggle_mode_btn.text = Уже есть аккаунт Войти
        else
            self.ids.form_title.text = Вход в аккаунт
            self.ids.display_name_input.opacity = 0
            self.ids.display_name_input.disabled = True
            self.ids.submit_btn.text = Войти
            self.ids.toggle_mode_btn.text = Нет аккаунта Зарегистрироваться

    def validate_username_realtime(self, text)
        if not text
            self.ids.username_input.error = False
            return
        cleaned = .join([c for c in text if c.isalnum() or c == '_']).lower()
        if cleaned != text
            self.ids.username_input.text = cleaned
            self.ids.username_input.cursor = (len(cleaned), 0)

    def process_auth(self)
        username = self.ids.username_input.text.strip().lower()
        password = self.ids.password_input.text.strip()
        display_name = self.ids.display_name_input.text.strip()

        if not username or not password
            toast(Заполните основные поля)
            return

        conn = db.get_connection()
        cursor = conn.cursor()

        if self.is_register_mode
            if not display_name
                toast(Введите отображаемое имя)
                conn.close()
                return
            cursor.execute(SELECT id FROM users WHERE username = , (username,))
            if cursor.fetchone()
                toast(Этот юзернейм уже занят!)
                conn.close()
                return

            password_hash = db.hash_password(password)
            cursor.execute(
                INSERT INTO users (username, display_name, password_hash, avatar_path) VALUES (, , , ),
                (username, display_name, password_hash, DEFAULT_AVATAR)
            )
            conn.commit()
            cursor.execute(SELECT  FROM users WHERE username = , (username,))
            user_row = cursor.fetchone()
            toast(Регистрация успешна!)
        else
            password_hash = db.hash_password(password)
            cursor.execute(SELECT  FROM users WHERE username =  AND password_hash = , (username, password_hash))
            user_row = cursor.fetchone()
            if not user_row
                toast(Неверный юзернейм или пароль)
                conn.close()
                return

        app = MDApp.get_running_app()
        app.current_user = {
            id user_row[id],
            username user_row[username],
            display_name user_row[display_name],
            avatar_path clean_secure_path(user_row[avatar_path])
        }
        conn.close()
        self.manager.current = 'main_chats'


class MainChatsScreen(MDScreen)
    plus_menu = None
    active_dialog = None
    chat_dialog = None
    chan_title_field = None
    chan_user_field = None
    chat_user_field = None

    def open_settings(self)
        self.manager.current = 'settings'

    def load_chats(self)
        self.ids.chats_list.clear_widgets()
        app = MDApp.get_running_app()
        if not app.current_user
            return

        conn = db.get_connection()
        cursor = conn.cursor()

        query = 
            SELECT c.id as chat_id, c.type, c.title, c.avatar_path,
                   (SELECT text FROM messages WHERE chat_id = c.id ORDER BY id DESC LIMIT 1) as last_msg,
                   co.local_name
            FROM chats c
            JOIN chat_members cm ON c.id = cm.chat_id
            LEFT JOIN chat_members cm2 ON c.id = cm2.chat_id AND cm2.user_id != 
            LEFT JOIN contacts co ON co.user_id =  AND co.contact_user_id = cm2.user_id
            WHERE cm.user_id =  AND c.type = 'private'
        
        cursor.execute(query, (app.current_user[id], app.current_user[id], app.current_user[id]))
        private_chats = cursor.fetchall()

        cursor.execute(
            SELECT c.id as chat_id, c.type, c.title, c.avatar_path,
                   (SELECT text FROM messages WHERE chat_id = c.id ORDER BY id DESC LIMIT 1) as last_msg,
                   (SELECT COUNT() FROM chat_members WHERE chat_id = c.id) as sub_count
            FROM chats c
            JOIN chat_members cm ON c.id = cm.chat_id
            WHERE cm.user_id =  AND c.type = 'channel'
        , (app.current_user[id],))
        channels = cursor.fetchall()
        conn.close()

        all_items = list(private_chats) + list(channels)
        for item in all_items
            title = item[local_name] if (local_name in item.keys() and item[local_name]) else item[title]
            last_msg = item[last_msg] if item[last_msg] else Нет сообщений
            if item[type] == 'channel'
                last_msg = fКанал ({item['sub_count']} подп.) {last_msg}

            avatar = clean_secure_path(item[avatar_path])
            if not avatar.startswith(http) and not os.path.exists(avatar)
                avatar = DEFAULT_AVATAR

            item_widget = TwoLineAvatarIconListItem(
                text=title,
                secondary_text=last_msg,
                on_release=lambda x, cid=item[chat_id] self.open_chat(cid)
            )
            item_widget.add_widget(ImageLeftWidget(source=avatar))
            self.ids.chats_list.add_widget(item_widget)

    def open_chat(self, chat_id)
        app = MDApp.get_running_app()
        app.current_chat_id = chat_id
        self.manager.current = 'chat'

    ### ОБЯЗАТЕЛЬНЫЙ ПОИСК С СИМВОЛОМ @ ###
    def perform_search(self)
        search_term = self.ids.search_input.text.strip().lower()
        if not search_term
            self.load_chats()
            return

        self.ids.chats_list.clear_widgets()
        app = MDApp.get_running_app()
        conn = db.get_connection()
        cursor = conn.cursor()

        # ЕСЛИ ПОИСК НАЧИНАЕТСЯ С @ - ИЩЕМ ЛЮДЕЙ
        if search_term.startswith('@')
            pure_username = search_term[1]  # Срезаем собачку
            cursor.execute(SELECT  FROM users WHERE username =  AND id != ,
                           (pure_username, app.current_user[id]))
            user_found = cursor.fetchone()

            if user_found
                avatar = clean_secure_path(user_found[avatar_path])
                if not avatar.startswith(http) and not os.path.exists(avatar)
                    avatar = DEFAULT_AVATAR

                item = TwoLineAvatarIconListItem(
                    text=user_found[display_name],
                    secondary_text=fПользователь @{user_found['username']},
                    on_release=lambda x, uid=user_found[id] self.start_private_chat(uid)
                )
                item.add_widget(ImageLeftWidget(source=avatar))
                self.ids.chats_list.add_widget(item)
            else
                self.ids.chats_list.add_widget(OneLineListItem(text=Пользователь не найден))

        # ЕСЛИ БЕЗ @ - ВЫДАЕМ ПОДСКАЗКУ И ИЩЕМ ТОЛЬКО КАНАЛЫ
        else
            self.ids.chats_list.add_widget(OneLineListItem(text=💡 Для поиска людей начните запрос с '@'))

            cursor.execute(SELECT  FROM chats WHERE (username LIKE  OR title LIKE ) AND type = 'channel',
                           (f%{search_term}%, f%{search_term}%))
            channels_found = cursor.fetchall()

            for channel_found in channels_found
                avatar = clean_secure_path(channel_found[avatar_path])
                if not avatar.startswith(http) and not os.path.exists(avatar)
                    avatar = DEFAULT_AVATAR

                item = TwoLineAvatarIconListItem(
                    text=channel_found[title],
                    secondary_text=fПубличный канал @{channel_found['username']},
                    on_release=lambda x, cid=channel_found[id] self.join_channel(cid)
                )
                item.add_widget(ImageLeftWidget(source=avatar))
                self.ids.chats_list.add_widget(item)

            if not channels_found
                self.ids.chats_list.add_widget(OneLineListItem(text=Каналы не найдены))

        conn.close()

    def start_private_chat(self, target_user_id)
        app = MDApp.get_running_app()
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            SELECT cm1.chat_id FROM chat_members cm1
            JOIN chat_members cm2 ON cm1.chat_id = cm2.chat_id
            JOIN chats c ON cm1.chat_id = c.id
            WHERE cm1.user_id =  AND cm2.user_id =  AND c.type = 'private'
        , (app.current_user[id], target_user_id))
        existing = cursor.fetchone()

        if existing
            chat_id = existing[chat_id]
        else
            cursor.execute(SELECT display_name FROM users WHERE id = , (target_user_id,))
            t_name = cursor.fetchone()[display_name]
            cursor.execute(INSERT INTO chats (type, title, avatar_path, creator_id) VALUES ('private', , , ),
                           (t_name, DEFAULT_AVATAR, app.current_user[id]))
            chat_id = cursor.lastrowid
            cursor.execute(INSERT INTO chat_members (chat_id, user_id) VALUES (, ),
                           (chat_id, app.current_user[id]))
            cursor.execute(INSERT INTO chat_members (chat_id, user_id) VALUES (, ), (chat_id, target_user_id))
            conn.commit()

        conn.close()
        self.open_chat(chat_id)

    def join_channel(self, channel_id)
        app = MDApp.get_running_app()
        conn = db.get_connection()
        cursor = conn.cursor()
        try
            cursor.execute(INSERT INTO chat_members (chat_id, user_id) VALUES (, ),
                           (channel_id, app.current_user[id]))
            conn.commit()
            toast(Вы подписались на канал)
        except sqlite3.IntegrityError
            pass
        conn.close()
        self.open_chat(channel_id)

    ### РЕАЛИЗАЦИЯ МЕНЮ ВЫБОРА ЧАТКАНАЛ НА КНОПКЕ ПЛЮС ###
    def show_plus_menu(self, button_instance)
        menu_items = [
            {
                text Создать личный чат,
                viewclass OneLineListItem,
                on_release lambda x=chat self.plus_menu_callback(x),
            },
            {
                text Создать новый канал,
                viewclass OneLineListItem,
                on_release lambda x=channel self.plus_menu_callback(x),
            }
        ]
        self.plus_menu = MDDropdownMenu(
            caller=button_instance,
            items=menu_items,
            width_mult=4,
        )
        self.plus_menu.open()

    def plus_menu_callback(self, selection_type)
        self.plus_menu.dismiss()
        if selection_type == chat
            self.show_create_chat_dialog()
        elif selection_type == channel
            self.show_creation_dialog()

    def show_create_chat_dialog(self)
        self.chat_user_field = Builder.load_string('MDTextFieldn  hint_text Юзернейм собеседника (без @)')
        self.chat_dialog = MDDialog(
            title=Начать личный чат,
            type=custom,
            content_cls=BoxLayout(orientation='vertical', size_hint_y=None, height=dp(56)),
            buttons=[
                MDFlatButton(text=Отмена, on_release=lambda x self.chat_dialog.dismiss()),
                MDRaisedButton(text=Создать, on_release=self.create_chat_flow)
            ]
        )
        self.chat_dialog.content_cls.add_widget(self.chat_user_field)
        self.chat_dialog.open()

    def create_chat_flow(self, instance)
        target_username = self.chat_user_field.text.strip().lower().replace('@', '')
        if not target_username
            return
        app = MDApp.get_running_app()
        if target_username == app.current_user[username]
            toast(Нельзя создать чат с самим собой)
            return

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(SELECT id FROM users WHERE username = , (target_username,))
        user_found = cursor.fetchone()
        conn.close()

        if user_found
            self.chat_dialog.dismiss()
            self.start_private_chat(user_found[id])
        else
            toast(Пользователь не найден)

    def show_creation_dialog(self)
        self.chan_title_field = Builder.load_string('MDTextFieldn  hint_text Название канала')
        self.chan_user_field = Builder.load_string('MDTextFieldn  hint_text Юзернейм канала (без @)')
        self.active_dialog = MDDialog(
            title=Создать новый канал,
            type=custom,
            content_cls=BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(120)),
            buttons=[
                MDFlatButton(text=Отмена, on_release=lambda x self.active_dialog.dismiss()),
                MDRaisedButton(text=Создать канал, on_release=self.create_channel_flow)
            ]
        )
        self.active_dialog.content_cls.add_widget(self.chan_title_field)
        self.active_dialog.content_cls.add_widget(self.chan_user_field)
        self.active_dialog.open()

    def create_channel_flow(self, instance)
        chan_title = self.chan_title_field.text.strip()
        chan_username = self.chan_user_field.text.strip().lower().replace('@', '')

        if not chan_title or not chan_username
            toast(Заполните все поля)
            return

        app = MDApp.get_running_app()
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute(SELECT id FROM chats WHERE username = , (chan_username,))
        if cursor.fetchone()
            toast(Юзернейм канала занят!)
            conn.close()
            return

        cursor.execute(
            INSERT INTO chats (type, title, username, avatar_path, creator_id) VALUES ('channel', , , , ),
            (chan_title, chan_username, DEFAULT_AVATAR, app.current_user[id])
        )
        chat_id = cursor.lastrowid
        cursor.execute(INSERT INTO chat_members (chat_id, user_id) VALUES (, ), (chat_id, app.current_user[id]))
        conn.commit()
        conn.close()

        self.active_dialog.dismiss()
        toast(Канал успешно создан!)
        self.load_chats()


class ChatMessageBubble(MDCard)
    Нативный сборщик облака во избежание падения строкового парсера KV из-за слэшей файловой системы.
    text = StringProperty()
    sender_name = StringProperty()
    timestamp = StringProperty()
    file_path = StringProperty()
    is_own = BooleanProperty(False)

    def __init__(self, kwargs)
        super().__init__(kwargs)
        self.orientation = vertical
        self.size_hint_x = 0.75
        self.adaptive_height = True
        self.padding = dp(10)
        self.radius = [dp(12), dp(12), dp(12), dp(12)]

        if self.is_own
            self.pos_hint = {right 1}
            self.md_bg_color = [0.14, 0.50, 0.80, 0.2]
        else
            self.pos_hint = {left 1}
            self.md_bg_color = [0.5, 0.5, 0.5, 0.1]

        from kivymd.uix.label import MDLabel
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.button import MDIconButton
        from kivy.uix.image import AsyncImage

        self.add_widget(MDLabel(text=self.sender_name, bold=True, font_style=Caption, theme_text_color=Primary,
                                adaptive_height=True))

        cleaned_file = clean_secure_path(self.file_path)
        if cleaned_file and os.path.exists(cleaned_file)
            ext = os.path.splitext(cleaned_file)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.gif']
                self.add_widget(AsyncImage(source=cleaned_file, size_hint_y=None, height=dp(150), allow_stretch=True,
                                           keep_ratio=True))
            else
                doc_box = MDBoxLayout(orientation=horizontal, spacing=dp(8), size_hint_y=None, height=dp(40))
                doc_box.add_widget(MDIconButton(icon=file-document))
                doc_box.add_widget(MDLabel(text=os.path.basename(cleaned_file), shorten=True))
                self.add_widget(doc_box)

        if self.text
            self.add_widget(MDLabel(text=self.text, adaptive_height=True))

        self.add_widget(MDLabel(text=self.timestamp, halign=right, font_style=Caption, theme_text_color=Secondary,
                                adaptive_height=True))


class ChatScreen(MDScreen)
    file_manager = None
    rename_dialog = None
    rename_field = None
    chat_type = 
    is_creator = False

    def on_screen_enter(self)
        self.load_messages()

    def back_to_main(self)
        self.manager.current = 'main_chats'

    def load_messages(self)
        self.ids.messages_container.clear_widgets()
        app = MDApp.get_running_app()

        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute(SELECT  FROM chats WHERE id = , (app.current_chat_id,))
        chat_data = cursor.fetchone()
        if not chat_data
            conn.close()
            return

        self.chat_type = chat_data[type]
        self.is_creator = (chat_data[creator_id] == app.current_user[id])

        chat_title = chat_data[title]
        if self.chat_type == 'private'
            cursor.execute(
                SELECT cm.user_id, co.local_name FROM chat_members cm
                LEFT JOIN contacts co ON co.user_id =  AND co.contact_user_id = cm.user_id
                WHERE cm.chat_id =  AND cm.user_id != 
            , (app.current_user[id], app.current_chat_id, app.current_user[id]))
            partner = cursor.fetchone()
            if partner and partner[local_name]
                chat_title = partner[local_name]
            self.ids.chat_toolbar.title = chat_title
        else
            cursor.execute(SELECT COUNT() as cnt FROM chat_members WHERE chat_id = , (app.current_chat_id,))
            subs = cursor.fetchone()[cnt]
            self.ids.chat_toolbar.title = f{chat_title} ({subs} подп.)

        cursor.execute(
            SELECT m., u.display_name as sender_name FROM messages m
            JOIN users u ON m.sender_id = u.id
            WHERE m.chat_id = 
            ORDER BY m.id ASC LIMIT 50
        , (app.current_chat_id,))
        messages = cursor.fetchall()
        conn.close()

        for msg in messages
            is_own = (msg[sender_id] == app.current_user[id])
            bubble = ChatMessageBubble(
                text=msg[text] or ,
                sender_name=msg[sender_name],
                timestamp=msg[timestamp][16],
                file_path=msg[file_path] or ,
                is_own=is_own
            )
            self.ids.messages_container.add_widget(bubble)

        self.ids.messages_scroll.scroll_y = 0

    def send_text_message(self, file_path=None)
        text = self.ids.message_input.text.strip()
        if not text and not file_path
            return

        if self.chat_type == 'channel' and not self.is_creator
            toast(Только создатель может писать в канал!)
            self.ids.message_input.text = 
            return

        app = MDApp.get_running_app()
        ts = datetime.now().isoformat()

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            INSERT INTO messages (chat_id, sender_id, text, file_path, timestamp) VALUES (, , , , ),
            (app.current_chat_id, app.current_user[id], text, clean_secure_path(file_path), ts)
        )
        conn.commit()
        conn.close()

        self.ids.message_input.text = 
        self.load_messages()

    def open_file_manager(self)
        if not self.file_manager
            self.file_manager = MDFileManager(
                exit_manager=self.close_file_manager,
                select_path=self.select_file,
                preview=True
            )
        path = os.path.expanduser(~) if sys.platform != 'android' else sdcard
        self.file_manager.show(path)

    def select_file(self, path)
        self.close_file_manager()
        cleaned_source = clean_secure_path(path)
        if os.path.exists(cleaned_source)
            media_dir = clean_secure_path(.ilkassages_media)
            if not os.path.exists(media_dir)
                os.makedirs(media_dir)

            dest_path = clean_secure_path(os.path.join(media_dir, os.path.basename(cleaned_source)))
            try
                import shutil
                shutil.copy(cleaned_source, dest_path)
            except Exception
                dest_path = cleaned_source

            self.send_text_message(file_path=dest_path)
            toast(Файл отправлен)

    def close_file_manager(self, args)
        if self.file_manager
            self.file_manager.close()

    def show_rename_dialog(self)
        if self.chat_type != 'private'
            toast(Переименование доступно только для приватных чатов)
            return
        self.rename_field = Builder.load_string('MDTextFieldn  hint_text Локальный псевдоним')
        self.rename_dialog = MDDialog(
            title=Имя контакта,
            type=custom,
            content_cls=BoxLayout(orientation='vertical', size_hint_y=None, height=dp(56)),
            buttons=[
                MDFlatButton(text=Отмена, on_release=lambda x self.rename_dialog.dismiss()),
                MDRaisedButton(text=Сохранить, on_release=self.save_local_name)
            ]
        )
        self.rename_dialog.content_cls.add_widget(self.rename_field)
        self.rename_dialog.open()

    def save_local_name(self, instance)
        new_name = self.rename_field.text.strip()
        if not new_name
            return

        app = MDApp.get_running_app()
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute(SELECT user_id FROM chat_members WHERE chat_id =  AND user_id != ,
                       (app.current_chat_id, app.current_user[id]))
        partner_row = cursor.fetchone()
        if partner_row
            partner_id = partner_row[user_id]
            cursor.execute(
                INSERT INTO contacts (user_id, contact_user_id, local_name) VALUES (, , )
                ON CONFLICT(user_id, contact_user_id) DO UPDATE SET local_name=excluded.local_name
            , (app.current_user[id], partner_id, new_name))
            conn.commit()
            toast(Имя изменено)
        conn.close()
        self.rename_dialog.dismiss()
        self.load_messages()


class SettingsScreen(MDScreen)
    file_manager = None

    def load_user_data(self)
        app = MDApp.get_running_app()
        if not app.current_user
            return
        self.ids.current_username.text = fТекущий ID @{app.current_user['username']}
        self.ids.edit_display_name.text = app.current_user[display_name]
        self.ids.edit_username.text = app.current_user[username]

        avatar = clean_secure_path(app.current_user[avatar_path])
        self.ids.avatar_img.source = avatar if (avatar.startswith(http) or os.path.exists(avatar)) else DEFAULT_AVATAR

    def change_avatar(self)
        if not self.file_manager
            self.file_manager = MDFileManager(
                exit_manager=self.close_file_manager,
                select_path=self.select_avatar,
                preview=True
            )
        path = os.path.expanduser(~) if sys.platform != 'android' else sdcard
        self.file_manager.show(path)

    def select_avatar(self, path)
        self.close_file_manager()
        cleaned_path = clean_secure_path(path)
        if os.path.exists(cleaned_path)
            app = MDApp.get_running_app()
            app.current_user[avatar_path] = cleaned_path
            self.ids.avatar_img.source = cleaned_path

            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(UPDATE users SET avatar_path =  WHERE id = , (cleaned_path, app.current_user[id]))
            conn.commit()
            conn.close()
            toast(Аватар обновлен)

    def close_file_manager(self, args)
        if self.file_manager
            self.file_manager.close()

    def save_settings(self)
        new_display = self.ids.edit_display_name.text.strip()
        new_user = self.ids.edit_username.text.strip().lower()
        new_pass = self.ids.edit_password.text.strip()

        if not new_display or not new_user
            toast(Поля не могут быть пустыми)
            return

        app = MDApp.get_running_app()
        conn = db.get_connection()
        cursor = conn.cursor()

        if new_user != app.current_user[username]
            cursor.execute(SELECT id FROM users WHERE username = , (new_user,))
            if cursor.fetchone()
                toast(Этот юзернейм уже занят!)
                conn.close()
                return

        cursor.execute(UPDATE users SET display_name = , username =  WHERE id = ,
                       (new_display, new_user, app.current_user[id]))

        if new_pass
            if len(new_pass)  4
                toast(Новый пароль слишком короткий!)
                conn.close()
                return
            h = db.hash_password(new_pass)
            cursor.execute(UPDATE users SET password_hash =  WHERE id = , (h, app.current_user[id]))

        conn.commit()
        conn.close()

        app.current_user[display_name] = new_display
        app.current_user[username] = new_user
        toast(Данные успешно сохранены)
        self.back_to_main()

    def logout(self)
        app = MDApp.get_running_app()
        app.current_user = None
        app.current_chat_id = 0  # Теперь это число, и Kivy спокойно его пропустит!
        self.manager.current = 'login_register'

    def back_to_main(self)
        self.manager.current = 'main_chats'


### SECTION Main Application Context Run ###

class IlkassagesApp(MDApp)
    current_chat_id = NumericProperty(None, allownone=True)
    current_chat_id = NumericProperty(0)

    def build(self)
        self.theme_cls.primary_palette = Blue
        self.theme_cls.theme_style = Light
        return Builder.load_string(KV_STR)

    def toggle_theme(self)
        if self.theme_cls.theme_style == Light
            self.theme_cls.theme_style = Dark
        else
            self.theme_cls.theme_style = Light

    def open_edit_channel(self, channel_id)
        # Находим нужный канал в базе и заполняем поля старыми данными
        # ...

        # ИСПРАВЛЕНИЕ явно говорим приложению, что мы РЕДАКТИРУЕМ, а не создаем
        self.is_new_chat = False
        self.current_editing_chat_id = channel_id  # сохраняем ID для UPDATE

        # Переходим на экран редактирования
        self.root.current = 'channel_edit_screen'



if __name__ == '__main__'
    IlkassagesApp().run()