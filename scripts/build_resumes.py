from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT_DIR = Path("/System/Library/Fonts/Supplemental")

INK = colors.HexColor("#101828")
NAVY = colors.HexColor("#102033")
BLUE = colors.HexColor("#1E5B92")
TEAL = colors.HexColor("#157A8C")
MUTED = colors.HexColor("#667085")
SOFT = colors.HexColor("#F4F7FB")
SOFT_BLUE = colors.HexColor("#EAF3FA")
RULE = colors.HexColor("#D8E2EC")
WHITE = colors.white


def register_fonts():
    pdfmetrics.registerFont(TTFont("Arial", FONT_DIR / "Arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", FONT_DIR / "Arial Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Italic", FONT_DIR / "Arial Italic.ttf"))


def styles():
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle("Name", parent=base["Normal"], fontName="Arial-Bold", fontSize=21, leading=24, textColor=INK, spaceAfter=2),
        "role": ParagraphStyle("Role", parent=base["Normal"], fontName="Arial-Bold", fontSize=10.5, leading=13, textColor=BLUE, spaceAfter=4),
        "headline": ParagraphStyle("Headline", parent=base["Normal"], fontName="Arial", fontSize=8.4, leading=10.8, textColor=MUTED),
        "contact": ParagraphStyle("Contact", parent=base["Normal"], fontName="Arial", fontSize=7.8, leading=9.6, textColor=BLUE, alignment=TA_RIGHT),
        "section": ParagraphStyle("Section", parent=base["Normal"], fontName="Arial-Bold", fontSize=8.8, leading=10.5, textColor=BLUE, spaceBefore=7, spaceAfter=4, uppercase=True),
        "side_section": ParagraphStyle("SideSection", parent=base["Normal"], fontName="Arial-Bold", fontSize=8.3, leading=10, textColor=NAVY, spaceBefore=7, spaceAfter=3, uppercase=True),
        "body": ParagraphStyle("Body", parent=base["Normal"], fontName="Arial", fontSize=8.25, leading=10.8, textColor=INK, spaceAfter=3.2),
        "compact": ParagraphStyle("Compact", parent=base["Normal"], fontName="Arial", fontSize=7.75, leading=9.5, textColor=INK, spaceAfter=2),
        "job_title": ParagraphStyle("JobTitle", parent=base["Normal"], fontName="Arial-Bold", fontSize=8.8, leading=10.8, textColor=INK, spaceAfter=0.5),
        "job_meta": ParagraphStyle("JobMeta", parent=base["Normal"], fontName="Arial", fontSize=7.6, leading=9, textColor=TEAL, spaceAfter=2.8),
        "bullet": ParagraphStyle("Bullet", parent=base["Normal"], fontName="Arial", fontSize=7.9, leading=9.8, textColor=INK, spaceAfter=1.8),
        "pill": ParagraphStyle("Pill", parent=base["Normal"], fontName="Arial-Bold", fontSize=7.1, leading=8.2, textColor=NAVY, alignment=TA_CENTER),
        "footer": ParagraphStyle("Footer", parent=base["Normal"], fontName="Arial-Italic", fontSize=7.2, leading=8.7, textColor=MUTED, alignment=TA_CENTER),
    }


def link(url, label):
    return f'<link href="{url}" color="#1E5B92">{label}</link>'


def para(text, style):
    return Paragraph(text, style)


def section(title, st, side=False):
    return [para(title, st["side_section" if side else "section"])]


def bullet_list(items, st):
    return ListFlowable(
        [ListItem(para(item, st["bullet"]), leftIndent=7) for item in items],
        bulletType="bullet",
        leftIndent=9,
        bulletFontName="Arial",
        bulletFontSize=5.5,
        bulletColor=BLUE,
        spaceBefore=0,
        spaceAfter=2.5,
    )


