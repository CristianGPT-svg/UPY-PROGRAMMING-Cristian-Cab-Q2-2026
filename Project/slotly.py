"""
Sam Beauty Dashboard — Backend
Automated appointment management system for a beauty studio in Mérida, Yucatán.

This script simulates the core data pipeline:
  1. Load appointment and client records (from CSV or mock data)
  2. Validate and process each record
  3. Calculate daily/weekly/monthly revenue
  4. Detect upcoming birthdays and retouching reminders
  5. Generate a summary report

All key events, warnings, and errors are logged to /logs/app.log
"""

import logging
import os
import csv
import json
from datetime import datetime, timedelta
from pathlib import Path

# ─────────────────────────────────────────────────────────
# LOGGING SETUP
# ─────────────────────────────────────────────────────────
LOGS_DIR = Path(__file__).parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOG_FILE = LOGS_DIR / "app.log"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s — [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("sam_beauty")

# ─────────────────────────────────────────────────────────
# MOCK DATA — simulates what the Google Sheets webhook
# writes to the database after each Cal.com booking
# ─────────────────────────────────────────────────────────
MOCK_APPOINTMENTS = [
    {"fecha": "10/07/2026", "hora": "10:00 am", "nombre": "Mareli Koh",       "whatsapp": "529991001001", "servicio": "Pestañas — Aplicación Nueva",  "precio": "650",  "formaPago": "Efectivo",       "estatus": "Confirmada", "notas": "",              "primeraVez": "Sí"},
    {"fecha": "10/07/2026", "hora": "12:00 pm", "nombre": "Valeria Loeza",     "whatsapp": "529991002002", "servicio": "Pestañas — Retoque 15 días",   "precio": "475",  "formaPago": "Tarjeta",        "estatus": "Confirmada", "notas": "Alergia al latex","primeraVez": "No"},
    {"fecha": "10/07/2026", "hora": "02:00 pm", "nombre": "Regina Aranda",     "whatsapp": "529991003003", "servicio": "Brow Art — Diseño de cejas",   "precio": "250",  "formaPago": "Transferencia",  "estatus": "Pendiente",  "notas": "",              "primeraVez": "No"},
    {"fecha": "10/07/2026", "hora": "04:00 pm", "nombre": "Venus Noh",         "whatsapp": "529991004004", "servicio": "Lash Lifting",                "precio": "450",  "formaPago": "",               "estatus": "Confirmada", "notas": "",              "primeraVez": "Sí"},
    {"fecha": "11/07/2026", "hora": "10:00 am", "nombre": "Clarisa Calderón",  "whatsapp": "529991005005", "servicio": "Pestañas — Retoque 20 días",   "precio": "550",  "formaPago": "Efectivo",       "estatus": "Confirmada", "notas": "",              "primeraVez": "No"},
    {"fecha": "11/07/2026", "hora": "01:00 pm", "nombre": "Melany Vilchis",    "whatsapp": "529991006006", "servicio": "Lami Brows",                  "precio": "450",  "formaPago": "Tarjeta",        "estatus": "Confirmada", "notas": "",              "primeraVez": "No"},
    {"fecha": "11/07/2026", "hora": "03:00 pm", "nombre": "Yamil Farah",       "whatsapp": "529991007007", "servicio": "Shot de Vitamina — Reparación","precio": "500",  "formaPago": "Efectivo",       "estatus": "Cancelada",  "notas": "Canceló por viaje","primeraVez": "No"},
    {"fecha": "12/07/2026", "hora": "11:00 am", "nombre": "Keyra Pool",        "whatsapp": "529991008008", "servicio": "Full Brows",                  "precio": "",     "formaPago": "",               "estatus": "Pendiente",  "notas": "",              "primeraVez": "Sí"},
    {"fecha": "09/07/2026", "hora": "10:00 am", "nombre": "Mareli Koh",        "whatsapp": "529991001001", "servicio": "Pestañas — Retoque 15 días",   "precio": "475",  "formaPago": "Efectivo",       "estatus": "Completada", "notas": "",              "primeraVez": "No"},
    {"fecha": "08/07/2026", "hora": "09:00 am", "nombre": "Venus Noh",         "whatsapp": "529991004004", "servicio": "Brow Tint — Tinte de cejas",   "precio": "400",  "formaPago": "Tarjeta",        "estatus": "Completada", "notas": "",              "primeraVez": "No"},
]

MOCK_CLIENTS = [
    {"nombre": "Mareli Koh",      "whatsapp": "529991001001", "cumpleanos": "10/07", "ultimaCita": "10/07/2026", "ultimoServicio": "Pestañas — Aplicación Nueva", "historialMedico": "Ninguno",       "notas": "Prefiere volumen natural"},
    {"nombre": "Valeria Loeza",   "whatsapp": "529991002002", "cumpleanos": "22/09", "ultimaCita": "10/07/2026", "ultimoServicio": "Pestañas — Retoque 15 días",  "historialMedico": "Alergia al latex","notas": ""},
    {"nombre": "Regina Aranda",   "whatsapp": "529991003003", "cumpleanos": "15/08", "ultimaCita": "10/07/2026", "ultimoServicio": "Brow Art — Diseño de cejas",  "historialMedico": "Ninguno",       "notas": ""},
    {"nombre": "Venus Noh",       "whatsapp": "529991004004", "cumpleanos": "11/07", "ultimaCita": "10/07/2026", "ultimoServicio": "Lash Lifting",                "historialMedico": "Ninguno",       "notas": ""},
    {"nombre": "Clarisa Calderón","whatsapp": "529991005005", "cumpleanos": "30/12", "ultimaCita": "11/07/2026", "ultimoServicio": "Pestañas — Retoque 20 días",  "historialMedico": "Ninguno",       "notas": ""},
    {"nombre": "Melany Vilchis",  "whatsapp": "529991006006", "cumpleanos": "05/03", "ultimaCita": "11/07/2026", "ultimoServicio": "Lami Brows",                  "historialMedico": "Ninguno",       "notas": ""},
    {"nombre": "Yamil Farah",     "whatsapp": "529991007007", "cumpleanos": "18/11", "ultimaCita": "11/07/2026", "ultimoServicio": "Shot de Vitamina",            "historialMedico": "Ninguno",       "notas": ""},
    {"nombre": "Keyra Pool",      "whatsapp": "529991008008", "cumpleanos": "25/07", "cumpleanos": "25/07",      "ultimaCita": "12/07/2026", "ultimoServicio": "Full Brows", "historialMedico": "Ninguno", "notas": ""},
]

# ─────────────────────────────────────────────────────────
# DATE HELPERS
# ─────────────────────────────────────────────────────────
def parse_fecha(fecha_str):
    """Parse dd/mm/yyyy date strings."""
    try:
        return datetime.strptime(fecha_str.strip(), "%d/%m/%Y")
    except (ValueError, AttributeError):
        return None

def is_today(fecha_str):
    d = parse_fecha(fecha_str)
    return d is not None and d.date() == datetime.today().date()

def is_this_week(fecha_str):
    d = parse_fecha(fecha_str)
    if not d:
        return False
    today = datetime.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return start.date() <= d.date() <= end.date()

def is_this_month(fecha_str):
    d = parse_fecha(fecha_str)
    if not d:
        return False
    today = datetime.today()
    return d.month == today.month and d.year == today.year

def birthday_within_7_days(cumpleanos_str):
    """Check if birthday (dd/mm) falls within the next 7 days."""
    try:
        parts = cumpleanos_str.strip().split("/")
        day, month = int(parts[0]), int(parts[1])
        today = datetime.today()
        bd = datetime(today.year, month, day)
        if bd.date() < today.date():
            bd = datetime(today.year + 1, month, day)
        return 0 <= (bd.date() - today.date()).days <= 7
    except (ValueError, IndexError, AttributeError):
        return False

def is_retoque(servicio):
    return "retoque" in servicio.lower() if servicio else False

# ─────────────────────────────────────────────────────────
# CORE FUNCTIONS
# ─────────────────────────────────────────────────────────
def load_appointments(data):
    """Load and validate appointment records."""
    logger.info(f"Loading appointments — {len(data)} records found")
    valid = []

    for i, row in enumerate(data, start=1):
        nombre = row.get("nombre", "").strip()
        fecha  = row.get("fecha", "").strip()
        precio = row.get("precio", "").strip()
        servicio = row.get("servicio", "").strip()

        if not nombre:
            logger.warning(f"Row {i}: missing client name — skipped")
            continue

        if not fecha or parse_fecha(fecha) is None:
            logger.warning(f"Row {i} ({nombre}): invalid or missing date '{fecha}' — skipped")
            continue

        if not servicio:
            logger.warning(f"Row {i} ({nombre}): missing service — skipped")
            continue

        if not precio:
            logger.warning(f"Row {i} ({nombre}): price not set for '{servicio}' — recorded as 0")
            row["precio"] = "0"

        try:
            float(row["precio"])
        except ValueError:
            logger.warning(f"Row {i} ({nombre}): non-numeric price '{row['precio']}' — set to 0")
            row["precio"] = "0"

        if not row.get("formaPago"):
            logger.warning(f"Row {i} ({nombre}, {fecha}): payment method missing")

        valid.append(row)

    logger.info(f"Appointments loaded — {len(valid)} valid, {len(data) - len(valid)} skipped")
    return valid


def load_clients(data):
    """Load and validate client records."""
    logger.info(f"Loading clients — {len(data)} records found")
    valid = []
    seen_names = set()

    for i, row in enumerate(data, start=1):
        nombre = row.get("nombre", "").strip()

        if not nombre:
            logger.warning(f"Client row {i}: missing name — skipped")
            continue

        if nombre in seen_names:
            logger.warning(f"Client row {i}: duplicate entry for '{nombre}' — skipped")
            continue

        alergias = row.get("historialMedico", "").strip()
        if alergias and alergias.lower() not in ("ninguno", "none", ""):
            logger.info(f"Client '{nombre}': medical/allergy record noted — '{alergias}'")

        seen_names.add(nombre)
        valid.append(row)

    logger.info(f"Clients loaded — {len(valid)} valid records")
    return valid


def calculate_revenue(appointments):
    """Calculate revenue totals by period and payment method."""
    logger.info("Calculating revenue totals")

    totals = {
        "today": 0.0, "week": 0.0, "month": 0.0,
        "efectivo": 0.0, "tarjeta": 0.0, "transferencia": 0.0, "sin_metodo": 0.0
    }

    for appt in appointments:
        if appt.get("estatus", "").lower() == "cancelada":
            continue

        precio = float(appt.get("precio", 0) or 0)
        fecha  = appt.get("fecha", "")
        metodo = appt.get("formaPago", "").lower()

        if is_today(fecha):
            totals["today"] += precio
        if is_this_week(fecha):
            totals["week"] += precio
        if is_this_month(fecha):
            totals["month"] += precio
            if "efectivo" in metodo:
                totals["efectivo"] += precio
            elif "tarjeta" in metodo:
                totals["tarjeta"] += precio
            elif "transfer" in metodo:
                totals["transferencia"] += precio
            else:
                totals["sin_metodo"] += precio

    logger.info(f"Revenue — Today: ${totals['today']:.2f} | Week: ${totals['week']:.2f} | Month: ${totals['month']:.2f}")
    logger.info(f"Payment methods — Efectivo: ${totals['efectivo']:.2f} | Tarjeta: ${totals['tarjeta']:.2f} | Transferencia: ${totals['transferencia']:.2f} | Sin método: ${totals['sin_metodo']:.2f}")

    if totals["sin_metodo"] > 0:
        logger.warning(f"${totals['sin_metodo']:.2f} in revenue has no payment method recorded — update Sheets")

    return totals


def detect_birthday_alerts(clients):
    """Flag clients with birthdays in the next 7 days."""
    logger.info("Scanning for upcoming birthdays")
    alerts = []

    for client in clients:
        nombre = client.get("nombre", "")
        cumple = client.get("cumpleanos", "")

        if not cumple:
            continue

        if birthday_within_7_days(cumple):
            logger.info(f"Birthday alert: {nombre} — birthday on {cumple} (within 7 days)")
            alerts.append(nombre)

    if not alerts:
        logger.info("No birthdays in the next 7 days")
    else:
        logger.info(f"Birthday alerts generated for {len(alerts)} client(s): {', '.join(alerts)}")

    return alerts


def detect_retouching_reminders(appointments):
    """Flag retouching appointments in the next 2 days."""
    logger.info("Scanning for upcoming retouching appointments")
    reminders = []
    today = datetime.today().date()

    for appt in appointments:
        if not is_retoque(appt.get("servicio", "")):
            continue

        fecha = parse_fecha(appt.get("fecha", ""))
        if not fecha:
            continue

        diff = (fecha.date() - today).days
        if 0 <= diff <= 2:
            nombre = appt.get("nombre", "—")
            logger.info(f"Retouching reminder: {nombre} — '{appt['servicio']}' in {diff} day(s) ({appt['fecha']})")
            reminders.append(appt)

    if not reminders:
        logger.info("No retouching appointments in the next 2 days")

    return reminders


def generate_report(appointments, clients, revenue):
    """Write a daily summary report to /logs/report_YYYY-MM-DD.log."""
    today_str = datetime.today().strftime("%Y-%m-%d")
    report_path = LOGS_DIR / f"report_{today_str}.log"

    logger.info(f"Generating daily report — {report_path.name}")

    today_appts = [a for a in appointments if is_today(a.get("fecha", ""))]
    confirmed   = [a for a in today_appts if "confirm" in a.get("estatus", "").lower()]
    pending     = [a for a in today_appts if "pend"    in a.get("estatus", "").lower()]
    cancelled   = [a for a in today_appts if "cancel"  in a.get("estatus", "").lower()]

    lines = [
        f"SAM BEAUTY — Daily Report",
        f"Generated: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}",
        f"{'─' * 48}",
        f"Appointments today : {len(today_appts)}",
        f"  Confirmed        : {len(confirmed)}",
        f"  Pending          : {len(pending)}",
        f"  Cancelled        : {len(cancelled)}",
        f"{'─' * 48}",
        f"Revenue today      : ${revenue['today']:.2f}",
        f"Revenue this week  : ${revenue['week']:.2f}",
        f"Revenue this month : ${revenue['month']:.2f}",
        f"{'─' * 48}",
        f"Total clients      : {len(clients)}",
        f"{'─' * 48}",
    ]

    if today_appts:
        lines.append("Today's agenda:")
        for a in today_appts:
            lines.append(f"  {a['hora']:12} {a['nombre']:20} {a['servicio'][:30]:30} ${float(a['precio'] or 0):.2f}  [{a['estatus']}]")

    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        logger.info(f"Report written successfully — {report_path.name}")
    except PermissionError:
        logger.error(f"Could not write report to '{report_path}': permission denied")
    except OSError as e:
        logger.error(f"Could not write report to '{report_path}': {e}")

    return report_path


# ─────────────────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────────────────
def main():
    logger.info("=" * 56)
    logger.info("Sam Beauty Dashboard — pipeline started")
    logger.info(f"Run date: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 56)

    # 1. Load data
    appointments = load_appointments(MOCK_APPOINTMENTS)
    clients      = load_clients(MOCK_CLIENTS)

    # 2. Revenue
    revenue = calculate_revenue(appointments)

    # 3. Alerts
    birthday_alerts     = detect_birthday_alerts(clients)
    retouching_reminders = detect_retouching_reminders(appointments)

    # 4. Report
    report_path = generate_report(appointments, clients, revenue)

    logger.info("Pipeline completed successfully")
    logger.info("=" * 56)

    print(f"\n✓ Log written to  : {LOG_FILE}")
    print(f"✓ Report written to: {report_path}")


if __name__ == "__main__":
    main()
