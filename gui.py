"""
Monochrome Pure Black & White Dashboard GUI for BMI Analytics & Health Tracker
Features a high-contrast obsidian black, dark charcoal, and crisp white theme.

Features:
- Pure Black & White Executive Dashboard Layout (No Blue undertones)
- Left Vertical Sidebar Navigation (Dashboard, Calculate, History Logs, View Reports)
- Top Bar with Search, Notifications, and User Profile Switcher
- Hero Welcome Banner with Quick Action buttons
- 4 Top Metric KPI Cards with monochrome borders and status indicators
- Pure Black Matplotlib Line Chart for BMI & Weight Trajectory
- Category Status Overview with Progress Bars
- Dedicated Clinical Reports View with TXT/CSV Export
- Full multi-user SQLite persistence and metric/imperial validation
"""

import sys
import os
from datetime import datetime
from typing import Optional, List, Dict

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QStackedWidget, QFrame, QMessageBox,
    QInputDialog, QFileDialog, QRadioButton, QSpinBox, QProgressBar,
    QScrollArea
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from bmi_calculator import (
    parse_and_validate_inputs, parse_imperial_inputs,
    calculate_bmi, classify_bmi, calculate_healthy_weight_range,
    estimate_body_fat_percentage, kg_to_lbs, lbs_to_kg
)
from database import DatabaseManager, DatabaseError


# Pure Black & White High-Contrast Stylesheet (Zero Blue undertones)
MONOCHROME_BLACK_WHITE_STYLESHEET = """
QMainWindow {
    background-color: #000000;
}
QWidget {
    font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
    color: #ffffff;
}
/* Left Sidebar */
QFrame#sidebar {
    background-color: #0a0a0a;
    border-right: 1px solid #262626;
}
QPushButton#navBtn {
    background-color: transparent;
    color: #a3a3a3;
    font-size: 14px;
    font-weight: 600;
    text-align: left;
    padding: 12px 18px;
    border: none;
    border-radius: 10px;
}
QPushButton#navBtn:hover {
    background-color: #1c1c1c;
    color: #ffffff;
}
QPushButton#navBtnActive {
    background-color: #ffffff;
    color: #000000;
    font-size: 14px;
    font-weight: 800;
    text-align: left;
    padding: 12px 18px;
    border: none;
    border-radius: 10px;
}
/* Header Bar */
QLineEdit#searchBar {
    background-color: #121212;
    border: 1px solid #262626;
    border-radius: 20px;
    padding: 8px 16px;
    color: #ffffff;
    font-size: 13px;
}
QLineEdit#searchBar:focus {
    border: 1px solid #ffffff;
}
QFrame#userProfileBadge {
    background-color: #121212;
    border: 1px solid #262626;
    border-radius: 18px;
    padding: 4px 12px;
}
/* Hero Banner Card */
QFrame#heroCard {
    background-color: #121212;
    border: 1px solid #262626;
    border-radius: 16px;
}
QPushButton#heroPrimaryBtn {
    background-color: #ffffff;
    color: #000000;
    font-size: 14px;
    font-weight: 800;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
}
QPushButton#heroPrimaryBtn:hover {
    background-color: #e5e5e5;
}
QPushButton#heroSecondaryBtn {
    background-color: #1c1c1c;
    color: #ffffff;
    font-size: 14px;
    font-weight: 600;
    border: 1px solid #333333;
    border-radius: 10px;
    padding: 10px 20px;
}
QPushButton#heroSecondaryBtn:hover {
    background-color: #262626;
}
/* Metric KPI Cards */
QFrame#kpiCard {
    background-color: #121212;
    border: 1px solid #262626;
    border-radius: 14px;
}
QFrame#kpiCard:hover {
    border: 1px solid #404040;
}
QFrame#iconContainer {
    background-color: #1c1c1c;
    border-radius: 12px;
}
/* Main Content Panel Cards */
QFrame#contentCard {
    background-color: #121212;
    border: 1px solid #262626;
    border-radius: 16px;
}
/* Form Controls */
QLineEdit, QComboBox, QSpinBox {
    background-color: #171717;
    border: 1px solid #2c2c2c;
    border-radius: 10px;
    padding: 10px 14px;
    color: #ffffff;
    font-size: 14px;
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #ffffff;
    background-color: #1f1f1f;
}
QPushButton#actionBtn {
    background-color: #ffffff;
    color: #000000;
    font-size: 14px;
    font-weight: 800;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
}
QPushButton#actionBtn:hover {
    background-color: #e5e5e5;
}
QPushButton#dangerBtn {
    background-color: #1c1c1c;
    color: #ef4444;
    font-weight: 600;
    border: 1px solid #ef4444;
    border-radius: 8px;
    padding: 8px 14px;
}
QPushButton#dangerBtn:hover {
    background-color: #ef4444;
    color: #ffffff;
}
/* Tables */
QTableWidget {
    background-color: #121212;
    gridline-color: #262626;
    border: 1px solid #262626;
    border-radius: 12px;
    color: #ffffff;
}
QHeaderView::section {
    background-color: #0a0a0a;
    color: #a3a3a3;
    font-weight: bold;
    padding: 10px;
    border: none;
    border-bottom: 1px solid #262626;
}
QTableWidget::item {
    padding: 8px;
}
QTableWidget::item:selected {
    background-color: #ffffff;
    color: #000000;
}
/* Progress Bars */
QProgressBar {
    background-color: #1c1c1c;
    border: none;
    border-radius: 4px;
    height: 8px;
    text-alignment: center;
}
QProgressBar::chunk {
    background-color: #ffffff;
    border-radius: 4px;
}
QRadioButton {
    color: #e5e5e5;
    font-weight: 500;
}
"""