def pills(items, st):
    rows = []
    row = []
    for item in items:
        row.append(para(item, st["pill"]))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        row.append("")
        rows.append(row)
    table = Table(rows, colWidths=[31 * mm, 31 * mm], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SOFT_BLUE),
        ("BOX", (0, 0), (-1, -1), 0.25, colors.HexColor("#CFE1EF")),
        ("INNERGRID", (0, 0), (-1, -1), 3, WHITE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return table


def role_block(item, st):
    block = [
        para(item["title"], st["job_title"]),
        para(f'{item["company"]} | {item["dates"]} | {item["duration"]}', st["job_meta"]),
        bullet_list(item["bullets"], st),
    ]
    return KeepTogether(block)


def build_resume(path, content):
    st = styles()
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=14 * mm,
        leftMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=11 * mm,
        title=content["name"],
        author=content["name"],
        subject=content["role"],
        creator="Natalia Lebedinskaya",
    )

    contact = [
        link("mailto:natalia.lebedinskaya@outlook.com", "natalia.lebedinskaya@outlook.com"),
        link("https://www.linkedin.com/in/natalia-lebedinskaya-a588a542b/", "LinkedIn"),
        link("https://github.com/ProhaskoNatalia", "GitHub"),
        link("https://natalia-lebedinskaya.github.io/portfolio/", "Portfolio"),
    ]
    header = Table([[[
        para(content["name"], st["name"]),
        para(content["role"], st["role"]),
        para(content["headline"], st["headline"]),
    ], para("<br/>".join(contact), st["contact"])]], colWidths=[121 * mm, 47 * mm])
    header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))

    fit_cards = Table(
        [
            [para(line, st["compact"]) for line in content["fit"][:3]],
            [para(line, st["compact"]) for line in (content["fit"][3:] + [""])[:3]],
        ],
        colWidths=[56 * mm, 56 * mm, 56 * mm],
    )
    fit_cards.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("BOX", (0, 0), (-1, -1), 0.35, RULE),
        ("INNERGRID", (0, 0), (-1, -1), 4, WHITE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))

    story = [
        header,
        HRFlowable(width="100%", thickness=0.7, color=RULE, spaceBefore=1, spaceAfter=6),
        *section(content["fit_heading"], st),
        fit_cards,
        *section(content["summary_heading"], st),
        para(content["summary"], st["body"]),
        *section(content["stack_heading"], st),
        pills(content["stack"], st),
        Spacer(1, 3),
        para(f'<b>{content["tools_heading"]}:</b> {content["tools"]}', st["body"]),
        para(f'<b>{content["languages_heading"]}:</b> {"; ".join(content["languages"])}', st["body"]),
        para(f'<b>{content["target_heading"]}:</b> {content["target"]}', st["body"]),
        *section(content["experience_heading"], st),
    ]
    for index, item in enumerate(content["experience"]):
        if index == 3:
            story.append(PageBreak())
            story += section(content["experience_heading"], st)
        story.append(role_block(item, st))
        story.append(Spacer(1, 3.5))
    story += section(content["projects_heading"], st)
    for item in content["projects"]:
        text = f'<b>{item["title"]}</b> - {item["description"]}'
        if item.get("url"):
            text += f' {link(item["url"], item["link_label"])}'
        story.append(para(text, st["body"]))
    story += section(content["education_heading"], st)
    story.append(para(content["education"], st["body"]))
    story += section(content["recognition_heading"], st)
    story.append(para(content["recognition"], st["body"]))
    story.append(Spacer(1, 5))
    story.append(para(content["footer"], st["footer"]))
    doc.build(story)


