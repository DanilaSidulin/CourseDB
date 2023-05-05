import streamlit as st
import database as db
import pandas as pd
import sqlite3
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://admin:admin@cluster0.cangr1s.mongodb.net/?retryWrites=true&w=majority"
mongo_client = MongoClient(uri)
mongo_db = mongo_client['Store']
Products_collection = mongo_db['Beverages']
conn = db.connect_db()

# Products_collection.insert_many([
# {
#        "_id": 0,
#        "model": "Добрый Кола 1л",
#        "Volume": "1L",
#        "Mass": "1kg",
#        "Flavour": "Cola",
#     },
#      {
#        "_id": 1,
#        "model": "Добрый Апельсин 1л",
#        "Volume": "1L",
#        "Mass": "1kg",
#        "Flavour": "Orange",
#     },
#      {
#        "_id": 2,
#        "model": "Добрый Сок Яблочный",
#        "Volume": "1L",
#        "Mass": "1kg",
#        "Flavour": "Apple",
#     },
#      {
#        "_id": 3,
#        "model": "Добрый Сок Апельсиновый",
#        "Volume": "1L",
#        "Mass": "1kg",
#        "Flavour": "Orange",
#     },
#      {
#        "_id": 4,
#        "model": "Добрый Черный Чай 1л",
#        "Volume": "1L",
#        "Mass": "1kg",
#        "Flavour": "Black Tea",
#     },
#      {
#        "_id": 5,
#        "model": "Добрый Зеленый Чай 1л",
#        "Volume": "1L",
#        "Mass": "1kg",
#        "Flavour": "Green Tea",
#     },
#      {
#        "_id": 6,
#        "model": "Yes Cola 0.7л",
#        "Volume": "0.7L",
#        "Mass": "0.7kg",
#        "Flavour": "Cola",
#     },
#      {
#        "_id": 7,
#        "model": "Yes Lemon 0.7л",
#        "Volume": "0.7L",
#        "Mass": "0.7kg",
#        "Flavour": "Lemon",
#     },
#      {
#        "_id": 8,
#        "model": "Yes Tea Lemon 1л",
#        "Volume": "1L",
#        "Mass": "1kg",
#        "Flavour": "Cola",
#     },
#      {
#        "_id": 9,
#        "model": "J7 Лимонад 0.5л",
#        "Volume": "0.5L",
#        "Mass": "0.5kg",
#        "Flavour": "Lemon",
#     },
#      {
#        "_id": 10,
#        "model": " J7 Тоник 0.5л ",
#        "Volume": "0.5L",
#        "Mass": "0.5kg",
#        "Flavour": "Tonic",
#     },
#      {
#        "_id": 11,
#        "model": "J7 Сок Гранатовый 1л",
#        "Volume": "1L",
#        "Mass": "1kg",
#        "Flavour": "Pomegranate",
#     },
#      {
#        "_id": 12,
#        "model": "J7 Сок Грейпфрут 1л",
#        "Volume": "1L",
#        "Mass": "1kg",
#        "Flavour": "Grapefruit",
#     },
# ])


def login_user(login, password):
    client = db.select_client(conn, login, password)
    worker = db.select_worker(conn, login, password)
    if client:
        return 'client'
    elif worker:
        if worker[0][5] == 1:
            return 'admin'
        elif worker[0][5] == 2:
            return 'worker'
    else:
        return None


