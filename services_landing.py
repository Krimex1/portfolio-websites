from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

# ---------------- БАЗОВЫЙ HTTP‑СЕРВЕР ---------------- #

class SimpleHandler(BaseHTTPRequestHandler):
    def _serve_html(self, content: str):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def send_error(self, code, message=None):
        # Страница ошибки в UTF‑8
        self.log_error("code %d, message %s", code, message)
        self.send_response(code, message)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Connection", "close")
        self.end_headers()
        html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ошибка {code}</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
        h1 {{ font-size: 48px; color: #333; }}
        p {{ font-size: 18px; color: #666; }}
    </style>
</head>
<body>
    <h1>Ошибка {code}</h1>
    <p>{message or "Страница не найдена или временно недоступна."}</p>
</body>
</html>
        """
        self.wfile.write(html.encode("utf-8"))

    def do_GET(self):
        # Убираем слеш в конце пути
        path = self.path.rstrip("/") or "/"

        # ---------------- СТАТИЧЕСКИЕ СТРАНИЦЫ ---------------- #
        # Словарь с шаблонами страниц
        pages = {}

        # ---------------- ГЛАВНАЯ СТРАНИЦА ---------------- #
        pages["/"] = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Krimex Development — инструменты, боты и инфраструктура</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
            color: #eee;
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header {
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            padding: 30px 20px;
            text-align: center;
            border-bottom: 3px solid #0f4c75;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        header h1 {
            font-size: 48px;
            color: #3cefff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }
        header p {
            font-size: 18px;
            color: #aaa;
            margin-top: 10px;
        }
        .services {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }
        .service {
            background: linear-gradient(135deg, #1e3a5f 0%, #263859 100%);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            transition: transform 0.3s, box-shadow 0.3s;
            border-left: 5px solid #0f4c75;
        }
        .service:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(60, 239, 255, 0.3);
        }
        .service h3 {
            font-size: 24px;
            color: #3cefff;
            margin-bottom: 10px;
        }
        .service p {
            font-size: 16px;
            color: #ccc;
            margin-bottom: 20px;
        }
        .service a {
            display: inline-block;
            padding: 12px 25px;
            background: #0f4c75;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
            font-weight: bold;
        }
        .service a:hover {
            background: #3cefff;
            color: #0f0f0f;
        }
        footer {
            text-align: center;
            margin-top: 60px;
            padding: 30px 20px;
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            border-top: 3px solid #0f4c75;
            box-shadow: 0 -4px 10px rgba(0,0,0,0.5);
            color: #888;
        }
        footer a {
            color: #3cefff;
            text-decoration: none;
            margin: 0 10px;
        }
        footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <h1>Krimex Development</h1>
        <p>Инструменты для разработчиков, владельцев проектов и сообществ</p>
    </header>

    <div class="container">
        <p style="text-align: center; font-size: 18px; margin-top: 30px; color: #bbb;">
            Krimex Development — это набор инструментов для разработчиков и владельцев проектов: мониторинг доступности, нагрузочное тестирование, интеллектуальный ассистент, OSINT‑инструменты, магазин цифровых товаров и инфраструктура на базе Lite‑Hosting.
        </p>
        <p style="text-align: center; font-size: 16px; margin-top: 10px; color: #999;">
            Каждый сервис закрывает свою задачу: от проверки аптайма и стресс‑тестов до интеллектуальной помощи, OSINT‑аналитики и монетизации через цифровой магазин.
        </p>

        <div class="services">
            <!-- Боты -->
            <div class="service">
                <h3>🔍 Network Bot</h3>
                <p>Следит за сайтами и API, фиксирует падения и восстановления и отправляет понятные уведомления в Telegram.</p>
                <a href="/network">Подробнее о мониторинге →</a>
            </div>
            <div class="service">
                <h3>⚡ Stresser Bot</h3>
                <p>ИСХОДНЫЙ КОД ПРОДАЕТСЯ НА ФАНПЕЕ БОТ ОКОНЧИЛ СВОЮ РАБОТУ Имитация высокой нагрузки на ваши ресурсы: помогает увидеть пределы системы и подготовиться к всплескам трафика.</p>
                <a href="/stresser">Подробнее о стресс‑тестах →</a>
            </div>
            <div class="service">
                <h3>🤖 AI Bot</h3>
                <p>Ассистент на базе современных моделей ИИ: тексты, код, идеи и быстрый анализ прямо в Telegram.</p>
                <a href="/ai">Подробнее об AI‑боте →</a>
            </div>
            <div class="service">
                <h3>🕵️ OSINT Bot</h3>
                <p>Инструмент для безопасного и аккуратного сбора открытой информации из множества источников.</p>
                <a href="/osint">Подробнее об OSINT‑боте →</a>
            </div>

            <!-- Магазин и канал -->
            <div class="service">
                <h3>🛒 Магазин FunPay</h3>
                <p>Качественные цифровые товары и услуги с акцентом на аккуратное исполнение и понятные условия.</p>
                <a href="/shop">Подробнее о магазине →</a>
            </div>
            <div class="service">
                <h3>📢 Telegram‑канал</h3>
                <p>Анонсы релизов, планы, технические заметки и обратная связь по всем проектам Krimex.</p>
                <a href="https://t.me/krimexAI" target="_blank">Перейти к каналу →</a>
            </div>

            <!-- Хостинг и сервер -->
            <div class="service">
                <h3>🖥️ Lite‑Hosting</h3>
                <p>Хостинг для Minecraft‑серверов и проектов: производительное железо, защита от атак и быстрая активация.</p>
                <a href="/hosting">Подробнее о хостинге →</a>
            </div>
            <div class="service">
                <h3>🏰 VanilaLite</h3>
                <p>Ванильный Minecraft‑сервер с уютным сообществом, без лишних модов, с акцентом на честный выживальный геймплей.</p>
                <a href="/vanila">Подробнее о VanilaLite →</a>
            </div>

            <!-- Разработка -->
            <div class="service">
                <h3>🤖 Разработка Telegram‑ботов</h3>
                <p>Разработка мощных Telegram‑ботов под ваши задачи: автоматизация, интеграция с API, обработка платежей и уникальные функции. Быстро, надёжно, с гарантией качества.</p>
                <a href="/telegram-bots">Заказать бота →</a>
            </div>
            <div class="service">
                <h3>🎮 Разработка Discord‑ботов</h3>
                <p>Создание кастомных Discord‑ботов для игровых серверов и сообществ: модерация, экономика, мини‑игры, интеграция с API и уникальный функционал. Профессионально и под ключ.</p>
                <a href="/discord-bots">Заказать бота →</a>
            </div>
        </div>
    </div>

    <footer>
        <p>&copy; 2025 Krimex Development. Все права защищены.</p>
        <p>
            <a href="https://t.me/krimexAI" target="_blank">Telegram</a> •
            <a href="https://funpay.com/lots/offer?id=37506389" target="_blank">FunPay</a> •
            <a href="https://discord.gg/vanilalite" target="_blank">Discord</a>
        </p>
    </footer>
</body>
</html>
        """

        # ---------------- NETWORK BOT ---------------- #
        pages["/network"] = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Network Bot — мониторинг доступности сайтов</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
            color: #eee;
            line-height: 1.6;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        header {
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            padding: 30px 20px;
            text-align: center;
            border-bottom: 3px solid #0f4c75;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            margin-bottom: 40px;
        }
        header h1 {
            font-size: 42px;
            color: #3cefff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }
        header p {
            font-size: 18px;
            color: #aaa;
            margin-top: 10px;
        }
        h2 {
            font-size: 32px;
            color: #3cefff;
            margin-bottom: 15px;
            border-left: 5px solid #0f4c75;
            padding-left: 15px;
        }
        p, li {
            font-size: 18px;
            color: #ccc;
            margin-bottom: 15px;
        }
        ul {
            margin-left: 20px;
        }
        .cta {
            display: inline-block;
            padding: 15px 30px;
            background: #0f4c75;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
            font-weight: bold;
            transition: background 0.3s;
        }
        .cta:hover {
            background: #3cefff;
            color: #0f0f0f;
        }
        footer {
            text-align: center;
            margin-top: 60px;
            padding: 30px 20px;
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            border-top: 3px solid #0f4c75;
            box-shadow: 0 -4px 10px rgba(0,0,0,0.5);
            color: #888;
        }
        footer a {
            color: #3cefff;
            text-decoration: none;
            margin: 0 10px;
        }
        footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <h1>Network Bot</h1>
        <p>Мониторинг доступности сайтов и API 24/7</p>
    </header>

    <div class="container">
        <p>Network Bot — это ваш личный страж, который 24/7 следит за доступностью сайтов и API. Он мгновенно сообщает о сбоях, чтобы вы могли реагировать раньше, чем это заметят пользователи.</p>

        <h2>Возможности</h2>
        <ul>
            <li><strong>Настоящий мониторинг:</strong> Бот имитирует реального пользователя, чтобы выявлять не только полные отключения, но и проблемы с загрузкой.</li>
            <li><strong>Умные уведомления:</strong> Только важная информация: отчёты о падении, восстановлении и длительных простоях, без лишнего спама.</li>
        </ul>

        <a href="https://t.me/YourNetworkBot" class="cta" target="_blank">Запустить Network Bot →</a>
        <a href="/" class="cta">← Назад к главной</a>
    </div>

    <footer>
        <p>&copy; 2025 Krimex Development</p>
        <p><a href="https://t.me/krimexAI" target="_blank">Telegram</a> • <a href="/">Главная</a></p>
    </footer>
</body>
</html>
        """

        # ---------------- STRESSER BOT ---------------- #
        pages["/stresser"] = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stresser Bot — нагрузочное тестирование</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
            color: #eee;
            line-height: 1.6;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        header {
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            padding: 30px 20px;
            text-align: center;
            border-bottom: 3px solid #0f4c75;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            margin-bottom: 40px;
        }
        header h1 {
            font-size: 42px;
            color: #3cefff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }
        header p {
            font-size: 18px;
            color: #aaa;
            margin-top: 10px;
        }
        h2 {
            font-size: 32px;
            color: #3cefff;
            margin-bottom: 15px;
            border-left: 5px solid #0f4c75;
            padding-left: 15px;
        }
        p, li {
            font-size: 18px;
            color: #ccc;
            margin-bottom: 15px;
        }
        ul {
            margin-left: 20px;
        }
        .warning {
            background: rgba(255, 193, 7, 0.1);
            border-left: 5px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .cta {
            display: inline-block;
            padding: 15px 30px;
            background: #0f4c75;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
            font-weight: bold;
            transition: background 0.3s;
        }
        .cta:hover {
            background: #3cefff;
            color: #0f0f0f;
        }
        footer {
            text-align: center;
            margin-top: 60px;
            padding: 30px 20px;
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            border-top: 3px solid #0f4c75;
            box-shadow: 0 -4px 10px rgba(0,0,0,0.5);
            color: #888;
        }
        footer a {
            color: #3cefff;
            text-decoration: none;
            margin: 0 10px;
        }
        footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <h1>Stresser Bot</h1>
        <p>ИСХОДНЫЙ КОД ПРОДАЕТСЯ НА ФАНПЕЕ БОТ ОКОНЧИЛ СВОЮ РАБОТУ Нагрузочное тестирование ваших проектов</p>
    </header>

    <div class="container">
        <p>Stresser Bot — это профессиональный инструмент для проверки вашего проекта на прочность. Узнайте, как поведёт себя ваша система под пиковой нагрузкой, и будьте готовы к любым вызовам.</p>

        <h2>Возможности</h2>
        <ul>
            <li><strong>Гибкая настройка:</strong> Настраивайте интенсивность и продолжительность тестов, чтобы точно имитировать желаемые условия.</li>
            <li><strong>Подробная аналитика:</strong> Анализируйте задержки, ошибки и поведение сервера, чтобы выявлять и устранять слабые места.</li>
        </ul>

        <div class="warning">
            <strong>⚠️ Внимание:</strong> Используйте только для тестирования собственных ресурсов или по согласованию с владельцами инфраструктуры.
        </div>

        <a href="https://t.me/YourStresserBot" class="cta" target="_blank">Запустить Stresser Bot →</a>
        <a href="/" class="cta">← Назад к главной</a>
    </div>

    <footer>
        <p>&copy; 2025 Krimex Development</p>
        <p><a href="https://t.me/krimexAI" target="_blank">Telegram</a> • <a href="/">Главная</a></p>
    </footer>
</body>
</html>
        """

        # ---------------- AI BOT ---------------- #
        pages["/ai"] = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Bot — интеллектуальный ассистент</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
            color: #eee;
            line-height: 1.6;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        header {
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            padding: 30px 20px;
            text-align: center;
            border-bottom: 3px solid #0f4c75;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            margin-bottom: 40px;
        }
        header h1 {
            font-size: 42px;
            color: #3cefff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }
        header p {
            font-size: 18px;
            color: #aaa;
            margin-top: 10px;
        }
        h2 {
            font-size: 32px;
            color: #3cefff;
            margin-bottom: 15px;
            border-left: 5px solid #0f4c75;
            padding-left: 15px;
        }
        p, li {
            font-size: 18px;
            color: #ccc;
            margin-bottom: 15px;
        }
        ul {
            margin-left: 20px;
        }
        .cta {
            display: inline-block;
            padding: 15px 30px;
            background: #0f4c75;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
            font-weight: bold;
            transition: background 0.3s;
        }
        .cta:hover {
            background: #3cefff;
            color: #0f0f0f;
        }
        footer {
            text-align: center;
            margin-top: 60px;
            padding: 30px 20px;
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            border-top: 3px solid #0f4c75;
            box-shadow: 0 -4px 10px rgba(0,0,0,0.5);
            color: #888;
        }
        footer a {
            color: #3cefff;
            text-decoration: none;
            margin: 0 10px;
        }
        footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <h1>AI Bot</h1>
        <p>Интеллектуальный ассистент в Telegram</p>
    </header>

    <div class="container">
        <p>AI Bot — это ваш персональный ассистент, который всегда под рукой в Telegram. Он поможет с кодом, текстами, идеями и анализом, освобождая ваше время для более важных задач.</p>

        <h2>Возможности</h2>
        <ul>
            <li><strong>Помощь с кодом:</strong> Получайте черновые наброски кода, объяснения ошибок и советы по архитектуре в режиме реального времени.</li>
            <li><strong>Генерация текстов:</strong> Создавайте посты, статьи, описания и любые другие тексты за считанные минуты.</li>
        </ul>

        <a href="https://t.me/YourAIBot" class="cta" target="_blank">Запустить AI Bot →</a>
        <a href="/" class="cta">← Назад к главной</a>
    </div>

    <footer>
        <p>&copy; 2025 Krimex Development</p>
        <p><a href="https://t.me/krimexAI" target="_blank">Telegram</a> • <a href="/">Главная</a></p>
    </footer>
</body>
</html>
        """

        # ---------------- OSINT BOT ---------------- #
        pages["/osint"] = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSINT Bot — инструмент для работы с открытыми источниками</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
            color: #eee;
            line-height: 1.6;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        header {
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            padding: 30px 20px;
            text-align: center;
            border-bottom: 3px solid #0f4c75;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            margin-bottom: 40px;
        }
        header h1 {
            font-size: 42px;
            color: #3cefff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }
        header p {
            font-size: 18px;
            color: #aaa;
            margin-top: 10px;
        }
        h2 {
            font-size: 32px;
            color: #3cefff;
            margin-bottom: 15px;
            border-left: 5px solid #0f4c75;
            padding-left: 15px;
        }
        p, li {
            font-size: 18px;
            color: #ccc;
            margin-bottom: 15px;
        }
        ul {
            margin-left: 20px;
        }
        .cta {
            display: inline-block;
            padding: 15px 30px;
            background: #0f4c75;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
            font-weight: bold;
            transition: background 0.3s;
        }
        .cta:hover {
            background: #3cefff;
            color: #0f0f0f;
        }
        footer {
            text-align: center;
            margin-top: 60px;
            padding: 30px 20px;
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            border-top: 3px solid #0f4c75;
            box-shadow: 0 -4px 10px rgba(0,0,0,0.5);
            color: #888;
        }
        footer a {
            color: #3cefff;
            text-decoration: none;
            margin: 0 10px;
        }
        footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <h1>OSINT Bot</h1>
        <p>Инструмент для работы с открытыми источниками</p>
    </header>

    <div class="container">
        <p>OSINT Bot — это аккуратный инструмент для работы с открытыми источниками информации. Он помогает собирать и структурировать данные из множества ресурсов, экономя ваше время.</p>

        <h2>Возможности</h2>
        <ul>
            <li><strong>Безопасный сбор данных:</strong> Бот работает только с публично доступной информацией и не требует никаких закрытых доступов.</li>
            <li><strong>Простой интерфейс:</strong> Чёткие команды, продуманная логика и читаемые результаты поиска для повседневных задач OSINT.</li>
        </ul>

        <a href="https://t.me/YourOSINTBot" class="cta" target="_blank">Запустить OSINT Bot →</a>
        <a href="/" class="cta">← Назад к главной</a>
    </div>

    <footer>
        <p>&copy; 2025 Krimex Development</p>
        <p><a href="https://t.me/krimexAI" target="_blank">Telegram</a> • <a href="/">Главная</a></p>
    </footer>
</body>
</html>
        """

        # ---------------- SHOP ---------------- #
        pages["/shop"] = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Магазин Krimex на FunPay</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
            color: #eee;
            line-height: 1.6;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        header {
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            padding: 30px 20px;
            text-align: center;
            border-bottom: 3px solid #0f4c75;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            margin-bottom: 40px;
        }
        header h1 {
            font-size: 42px;
            color: #3cefff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }
        header p {
            font-size: 18px;
            color: #aaa;
            margin-top: 10px;
        }
        h2 {
            font-size: 32px;
            color: #3cefff;
            margin-bottom: 15px;
            border-left: 5px solid #0f4c75;
            padding-left: 15px;
        }
        p, li {
            font-size: 18px;
            color: #ccc;
            margin-bottom: 15px;
        }
        ul {
            margin-left: 20px;
        }
        .cta {
            display: inline-block;
            padding: 15px 30px;
            background: #0f4c75;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
            font-weight: bold;
            transition: background 0.3s;
        }
        .cta:hover {
            background: #3cefff;
            color: #0f0f0f;
        }
        footer {
            text-align: center;
            margin-top: 60px;
            padding: 30px 20px;
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            border-top: 3px solid #0f4c75;
            box-shadow: 0 -4px 10px rgba(0,0,0,0.5);
            color: #888;
        }
        footer a {
            color: #3cefff;
            text-decoration: none;
            margin: 0 10px;
        }
        footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <h1>Магазин на FunPay</h1>
        <p>Качественные цифровые товары и услуги</p>
    </header>

    <div class="container">
        <p>Магазин Krimex на FunPay — это тщательно отобранные цифровые товары и услуги, где качество и прозрачность стоят на первом месте.</p>

        <h2>Преимущества</h2>
        <ul>
            <li><strong>Полная прозрачность:</strong> Все товары и услуги подробно описаны, чтобы вы точно знали, что получаете.</li>
            <li><strong>Гарантия FunPay:</strong> Платформа FunPay защищает ваши покупки и выступает гарантом честной сделки.</li>
        </ul>

        <a href="https://funpay.com/lots/offer?id=37506389" class="cta" target="_blank">Перейти в магазин →</a>
        <a href="/" class="cta">← Назад к главной</a>
    </div>

    <footer>
        <p>&copy; 2025 Krimex Development</p>
        <p><a href="https://t.me/krimexAI" target="_blank">Telegram</a> • <a href="/">Главная</a></p>
    </footer>
</body>
</html>
        """

        # ---------------- TELEGRAM CHANNEL ---------------- #
        # (перенаправление на telegram)

        # ---------------- HOSTING ---------------- #
        pages["/hosting"] = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lite‑Hosting — производительный хостинг для проектов</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
            color: #eee;
            line-height: 1.6;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        header {
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            padding: 30px 20px;
            text-align: center;
            border-bottom: 3px solid #0f4c75;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            margin-bottom: 40px;
        }
        header h1 {
            font-size: 42px;
            color: #3cefff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }
        header p {
            font-size: 18px;
            color: #aaa;
            margin-top: 10px;
        }
        h2 {
            font-size: 32px;
            color: #3cefff;
            margin-bottom: 15px;
            border-left: 5px solid #0f4c75;
            padding-left: 15px;
        }
        p, li {
            font-size: 18px;
            color: #ccc;
            margin-bottom: 15px;
        }
        ul {
            margin-left: 20px;
        }
        .cta {
            display: inline-block;
            padding: 15px 30px;
            background: #0f4c75;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
            font-weight: bold;
            transition: background 0.3s;
        }
        .cta:hover {
            background: #3cefff;
            color: #0f0f0f;
        }
        footer {
            text-align: center;
            margin-top: 60px;
            padding: 30px 20px;
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            border-top: 3px solid #0f4c75;
            box-shadow: 0 -4px 10px rgba(0,0,0,0.5);
            color: #888;
        }
        footer a {
            color: #3cefff;
            text-decoration: none;
            margin: 0 10px;
        }
        footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <h1>Lite‑Hosting</h1>
        <p>Производительный хостинг для Minecraft и других проектов</p>
    </header>

    <div class="container">
        <p>Lite‑Hosting — это хостинг, созданный для проектов, которым важна максимальная производительность, стабильность и защита от внешних угроз.</p>

        <h2>Преимущества</h2>
        <ul>
            <li><strong>Мощное железо:</strong> Процессоры Ryzen 3900X обеспечивают высокую производительность даже под пиковыми нагрузками.</li>
            <li><strong>Быстрая активация:</strong> Сервер активируется автоматически в течение минуты после оплаты.</li>
            <li><strong>Защита от атак:</strong> Инфраструктура защищена от DDoS-атак, что гарантирует стабильную работу вашего проекта.</li>
            <li><strong>Поддержка 24/7:</strong> Специалисты помогут с настройкой, переносом и любыми вопросами по хостингу.</li>
        </ul>

        <a href="https://litehosting.su" class="cta" target="_blank">Выбрать тариф →</a>
        <a href="/" class="cta">← Назад к главной</a>
    </div>

    <footer>
        <p>&copy; 2025 Krimex Development</p>
        <p><a href="https://t.me/krimexAI" target="_blank">Telegram</a> • <a href="/">Главная</a></p>
    </footer>
</body>
</html>
        """

        # ---------------- VANILA ---------------- #
        pages["/vanila"] = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VanilaLite — ванильный Minecraft‑сервер</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
            color: #eee;
            line-height: 1.6;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        header {
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            padding: 30px 20px;
            text-align: center;
            border-bottom: 3px solid #0f4c75;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            margin-bottom: 40px;
        }
        header h1 {
            font-size: 42px;
            color: #3cefff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }
        header p {
            font-size: 18px;
            color: #aaa;
            margin-top: 10px;
        }
        h2 {
            font-size: 32px;
            color: #3cefff;
            margin-bottom: 15px;
            border-left: 5px solid #0f4c75;
            padding-left: 15px;
        }
        p, li {
            font-size: 18px;
            color: #ccc;
            margin-bottom: 15px;
        }
        ul {
            margin-left: 20px;
        }
        .cta {
            display: inline-block;
            padding: 15px 30px;
            background: #0f4c75;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
            font-weight: bold;
            transition: background 0.3s;
        }
        .cta:hover {
            background: #3cefff;
            color: #0f0f0f;
        }
        footer {
            text-align: center;
            margin-top: 60px;
            padding: 30px 20px;
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            border-top: 3px solid #0f4c75;
            box-shadow: 0 -4px 10px rgba(0,0,0,0.5);
            color: #888;
        }
        footer a {
            color: #3cefff;
            text-decoration: none;
            margin: 0 10px;
        }
        footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <h1>VanilaLite</h1>
        <p>Ванильный Minecraft‑сервер с честным выживанием</p>
    </header>

    <div class="container">
        <p>VanilaLite — это аккуратный ванильный сервер Minecraft без лишних модов и нагромождений. Честное выживание, спокойное развитие и комфортное комьюнити.</p>

        <h2>Особенности</h2>
        <ul>
            <li><strong>Чистая ваниль:</strong> Классический игровой опыт без перегруженных модпаками и pay‑to‑win механик.</li>
            <li><strong>Уютное сообщество:</strong> Дружелюбные игроки, адекватная администрация и аккуратное отношение к миру.</li>
            <li><strong>Стабильность:</strong> Сервер работает на базе Lite‑Hosting с упором на стабильность и минимальные лаги.</li>
            <li><strong>Discord‑комьюнити:</strong> Присоединяйтесь через Discord — там вся актуальная информация, правила и события.</li>
        </ul>

        <a href="https://discord.gg/vanilalite" class="cta" target="_blank">Присоединиться к Discord →</a>
        <a href="/" class="cta">← Назад к главной</a>
    </div>

    <footer>
        <p>&copy; 2025 Krimex Development</p>
        <p><a href="https://t.me/krimexAI" target="_blank">Telegram</a> • <a href="/">Главная</a></p>
    </footer>
</body>
</html>
        """

        # ---------------- TELEGRAM BOTS ---------------- #
        pages["/telegram-bots"] = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Разработка Telegram‑ботов</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
            color: #eee;
            line-height: 1.6;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        header {
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            padding: 30px 20px;
            text-align: center;
            border-bottom: 3px solid #0f4c75;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            margin-bottom: 40px;
        }
        header h1 {
            font-size: 42px;
            color: #3cefff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }
        header p {
            font-size: 18px;
            color: #aaa;
            margin-top: 10px;
        }
        h2 {
            font-size: 32px;
            color: #3cefff;
            margin-bottom: 15px;
            border-left: 5px solid #0f4c75;
            padding-left: 15px;
        }
        p, li {
            font-size: 18px;
            color: #ccc;
            margin-bottom: 15px;
        }
        ul {
            margin-left: 20px;
        }
        .cta {
            display: inline-block;
            padding: 15px 30px;
            background: #0f4c75;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
            font-weight: bold;
            transition: background 0.3s;
        }
        .cta:hover {
            background: #3cefff;
            color: #0f0f0f;
        }
        footer {
            text-align: center;
            margin-top: 60px;
            padding: 30px 20px;
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            border-top: 3px solid #0f4c75;
            box-shadow: 0 -4px 10px rgba(0,0,0,0.5);
            color: #888;
        }
        footer a {
            color: #3cefff;
            text-decoration: none;
            margin: 0 10px;
        }
        footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <h1>Разработка Telegram‑ботов</h1>
        <p>Профессиональные решения под ваши задачи</p>
    </header>

    <div class="container">
        <p>TelegramBots — это профессиональная разработка ботов под ваши задачи. От простых уведомлений до сложных систем с базами данных и оплатой.</p>

        <h2>Что мы делаем</h2>
        <ul>
            <li><strong>Широкий функционал:</strong> От простых информационных ботов до многофункциональных систем с API‑интеграцией.</li>
            <li><strong>Современные технологии:</strong> Используем aiogram и современные инструменты для создания надёжных решений.</li>
            <li><strong>Поддержка после релиза:</strong> Техническая поддержка, обновления и доработки после запуска проекта.</li>
            <li><strong>Прозрачная работа:</strong> Обсуждаем все детали, показываем прогресс и предоставляем полную документацию.</li>
        </ul>

        <a href="https://t.me/krimexAI" class="cta" target="_blank">Обсудить проект →</a>
        <a href="/" class="cta">← Назад к главной</a>
    </div>

    <footer>
        <p>&copy; 2025 Krimex Development</p>
        <p><a href="https://t.me/krimexAI" target="_blank">Telegram</a> • <a href="/">Главная</a></p>
    </footer>
</body>
</html>
        """

        # ---------------- DISCORD BOTS ---------------- #
        pages["/discord-bots"] = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Разработка Discord‑ботов</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
            color: #eee;
            line-height: 1.6;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        header {
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            padding: 30px 20px;
            text-align: center;
            border-bottom: 3px solid #0f4c75;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            margin-bottom: 40px;
        }
        header h1 {
            font-size: 42px;
            color: #3cefff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }
        header p {
            font-size: 18px;
            color: #aaa;
            margin-top: 10px;
        }
        h2 {
            font-size: 32px;
            color: #3cefff;
            margin-bottom: 15px;
            border-left: 5px solid #0f4c75;
            padding-left: 15px;
        }
        p, li {
            font-size: 18px;
            color: #ccc;
            margin-bottom: 15px;
        }
        ul {
            margin-left: 20px;
        }
        .cta {
            display: inline-block;
            padding: 15px 30px;
            background: #0f4c75;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
            font-weight: bold;
            transition: background 0.3s;
        }
        .cta:hover {
            background: #3cefff;
            color: #0f0f0f;
        }
        footer {
            text-align: center;
            margin-top: 60px;
            padding: 30px 20px;
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
            border-top: 3px solid #0f4c75;
            box-shadow: 0 -4px 10px rgba(0,0,0,0.5);
            color: #888;
        }
        footer a {
            color: #3cefff;
            text-decoration: none;
            margin: 0 10px;
        }
        footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <h1>Разработка Discord‑ботов</h1>
        <p>Кастомные боты для игровых серверов и сообществ</p>
    </header>

    <div class="container">
        <p>DiscordBots — это кастомные боты для вашего Discord‑сервера. Модерация, экономика, игры и уникальные функции под любые задачи.</p>

        <h2>Что мы предлагаем</h2>
        <ul>
            <li><strong>Игровые системы:</strong> Внутриигровая экономика, мини‑игры, рейтинговые системы и роли за достижения.</li>
            <li><strong>Автоматизация:</strong> Модерация сообщений, выдача ролей, управление участниками и защита от спама.</li>
            <li><strong>Интеграции:</strong> Подключение внешних API, синхронизация с играми и другими платформами.</li>
            <li><strong>Надёжность:</strong> Стабильная работа 24/7, регулярные обновления и техническая поддержка.</li>
        </ul>

        <a href="https://t.me/krimexAI" class="cta" target="_blank">Обсудить проект →</a>
        <a href="/" class="cta">← Назад к главной</a>
    </div>

    <footer>
        <p>&copy; 2025 Krimex Development</p>
        <p><a href="https://t.me/krimexAI" target="_blank">Telegram</a> • <a href="/">Главная</a></p>
    </footer>
</body>
</html>
        """

        # ---------------- РОУТИНГ ---------------- #
        if path in pages:
            self._serve_html(pages[path])
        elif path == "/favicon.ico":
            # Игнорируем запросы favicon
            self.send_error(204, "No Content")
        else:
            self.send_error(404, "Страница не найдена")

if __name__ == "__main__":
    PORT = 25616
    try:
        with HTTPServer(("", PORT), SimpleHandler) as httpd:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            print(f"✅ Сервер запущен:")
            print(f"   http://localhost:{PORT}")
            print(f"   http://{local_ip}:{PORT}")
            print("\n[Ctrl+C для остановки]")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n❌ Сервер остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
