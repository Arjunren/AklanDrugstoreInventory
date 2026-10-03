from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    XPreformatted,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Arjunren_Valdez_IntermediateMobileProg_04TaskPerformance1.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

GREEN = colors.HexColor("#167A53")
DARK_GREEN = colors.HexColor("#123D2E")
PALE_GREEN = colors.HexColor("#E8F2ED")
INK = colors.HexColor("#18352A")
MUTED = colors.HexColor("#61736B")
LIGHT = colors.HexColor("#F3F6F4")
ORANGE = colors.HexColor("#C65911")


class SubmissionDocTemplate(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=16 * mm,
            rightMargin=16 * mm,
            topMargin=18 * mm,
            bottomMargin=16 * mm,
            title="Aklan Drugstore Inventory - Project Documentation",
            author="Arjunren Valdez",
            subject="Intermediate Mobile Programming Task Performance",
        )
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="content",
        )
        self.addPageTemplates(PageTemplate(id="standard", frames=frame, onPage=self.draw_page))

    def draw_page(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D6E2DC"))
        canvas.line(16 * mm, 13 * mm, A4[0] - 16 * mm, 13 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(16 * mm, 8.5 * mm, "Aklan Drugstore Inventory")
        canvas.drawRightString(A4[0] - 16 * mm, 8.5 * mm, f"Page {doc.page}")
        canvas.restoreState()


class ScreenMockup(Flowable):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.width = 175 * mm
        self.height = 102 * mm

    def draw_label(self, canvas, x, y, text, size=8, color=INK, font="Helvetica"):
        canvas.setFillColor(color)
        canvas.setFont(font, size)
        canvas.drawString(x, y, text)

    def card(self, canvas, x, y, w, h, fill=colors.white):
        canvas.setFillColor(fill)
        canvas.setStrokeColor(colors.HexColor("#D8E3DD"))
        canvas.roundRect(x, y, w, h, 7, fill=1, stroke=1)

    def draw(self):
        c = self.canv
        c.setFillColor(colors.HexColor("#E9EFEC"))
        c.setStrokeColor(colors.HexColor("#B8C9C0"))
        c.roundRect(0, 0, self.width, self.height, 10, fill=1, stroke=1)
        c.setFillColor(colors.white)
        c.roundRect(7, 7, self.width - 14, self.height - 14, 6, fill=1, stroke=0)

        if self.screen == "login":
            self.draw_login(c)
        elif self.screen == "dashboard":
            self.draw_dashboard(c)
        elif self.screen == "inventory":
            self.draw_inventory(c)
        else:
            self.draw_audit(c)

    def draw_login(self, c):
        w, h = 76 * mm, 72 * mm
        x, y = (self.width - w) / 2, (self.height - h) / 2
        self.card(c, x, y, w, h)
        c.setFillColor(GREEN)
        c.roundRect(x + 30 * mm, y + 53 * mm, 16 * mm, 13 * mm, 5, fill=1, stroke=0)
        self.draw_label(c, x + 35 * mm, y + 57 * mm, "Rx", 14, colors.white, "Helvetica-Bold")
        self.draw_label(c, x + 17 * mm, y + 44 * mm, "Aklan Drugstore", 14, DARK_GREEN, "Helvetica-Bold")
        self.draw_label(c, x + 16 * mm, y + 38 * mm, "Inventory Management System", 8, MUTED)
        for offset, label in [(28, "Username: admin"), (19, "Password: ********")]:
            c.setFillColor(LIGHT)
            c.roundRect(x + 10 * mm, y + offset * mm, w - 20 * mm, 7 * mm, 3, fill=1, stroke=0)
            self.draw_label(c, x + 13 * mm, y + (offset + 2.4) * mm, label, 7, MUTED)
        c.setFillColor(GREEN)
        c.roundRect(x + 10 * mm, y + 8 * mm, w - 20 * mm, 7 * mm, 3, fill=1, stroke=0)
        self.draw_label(c, x + 31 * mm, y + 10.3 * mm, "LOG IN", 8, colors.white, "Helvetica-Bold")

    def sidebar(self, c, title):
        c.setFillColor(DARK_GREEN)
        c.roundRect(7, 7, 36 * mm, self.height - 14, 6, fill=1, stroke=0)
        self.draw_label(c, 12 * mm, self.height - 17 * mm, "AKLAN", 7, colors.HexColor("#A7E0C6"))
        self.draw_label(c, 12 * mm, self.height - 24 * mm, "Drugstore", 10, colors.white, "Helvetica-Bold")
        for index, name in enumerate(["Dashboard", "Inventory", "Audit Trail"]):
            color = colors.white if name == title else colors.HexColor("#C9E0D5")
            self.draw_label(c, 12 * mm, self.height - (40 + index * 11) * mm, name, 8, color)
        self.draw_label(c, 12 * mm, 16 * mm, "Arjunren Valdez", 6.5, colors.HexColor("#C9E0D5"))
        self.draw_label(c, 12 * mm, 11 * mm, "Log out", 7, colors.white)

    def draw_dashboard(self, c):
        self.sidebar(c, "Dashboard")
        x0 = 49 * mm
        self.draw_label(c, x0, self.height - 18 * mm, "Dashboard", 15, DARK_GREEN, "Helvetica-Bold")
        stats = [("Products", "4", GREEN), ("Total units", "84", GREEN), ("Low stock", "1", ORANGE)]
        for i, (label, value, color) in enumerate(stats):
            x = x0 + i * 39 * mm
            self.card(c, x, self.height - 45 * mm, 34 * mm, 20 * mm)
            self.draw_label(c, x + 4 * mm, self.height - 32 * mm, label, 7, MUTED)
            self.draw_label(c, x + 4 * mm, self.height - 41 * mm, value, 16, color, "Helvetica-Bold")
        self.card(c, x0, 14 * mm, 112 * mm, 37 * mm)
        self.draw_label(c, x0 + 4 * mm, 45 * mm, "Stock level chart", 9, INK, "Helvetica-Bold")
        bars = [(18, "Para"), (13, "Vit C"), (7, "Alcohol"), (23, "Mask")]
        for i, (bar_h, label) in enumerate(bars):
            x = x0 + (15 + i * 22) * mm
            c.setFillColor(colors.HexColor("#3BA575"))
            c.roundRect(x, 21 * mm, 8 * mm, bar_h * mm / 2, 3, fill=1, stroke=0)
            self.draw_label(c, x - 1 * mm, 17 * mm, label, 6, MUTED)

    def draw_inventory(self, c):
        self.sidebar(c, "Inventory")
        x0 = 49 * mm
        self.draw_label(c, x0, self.height - 17 * mm, "Inventory Management", 14, DARK_GREEN, "Helvetica-Bold")
        self.card(c, x0, 13 * mm, 43 * mm, 65 * mm)
        self.draw_label(c, x0 + 4 * mm, 70 * mm, "Product details", 9, INK, "Helvetica-Bold")
        for i, label in enumerate(["Product name", "Category", "Quantity", "Price", "Expiry date"]):
            y = (61 - i * 9) * mm
            c.setFillColor(LIGHT)
            c.roundRect(x0 + 4 * mm, y, 35 * mm, 6 * mm, 2, fill=1, stroke=0)
            self.draw_label(c, x0 + 6 * mm, y + 2 * mm, label, 6, MUTED)
        for i, (label, color) in enumerate([("Add", GREEN), ("Update", colors.HexColor("#2F6F9F")), ("Delete", colors.HexColor("#B33A3A")), ("Clear", MUTED)]):
            bx = x0 + (4 + (i % 2) * 18) * mm
            by = (16 + (1 - i // 2) * 8) * mm
            c.setFillColor(color)
            c.roundRect(bx, by, 16 * mm, 6 * mm, 2, fill=1, stroke=0)
            self.draw_label(c, bx + 4 * mm, by + 2 * mm, label, 6, colors.white)
        tx = x0 + 48 * mm
        self.card(c, tx, 13 * mm, 64 * mm, 65 * mm)
        headers = ["Product", "Category", "Qty", "Price"]
        positions = [tx + 3 * mm, tx + 27 * mm, tx + 47 * mm, tx + 55 * mm]
        c.setFillColor(PALE_GREEN)
        c.rect(tx + 2 * mm, 66 * mm, 60 * mm, 8 * mm, fill=1, stroke=0)
        for pos, header in zip(positions, headers):
            self.draw_label(c, pos, 69 * mm, header, 6, INK, "Helvetica-Bold")
        rows = [
            ("Paracetamol", "Medicine", "25", "5.50"),
            ("Vitamin C", "Vitamins", "18", "8.00"),
            ("Alcohol 70%", "First Aid", "9", "45.00"),
            ("Face Mask", "Supplies", "32", "3.00"),
        ]
        for i, row in enumerate(rows):
            y = (58 - i * 10) * mm
            for pos, value in zip(positions, row):
                self.draw_label(c, pos, y, value, 5.5, MUTED)
            c.setStrokeColor(colors.HexColor("#E4EBE7"))
            c.line(tx + 2 * mm, y - 2 * mm, tx + 62 * mm, y - 2 * mm)

    def draw_audit(self, c):
        self.sidebar(c, "Audit Trail")
        x0 = 49 * mm
        self.draw_label(c, x0, self.height - 17 * mm, "Audit Trail", 14, DARK_GREEN, "Helvetica-Bold")
        self.card(c, x0, 14 * mm, 112 * mm, 63 * mm)
        c.setFillColor(PALE_GREEN)
        c.rect(x0 + 3 * mm, 65 * mm, 106 * mm, 8 * mm, fill=1, stroke=0)
        for x, label in [(x0 + 5 * mm, "Date and time"), (x0 + 42 * mm, "Action"), (x0 + 67 * mm, "Details")]:
            self.draw_label(c, x, 68 * mm, label, 7, INK, "Helvetica-Bold")
        rows = [
            ("Oct 04, 01:22", "UPDATE", "Updated Alcohol 70%"),
            ("Oct 04, 01:20", "ADD", "Added Face Mask"),
            ("Oct 04, 01:18", "LOGIN", "Administrator logged in"),
        ]
        for i, row in enumerate(rows):
            y = (56 - i * 13) * mm
            self.draw_label(c, x0 + 5 * mm, y, row[0], 6.5, MUTED)
            self.draw_label(c, x0 + 42 * mm, y, row[1], 6.5, GREEN, "Helvetica-Bold")
            self.draw_label(c, x0 + 67 * mm, y, row[2], 6.5, MUTED)


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=27,
    leading=32, textColor=DARK_GREEN, alignment=TA_CENTER, spaceAfter=6 * mm,
))
styles.add(ParagraphStyle(
    name="CoverSubtitle", parent=styles["Normal"], fontSize=13, leading=18,
    textColor=MUTED, alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=18,
    leading=22, textColor=DARK_GREEN, spaceBefore=3 * mm, spaceAfter=4 * mm,
))
styles.add(ParagraphStyle(
    name="Subsection", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12,
    leading=15, textColor=GREEN, spaceBefore=3 * mm, spaceAfter=2 * mm,
))
styles.add(ParagraphStyle(
    name="BodyText2", parent=styles["BodyText"], fontSize=9.5, leading=14,
    textColor=INK, spaceAfter=2.5 * mm,
))
styles.add(ParagraphStyle(
    name="Small", parent=styles["BodyText"], fontSize=8, leading=11, textColor=MUTED,
))
styles.add(ParagraphStyle(
    name="SourceCode", fontName="Courier", fontSize=5.2, leading=6.4,
    textColor=colors.HexColor("#23332C"), leftIndent=2 * mm, rightIndent=2 * mm,
))


def p(text, style="BodyText2"):
    return Paragraph(text, styles[style])


def feature_table():
    rows = [
        ["Requirement", "Implementation", "Status"],
        ["Login / Logout", "Local demo account with visible validation", "Complete"],
        ["Menu screen", "Dashboard, Inventory, Audit Trail navigation", "Complete"],
        ["Inventory management", "Add, update, delete, select, and display", "Complete"],
        ["Data visualization", "Totals, low-stock count, and stock bar chart", "Complete"],
        ["Audit trail", "Login, logout, add, update, and delete records", "Complete"],
        ["Windows / Android", "Single .NET MAUI project built for both targets", "Complete"],
    ]
    table = Table(rows, colWidths=[42 * mm, 100 * mm, 26 * mm], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_GREEN),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (-1, 1), (-1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (-1, 1), (-1, -1), GREEN),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("LEADING", (0, 0), (-1, -1), 11),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D3E0D9")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def add_code_file(story, relative_path, title=None):
    path = ROOT / relative_path
    code = path.read_text(encoding="utf-8")
    story.append(PageBreak())
    story.append(p(title or relative_path, "Section"))
    story.append(p(f"Source file: {escape(relative_path)}", "Small"))
    story.append(Spacer(1, 3 * mm))
    story.append(XPreformatted(escape(code), styles["SourceCode"]),)


story = []

story.append(Spacer(1, 25 * mm))
story.append(p("AKLAN DRUGSTORE", "CoverSubtitle"))
story.append(p("Inventory Management System", "CoverTitle"))
story.append(Spacer(1, 6 * mm))
story.append(p("Intermediate Mobile Programming<br/>Task Performance 1", "CoverSubtitle"))
story.append(Spacer(1, 25 * mm))
cover_data = [
    ["Developer", "Arjunren Valdez"],
    ["Technology", ".NET MAUI and C#"],
    ["Platforms", "Windows and Android"],
    ["Project type", "Simple local student application"],
    ["Date", "October 4, 2026"],
]
cover_table = Table(cover_data, colWidths=[42 * mm, 82 * mm], hAlign="CENTER")
cover_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), PALE_GREEN),
    ("TEXTCOLOR", (0, 0), (0, -1), DARK_GREEN),
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("TEXTCOLOR", (1, 0), (1, -1), INK),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C9D8D0")),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(cover_table)
story.append(Spacer(1, 25 * mm))
story.append(p("Developed by Arjunren Valdez", "CoverSubtitle"))