EN = {
    "name": "Natalia Lebedinskaya",
    "role": "Manual QA Engineer | API, Backend and Mobile Testing | Fintech",
    "headline": "QA specialist with banking domain depth, strong manual/API testing practice, SQL validation and product-minded release ownership. Priority: Belgrade office/hybrid QA roles; open to Serbia and remote from Serbia.",
    "fit_heading": "Recruiter fit",
    "fit": ["<b>Target:</b> Manual QA / API QA / Product QA", "<b>Seniority:</b> junior+ / middle- manual QA track", "<b>Salary target:</b> from $1100/month", "<b>Availability:</b> remote start; Serbia-focused", "<b>Work format:</b> Belgrade office/hybrid first"],
    "stack_heading": "Core stack",
    "stack": ["Manual QA", "API testing", "Postman", "SQL", "PostgreSQL", "Swagger", "Regression", "Test cases", "Checklists", "Bug reports", "Mobile QA", "DevTools"],
    "tools_heading": "Tools",
    "tools": "Postman, Swagger/OpenAPI, SQL, PostgreSQL, DBeaver, Test IT, Chrome DevTools, Charles Proxy, Kafka, Kibana, Kubernetes basics, Git/GitHub, Linux/Windows.",
    "languages_heading": "Languages",
    "languages": ["Russian - native", "Ukrainian - native", "English - A1, actively studying", "Serbian - beginner"],
    "education_heading": "Education",
    "education": "Professional retraining diploma - Software Testing Engineer. QA Course - Yandex Educational Technologies, 18 Apr 2024.",
    "target_heading": "Location target",
    "target": "Belgrade, Serbia is the first priority. Open to office/hybrid in Serbia and remote international work from Serbia. Russian-speaking teams or beginner-friendly English/Serbian communication are preferred.",
    "summary_heading": "Profile",
    "summary": "Manual QA / API QA specialist with 2+ years in hands-on testing and 3+ years in banking/fintech operations. I test complex product flows where quality depends on more than UI: API contracts, backend behavior, SQL data integrity, payment/terminal scenarios, migration logic and release risk. My strongest value for recruiters is the combination of QA discipline, fintech domain understanding, clear bug communication and fast onboarding into product context.",
    "experience_heading": "Experience",
    "experience": [
        {"title": "Software Testing Specialist", "company": "VTB Bank", "dates": "Jun 2025 - Present", "duration": "1 yr 3 mos", "bullets": ["Test internal banking services and client-data migration scenarios across UI, API/backend behavior and PostgreSQL data integrity.", "Design focused test cases, checklists and regression coverage for risk areas: data consistency, edge cases, service responses and release readiness.", "Investigate failures with developers and adjacent teams, localize reproducible conditions and turn ambiguous issues into actionable defect reports."]},
        {"title": "QA Engineer", "company": "RNKB Bank", "dates": "Jul 2024 - Jun 2025", "duration": "1 yr", "bullets": ["Tested a federal public-transport payment product, dispatcher and driver services, GPS/telemetry and terminal-related scenarios.", "Covered functional, integration, API and regression checks using Postman, Swagger, Test IT, SQL and Excel.", "Completed onboarding and moved to independent project work in 2 weeks; prepared clear defects and supported release validation."]},
        {"title": "Banking User Support Specialist", "company": "RNKB Bank", "dates": "Mar 2023 - Jul 2024", "duration": "1 yr 5 mos", "bullets": ["Resolved customer and financial requests in a high-volume banking environment, building practical domain knowledge of user pain points and operational flows.", "Reproduced issues, documented context and coordinated resolution with adjacent departments - a foundation for clear QA investigation and bug reporting."]},
        {"title": "Product QA", "company": "Independent AI web/mobile products", "dates": "May 2026 - Present", "duration": "4 mos", "bullets": ["Test user journeys, mobile UI, Telegram Mini App flows, AI generation, API/payment scenarios, edge cases, fixes and release readiness.", "Use product QA thinking: validate not only whether a feature works, but whether the user can recover from errors and complete the intended flow."]},
    ],
    "projects_heading": "Selected product QA projects",
    "projects": [
        {"title": "CareerMove", "description": "private job-search and application-tracking product; QA of aggregation, matching, deduplication, auth, persistence, Telegram/Google Sheets integrations and Serbia-focused vacancy filtering."},
        {"title": "FOT AI", "description": "Telegram Mini App for event photo generation; QA coverage for requirements, negative scenarios, mobile flow, API/payment logic and release checks.", "url": "https://github.com/ProhaskoNatalia/fototime-ai-mini-app", "link_label": "GitHub"},
    ],
    "recognition_heading": "Recognition",
    "recognition": "VTB NFC Award for Outstanding Contribution to Key Business Results (H1 2025) and Award for Excellence in Team Collaboration (2025).",
    "footer": "Portfolio: natalia-lebedinskaya.github.io/portfolio | LinkedIn: natalia-lebedinskaya-a588a542b",
}


