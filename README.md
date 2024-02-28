# Проект DjangoStripe
### Задача
- Реализовать Django + Stripe API бэкенд со следующим функционалом и условиями:

- Django Модель Item с полями (name, description, price)

API с двумя методами:

- GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос stripe.checkout.Session.create(...) и полученный session.id выдаваться в результате запроса
- GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном Item и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее с помощью JS библиотеки Stripe происходить редирект на Checkout форму stripe.redirectToCheckout(sessionId=session_id)

Бонусные задачи: <br>
☑ Запуск используя Docker

☑ Использование environment variables

☑ Просмотр Django Моделей в Django Admin панели

☑ Запуск приложения на удаленном сервере, доступном для тестирования

☑ Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items

☑ Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме.

☐ Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте.

☐ Реализовать не Stripe Session, а Stripe Payment Intent.

# Установка проекта
Для разворачивания проекта используется docker-compose. Для этого необходимо:
- указать переменные окружения в файле .env
```
SECRET_KEY=
# Stripe
STRIPE_PUBLIC_KEY=
STRIPE_SECRET_KEY=
ALLOWED_HOSTS=127.0.0.1 localhost
```
- скачать данные репозитория и запустить docker:
```
docker-compose up -d --build
```

### Получение api ключей
- Зарегистрироваться на сайте: https://stripe.com/
- Publishable key: https://dashboard.stripe.com/apikeys
- Secret key: https://dashboard.stripe.com/apikeys

## Приложение интернет-магазина
Разворачивается в контейнере app. Состоит из 3 приложений:
- товары (store),
- корзина (cart),
- заказы (orders).

В данном проекте используется наследование в html-шаблонах. Имеется базовый шаблон, 
от которого наследуются остальные шаблоны. Имеются блоки header и 
content(сами шаблоны, которые передаются во view).

### store
Приложение отвечающее за товары.

Модели:
- Item
- Discount
- Tax

Представления:
- ItemListView
- ItemDetailView
- CreateCheckoutSessionView
- CreateOrderCheckoutSessionView
- SuccessView
- CancelView

### cart
Приложение, реализующее работу с корзиной пользователя. 

Модели:
- Cart
- CartItem

Представления:
- cart_id
- add_cart
- cart_page
- remove_cart_item
- checkout

### orders
Приложение отвечающее за заказы

Модели:
- Order
- OrderItem

Представления:
- randomString
- get_user
- order_create
