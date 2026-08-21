from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT_DIR = Path("/System/Library/Fonts/Supplemental")

NAVY = colors.HexColor("#0B1728")
BLUE = colors.HexColor("#1565A8")
MUTED = colors.HexColor("#53657A")
RULE = colors.HexColor("#CCD8E5")


def register_fonts():
    pdfmetrics.registerFont(TTFont("Arial", FONT_DIR / "Arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", FONT_DIR / "Arial Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Italic", FONT_DIR / "Arial Italic.ttf"))


def styles():
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "Name",
            parent=base["Normal"],
            fontName="Arial-Bold",
            fontSize=20,
            leading=22,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=3,
        ),
        "role": ParagraphStyle(
            "Role",
            parent=base["Normal"],
            fontName="Arial-Bold",
            fontSize=10.5,
            leading=12.5,
            textColor=BLUE,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=base["Normal"],
            fontName="Arial",
            fontSize=8,
            leading=10,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=3,
        ),
        "contact": ParagraphStyle(
            "Contact",
            parent=base["Normal"],
            fontName="Arial",
            fontSize=7.8,
            leading=9.5,
            textColor=BLUE,
            alignment=TA_CENTER,
            spaceAfter=5,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base["Normal"],
            fontName="Arial-Bold",
            fontSize=10.2,
            leading=12,
            textColor=BLUE,
            spaceBefore=4,
            spaceAfter=2.5,
            borderWidth=0,
            borderColor=RULE,
            borderPadding=0,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontName="Arial",
            fontSize=8.3,
            leading=10.3,
            textColor=NAVY,
            spaceAfter=2.5,
        ),
        "job": ParagraphStyle(
            "Job",
            parent=base["Normal"],
            fontName="Arial-Bold",
            fontSize=8.5,
            leading=10.4,
            textColor=NAVY,
            spaceBefore=1.5,
            spaceAfter=1,
        ),
        "detail": ParagraphStyle(
            "Detail",
            parent=base["Normal"],
            fontName="Arial",
            fontSize=8.05,
            leading=9.8,
            textColor=NAVY,
            leftIndent=7,
            firstLineIndent=-7,
            spaceAfter=1.5,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base["Normal"],
            fontName="Arial-Italic",
            fontSize=7.3,
            leading=9,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceBefore=4,
        ),
    }


def link(url, label):
    return f'<link href="{url}" color="#1565A8">{label}</link>'


def section(story, st, title):
    story.append(Paragraph(title, st["section"]))
    story.append(Spacer(1, 0.7))


def job(story, st, title, lines):
    block = [Paragraph(title, st["job"])]
    block.extend(Paragraph(f"- {line}", st["detail"]) for line in lines)
    story.append(KeepTogether(block))


def build_resume(path, content):
    st = styles()
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=12 * mm,
        bottomMargin=11 * mm,
        title=content["name"],
        author=content["name"],
        subject=content["role"],
        creator="Natalia Lebedinskaya",
    )

    story = [
        Paragraph(content["name"], st["name"]),
        Paragraph(content["role"], st["role"]),
        Paragraph(content["meta"], st["meta"]),
        Paragraph(
            " | ".join(
                [
                    link("mailto:natalia.lebedinskaya@outlook.com", "natalia.lebedinskaya@outlook.com"),
                    link("https://github.com/ProhaskoNatalia", "GitHub"),
                    link("https://natalia-lebedinskaya.github.io/portfolio/", "Portfolio"),
                    link("https://www.linkedin.com/in/natalia-lebedinskaya-a588a542b/", "LinkedIn"),
                ]
            ),
            st["contact"],
        ),
    ]

    section(story, st, content["summary_heading"])
    story.append(Paragraph(content["summary"], st["body"]))

    section(story, st, content["skills_heading"])
    for label, value in content["skills"]:
        story.append(Paragraph(f"<b>{label}:</b> {value}", st["body"]))

    section(story, st, content["experience_heading"])
    for item in content["experience"]:
        job(story, st, item["title"], item["lines"])

    section(story, st, content["projects_heading"])
    for item in content["projects"]:
        project_text = f'<b>{item["title"]}</b> - {item["description"]}'
        if item.get("url"):
            project_text += f' {link(item["url"], item["link_label"])}'
        story.append(
            Paragraph(
                project_text,
                st["body"],
            )
        )

    section(story, st, content["education_heading"])
    story.append(Paragraph(content["education"], st["body"]))

    story.append(Paragraph(content["footer"], st["footer"]))
    doc.build(story)


