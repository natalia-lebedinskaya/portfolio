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
                    link("https://www.linkedin.com/in/natalia-lebedinskaya-115512422/", "LinkedIn"),
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
        story.append(
            Paragraph(
                f'<b>{item["title"]}</b> - {item["description"]} {link(item["url"], item["link_label"])}',
                st["body"],
            )
        )

    section(story, st, content["education_heading"])
    story.append(Paragraph(content["education"], st["body"]))

    story.append(Paragraph(content["footer"], st["footer"]))
    doc.build(story)


EN = {
    "name": "Natalia Lebedinskaya",
    "role": "Manual QA Engineer | API / Backend Testing | Fintech and AI Products",
    "meta": "Russian citizen | Moving to Da Nang, Vietnam in early September 2026 | Remote worldwide / Vietnam | English A1, actively studying",
    "summary_heading": "PROFILE",
    "summary": (
        "Manual QA / API QA specialist with 2+ years of hands-on QA and 3+ years in banking and fintech. "
        "Experience testing banking services, client-data migrations, payment and terminal flows, and web/mobile AI products. "
        "Strong in API/backend validation, SQL data checks, regression, defect investigation, test documentation and user support. "
        "Available to start remotely now; based in Da Nang from early September 2026. Seeking remote international or Vietnam-based work with clear written contract and payment terms."
    ),
    "skills_heading": "SKILLS AND PROFICIENCY",
    "skills": [
        ("Strong", "Manual, functional, regression, smoke, integration and exploratory testing; test design; test cases; checklists; actionable bug reports; Postman; REST API; SQL; PostgreSQL; Swagger/OpenAPI"),
        ("Working knowledge", "DBeaver, Kafka, Kibana, Kubernetes, Linux/Windows, Test IT, Chrome DevTools, Charles Proxy, Git/GitHub, mobile and web testing, release validation"),
        ("Fundamentals", "Playwright and test-automation concepts"),
        ("Soft skills", "Analytical thinking, clear written communication, ownership, cross-functional collaboration and user empathy"),
        ("Languages", "Russian and Ukrainian - native; English - A1, actively studying"),
    ],
    "experience_heading": "EXPERIENCE",
    "experience": [
        {
            "title": "Software Testing Specialist | VTB Bank | Jun 2025 - Present",
            "lines": [
                "Test internal banking services and client-data migration scenarios; validate UI, API/backend flows and SQL/PostgreSQL data.",
                "Create test cases, checklists and defect reports; investigate failures and support regression and release validation with development and adjacent teams.",
            ],
        },
        {
            "title": "QA Engineer | RNKB Bank | Jul 2024 - Jun 2025",
            "lines": [
                "Tested a federal public-transport payment product, dispatcher and driver services, GPS and telemetry through functional, integration, API and regression checks.",
                "Used Postman, Swagger, Test IT, SQL and Excel; completed onboarding and moved to independent project work in 2 weeks.",
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
                "Test user journeys, mobile UI, AI generation, API and payment scenarios, edge cases, fixes and release readiness.",
            ],
        },
    ],
    "projects_heading": "SELECTED PET PROJECTS",
    "projects": [
        {
            "title": "CareerMove",
            "description": "job-search and application-tracking web app; QA of aggregation, filtering, deduplication, auth, persistence and integrations.",
            "url": "https://careermove-web.vercel.app",
            "link_label": "Live product",
        },
        {
            "title": "FOT AI",
            "description": "Telegram Mini App for event photo generation; requirements, negative scenarios, API and payment-flow coverage, and release checks.",
            "url": "https://github.com/natalia-lebedinskaya/fototime-ai-mini-app",
            "link_label": "GitHub",
        },
    ],
    "education_heading": "EDUCATION AND RECOGNITION",
    "education": (
        "Professional retraining diploma - Software Testing Engineer. QA Course - Yandex Educational Technologies, 18 Apr 2024. "
        "VTB NFC Award for Outstanding Contribution to Key Business Results (H1 2025) and Award for Excellence in Team Collaboration (2025)."
    ),
    "footer": "Available for remote international work now | Relocating to Da Nang, Vietnam in early September 2026",
}


