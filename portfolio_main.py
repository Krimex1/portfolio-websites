from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import socket

# ---------------- КОНФИГУРАЦИЯ ---------------- #
PORT = 25616

class SimpleHandler(BaseHTTPRequestHandler):
    def _serve_html(self, content: str):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def send_error(self, code, message=None):
        self.send_response(code)
        self.end_headers()
        self.wfile.write(f"Error {code}: {message}".encode("utf-8"))

    def do_GET(self):
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        path = self.path.rstrip("/") or "/"

        # ---------------- СТИЛИ (NEO-BRUTALISM) ---------------- #
        base_styles = """
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #1a1a1a;
        color: #fff;
        line-height: 1.6;
    }
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    /* НАВИГАЦИЯ */
    nav {
        background: #000;
        border-bottom: 4px solid #00ff88;
        padding: 20px 0;
        position: sticky;
        top: 0;
        z-index: 100;
        box-shadow: 0 4px 0 #00ff88;
    }
    .nav-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .logo {
        font-size: 28px;
        font-weight: 900;
        color: #00ff88;
        text-decoration: none;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .nav-links {
        display: flex;
        gap: 30px;
        list-style: none;
    }
    .nav-links a {
        color: #fff;
        text-decoration: none;
        font-weight: 700;
        font-size: 16px;
        padding: 10px 20px;
        border: 3px solid transparent;
        transition: all 0.2s;
        text-transform: uppercase;
    }
    .nav-links a:hover, .nav-links a.active {
        border: 3px solid #00ff88;
        background: #00ff88;
        color: #000;
        box-shadow: 4px 4px 0 rgba(0,255,136,0.3);
    }
    
    /* МОБИЛЬНОЕ МЕНЮ */
    .burger {
        display: none;
        flex-direction: column;
        cursor: pointer;
        gap: 5px;
    }
    .burger div {
        width: 30px;
        height: 3px;
        background: #00ff88;
    }
    .mobile-menu {
        display: none;
        background: #000;
        border-top: 3px solid #00ff88;
        padding: 20px;
    }
    .mobile-menu.active {
        display: block;
    }
    .mobile-menu a {
        display: block;
        color: #fff;
        padding: 15px;
        text-decoration: none;
        font-weight: 700;
        border: 3px solid #00ff88;
        margin-bottom: 10px;
        text-align: center;
        text-transform: uppercase;
    }
    .mobile-menu a:hover {
        background: #00ff88;
        color: #000;
    }
    
    /* HERO */
    .hero {
        padding: 100px 20px;
        text-align: center;
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border-bottom: 4px solid #00ff88;
    }
    .hero h1 {
        font-size: 64px;
        font-weight: 900;
        margin-bottom: 20px;
        text-transform: uppercase;
        line-height: 1.1;
        color: #00ff88;
        text-shadow: 4px 4px 0 rgba(0,0,0,0.5);
    }
    .hero p {
        font-size: 20px;
        margin-bottom: 40px;
        color: #ccc;
    }
    .cta-btn {
        display: inline-block;
        padding: 18px 40px;
        background: #00ff88;
        color: #000;
        text-decoration: none;
        font-weight: 900;
        font-size: 18px;
        border: 4px solid #00ff88;
        box-shadow: 6px 6px 0 rgba(0,255,136,0.3);
        transition: all 0.2s;
        text-transform: uppercase;
    }
    .cta-btn:hover {
        transform: translate(4px, 4px);
        box-shadow: 2px 2px 0 rgba(0,255,136,0.3);
    }
    
    /* СЕКЦИИ */
    .section {
        padding: 80px 20px;
    }
    .section h2 {
        font-size: 48px;
        margin-bottom: 40px;
        font-weight: 900;
        text-transform: uppercase;
        border-left: 6px solid #00ff88;
        padding-left: 20px;
    }
    
    /* КАРТОЧКИ */
    .cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 30px;
        margin-top: 40px;
    }
    .card {
        background: #2a2a2a;
        border: 4px solid #00ff88;
        padding: 30px;
        box-shadow: 8px 8px 0 rgba(0,255,136,0.2);
        transition: all 0.3s;
    }
    .card:hover {
        transform: translate(-4px, -4px);
        box-shadow: 12px 12px 0 rgba(0,255,136,0.3);
    }
    .card h3 {
        font-size: 24px;
        margin-bottom: 15px;
        color: #00ff88;
        font-weight: 900;
        text-transform: uppercase;
    }
    .card p {
        color: #ccc;
        margin-bottom: 20px;
    }
    .card-btn {
        display: inline-block;
        padding: 12px 24px;
        background: transparent;
        color: #00ff88;
        border: 3px solid #00ff88;
        text-decoration: none;
        font-weight: 700;
        transition: all 0.2s;
        text-transform: uppercase;
    }
    .card-btn:hover {
        background: #00ff88;
        color: #000;
    }
    
    /* ФУТЕР */
    footer {
        background: #000;
        border-top: 4px solid #00ff88;
        padding: 40px 20px;
        text-align: center;
    }
    footer p {
        color: #666;
    }
    
    /* АДАПТИВ */
    @media (max-width: 768px) {
        .nav-links {
            display: none;
        }
        .burger {
            display: flex;
        }
        .hero h1 {
            font-size: 36px;
        }
        .section h2 {
            font-size: 32px;
        }
        .cards {
            grid-template-columns: 1fr;
        }
    }
</style>
        """

        def get_nav(active_path):
            links = [
                ("/", "ГЛАВНАЯ"),
                ("/bots", "УСЛУГИ"),
                ("/hosting", "ХОСТИНГ"),
                ("https://t.me/krimexAI", "TELEGRAM"),
            ]
            desk_html = ""
            mob_html = ""
            for href, label in links:
                cls = "active" if href == active_path else ""
                desk_html += f'<a href="{href}" class="{cls}">{label}</a>'
                mob_html += f'<a href="{href}">{label}</a>'
            
            return f"""
<nav>
    <div class="container nav-content">
        <a href="/" class="logo">KRIMEX.DEV</a>
        <div class="nav-links">
            {desk_html}
        </div>
        <div class="burger" onclick="document.querySelector('.mobile-menu').classList.toggle('active')">
            <div></div><div></div><div></div>
        </div>
    </div>
</nav>
<div class="mobile-menu">
    {mob_html}
</div>
            """

        # ---------------- ГЛАВНАЯ ---------------- #
        if path == "/":
            html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KRIMEX.DEV - Разработка Telegram ботов</title>
    {base_styles}