def main():
    db.create_tables(conn)
    st.sidebar.header('Вход в аккаунт')
    login = st.sidebar.text_input('Логин')
    password = st.sidebar.text_input('Пароль', type='password')
    entry_btn = st.sidebar.checkbox('Войти')
    if entry_btn:
        menu = login_user(login, password)
        if menu is None:
            st.error('Вы ввели неправильные данные')
        elif menu == 'client':
            current_client = db.select_client(conn, login, password)[0]
            client_id = current_client[0]
            st.subheader('Здравствуйте, ' + current_client[1])
            menu_choice = st.selectbox('Выберите меню', ['Каталог товаров', 'Избранное', 'Корзина', 'Заказы'])
            if menu_choice == 'Каталог товаров':
                Products = db.select_Products(conn)
                selected_Products = pd.DataFrame(Products, columns=['id', 'Product_name', 'Product_type_id', 'company_id',
                                                                  'remainder'])
                companies = db.select_companies(conn)
                col1, col2 = st.columns(2)
                with col1:
                    Product_type = st.selectbox('Тип продукта', ['Все', 'Газированный напиток', 'Сок', 'Холодный чай'])
                    if Product_type == 'Газированный напиток':
                        selected_Products = selected_Products[selected_Products['Product_type_id'] == 1]
                    elif Product_type == 'Сок':
                        selected_Products = selected_Products[selected_Products['Product_type_id'] == 2]
                    elif Product_type == 'Холодный чай':
                        selected_Products = selected_Products[selected_Products['Product_type_id'] == 3]
                with col2:
                    company = st.selectbox('Производитель', ['Все', 'Добрый', 'Yes', 'J7', 'Arizona'])
                    if company == 'Добрый':
                        selected_Products = selected_Products[selected_Products['company_id'] == 1]
                    elif company == 'Yes':
                        selected_Products = selected_Products[selected_Products['company_id'] == 2]
                    elif company == 'J7':
                        selected_Products = selected_Products[selected_Products['company_id'] == 3]
                    elif company == 'Arizona':
                        selected_Products = selected_Products[selected_Products['company_id'] == 4]
                for ind, Product in selected_Products.iterrows():
                    with st.container():
                        Product_id = Product[0]
                        Product_remainder = int(Product[4])
                        st.text(f'Компания: {companies[Product[3] - 1][1]}')
                        st.text(f'Название Продукта: {Product[1]}')
                        Product_char = Products_collection.find_one({"model": Product[1]})
                        st.text(f'Объем: {Product_char["Volume"]}')
                        st.text(f'Масса Нетто: {Product_char["Mass"]}')
                        st.text(f'Вкус: {Product_char["Flavour"]}')
                        st.text(f'Остаток на складе: {Product_remainder}')
                        wish_btn, cart_btn = st.columns(2)
                        wish_btn_key = '1' + Product[1]
                        cart_btn_key = '2' + Product[1]
                        with wish_btn:
                            if st.button('В избранное', key=wish_btn_key):
                                if db.select_wish_list_item(conn, client_id, Product_id):
                                    st.error('Данный продукт уже есть в избранном')
                                else:
                                    if db.insert_wish_list_item(conn, client_id, Product_id):
                                        st.success('Продукт добавлен')
                                    else:
                                        st.error('Ошибка добавления')
                        with cart_btn:
                            if st.button('В корзину', key=cart_btn_key):
                                if db.select_cart_list_item(conn, client_id, Product_id):
                                    st.error('Данный продукт уже есть в корзине')
                                else:
                                    if db.insert_cart_list_item(conn, client_id, Product_id):
                                        st.success('Устройство добавлено в корзину')
                                    else:
                                        st.error('Ошибка добавления')
            elif menu_choice == 'Избранное':
                wish_list_items = db.select_wish_list_items(conn, client_id)
                companies = db.select_companies(conn)
                for item in wish_list_items:
                    Product_id = item[2]
                    Product = db.select_Product(conn, Product_id)
                    Product_remainder = int(Product[0][4])
                    with st.container():
                        st.text(f'Компания: {companies[Product[0][3] - 1][1]}')
                        st.text(f'Название продукта: {Product[0][1]}')
                        Product_char = Products_collection.find_one({"model": Product[0][1]})
                        st.text(f'Объем: {Product_char["Volume"]}')
                        st.text(f'Масса Нетто: {Product_char["Mass"]}')
                        st.text(f'Вкус: {Product_char["Flavour"]}')
                        st.text(f'Остаток на складе: {Product_remainder}')
                        wish_btn, cart_btn = st.columns(2)
                        wish_btn_key = '3' + Product[0][1]
                        cart_btn_key = '4' + Product[0][1]
                        with wish_btn:
                            if st.button('Удалить из избранного', key=wish_btn_key):
                                if db.delete_wish_list_item(conn, client_id, Product_id):
                                    st._rerun()
                        with cart_btn:
                            if st.button('В корзину', key=cart_btn_key):
                                if db.select_cart_list_item(conn, client_id, Product_id):
                                    st.error('Данный продукт уже есть в корзине')
                                else:
                                    if db.insert_cart_list_item(conn, client_id, Product_id):
                                        st.success('Продукт добавлен в корзину')
                                    else:
                                        st.error('Ошибка добавления')
            elif menu_choice == 'Корзина':
                cart_list_items = db.select_cart_list_items(conn, str(client_id))
                companies = db.select_companies(conn)
                for item in cart_list_items:
                    Product_id = item[2]
                    Product = db.select_Product(conn, str(Product_id))[0]
                    Product_remainder = int(Product[4])
                    with st.container():
                        st.text(f'Компания: {companies[Product[3] - 1][1]}')
                        st.text(f'Название продукта: {Product[1]}')
                        st.text(f'Остаток на складе: {Product_remainder}')
                        confirm_btn, del_btn = st.columns(2)
                        confirm_btn_key = '5' + Product[1]
                        del_btn_key = '6' + Product[1]
                        with confirm_btn:
                            if st.button('Подтвердить заказ', key=confirm_btn_key):
                                if Product_remainder > 0:
                                    if db.insert_reservation(conn, client_id, Product_id, 1) and \
                                            db.delete_cart_list_item(conn, client_id, Product_id):
                                        db.set_Product_remainder(conn, Product_remainder - 1, Product_id)
                                        st._rerun()
                                else:
                                    st.error('Недостаточно товара')
                        with del_btn:
                            if st.button('Удалить из корзины', key=del_btn_key):
                                if db.delete_cart_list_item(conn, client_id, Product_id):
                                    st._rerun()
            elif menu_choice == 'Заказы':
                client_reservations = db.select_client_reservations(conn, str(client_id), 1)
                companies = db.select_companies(conn)
                for item in client_reservations:
                    Product_id = item[2]
                    reservation_id = item[0]
                    Product = db.select_Product(conn, str(Product_id))[0]
                    Product_remainder = Product[4]
                    with st.container():
                        st.text(f'Компания: {companies[Product[3] - 1][1]}')
                        st.text(f'Название продукта: {Product[1]}')
                        cancel_btn_key = '7' + Product[1]
                        if st.button('Отменить заказ', key=cancel_btn_key):
                            db.set_reservation_status(conn, reservation_id, 4)
                            db.set_Product_remainder(conn, Product_remainder + 1, Product_id)
                            st._rerun()
        elif menu == 'worker':
            current_worker = db.select_worker(conn, login, password)[0]
            worker_id = current_worker[0]
            status_choice = st.selectbox('Статус заказа', ['Новые', 'Собранные', 'Выданные', 'Отмененные'])
            reservations = db.select_reservations(conn)
            companies = db.select_companies(conn)
            df_reservations = pd.DataFrame(reservations, columns=['id', 'client_id', 'Product_id', 'status_id',
                                                                  'worker_id'])
            common_btn_name = ''
            if status_choice == 'Новые':
                df_reservations = df_reservations[df_reservations['status_id'] == 1]
                common_btn_name = 'Собрать'
            elif status_choice == 'Собранные':
                df_reservations = df_reservations[df_reservations['status_id'] == 2]
                common_btn_name = 'Выдать'
            elif status_choice == 'Выданные':
                df_reservations = df_reservations[df_reservations['status_id'] == 3]
                common_btn_name = 'Удалить'
            elif status_choice == 'Отмененные':
                df_reservations = df_reservations[df_reservations['status_id'] == 4]
                common_btn_name = 'Удалить'
            for item in df_reservations.iterrows():
                reservation = item[1]
                reservation_client = db.select_client_by_id(conn, reservation[1])
                Product_id = reservation[2]
                reservation_id = reservation[0]
                Product = db.select_Product(conn, str(Product_id))[0]
                Product_remainder = int(Product[4])
                with st.container():
                    st.text(f'Компания: {companies[Product[3] - 1][1]}')
                    st.text(f'Название продукта: {Product[1]}')
                    st.text(f'Имя клиента: {reservation_client[1]}')
                    st.text(f'Телефон клиента: {reservation_client[4]}')
                    common_btn_key = '8' + Product[1]
                    cancel_btn_key = '9' + Product[1]
                    common_btn, cancel_btn = st.columns(2)
                    with common_btn:
                        if st.button(common_btn_name, key=common_btn_key):
                            if common_btn_name == 'Собрать':
                                db.set_reservation_worker(conn, reservation_id, worker_id)
                                db.set_reservation_status(conn, reservation_id, 2)
                                st._rerun()
                            elif common_btn_name == 'Выдать':
                                db.set_reservation_status(conn, reservation_id, 3)
                                st._rerun()
                            elif common_btn_name == 'Удалить':
                                db.delete_reservation(conn, reservation_id)
                                st._rerun()
                    with cancel_btn:
                        if st.button('Отменить заказ', key=cancel_btn_key):
                            db.set_reservation_status(conn, reservation_id, 4)
                            db.set_Product_remainder(conn, Product_remainder + 1, Product_id)
                            st._rerun()
        elif menu == 'admin':
            st.title('Меню Админа')
            admin_choice = st.selectbox('Выберите меню', ['Товары', 'Работники'])
            if admin_choice == 'Товары':
                Products = db.select_Products(conn)
                selected_Products = pd.DataFrame(Products, columns=['id', 'Product_name', 'Product_type_id', 'company_id',
                                                                  'remainder'])
                companies = db.select_companies(conn)
                col1, col2 = st.columns(2)
                with col1:
                    Product_type = st.selectbox('Тип продукта', ['Все', 'Газированный напиток', 'Сок', 'Холодный чай'])
                    if Product_type == 'Газированный напиток':
                        selected_Products = selected_Products[selected_Products['Product_type_id'] == 1]
                    elif Product_type == 'Сок':
                        selected_Products = selected_Products[selected_Products['Product_type_id'] == 2]
                    elif Product_type == 'Холодный чай':
                        selected_Products = selected_Products[selected_Products['Product_type_id'] == 3]
                with col2:
                    company = st.selectbox('Производитель', ['Все', 'Добрый', 'Yes', 'J7', 'Arizona'])
                    if company == 'Добрый':
                        selected_Products = selected_Products[selected_Products['company_id'] == 1]
                    elif company == 'Yes':
                        selected_Products = selected_Products[selected_Products['company_id'] == 2]
                    elif company == 'J7':
                        selected_Products = selected_Products[selected_Products['company_id'] == 3]
                    elif company == 'Arizona':
                        selected_Products = selected_Products[selected_Products['company_id'] == 4]
                for ind, Product in selected_Products.iterrows():
                    with st.container():
                        Product_id = Product[0]
                        Product_remainder = int(Product[4])
                        st.text(f'Компания: {companies[Product[3] - 1][1]}')
                        st.text(f'Название продукта: {Product[1]}')
                        Product_char = Products_collection.find_one({"model": Product[1]})
                        st.text(f'Объем: {Product_char["Volume"]}')
                        st.text(f'Масса Нетто: {Product_char["Mass"]}')
                        st.text(f'Вкус: {Product_char["Flavour"]}')
                        st.text(f'Остаток на складе: {Product_remainder}')
                        add_dev_btn, rem_dev_btn, del_dev_btn = st.columns(3)
                        add_dev_btn_key = '1' + Product[1]
                        rem_dev_btn_key = '2' + Product[1]
                        del_dev_btn_key = '3' + Product[1]
                        with add_dev_btn:
                            if st.button('Добавить', key=add_dev_btn_key):
                                db.set_Product_remainder(conn, Product_remainder + 1, Product_id)
                                st._rerun()
                        with rem_dev_btn:
                            if st.button('Убавить', key=rem_dev_btn_key):
                                if Product_remainder > 0:
                                    db.set_Product_remainder(conn, Product_remainder - 1, Product_id)
                                    st._rerun()
                                else:
                                    st.error('Продукта уже нет на складе')
                        with del_dev_btn:
                            if st.button('Удалить продукт', key=del_dev_btn_key):
                                db.delete_Product(conn, Product_id)
            elif admin_choice == 'Работники':
                with st.form(key='new_worker', clear_on_submit=True):
                    st.subheader('Создание нового аккаунта работника')
                    worker_name = st.text_input("Имя")
                    worker_login = st.text_input('Логин')
                    worker_password = st.text_input('Пароль')
                    worker_phone = st.text_input('Телефон')
                    role_id = 2
                    signup_btn = st.form_submit_button('Создать нового работника')
                    if signup_btn:
                        db.insert_worker(conn, worker_name, worker_login, worker_password, worker_phone, role_id)
    else:
        st.title('Магазин напитков')
        st.markdown('Добро пожаловать в наш магазин!')
        st.markdown('Для пользования приложением вам необходимо авторизоваться в систему. '
                    'Если вы еще не имеете аккаунт, то вам необходимо зарегистрироваться в контекстном меню, '
                    'расположенном в нижней часте меню.')
        st.subheader('Регистрация')
        st.text('Введите ваши данные')
        with st.form(key='signup', clear_on_submit=True):
            client_name = st.text_input("Имя")
            client_phone = st.text_input('Телефон')
            client_login = st.text_input('Логин')
            client_password = st.text_input('Пароль')
            signup_btn = st.form_submit_button('Зарегистрироваться')
            if signup_btn:
                if db.insert_client(conn, client_name, client_phone, client_login, client_password):
                    st.success('Аккаунт успешно создан')
                else:
                    st.error('Не удалось создать аккаунт')
        st.markdown('Данные для связи:')
        st.markdown('Email: store@mail.ru')
        st.markdown('Телефон: 8-800-555-3535')


if __name__ == '__main__':
    main()