story.append(PageBreak())
story.append(p("1. Project Overview", "Section"))
story.append(p(
    "This application is a simple inventory management system for a local drugstore in Aklan, "
    "Panay Island. It reduces manual inventory checking by giving employees one place to view "
    "product quantities, update records, see low-stock information, and review transactions."
))
story.append(p(
    "The implementation uses one .NET MAUI codebase for Windows and Android. Product and audit "
    "records are stored as JSON files in the device application-data folder, so the classroom "
    "demo does not need a database server or an internet connection."
))
story.append(p("Feature checklist", "Subsection"))
story.append(feature_table())
story.append(Spacer(1, 7 * mm))
story.append(p("Demo account", "Subsection"))
story.append(p("Username: <b>admin</b><br/>Password: <b>admin123</b>"))
story.append(p(
    "Security note: the fixed account is only for a student demonstration. A real deployment "
    "should use password hashing, role-based access, secure key storage, and an online backup."
))

story.append(PageBreak())
story.append(p("2. Interface Mockups", "Section"))
story.append(p(
    "The interface uses a clean green drugstore theme. These mockups match the layout implemented "
    "in MainPage.xaml and show the intended Windows presentation."
))
story.append(p("Login screen", "Subsection"))
story.append(ScreenMockup("login"))

story.append(PageBreak())
story.append(p("Dashboard and data visualization", "Subsection"))
story.append(ScreenMockup("dashboard"))
story.append(Spacer(1, 5 * mm))
story.append(p(
    "The dashboard summarizes the number of products, total quantity, and low-stock items. "
    "A simple bar chart compares the current quantity of each product."
))