</head>
<body>
    {get_nav("/")}
    
    <div class="hero">
        <div class="container">
            <h1>РАЗРАБОТКА<br>TELEGRAM БОТОВ</h1>
            <p>Разработка Telegram/Discord ботов, и инфраструктура. Без лишних слов, только рабочий код.</p>
            <a href="/bots" class="cta-btn">СМОТРЕТЬ УСЛУГИ</a>
        </div>
    </div>
    
    <div class="section">
        <div class="container">
            <h2>МОИ ПРОЕКТЫ</h2>
            <div class="cards">
                <div class="card">
                    <h3>🤖 DARKGPT</h3>
                    <p>Мощный ассистент в Telegram. Пишет код, решает задачи, генерирует контент.</p>
                    <a href="https://t.me/YourBot" class="card-btn">ЗАПУСТИТЬ</a>
                </div>
                <div class="card">
                    <h3>📈 CRYPTO ANALYST</h3>
                    <p>Анализ трендов и курсов криптовалют в реальном времени.</p>
                    <a href="https://t.me/YourBot" class="card-btn">ЗАПУСТИТЬ</a>
                </div>
                <div class="card">
                    <h3>🔍 OSINT TOOLS</h3>
                    <p>Поиск и агрегация информации из открытых источников.</p>
                    <a href="https://t.me/YourBot" class="card-btn">ЗАПУСТИТЬ</a>
                </div>
                <div class="card">
                    <h3>🎮 MINECRAFT</h3>
                    <p>Честный Minecraft сервер без доната и лишних плагинов.</p>
                    <a href="#" class="card-btn">ПОДКЛЮЧИТЬСЯ</a>
                </div>
            </div>
        </div>
    </div>
    
    <footer>
        <div class="container">
            <p>© 2025 KRIMEX.DEV — Все права защищены</p>
        </div>
    </footer>
</body>
</html>
            """
            self._serve_html(html)

        # ---------------- УСЛУГИ ---------------- #
        elif path == "/bots":
            html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Услуги - KRIMEX.DEV</title>
    {base_styles}
</head>
<body>
    {get_nav("/bots")}
    
    <div class="section">
        <div class="container">
            <h2>РАЗРАБОТКА TELEGRAM БОТОВ</h2>
            <div class="cards">
                <div class="card">
                    <h3>💬 БАЗОВЫЕ БОТЫ</h3>
                    <p>Магазины, Web Apps, Платежки, Админки</p>
                    <a href="https://t.me/krimexAI" class="card-btn">ЗАКАЗАТЬ</a>
                </div>
                <div class="card">
                    <h3>🎮 ИГРОВЫЕ БОТЫ</h3>
                    <p>Экономика, Модерация, Игры, Тикеты</p>
                    <a href="https://t.me/krimexAI" class="card-btn">ЗАКАЗАТЬ</a>
                </div>
                <div class="card">
                    <h3>🎨 ДИЗАЙН</h3>
                    <p>Красивые сайты, обложки, сервисы</p>
                    <a href="https://t.me/krimexAI" class="card-btn">ЗАКАЗАТЬ</a>
                </div>
            </div>
        </div>
    </div>
    
    <footer>
        <div class="container">
            <p>© 2025 KRIMEX.DEV</p>
        </div>
    </footer>
</body>
</html>
            """
            self._serve_html(html)

        # ---------------- ХОСТИНГ ---------------- #
        elif path == "/hosting":
            html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Хостинг - KRIMEX.DEV</title>
    {base_styles}
</head>
<body>
    {get_nav("/hosting")}
    
    <div class="hero">
        <div class="container">
            <h1>ПАРТНЕРСКИЙ ХОСТИНГ. ЧЕСТНЫЕ РЕСУРСЫ.</h1>
            <p>Никакого оверселлинга. Только выделенные ядра Ryzen 9 5900X для максимального FPS и скорости работы ботов.</p>
            <a href="https://litehosting.su" class="cta-btn">ВЫБРАТЬ ТАРИФ</a>
        </div>
    </div>
    
    <footer>
        <div class="container">
            <p>© 2025 KRIMEX.DEV</p>
        </div>
    </footer>
</body>
</html>
            """
            self._serve_html(html)

        else:
            self.send_error(404, "Page Not Found")

if __name__ == "__main__":
    try:
        with ThreadingHTTPServer(("", PORT), SimpleHandler) as httpd:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            print(f"✅ Server running:")
            print(f"   http://localhost:{PORT}")
            print(f"   http://{local_ip}:{PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n❌ Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