RU = {
    "name": "Наталия Лебединская",
    "role": "Manual QA Engineer | API, Backend и Mobile тестирование | Fintech",
    "headline": "QA-специалист с банковским доменным опытом, сильной практикой manual/API testing, SQL-валидацией и продуктовым подходом к релизам. Приоритет - QA office/hybrid в Белграде; также Сербия и remote из Сербии.",
    "fit_heading": "Для рекрутера",
    "fit": ["<b>Цель:</b> Manual QA / API QA / Product QA", "<b>Уровень:</b> junior+ / middle- manual QA track", "<b>Зарплата:</b> от $1100/мес", "<b>Старт:</b> remote start; фокус Сербия", "<b>Формат:</b> Белград office/hybrid в приоритете"],
    "stack_heading": "Ключевой стек",
    "stack": ["Manual QA", "API testing", "Postman", "SQL", "PostgreSQL", "Swagger", "Regression", "Test cases", "Checklists", "Bug reports", "Mobile QA", "DevTools"],
    "tools_heading": "Инструменты",
    "tools": "Postman, Swagger/OpenAPI, SQL, PostgreSQL, DBeaver, Test IT, Chrome DevTools, Charles Proxy, Kafka, Kibana, базово Kubernetes, Git/GitHub, Linux/Windows.",
    "languages_heading": "Языки",
    "languages": ["Русский - родной", "Украинский - родной", "Английский - A1, активно изучаю", "Сербский - начальный"],
    "education_heading": "Образование",
    "education": "Диплом о профессиональной переподготовке - инженер по тестированию ПО. Курс QA - АНО ДПО «Образовательные технологии Яндекса», 18.04.2024.",
    "target_heading": "География",
    "target": "Первый приоритет - Белград, Сербия. Рассматриваю office/hybrid в Сербии и международную удаленную работу из Сербии. Предпочтительны русскоязычные команды или коммуникация, допускающая начальный английский/сербский.",
    "summary_heading": "Профиль",
    "summary": "Manual QA / API QA специалист с 2+ годами практического тестирования и 3+ годами в banking/fintech. Тестирую сложные продуктовые потоки, где качество зависит не только от UI: API-контракты, backend-логика, SQL-целостность данных, платежные/терминальные сценарии, миграции и релизные риски. Моя ценность для команды - сочетание QA-дисциплины, банковского доменного опыта, понятной коммуникации по дефектам и быстрого погружения в продуктовый контекст.",
    "experience_heading": "Опыт",
    "experience": [
        {"title": "Специалист по тестированию", "company": "Банк ВТБ", "dates": "июнь 2025 - настоящее время", "duration": "1 год 3 мес", "bullets": ["Тестирую внутренние банковские сервисы и сценарии миграции клиентских данных: UI, API/backend-поведение и целостность данных в PostgreSQL.", "Проектирую тест-кейсы, чек-листы и регрессионное покрытие для риск-зон: консистентность данных, edge cases, ответы сервисов и готовность релиза.", "Разбираю сбои совместно с разработкой и смежными командами, локализую условия воспроизведения и превращаю неясные проблемы в actionable bug reports."]},
        {"title": "QA Engineer", "company": "РНКБ Банк", "dates": "июль 2024 - июнь 2025", "duration": "1 год", "bullets": ["Тестировала федеральный транспортный платежный продукт, сервисы диспетчеров и водителей, GPS/телеметрию и терминальные сценарии.", "Покрывала functional, integration, API и regression checks с использованием Postman, Swagger, Test IT, SQL и Excel.", "Завершила онбординг и перешла к самостоятельной проектной работе за 2 недели; готовила понятные дефекты и участвовала в release validation."]},
        {"title": "Специалист банковской поддержки", "company": "РНКБ Банк", "dates": "март 2023 - июль 2024", "duration": "1 год 5 мес", "bullets": ["Решала клиентские и финансовые запросы в высоконагруженной банковской среде, сформировала доменное понимание пользовательских проблем и операционных процессов.", "Воспроизводила проблемы, фиксировала контекст и координировала решение со смежными подразделениями - это стало базой для QA investigation и баг-репортинга."]},
        {"title": "Product QA", "company": "Независимые AI web/mobile продукты", "dates": "май 2026 - настоящее время", "duration": "4 мес", "bullets": ["Проверяю user journeys, mobile UI, Telegram Mini App flows, AI-генерацию, API/payment scenarios, edge cases, исправления и готовность релиза.", "Использую продуктовый QA-подход: проверяю не только работу функции, но и восстановление после ошибок и завершение целевого пользовательского сценария."]},
    ],
    "projects_heading": "Product QA проекты",
    "projects": [
        {"title": "CareerMove", "description": "приватный продукт для поиска вакансий и учета откликов; QA агрегации, matching, дедупликации, авторизации, сохранения данных, Telegram/Google Sheets интеграций и Serbia-focused фильтрации вакансий."},
        {"title": "FOT AI", "description": "Telegram Mini App для генерации фотографий с мероприятия; QA-покрытие требований, негативных сценариев, mobile flow, API/payment logic и release checks.", "url": "https://github.com/ProhaskoNatalia/fototime-ai-mini-app", "link_label": "GitHub"},
    ],
    "recognition_heading": "Признание",
    "recognition": "Награды VTB NFC за значимый вклад в ключевые бизнес-результаты (I полугодие 2025) и командное взаимодействие (2025).",
    "footer": "Portfolio: natalia-lebedinskaya.github.io/portfolio | LinkedIn: natalia-lebedinskaya-a588a542b",
}


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    register_fonts()
    build_resume(ASSETS / "Natalia_Lebedinskaya_EN.pdf", EN)
    build_resume(ASSETS / "Natalia_Lebedinskaya_RU.pdf", RU)
    build_resume(ASSETS / "Natalia_Lebedinskaya_QA_EN_2026-08.pdf", EN)
    build_resume(ASSETS / "Natalia_Lebedinskaya_QA_RU_2026-08.pdf", RU)