story.append(PageBreak())
story.append(p("Inventory management", "Subsection"))
story.append(ScreenMockup("inventory"))
story.append(Spacer(1, 5 * mm))
story.append(p(
    "Employees can enter product details and use Add, Update, Delete, or Clear. Selecting a row "
    "loads its values into the form for editing. Validation prevents blank names, blank categories, "
    "negative quantities, and negative prices."
))

story.append(PageBreak())
story.append(p("Audit trail", "Subsection"))
story.append(ScreenMockup("audit"))
story.append(Spacer(1, 5 * mm))
story.append(p(
    "The audit trail places the newest record first and records login, logout, add, update, and "
    "delete actions with their date, time, and details."
))

story.append(PageBreak())
story.append(p("3. How to Open and Run", "Section"))
run_rows = [
    ["Step", "Instruction"],
    ["1", "Open AklanDrugstoreInventory.slnx in Visual Studio 2026."],
    ["2", "Confirm that the .NET MAUI workload and .NET 10 SDK are installed."],
    ["3", "Choose Windows Machine or an Android emulator as the debug target."],
    ["4", "Press F5 and wait for the application to start."],
    ["5", "Log in using admin / admin123."],
    ["6", "Use the menu to open Dashboard, Inventory, or Audit Trail."],
]
run_table = Table(run_rows, colWidths=[18 * mm, 148 * mm], repeatRows=1)
run_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), DARK_GREEN),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D3E0D9")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(run_table)
story.append(Spacer(1, 6 * mm))
story.append(p("Build commands", "Subsection"))
commands = (
    "dotnet build AklanDrugstoreInventory.csproj -f net10.0-windows10.0.19041.0\n"
    "dotnet build AklanDrugstoreInventory.csproj -f net10.0-android"
)
story.append(XPreformatted(commands, styles["SourceCode"]))
story.append(Spacer(1, 6 * mm))
story.append(p("Important files", "Subsection"))
story.append(p(
    "MainPage.xaml contains the visible screens. MainPage.xaml.cs contains login, menu navigation, "
    "inventory CRUD, validation, dashboard totals, JSON persistence, and audit logic. The Models "
    "folder contains InventoryItem and AuditEntry. AppShell.xaml provides the application shell."
))