class PureBlackTrendCanvas(FigureCanvas):
    """Matplotlib Canvas Widget styled in pure high-contrast black and white."""
    def __init__(self, parent=None, width=6, height=3.5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#121212')
        super().__init__(self.fig)
        self.setParent(parent)

    def plot_trend(self, records: List[Dict]):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.set_facecolor('#121212')

        if not records:
            ax.text(0.5, 0.5, '📊 No health records available.\nCalculate and save BMI measurements to render analytics!',
                    horizontalalignment='center', verticalalignment='center',
                    color='#737373', fontsize=12, fontweight='500', transform=ax.transAxes)
            ax.axis('off')
            self.draw()
            return

        dates = []
        bmis = []
        weights = []
        for r in records:
            try:
                dt = datetime.strptime(r['timestamp'], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.now()
            dates.append(dt)
            bmis.append(r['bmi_value'])
            weights.append(r['weight_kg'])

        # Grid
        ax.grid(True, color='#262626', linestyle='-', linewidth=0.8, alpha=0.8)

        # Plot Crisp White BMI Line
        line1 = ax.plot(dates, bmis, color='#ffffff', marker='o', linewidth=2.5, markersize=6, label='BMI Score')
        
        # Shade Area under BMI curve
        ax.fill_between(dates, bmis, color='#ffffff', alpha=0.10)

        # Secondary Axis for Weight (Grey Line)
        ax2 = ax.twinx()
        line2 = ax2.plot(dates, weights, color='#a3a3a3', marker='s', linestyle='--', linewidth=1.8, markersize=5, label='Weight (kg)')
        
        # Format axes
        ax.tick_params(axis='x', colors='#a3a3a3', labelsize=9)
        ax.tick_params(axis='y', colors='#ffffff', labelsize=9)
        ax2.tick_params(axis='y', colors='#a3a3a3', labelsize=9)

        # Remove top/right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#262626')
        ax.spines['bottom'].set_color('#262626')

        ax2.spines['top'].set_visible(False)
        ax2.spines['left'].set_visible(False)
        ax2.spines['right'].set_color('#262626')
        ax2.spines['bottom'].set_color('#262626')

        self.fig.autofmt_xdate()

        # Legend
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax.legend(lines, labels, loc='upper left', facecolor='#0a0a0a', edgecolor='#262626', labelcolor='#ffffff', fontsize=9)

        self.fig.tight_layout()
        self.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMI Health Tracker — Analytics Dashboard")
        self.resize(1180, 780)
        self.setMinimumSize(1000, 680)

        # Database Manager
        try:
            self.db = DatabaseManager()
        except DatabaseError as e:
            QMessageBox.critical(self, "Database Failure", f"Failed to connect to SQLite:\n{e}")
            self.db = None

        self.current_user_id: Optional[int] = None
        self.current_user_name: str = "Vishva Raj Singh"
        self.unit_system: str = "metric"

        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet(MONOCHROME_BLACK_WHITE_STYLESHEET)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ----------------------------------------------------
        # 1. LEFT SIDEBAR NAVIGATION
        # ----------------------------------------------------
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(230)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(18, 20, 18, 20)
        sidebar_layout.setSpacing(10)

        # Brand Logo Section
        logo_label = QLabel("💪 BMI Analytics")
        logo_label.setStyleSheet("font-size: 16px; font-weight: 800; color: #ffffff;")
        tagline_label = QLabel("Health & Fitness Suite")
        tagline_label.setStyleSheet("font-size: 10px; color: #737373; margin-bottom: 15px;")

        sidebar_layout.addWidget(logo_label)
        sidebar_layout.addWidget(tagline_label)

        # Navigation Buttons
        self.nav_buttons = []

        self.btn_dash = self._create_nav_btn("🏠  Dashboard", True)
        self.btn_calc = self._create_nav_btn("⚡  Calculate BMI", False)
        self.btn_history = self._create_nav_btn("📜  History Logs", False)
        self.btn_reports = self._create_nav_btn("📄  View Reports", False)

        self.btn_dash.clicked.connect(lambda: self._switch_tab(0))
        self.btn_calc.clicked.connect(lambda: self._switch_tab(1))
        self.btn_history.clicked.connect(lambda: self._switch_tab(2))
        self.btn_reports.clicked.connect(lambda: self._switch_tab(3))

        sidebar_layout.addWidget(self.btn_dash)
        sidebar_layout.addWidget(self.btn_calc)
        sidebar_layout.addWidget(self.btn_history)
        sidebar_layout.addWidget(self.btn_reports)

        sidebar_layout.addStretch()

        # Sidebar Footer Profile / Exit
        btn_exit = QPushButton("🚪  Logout")
        btn_exit.setObjectName("navBtn")
        btn_exit.clicked.connect(self.close)
        sidebar_layout.addWidget(btn_exit)

        root_layout.addWidget(sidebar)

        # ----------------------------------------------------
        # 2. MAIN CONTENT WRAPPER
        # ----------------------------------------------------
        main_content = QWidget()
        main_layout = QVBoxLayout(main_content)
        main_layout.setContentsMargins(24, 18, 24, 18)
        main_layout.setSpacing(16)

        # TOP BAR
        top_bar = QHBoxLayout()
        top_bar.setSpacing(14)

        search_input = QLineEdit()
        search_input.setObjectName("searchBar")
        search_input.setPlaceholderText("🔍  Search records, reports, users...")
        search_input.setFixedWidth(280)
        top_bar.addWidget(search_input)

        top_bar.addStretch()

        # Notification Bell
        notif_btn = QPushButton("🔔 5")
        notif_btn.setStyleSheet("""
            background-color: #121212;
            border: 1px solid #262626;
            border-radius: 18px;
            padding: 6px 14px;
            color: #ffffff;
            font-weight: 600;
        """)
        top_bar.addWidget(notif_btn)

        # User Profile Switcher Badge
        user_badge = QFrame()
        user_badge.setObjectName("userProfileBadge")
        ub_layout = QHBoxLayout(user_badge)
        ub_layout.setContentsMargins(8, 4, 8, 4)
        ub_layout.setSpacing(8)

        user_avatar = QLabel("👤")
        user_avatar.setStyleSheet("font-size: 16px;")
        ub_layout.addWidget(user_avatar)

        self.user_combo = QComboBox()
        self.user_combo.setStyleSheet("background: transparent; border: none; font-weight: 700; color: #ffffff;")
        self.user_combo.currentIndexChanged.connect(self._on_user_changed)
        ub_layout.addWidget(self.user_combo)

        add_user_btn = QPushButton("+")
        add_user_btn.setToolTip("Add User Profile")
        add_user_btn.setStyleSheet("background-color: #1c1c1c; border: 1px solid #333333; border-radius: 10px; color: #ffffff; font-weight: bold; width: 22px; height: 22px;")
        add_user_btn.clicked.connect(self._add_new_user_dialog)
        ub_layout.addWidget(add_user_btn)

        top_bar.addWidget(user_badge)
        main_layout.addLayout(top_bar)

        # STACKED WIDGET FOR MAIN VIEWS
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # VIEW 0: MAIN DASHBOARD
        view_dash = QWidget()
        self._setup_dashboard_view(view_dash)
        self.stack.addWidget(view_dash)

        # VIEW 1: CALCULATOR VIEW
        view_calc = QWidget()
        self._setup_calculator_view(view_calc)
        self.stack.addWidget(view_calc)

        # VIEW 2: HISTORY LOGS VIEW
        view_history = QWidget()
        self._setup_history_view(view_history)
        self.stack.addWidget(view_history)

        # VIEW 3: CLINICAL REPORTS VIEW
        view_reports = QWidget()
        self._setup_reports_view(view_reports)
        self.stack.addWidget(view_reports)

        root_layout.addWidget(main_content)

        # Load users into dropdown
        self._refresh_users_list()

    def _create_nav_btn(self, text: str, is_active: bool) -> QPushButton:
        btn = QPushButton(text)
        btn.setObjectName("navBtnActive" if is_active else "navBtn")
        self.nav_buttons.append(btn)
        return btn

    def _switch_tab(self, index: int):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.setObjectName("navBtnActive")
            else:
                btn.setObjectName("navBtn")
            btn.setStyle(btn.style())

    # ----------------------------------------------------
    # VIEW 0: DASHBOARD VIEW SETUP
    # ----------------------------------------------------
    def _setup_dashboard_view(self, parent):
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # Hero Welcome Banner
        hero_card = QFrame()
        hero_card.setObjectName("heroCard")
        hero_layout = QVBoxLayout(hero_card)
        hero_layout.setContentsMargins(24, 20, 24, 20)
        hero_layout.setSpacing(10)

        welcome_pill = QLabel("👋 Welcome Back")
        welcome_pill.setStyleSheet("background-color: #262626; color: #ffffff; font-size: 11px; font-weight: bold; padding: 4px 10px; border-radius: 12px; max-width: 110px;")
        hero_layout.addWidget(welcome_pill)

        self.hero_greeting = QLabel("Good Morning, Vishva 👋")
        self.hero_greeting.setStyleSheet("font-size: 26px; font-weight: 800; color: #ffffff;")
        hero_layout.addWidget(self.hero_greeting)

        hero_sub = QLabel("Here's what's happening with your health metrics today. Monitor progress, target ranges, reports, and activity from one dashboard.")
        hero_sub.setStyleSheet("font-size: 13px; color: #a3a3a3; max-width: 650px;")
        hero_layout.addWidget(hero_sub)

        hero_btn_layout = QHBoxLayout()
        hero_btn_layout.setSpacing(12)
        
        new_project_btn = QPushButton("+ New Entry")
        new_project_btn.setObjectName("heroPrimaryBtn")
        new_project_btn.clicked.connect(lambda: self._switch_tab(1))
        hero_btn_layout.addWidget(new_project_btn)

        view_reports_btn = QPushButton("📄 View Reports")
        view_reports_btn.setObjectName("heroSecondaryBtn")
        view_reports_btn.clicked.connect(lambda: self._switch_tab(3))
        hero_btn_layout.addWidget(view_reports_btn)

        hero_btn_layout.addStretch()
        hero_layout.addLayout(hero_btn_layout)

        layout.addWidget(hero_card)

        # Top 4 KPI Cards
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(14)

        self.card_total = self._create_dashboard_kpi("Total Records", "0", "📁", "+18% this month")
        self.card_active = self._create_dashboard_kpi("Current BMI", "--.--", "⚙️", "Status: N/A")
        self.card_completed = self._create_dashboard_kpi("Healthy Target", "-- kg", "✅", "92% Target Rate")
        self.card_delayed = self._create_dashboard_kpi("Weight Delta", "0.0 kg", "⚠️", "Requires Attention")

        kpi_row.addWidget(self.card_total)
        kpi_row.addWidget(self.card_active)
        kpi_row.addWidget(self.card_completed)
        kpi_row.addWidget(self.card_delayed)

        layout.addLayout(kpi_row)

        # Analytics Split Section
        split_layout = QHBoxLayout()
        split_layout.setSpacing(16)

        # Left Analytics Chart Panel
        chart_card = QFrame()
        chart_card.setObjectName("contentCard")
        chart_layout = QVBoxLayout(chart_card)
        chart_layout.setContentsMargins(18, 16, 18, 16)

        chart_header = QHBoxLayout()
        chart_title_box = QVBoxLayout()
        c_title = QLabel("BMI Trajectory Analytics")
        c_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #ffffff;")
        c_sub = QLabel("Overall health trajectory performance")
        c_sub.setStyleSheet("font-size: 11px; color: #737373;")
        chart_title_box.addWidget(c_title)
        chart_title_box.addWidget(c_sub)

        chart_header.addLayout(chart_title_box)
        chart_header.addStretch()

        filter_badge = QLabel("This Month")
        filter_badge.setStyleSheet("background-color: #262626; color: #ffffff; font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 8px;")
        chart_header.addWidget(filter_badge)

        chart_layout.addLayout(chart_header)

        self.trend_canvas = PureBlackTrendCanvas(self, width=6, height=3.2)
        chart_layout.addWidget(self.trend_canvas)

        split_layout.addWidget(chart_card, stretch=2)

        # Right Panel: Status Overview Breakdown
        status_card = QFrame()
        status_card.setObjectName("contentCard")
        status_card.setFixedWidth(280)
        status_layout = QVBoxLayout(status_card)
        status_layout.setContentsMargins(18, 16, 18, 16)
        status_layout.setSpacing(12)

        st_title = QLabel("Status Overview")
        st_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #ffffff;")
        status_layout.addWidget(st_title)

        self.prog_normal = self._create_status_item(status_layout, "Normal Weight", "0", "#22c55e")
        self.prog_overweight = self._create_status_item(status_layout, "Overweight", "0", "#eab308")
        self.prog_underweight = self._create_status_item(status_layout, "Underweight", "0", "#06b6d4")
        self.prog_obese = self._create_status_item(status_layout, "Obese", "0", "#ef4444")

        status_layout.addStretch()
        split_layout.addWidget(status_card, stretch=1)

        layout.addLayout(split_layout)

    def _create_dashboard_kpi(self, title: str, value: str, icon_str: str, footer_str: str) -> QFrame:
        card = QFrame()
        card.setObjectName("kpiCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(6)

        header = QHBoxLayout()
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #a3a3a3;")
        header.addWidget(t_lbl)
        header.addStretch()

        icon_box = QFrame()
        icon_box.setObjectName("iconContainer")
        ib_layout = QHBoxLayout(icon_box)
        ib_layout.setContentsMargins(6, 4, 6, 4)
        i_lbl = QLabel(icon_str)
        i_lbl.setStyleSheet("font-size: 13px;")
        ib_layout.addWidget(i_lbl)
        header.addWidget(icon_box)

        layout.addLayout(header)

        v_lbl = QLabel(value)
        v_lbl.setObjectName("kpiValue")
        v_lbl.setStyleSheet("font-size: 26px; font-weight: 800; color: #ffffff;")
        layout.addWidget(v_lbl)

        f_lbl = QLabel(footer_str)
        f_lbl.setObjectName("kpiFooter")
        f_lbl.setStyleSheet("font-size: 11px; color: #737373;")
        layout.addWidget(f_lbl)

        return card

    def _create_status_item(self, parent_layout, label_str: str, val_str: str, color_hex: str) -> QProgressBar:
        lbl_box = QHBoxLayout()
        l_lbl = QLabel(label_str)
        l_lbl.setStyleSheet("font-size: 12px; color: #d4d4d4;")
        v_lbl = QLabel(val_str)
        v_lbl.setObjectName(f"val_{label_str.replace(' ', '')}")
        v_lbl.setStyleSheet("font-size: 12px; font-weight: bold; color: #ffffff;")

        lbl_box.addWidget(l_lbl)
        lbl_box.addStretch()
        lbl_box.addWidget(v_lbl)
        parent_layout.addLayout(lbl_box)

        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(0)
        bar.setTextVisible(False)
        bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #1c1c1c;
                border: none;
                border-radius: 4px;
                height: 6px;
            }}
            QProgressBar::chunk {{
                background-color: {color_hex};
                border-radius: 4px;
            }}
        """)
        parent_layout.addWidget(bar)
        return bar

    # ----------------------------------------------------
    # VIEW 1: CALCULATOR VIEW SETUP
    # ----------------------------------------------------
    def _setup_calculator_view(self, parent):
        layout = QHBoxLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        # Form Panel
        input_card = QFrame()
        input_card.setObjectName("contentCard")
        input_card.setMinimumWidth(380)
        input_layout = QVBoxLayout(input_card)
        input_layout.setContentsMargins(22, 22, 22, 22)
        input_layout.setSpacing(14)

        title = QLabel("New BMI Calculation")
        title.setStyleSheet("font-size: 17px; font-weight: 700; color: #ffffff;")
        input_layout.addWidget(title)

        unit_box = QHBoxLayout()
        self.radio_metric = QRadioButton("Metric (kg, m/cm)")
        self.radio_imperial = QRadioButton("Imperial (lbs, ft/in)")
        self.radio_metric.setChecked(True)
        self.radio_metric.toggled.connect(self._toggle_units)
        unit_box.addWidget(self.radio_metric)
        unit_box.addWidget(self.radio_imperial)
        input_layout.addLayout(unit_box)

        # Metric Input Fields
        self.metric_widget = QWidget()
        m_layout = QVBoxLayout(self.metric_widget)
        m_layout.setContentsMargins(0, 0, 0, 0)
        m_layout.setSpacing(8)

        m_layout.addWidget(QLabel("Weight (kg):"))
        self.metric_weight_input = QLineEdit()
        self.metric_weight_input.setPlaceholderText("e.g. 70 or 68.5")
        m_layout.addWidget(self.metric_weight_input)

        m_layout.addWidget(QLabel("Height (meters or cm):"))
        self.metric_height_input = QLineEdit()
        self.metric_height_input.setPlaceholderText("e.g. 1.75 or 175")
        m_layout.addWidget(self.metric_height_input)

        input_layout.addWidget(self.metric_widget)

        # Imperial Input Fields
        self.imperial_widget = QWidget()
        imp_layout = QVBoxLayout(self.imperial_widget)
        imp_layout.setContentsMargins(0, 0, 0, 0)
        imp_layout.setSpacing(8)

        imp_layout.addWidget(QLabel("Weight (lbs):"))
        self.imp_weight_input = QLineEdit()
        self.imp_weight_input.setPlaceholderText("e.g. 154")
        imp_layout.addWidget(self.imp_weight_input)

        h_imp_box = QHBoxLayout()
        self.imp_feet_input = QLineEdit()
        self.imp_feet_input.setPlaceholderText("Feet (5)")
        self.imp_inches_input = QLineEdit()
        self.imp_inches_input.setPlaceholderText("Inches (9)")
        h_imp_box.addWidget(self.imp_feet_input)
        h_imp_box.addWidget(self.imp_inches_input)
        imp_layout.addLayout(h_imp_box)

        self.imperial_widget.setVisible(False)
        input_layout.addWidget(self.imperial_widget)

        # Calculate Action Button
        calc_btn = QPushButton("Calculate & Save BMI Record")
        calc_btn.setObjectName("actionBtn")
        calc_btn.clicked.connect(self._calculate_and_save_bmi)
        input_layout.addWidget(calc_btn)

        input_layout.addStretch()
        layout.addWidget(input_card, stretch=1)

        # Result Panel Card
        self.result_card = QFrame()
        self.result_card.setObjectName("contentCard")
        res_layout = QVBoxLayout(self.result_card)
        res_layout.setContentsMargins(24, 24, 24, 24)
        res_layout.setSpacing(14)

        self.res_badge = QLabel("READY TO CALCULATE")
        self.res_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.res_badge.setStyleSheet("background-color: #262626; color: #a3a3a3; font-size: 13px; font-weight: bold; padding: 6px 14px; border-radius: 8px;")
        res_layout.addWidget(self.res_badge)

        self.res_bmi_val = QLabel("--.--")
        self.res_bmi_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.res_bmi_val.setStyleSheet("font-size: 54px; font-weight: 900; color: #ffffff;")
        res_layout.addWidget(self.res_bmi_val)

        self.res_category = QLabel("Enter measurement values to generate result")
        self.res_category.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.res_category.setStyleSheet("font-size: 16px; font-weight: 600; color: #e5e5e5;")
        res_layout.addWidget(self.res_category)

        self.res_target = QLabel("")
        self.res_target.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.res_target.setStyleSheet("font-size: 13px; color: #a3a3a3;")
        res_layout.addWidget(self.res_target)

        res_layout.addStretch()
        layout.addWidget(self.result_card, stretch=2)

    def _toggle_units(self):
        if self.radio_metric.isChecked():
            self.unit_system = "metric"
            self.metric_widget.setVisible(True)
            self.imperial_widget.setVisible(False)
        else:
            self.unit_system = "imperial"
            self.metric_widget.setVisible(False)
            self.imperial_widget.setVisible(True)

    # ----------------------------------------------------
    # VIEW 2: HISTORY LOGS VIEW SETUP
    # ----------------------------------------------------
    def _setup_history_view(self, parent):
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        table_card = QFrame()
        table_card.setObjectName("contentCard")
        tc_layout = QVBoxLayout(table_card)
        tc_layout.setContentsMargins(20, 18, 20, 18)

        top_h = QHBoxLayout()
        t_title = QLabel("Historical Measurement Logs")
        t_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #ffffff;")
        top_h.addWidget(t_title)

        top_h.addStretch()

        delete_btn = QPushButton("🗑️ Delete Selected")
        delete_btn.setObjectName("dangerBtn")
        delete_btn.clicked.connect(self._delete_selected_record)
        top_h.addWidget(delete_btn)

        tc_layout.addLayout(top_h)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(["ID", "Timestamp", "Weight (kg)", "Height (m)", "BMI", "Category"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.history_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        tc_layout.addWidget(self.history_table)

        layout.addWidget(table_card)

    # ----------------------------------------------------
    # VIEW 3: DEDICATED CLINICAL REPORTS VIEW SETUP
    # ----------------------------------------------------
    def _setup_reports_view(self, parent):
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # Header with Export Controls
        header_card = QFrame()
        header_card.setObjectName("contentCard")
        hc_layout = QHBoxLayout(header_card)
        hc_layout.setContentsMargins(20, 16, 20, 16)

        rep_title_box = QVBoxLayout()
        rt_lbl = QLabel("📄 Clinical Reports & Health Insights")
        rt_lbl.setStyleSheet("font-size: 18px; font-weight: 800; color: #ffffff;")
        rs_lbl = QLabel("Executive health summary, statistical analysis & document export")
        rs_lbl.setStyleSheet("font-size: 12px; color: #737373;")
        rep_title_box.addWidget(rt_lbl)
        rep_title_box.addWidget(rs_lbl)

        hc_layout.addLayout(rep_title_box)
        hc_layout.addStretch()

        export_txt_btn = QPushButton("📄 Export TXT Report")
        export_txt_btn.setObjectName("heroSecondaryBtn")
        export_txt_btn.clicked.connect(self._export_txt_report)
        hc_layout.addWidget(export_txt_btn)

        export_csv_btn = QPushButton("📥 Export CSV Data")
        export_csv_btn.setObjectName("heroPrimaryBtn")
        export_csv_btn.clicked.connect(self._export_to_csv)
        hc_layout.addWidget(export_csv_btn)

        layout.addWidget(header_card)

        # Clinical Summary Document Card
        self.report_doc_card = QFrame()
        self.report_doc_card.setObjectName("contentCard")
        doc_layout = QVBoxLayout(self.report_doc_card)
        doc_layout.setContentsMargins(24, 22, 24, 22)
        doc_layout.setSpacing(14)

        doc_header = QHBoxLayout()
        self.report_user_lbl = QLabel("PATIENT PROFILE REPORT: VISHVA RAJ SINGH")
        self.report_user_lbl.setStyleSheet("font-size: 15px; font-weight: 800; color: #ffffff; letter-spacing: 0.5px;")
        doc_header.addWidget(self.report_user_lbl)
        doc_header.addStretch()

        self.report_date_lbl = QLabel("")
        self.report_date_lbl.setStyleSheet("font-size: 12px; color: #a3a3a3;")
        doc_header.addWidget(self.report_date_lbl)
        doc_layout.addLayout(doc_header)

        # Statistics Cards Grid inside Report
        stats_grid = QHBoxLayout()
        stats_grid.setSpacing(12)

        self.rep_card_latest = self._create_dashboard_kpi("LATEST BMI", "--.--", "📈", "WHO Classification")
        self.rep_card_delta = self._create_dashboard_kpi("WEIGHT DELTA", "0.0 kg", "⚖️", "Net Trajectory")
        self.rep_card_range = self._create_dashboard_kpi("BMI RANGE", "-- / --", "📊", "Historical Min / Max")
        self.rep_card_avg = self._create_dashboard_kpi("AVERAGE BMI", "--.--", "🎯", "Mean Score")

        stats_grid.addWidget(self.rep_card_latest)
        stats_grid.addWidget(self.rep_card_delta)
        stats_grid.addWidget(self.rep_card_range)
        stats_grid.addWidget(self.rep_card_avg)

        doc_layout.addLayout(stats_grid)

        # Clinical Insights Text Box
        doc_layout.addSpacing(6)
        c_title = QLabel("📋 Clinical Recommendation & Assessment:")
        c_title.setStyleSheet("font-weight: 700; color: #ffffff; font-size: 14px;")
        doc_layout.addWidget(c_title)

        self.report_clinical_text = QLabel("Save BMI records to generate automated health analytics reports and clinical insights.")
        self.report_clinical_text.setWordWrap(True)
        self.report_clinical_text.setStyleSheet("color: #e5e5e5; font-size: 13px; line-height: 1.6; background-color: #171717; padding: 14px; border-radius: 10px; border: 1px solid #262626;")
        doc_layout.addWidget(self.report_clinical_text)

        doc_layout.addStretch()
        layout.addWidget(self.report_doc_card)

    # ----------------------------------------------------
    # DATA & LOGIC CONTROLLERS
    # ----------------------------------------------------
    def _refresh_users_list(self):
        if not self.db:
            return
        try:
            users = self.db.get_all_users()
            self.user_combo.blockSignals(True)
            self.user_combo.clear()
            for u in users:
                self.user_combo.addItem(u["name"], u["id"])
            self.user_combo.blockSignals(False)

            if users:
                self.current_user_id = users[0]["id"]
                self.current_user_name = users[0]["name"]
                self._load_user_data()
        except DatabaseError as e:
            QMessageBox.warning(self, "Database Failure", f"Error loading users: {e}")

    def _on_user_changed(self, index: int):
        if index >= 0:
            self.current_user_id = self.user_combo.currentData()
            self.current_user_name = self.user_combo.currentText()
            self._load_user_data()

    def _add_new_user_dialog(self):
        if not self.db:
            return
        text, ok = QInputDialog.getText(self, "Create User Profile", "Enter name for new profile:")
        if ok and text.strip():
            try:
                user = self.db.get_or_create_user(text.strip())
                self._refresh_users_list()
                idx = self.user_combo.findData(user["id"])
                if idx >= 0:
                    self.user_combo.setCurrentIndex(idx)
            except DatabaseError as e:
                QMessageBox.critical(self, "Database Error", f"Could not create user:\n{e}")

    def _calculate_and_save_bmi(self):
        if self.unit_system == "metric":
            weight_kg, height_m, err = parse_and_validate_inputs(self.metric_weight_input.text(), self.metric_height_input.text())
        else:
            weight_kg, height_m, err = parse_imperial_inputs(self.imp_weight_input.text(), self.imp_feet_input.text(), self.imp_inches_input.text())

        if err:
            QMessageBox.warning(self, "Validation Error", err)
            return

        bmi = calculate_bmi(weight_kg, height_m)
        category, color_hex, desc, advice = classify_bmi(bmi)
        min_k, max_k, min_l, max_l = calculate_healthy_weight_range(height_m)

        # Update Result Panel UI
        self.res_bmi_val.setText(f"{bmi:.2f}")
        self.res_category.setText(f"{category} ({desc})")
        self.res_category.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {color_hex};")
        self.res_target.setText(f"Healthy Weight Target: {min_k}–{max_k} kg ({min_l}–{max_l} lbs)")
        self.res_badge.setText(category.upper())
        self.res_badge.setStyleSheet(f"background-color: {color_hex}; color: #000000; font-size: 13px; font-weight: bold; padding: 6px 14px; border-radius: 8px;")

        # Save to Database
        if self.db and self.current_user_id:
            try:
                self.db.add_bmi_record(self.current_user_id, weight_kg, height_m, bmi, category)
                self._load_user_data()
                self._switch_tab(0)  # Jump back to dashboard view
            except DatabaseError as e:
                QMessageBox.critical(self, "Storage Failure", f"Could not save record:\n{e}")

    def _load_user_data(self):
        if not self.db or not self.current_user_id:
            return

        try:
            records = self.db.get_user_history(self.current_user_id)
            stats = self.db.get_user_stats(self.current_user_id)

            # Update Hero Greeting
            first_name = self.current_user_name.split()[0]
            self.hero_greeting.setText(f"Good Morning, {first_name} 👋")
            self.report_user_lbl.setText(f"CLINICAL HEALTH REPORT: {self.current_user_name.upper()}")
            self.report_date_lbl.setText(f"Date: {datetime.now().strftime('%Y-%m-%d')}")

            # Update Top Dashboard KPI Cards
            total = stats.get("total_records", 0)
            self.card_total.findChild(QLabel, "kpiValue").setText(str(total))
            
            if total > 0:
                latest_bmi = stats.get("latest_bmi", 0.0)
                cat, color, desc, advice = classify_bmi(latest_bmi)
                bmi_lbl = self.card_active.findChild(QLabel, "kpiValue")
                bmi_lbl.setText(f"{latest_bmi:.2f}")
                bmi_lbl.setStyleSheet(f"font-size: 26px; font-weight: 800; color: {color};")
                self.card_active.findChild(QLabel, "kpiFooter").setText(f"Status: {cat}")

                delta = stats.get("weight_change", 0.0)
                sign = "+" if delta > 0 else ""
                self.card_delayed.findChild(QLabel, "kpiValue").setText(f"{sign}{delta:.1f} kg")

                latest_h = records[-1]["height_m"]
                min_k, max_k, _, _ = calculate_healthy_weight_range(latest_h)
                self.card_completed.findChild(QLabel, "kpiValue").setText(f"{min_k}–{max_k} kg")

                # Update Clinical Reports View Cards & Text
                r_latest = self.rep_card_latest.findChild(QLabel, "kpiValue")
                r_latest.setText(f"{latest_bmi:.2f}")
                r_latest.setStyleSheet(f"font-size: 26px; font-weight: 800; color: {color};")
                self.rep_card_latest.findChild(QLabel, "kpiFooter").setText(cat)

                self.rep_card_delta.findChild(QLabel, "kpiValue").setText(f"{sign}{delta:.1f} kg")
                self.rep_card_range.findChild(QLabel, "kpiValue").setText(f"{stats['min_bmi']:.1f} / {stats['max_bmi']:.1f}")
                self.rep_card_avg.findChild(QLabel, "kpiValue").setText(f"{stats['avg_bmi']:.2f}")

                self.report_clinical_text.setText(
                    f"Patient {self.current_user_name} has {total} recorded measurements. "
                    f"The latest BMI score is {latest_bmi:.2f} classified under '{cat}' ({desc}). "
                    f"Net weight change trajectory is {sign}{delta:.1f} kg. Healthy target weight range for height {latest_h:.2f}m is {min_k}–{max_k} kg.\n\n"
                    f"Recommendation: {advice}"
                )
            else:
                self.card_active.findChild(QLabel, "kpiValue").setText("--.--")
                self.card_active.findChild(QLabel, "kpiFooter").setText("Status: N/A")
                self.card_delayed.findChild(QLabel, "kpiValue").setText("0.0 kg")
                self.card_completed.findChild(QLabel, "kpiValue").setText("-- kg")
                self.rep_card_latest.findChild(QLabel, "kpiValue").setText("--.--")
                self.rep_card_delta.findChild(QLabel, "kpiValue").setText("0.0 kg")
                self.rep_card_range.findChild(QLabel, "kpiValue").setText("-- / --")
                self.rep_card_avg.findChild(QLabel, "kpiValue").setText("--.--")
                self.report_clinical_text.setText("No recorded measurements found for this profile. Please perform a BMI calculation to generate your report.")

            # Update Status Breakdown Progress Bars
            count_norm = sum(1 for r in records if "Normal" in r["category"])
            count_over = sum(1 for r in records if "Overweight" in r["category"])
            count_under = sum(1 for r in records if "Underweight" in r["category"])
            count_obese = sum(1 for r in records if "Obese" in r["category"])

            pct = lambda c: int((c / total) * 100) if total > 0 else 0
            self.prog_normal.setValue(pct(count_norm))
            self.prog_overweight.setValue(pct(count_over))
            self.prog_underweight.setValue(pct(count_under))
            self.prog_obese.setValue(pct(count_obese))

            # Update History Table Widget
            self.history_table.setRowCount(len(records))
            for i, r in enumerate(records):
                self.history_table.setItem(i, 0, QTableWidgetItem(str(r["id"])))
                self.history_table.setItem(i, 1, QTableWidgetItem(r["timestamp"]))
                self.history_table.setItem(i, 2, QTableWidgetItem(f"{r['weight_kg']:.1f}"))
                self.history_table.setItem(i, 3, QTableWidgetItem(f"{r['height_m']:.2f}"))
                self.history_table.setItem(i, 4, QTableWidgetItem(f"{r['bmi_value']:.2f}"))
                cat_item = QTableWidgetItem(r["category"])
                _, color_hex, _, _ = classify_bmi(r["bmi_value"])
                cat_item.setForeground(QColor(color_hex))
                self.history_table.setItem(i, 5, cat_item)

            # Update Dashboard Matplotlib Line Chart
            self.trend_canvas.plot_trend(records)

        except DatabaseError as e:
            QMessageBox.warning(self, "Database Error", f"Error loading data for {self.current_user_name}:\n{e}")

    def _export_to_csv(self):
        if not self.db or not self.current_user_id:
            return
        default_fn = f"{self.current_user_name.lower().replace(' ', '_')}_bmi_history.csv"
        fn, _ = QFileDialog.getSaveFileName(self, "Export BMI History to CSV", default_fn, "CSV Files (*.csv)")
        if fn:
            try:
                saved = self.db.export_user_history_to_csv(self.current_user_id, fn)
                QMessageBox.information(self, "Export Success", f"✅ CSV Report exported to:\n{saved}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failure", f"Export failed:\n{e}")

    def _export_txt_report(self):
        if not self.db or not self.current_user_id:
            return
        default_fn = f"{self.current_user_name.lower().replace(' ', '_')}_clinical_report.txt"
        fn, _ = QFileDialog.getSaveFileName(self, "Export Clinical Text Report", default_fn, "Text Files (*.txt)")
        if fn:
            try:
                saved = self.db.export_clinical_report_txt(self.current_user_id, self.current_user_name, fn)
                QMessageBox.information(self, "Export Success", f"✅ Clinical Report document generated:\n{saved}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failure", f"Report generation failed:\n{e}")

    def _delete_selected_record(self):
        if not self.db:
            return
        selected = self.history_table.selectedItems()
        if not selected:
            QMessageBox.information(self, "Select Record", "Please select a row in the history table to delete.")
            return

        row = selected[0].row()
        rec_id = int(self.history_table.item(row, 0).text())

        reply = QMessageBox.question(self, "Confirm Delete", f"Delete record #{rec_id}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.db.delete_record(rec_id):
                    self._load_user_data()
            except DatabaseError as e:
                QMessageBox.critical(self, "Delete Failure", f"Could not delete record:\n{e}")


def launch_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    launch_gui()