RU = {
    "name": "Наталия Лебединская",
    "role": "Manual QA Engineer | API / Backend тестирование | Fintech и AI-продукты",
    "meta": "Гражданство РФ | Переезд в Дананг, Вьетнам в начале сентября 2026 | Международная удаленка / Вьетнам | Английский A1, активно изучаю",
    "summary_heading": "ПРОФИЛЬ",
    "summary": (
        "Manual QA / API QA специалист с 2+ годами практического опыта в тестировании и 3+ годами в банковской и fintech-сфере. "
        "Тестирую банковские сервисы, миграцию клиентских данных, платежные и терминальные сценарии, web/mobile AI-продукты. "
        "Сильные стороны: API/backend-проверки, SQL-валидация данных, регресс, локализация дефектов, тестовая документация и поддержка пользователей. "
        "Могу начать удаленно сейчас; с начала сентября 2026 живу в Дананге. Рассматриваю международную удаленную работу или работу во Вьетнаме с понятным письменным договором и условиями оплаты."
    ),
    "skills_heading": "НАВЫКИ И УРОВЕНЬ",
    "skills": [
        ("Уверенно", "ручное, функциональное, регрессионное, smoke, интеграционное и исследовательское тестирование; тест-дизайн; тест-кейсы; чек-листы; баг-репорты; Postman; REST API; SQL; PostgreSQL; Swagger/OpenAPI"),
        ("Рабочий уровень", "DBeaver, Kafka, Kibana, Kubernetes, Linux/Windows, Test IT, Chrome DevTools, Charles Proxy, Git/GitHub, mobile/web тестирование, release validation"),
        ("Основы", "Playwright и принципы автоматизации тестирования"),
        ("Soft skills", "аналитическое мышление, ясная письменная коммуникация, ответственность, взаимодействие со смежными командами, внимание к пользовательскому опыту"),
        ("Языки", "русский и украинский - родные; английский - A1, активно изучаю"),
    ],
    "experience_heading": "ОПЫТ",
    "experience": [
        {
            "title": "Специалист по тестированию | Банк ВТБ | июнь 2025 - настоящее время",
            "lines": [
                "Тестирую внутренние банковские сервисы и сценарии миграции клиентских данных; проверяю UI, API/backend-потоки и данные в SQL/PostgreSQL.",
                "Создаю тест-кейсы, чек-листы и баг-репорты; локализую сбои, провожу регресс и release validation совместно с разработкой и смежными командами.",
            ],
        },
        {
            "title": "QA Engineer | РНКБ Банк | июль 2024 - июнь 2025",
            "lines": [
                "Тестировала федеральный транспортный платежный продукт, сервисы диспетчеров и водителей, GPS и телеметрию: functional, integration, API и regression.",
                "Работала с Postman, Swagger, Test IT, SQL и Excel; завершила онбординг и перешла к самостоятельной проектной работе за 2 недели.",
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
                "Проверяю пользовательские сценарии, mobile UI, AI-генерацию, API и платежные потоки, edge cases, исправления и готовность релиза.",
            ],
        },
    ],
    "projects_heading": "PET PROJECTS",
    "projects": [
        {
            "title": "CareerMove",
            "description": "web-сервис поиска вакансий и учета откликов; тестирование агрегации, фильтров, дедупликации, авторизации, сохранения данных и интеграций.",
            "url": "https://careermove-web.vercel.app",
            "link_label": "Открыть сервис",
        },
        {
            "title": "FOT AI",
            "description": "Telegram Mini App для генерации фотографий с мероприятия; требования, негативные сценарии, API, платежные потоки и release checks.",
            "url": "https://github.com/natalia-lebedinskaya/fototime-ai-mini-app",
            "link_label": "GitHub",
        },
    ],
    "education_heading": "ОБРАЗОВАНИЕ И ПРИЗНАНИЕ",
    "education": (
        "Диплом о профессиональной переподготовке - инженер по тестированию ПО. Курс QA - АНО ДПО «Образовательные технологии Яндекса», 18.04.2024. "
        "Награды VTB NFC за значимый вклад в ключевые бизнес-результаты (I полугодие 2025) и командное взаимодействие (2025)."
    ),
    "footer": "Готова к международной удаленной работе сейчас | Переезд в Дананг, Вьетнам в начале сентября 2026",
}


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    register_fonts()
    build_resume(ASSETS / "Natalia_Lebedinskaya_EN.pdf", EN)
    build_resume(ASSETS / "Natalia_Lebedinskaya_RU.pdf", RU)