story.append(PageBreak())
story.append(p("4. Source Code", "Section"))
story.append(p(
    "The following pages contain the complete core source used by the project. Standard files "
    "generated by the .NET MAUI template remain in the repository, including platform manifests, "
    "font resources, icons, splash artwork, and default resource dictionaries."
))

for relative, title in [
    ("AklanDrugstoreInventory.csproj", "Project File - AklanDrugstoreInventory.csproj"),
    ("App.xaml", "Application Resources - App.xaml"),
    ("App.xaml.cs", "Application Startup - App.xaml.cs"),
    ("AppShell.xaml", "Application Shell - AppShell.xaml"),
    ("AppShell.xaml.cs", "Application Shell Code - AppShell.xaml.cs"),
    ("MauiProgram.cs", "MAUI Configuration - MauiProgram.cs"),
    ("Models/InventoryItem.cs", "Data Model - InventoryItem.cs"),
    ("Models/AuditEntry.cs", "Data Model - AuditEntry.cs"),
    ("MainPage.xaml", "User Interface - MainPage.xaml"),
    ("MainPage.xaml.cs", "Application Logic - MainPage.xaml.cs"),
]:
    add_code_file(story, relative, title)

story.append(PageBreak())
story.append(p("5. Credits and License", "Section"))
story.append(p("Designed and developed by <b>Arjunren Valdez</b>."))
story.append(p(
    "This project is released under the MIT License. The repository includes the full LICENSE file, "
    "README, source code, assets, and this documentation."
))

doc = SubmissionDocTemplate(str(OUTPUT))
doc.build(story)
print(OUTPUT)