EN = {
    "name": "Natalia Lebedinskaya",
    "role": "Manual QA Engineer | API / Backend / Mobile Testing | Fintech and AI Products",
    "meta": "Russian citizen | Belgrade, Serbia focus | Office/hybrid in Serbia or remote from Serbia | English A1, Serbian beginner, actively studying",
    "summary_heading": "PROFILE",
    "summary": (
        "Manual QA / API QA specialist with 2+ years of hands-on QA and 3+ years in banking and fintech. "
        "Experience testing banking services, client-data migrations, public-transport payment products, terminal flows, web/mobile AI products and Telegram Mini App scenarios. "
        "Strong in requirements analysis, API/backend validation, SQL data checks, regression, defect investigation, test documentation and clear user-facing bug reports. "
        "Focused on Serbia: office/hybrid roles in Belgrade are the first priority, other Serbian cities are open, and international remote work from Serbia is also suitable."
    ),
    "skills_heading": "SKILLS AND PROFICIENCY",
    "skills": [
        ("Strong", "Manual, functional, regression, smoke, integration and exploratory testing; requirements analysis; test design; test cases; checklists; actionable bug reports; Postman; REST API; SQL; PostgreSQL; Swagger/OpenAPI"),
        ("Working knowledge", "DBeaver, Kafka, Kibana, Kubernetes, Linux/Windows, Test IT, Chrome DevTools, Charles Proxy, Git/GitHub, mobile and web testing, Telegram bot and Mini App testing, release validation"),
        ("Fundamentals", "Playwright, test-automation concepts, HTML/CSS/JavaScript basics for QA communication"),
        ("Soft skills", "Analytical thinking, clear written communication, ownership, cross-functional collaboration and user empathy"),
        ("Languages", "Russian and Ukrainian - native; English - A1, actively studying; Serbian - beginner"),
    ],
    "experience_heading": "EXPERIENCE",
    "experience": [
        {
            "title": "Software Testing Specialist | VTB Bank | Jun 2025 - Present",
            "lines": [
                "Test internal banking services and client-data migration scenarios; validate UI, API/backend flows and SQL/PostgreSQL data integrity.",
                "Create test cases, checklists and defect reports; investigate failures, localize root conditions and support regression and release validation with development and adjacent teams.",
            ],
        },
        {
            "title": "QA Engineer | RNKB Bank | Jul 2024 - Jun 2025",
            "lines": [
                "Tested a federal public-transport payment product, dispatcher and driver services, GPS/telemetry and terminal-related scenarios through functional, integration, API and regression checks.",
                "Used Postman, Swagger, Test IT, SQL and Excel; prepared clear defects and completed onboarding to independent project work in 2 weeks.",
            ],
        },
        {
            "title": "Banking User Support Specialist | RNKB Bank | Mar 2023 - Jul 2024",
            "lines": [
                "Resolved customer and financial requests in a high-volume contact center; reproduced issues, documented context and coordinated resolution with adjacent departments.",
            ],
        },
        {
            "title": "Product QA | Independent AI web/mobile products | May 2026 - Present",
            "lines": [
                "Test user journeys, mobile UI, Telegram Mini App flows, AI generation, API and payment scenarios, edge cases, fixes and release readiness.",
            ],
        },
    ],
    "projects_heading": "SELECTED PET PROJECTS",
    "projects": [
        {
            "title": "CareerMove (private pet project)",
            "description": "job-search and application-tracking web app; QA of aggregation, filtering, deduplication, auth, persistence, Telegram/Google Sheets integrations and Serbia-focused matching logic.",
        },
        {
            "title": "FOT AI",
            "description": "Telegram Mini App for event photo generation; requirements, negative scenarios, API and payment-flow coverage, and release checks.",
            "url": "https://github.com/ProhaskoNatalia/fototime-ai-mini-app",
            "link_label": "GitHub",
        },
    ],
    "education_heading": "EDUCATION AND RECOGNITION",
    "education": (
        "Professional retraining diploma - Software Testing Engineer. QA Course - Yandex Educational Technologies, 18 Apr 2024. "
        "VTB NFC Award for Outstanding Contribution to Key Business Results (H1 2025) and Award for Excellence in Team Collaboration (2025)."
    ),
    "footer": "Priority: Belgrade office/hybrid QA role | Open to Serbia and remote from Serbia",
}


RU = {
    "name": "Наталия Лебединская",
    "role": "Manual QA Engineer | API / Backend / Mobile тестирование | Fintech и AI-продукты",
    "meta": "Гражданство РФ | Фокус Белград, Сербия | Офис/гибрид в Сербии или remote из Сербии | Английский A1, сербский начальный, активно изучаю",
    "summary_heading": "ПРОФИЛЬ",
    "summary": (
        "Manual QA / API QA специалист с 2+ годами практического опыта в тестировании и 3+ годами в banking/fintech. "
        "Тестирую банковские сервисы, миграцию клиентских данных, транспортные платежные продукты, терминальные сценарии, web/mobile AI-продукты и Telegram Mini App сценарии. "
        "Сильные стороны: анализ требований, API/backend-проверки, SQL-валидация данных, регресс, локализация дефектов, тестовая документация и понятные баг-репорты. "
        "Фокус на Сербии: первый приоритет - офис/гибрид в Белграде, также рассматриваю другие города Сербии и международную удаленную работу из Сербии."
    ),
    "skills_heading": "НАВЫКИ И УРОВЕНЬ",
    "skills": [
        ("Уверенно", "ручное, функциональное, регрессионное, smoke, интеграционное и исследовательское тестирование; анализ требований; тест-дизайн; тест-кейсы; чек-листы; баг-репорты; Postman; REST API; SQL; PostgreSQL; Swagger/OpenAPI"),
        ("Рабочий уровень", "DBeaver, Kafka, Kibana, Kubernetes, Linux/Windows, Test IT, Chrome DevTools, Charles Proxy, Git/GitHub, mobile/web тестирование, тестирование Telegram bot/Mini App, release validation"),
        ("Основы", "Playwright, принципы автоматизации тестирования, HTML/CSS/JavaScript для коммуникации с разработкой"),
        ("Soft skills", "аналитическое мышление, ясная письменная коммуникация, ответственность, взаимодействие со смежными командами, внимание к пользовательскому опыту"),
        ("Языки", "русский и украинский - родные; английский - A1, активно изучаю; сербский - начальный"),
    ],
    "experience_heading": "ОПЫТ",
    "experience": [
        {
            "title": "Специалист по тестированию | Банк ВТБ | июнь 2025 - настоящее время",
            "lines": [
                "Тестирую внутренние банковские сервисы и сценарии миграции клиентских данных; проверяю UI, API/backend-потоки и целостность данных в SQL/PostgreSQL.",
                "Создаю тест-кейсы, чек-листы и баг-репорты; локализую условия воспроизведения, провожу регресс и release validation совместно с разработкой и смежными командами.",
            ],
        },
        {
            "title": "QA Engineer | РНКБ Банк | июль 2024 - июнь 2025",
            "lines": [
                "Тестировала федеральный транспортный платежный продукт, сервисы диспетчеров и водителей, GPS/телеметрию и терминальные сценарии: functional, integration, API и regression.",
                "Работала с Postman, Swagger, Test IT, SQL и Excel; готовила понятные дефекты и перешла к самостоятельной проектной работе за 2 недели.",
            ],
        },
        {
            "title": "Специалист банковской поддержки | РНКБ Банк | март 2023 - июль 2024",
            "lines": [
                "Решала клиентские и финансовые запросы в контакт-центре, воспроизводила проблемы, фиксировала контекст и координировала решение со смежными подразделениями.",
            ],
        },
        {
            "title": "Product QA | Независимые AI web/mobile продукты | май 2026 - настоящее время",
            "lines": [
                "Проверяю пользовательские сценарии, mobile UI, Telegram Mini App flows, AI-генерацию, API и платежные потоки, edge cases, исправления и готовность релиза.",
            ],
        },
    ],
    "projects_heading": "PET PROJECTS",
    "projects": [
        {
            "title": "CareerMove (приватный pet project)",
            "description": "web-сервис поиска вакансий и учета откликов; тестирование агрегации, фильтров, дедупликации, авторизации, сохранения данных, Telegram/Google Sheets интеграций и Serbia-focused matching logic.",
        },
        {
            "title": "FOT AI",
            "description": "Telegram Mini App для генерации фотографий с мероприятия; требования, негативные сценарии, API, платежные потоки и release checks.",
            "url": "https://github.com/ProhaskoNatalia/fototime-ai-mini-app",
            "link_label": "GitHub",
        },
    ],
    "education_heading": "ОБРАЗОВАНИЕ И ПРИЗНАНИЕ",
    "education": (
        "Диплом о профессиональной переподготовке - инженер по тестированию ПО. Курс QA - АНО ДПО «Образовательные технологии Яндекса», 18.04.2024. "
        "Награды VTB NFC за значимый вклад в ключевые бизнес-результаты (I полугодие 2025) и командное взаимодействие (2025)."
    ),
    "footer": "Приоритет: QA office/hybrid в Белграде | Открыта к Сербии и remote из Сербии",
}


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    register_fonts()
    build_resume(ASSETS / "Natalia_Lebedinskaya_EN.pdf", EN)
    build_resume(ASSETS / "Natalia_Lebedinskaya_RU.pdf", RU)
    build_resume(ASSETS / "Natalia_Lebedinskaya_QA_EN_2026-08.pdf", EN)
    build_resume(ASSETS / "Natalia_Lebedinskaya_QA_RU_2026-08.pdf", RU)
