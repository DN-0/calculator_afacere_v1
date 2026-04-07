# ============================================================
# STEP 1: Imports + CONFIG
# ============================================================
import os
import json
import datetime

import streamlit as st
import pandas as pd

# ============================================================
# CONFIG — reguli fiscale România 2026
# ============================================================
CONFIG = {
    'COTA_IMPOZIT_PROFIT': 0.16,
    'COTA_IMPOZIT_DIVIDENDE': 0.16,
    'COTA_CASS_DIVIDENDE': 0.10,
    'CASS_PLAFON_6SAL': 25950,
    'CASS_PLAFON_12SAL': 51900,
    'CASS_PLAFON_24SAL': 103800,
    'CAS_ANGAJAT': 0.25,
    'CASS_ANGAJAT': 0.10,
    'IMPOZIT_VENIT': 0.10,
    'CAM_ANGAJATOR': 0.0225,
    'SALARIU_MINIM_BRUT': 4325,
    'CURS_EUR_RON_DEFAULT': 5.10,
}

# ============================================================
# TRANSLATIONS
# ============================================================
TRANSLATIONS = {
    'RO': {
        'title': 'Calculator Profit Afacere — Chioșc/Container 2026',
        'subtitle': 'Planifică profitabilitatea | Romania 2026',
        'settings': 'Setări',
        'language': 'Limbă / Language',
        'currency': 'Monedă',
        'eur_rate': 'Curs EUR/RON',
        'include_cass': 'Includeți CASS pe dividende',
        'reset_btn': '🔄 Reset la valori implicite',
        'load_example_btn': '📋 Încarcă exemplu',
        'owner_section': '👤 Owner',
        'net_salary': 'Salariu net dorit (RON/lună)',
        'net_dividends': 'Dividende nete dorite (RON/lună)',
        'employees_section': '👥 Angajați',
        'num_employees': 'Număr angajați (fără owner)',
        'use_min_wage': 'Salariu minim',
        'custom_wage': 'Salariu personalizat',
        'employee_gross': 'Salariu brut angajat',
        'fixed_costs_section': '🏠 Costuri Fixe Lunare',
        'chirie_teren': 'Chirie teren',
        'chirie_container': 'Chirie container/spațiu',
        'contabilitate': 'Contabilitate',
        'utilitati': 'Utilități',
        'combustibil': 'Combustibil/transport',
        'leasing': 'Leasing/rate',
        'alte_costuri': 'Alte costuri',
        'total_fixed': 'Total costuri fixe',
        'business_section': '📊 Parametri Business',
        'margin': 'Marja comercială (%)',
        'working_days': 'Zile lucratoare/lună',
        'basket': 'Valoare medie coș (RON/client)',
        'products_section': '🛒 Prețuri și Mix Produse',
        'prices_header': 'Prețuri unitare',
        'mix_header': 'Mix vânzări (%)',
        'pret_apa': 'Preț apă',
        'pret_suc': 'Preț suc',
        'pret_dulciuri': 'Preț dulciuri/snacks',
        'pret_tigari': 'Preț țigări',
        'mix_apa': 'Mix apă (%)',
        'mix_suc': 'Mix suc (%)',
        'mix_dulciuri': 'Mix dulciuri (%)',
        'mix_tigari': 'Mix țigări (%)',
        'results_title': '📈 Rezultate',
        'monthly_revenue': 'Venituri lunare necesare',
        'daily_revenue': 'Venituri zilnice',
        'clients_day': 'Clienți/zi',
        'items_day': 'Produse/zi',
        'breakdown_owner': '🔍 Detaliu Salariu Owner',
        'breakdown_employees': '🔍 Detaliu Costuri Angajați',
        'breakdown_fixed': '🔍 Detaliu Costuri Fixe',
        'breakdown_dividends': '🔍 Detaliu Dividende',
        'breakdown_total': '🔍 Total Costuri de Acoperit',
        'product_mix_output': '🛒 Mix Produse Zilnic',
        'sensitivity_table': '📊 Tabel Sensibilitate Marja',
        'dividends_table': '📊 Tabel Dividende Comparative',
        'save_section': '💾 Salvare / Încărcare Versiuni',
        'version_name': 'Nume versiune (opțional)',
        'save_btn': '💾 Salvează versiune',
        'saved_ok': '✅ Versiunea a fost salvată!',
        'load_btn': '⬅️ Încarcă',
        'delete_btn': '🗑️ Șterge',
        'download_current': '⬇️ Descarcă raport curent (CSV)',
        'download_version': '⬇️ CSV',
        'download_comparison': '⬇️ Descarcă comparație versiuni (CSV)',
        'no_versions': 'Nu există versiuni salvate.',
        'gross': 'Brut',
        'net': 'Net',
        'cas': 'CAS (25%)',
        'cass': 'CASS (10%)',
        'tax': 'Impozit venit (10%)',
        'employer_cost': 'Cost angajator',
        'cam': 'CAM (2.25%)',
        'dividends_net': 'Dividende nete dorite',
        'dividends_cass': 'CASS dividende (lunar)',
        'dividends_gross': 'Dividende brute',
        'dividends_tax': 'Impozit dividende (16%)',
        'pretax_profit': 'Profit pre-tax necesar',
        'margin_pct': 'Marja (%)',
        'annual': 'Anual',
        'cass_plafon': 'Plafon CASS',
        'monthly': 'Lunar',
        'total': 'Total',
        'warning_margin_low': '⚠️ Marja sub 15% — risc ridicat pentru afacere',
        'warning_margin_high': '⚠️ Marja peste 40% — verificați calculele',
        'warning_tigari': '⚠️ Procent ridicat de țigări — risc fiscal (accize)',
        'warning_clienti': '⚠️ Peste 500 clienți/zi — verificați capacitatea',
        'error_mix': '❌ Suma mixului de produse trebuie să fie 100%',
        'error_zile': '❌ Zilele lucrătoare trebuie să fie > 0',
        'revenue_needed': 'Venituri necesare',
        'profit_remaining': 'Profit rămas',
        'net_in_hand': 'Net în mână',
        'fixed_costs_comparison': '📊 Tabel Costuri Fixe Comparative',
    },
    'EN': {
        'title': 'Business Profit Calculator — Kiosk/Container 2026',
        'subtitle': 'Plan profitability | Romania 2026',
        'settings': 'Settings',
        'language': 'Language / Limbă',
        'currency': 'Currency',
        'eur_rate': 'EUR/RON Rate',
        'include_cass': 'Include CASS on dividends',
        'reset_btn': '🔄 Reset to defaults',
        'load_example_btn': '📋 Load example',
        'owner_section': '👤 Owner',
        'net_salary': 'Desired net salary (RON/month)',
        'net_dividends': 'Desired net dividends (RON/month)',
        'employees_section': '👥 Employees',
        'num_employees': 'Number of employees (excl. owner)',
        'use_min_wage': 'Minimum wage',
        'custom_wage': 'Custom wage',
        'employee_gross': 'Employee gross salary',
        'fixed_costs_section': '🏠 Monthly Fixed Costs',
        'chirie_teren': 'Land rent',
        'chirie_container': 'Container/space rent',
        'contabilitate': 'Accounting',
        'utilitati': 'Utilities',
        'combustibil': 'Fuel/transport',
        'leasing': 'Leasing/installments',
        'alte_costuri': 'Other costs',
        'total_fixed': 'Total fixed costs',
        'business_section': '📊 Business Parameters',
        'margin': 'Commercial margin (%)',
        'working_days': 'Working days/month',
        'basket': 'Average basket value (RON/client)',
        'products_section': '🛒 Prices and Product Mix',
        'prices_header': 'Unit prices',
        'mix_header': 'Sales mix (%)',
        'pret_apa': 'Water price',
        'pret_suc': 'Juice price',
        'pret_dulciuri': 'Candy/snacks price',
        'pret_tigari': 'Cigarettes price',
        'mix_apa': 'Water mix (%)',
        'mix_suc': 'Juice mix (%)',
        'mix_dulciuri': 'Candy mix (%)',
        'mix_tigari': 'Cigarettes mix (%)',
        'results_title': '📈 Results',
        'monthly_revenue': 'Required monthly revenue',
        'daily_revenue': 'Daily revenue',
        'clients_day': 'Clients/day',
        'items_day': 'Products/day',
        'breakdown_owner': '🔍 Owner Salary Breakdown',
        'breakdown_employees': '🔍 Employee Cost Breakdown',
        'breakdown_fixed': '🔍 Fixed Cost Breakdown',
        'breakdown_dividends': '🔍 Dividend Breakdown',
        'breakdown_total': '🔍 Total Costs to Cover',
        'product_mix_output': '🛒 Daily Product Mix',
        'sensitivity_table': '📊 Margin Sensitivity Table',
        'dividends_table': '📊 Dividend Comparison Table',
        'save_section': '💾 Save / Load Versions',
        'version_name': 'Version name (optional)',
        'save_btn': '💾 Save version',
        'saved_ok': '✅ Version saved!',
        'load_btn': '⬅️ Load',
        'delete_btn': '🗑️ Delete',
        'download_current': '⬇️ Download current report (CSV)',
        'download_version': '⬇️ CSV',
        'download_comparison': '⬇️ Download version comparison (CSV)',
        'no_versions': 'No saved versions.',
        'gross': 'Gross',
        'net': 'Net',
        'cas': 'CAS (25%)',
        'cass': 'CASS (10%)',
        'tax': 'Income tax (10%)',
        'employer_cost': 'Employer cost',
        'cam': 'CAM (2.25%)',
        'dividends_net': 'Desired net dividends',
        'dividends_cass': 'Dividend CASS (monthly)',
        'dividends_gross': 'Gross dividends',
        'dividends_tax': 'Dividend tax (16%)',
        'pretax_profit': 'Required pre-tax profit',
        'margin_pct': 'Margin (%)',
        'annual': 'Annual',
        'cass_plafon': 'CASS ceiling',
        'monthly': 'Monthly',
        'total': 'Total',
        'warning_margin_low': '⚠️ Margin below 15% — high business risk',
        'warning_margin_high': '⚠️ Margin above 40% — check calculations',
        'warning_tigari': '⚠️ High cigarette percentage — tax risk (excise)',
        'warning_clienti': '⚠️ Over 500 clients/day — check capacity',
        'error_mix': '❌ Product mix must sum to 100%',
        'error_zile': '❌ Working days must be > 0',
        'revenue_needed': 'Revenue needed',
        'profit_remaining': 'Profit remaining',
        'net_in_hand': 'Net in hand',
        'fixed_costs_comparison': '📊 Fixed Costs Comparison Table',
    }
}

# ============================================================
# STEP 2: Pure calculation functions (no side effects)
# ============================================================

HISTORY_FILE = "history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def calculateGrossFromNetSalary(net_ron):
    """Net = Brut × 0.585 → Brut = Net / 0.585"""
    return net_ron / 0.585


def calculateEmployerCost(gross_ron):
    """Cost angajator = Brut × 1.0225"""
    return gross_ron * (1 + CONFIG['CAM_ANGAJATOR'])


def calculateEmployeeCost(gross_ron):
    """Returns dict with CAS, CASS, impozit, net"""
    cas = gross_ron * CONFIG['CAS_ANGAJAT']
    cass = gross_ron * CONFIG['CASS_ANGAJAT']
    baza_impozit = gross_ron - cas - cass
    impozit = baza_impozit * CONFIG['IMPOZIT_VENIT']
    net = gross_ron - cas - cass - impozit
    return {'cas': cas, 'cass': cass, 'impozit': impozit, 'net': net, 'gross': gross_ron}


def calculateDividendCASS(dividende_nete_anuale_ron, include_cass):
    if not include_cass or dividende_nete_anuale_ron <= 0:
        return {'plafon': 0, 'cass_anual': 0, 'cass_lunar': 0}

    if dividende_nete_anuale_ron <= CONFIG['CASS_PLAFON_6SAL']:
        plafon = CONFIG['CASS_PLAFON_6SAL']
    elif dividende_nete_anuale_ron <= CONFIG['CASS_PLAFON_12SAL']:
        plafon = CONFIG['CASS_PLAFON_12SAL']
    else:
        plafon = CONFIG['CASS_PLAFON_24SAL']

    cass_anual = plafon * CONFIG['COTA_CASS_DIVIDENDE']
    return {'plafon': plafon, 'cass_anual': cass_anual, 'cass_lunar': cass_anual / 12}


def calculateGrossDividendsNeeded(net_dividende_lunar_ron, include_cass):
    cass_info = calculateDividendCASS(net_dividende_lunar_ron * 12, include_cass)
    brut = (net_dividende_lunar_ron + cass_info['cass_lunar']) / (1 - CONFIG['COTA_IMPOZIT_DIVIDENDE'])
    return {
        'brut_lunar': brut,
        'cass_lunar': cass_info['cass_lunar'],
        'impozit_dividende': brut * CONFIG['COTA_IMPOZIT_DIVIDENDE'],
        'cass_info': cass_info,
    }


def calculatePretaxProfitForDividends(dividende_brute_lunar_ron):
    return dividende_brute_lunar_ron / (1 - CONFIG['COTA_IMPOZIT_PROFIT'])


def calculateTotalCosts(params):
    gross_owner = calculateGrossFromNetSalary(params['net_salariu'])
    cost_owner = calculateEmployerCost(gross_owner)

    cost_angajati = 0
    for sal_brut in params['salarii_angajati']:
        cost_angajati += calculateEmployerCost(sal_brut)

    costuri_fixe = (
        params['chirie_teren'] + params['chirie_container'] +
        params['contabilitate'] + params['utilitati'] +
        params['combustibil'] + params['leasing'] + params['alte_costuri']
    )

    div_info = calculateGrossDividendsNeeded(params['net_dividende'], params['include_cass'])
    profit_necesar = calculatePretaxProfitForDividends(div_info['brut_lunar'])

    return {
        'cost_owner': cost_owner,
        'gross_owner': gross_owner,
        'cost_angajati': cost_angajati,
        'costuri_fixe': costuri_fixe,
        'profit_necesar_dividende': profit_necesar,
        'div_info': div_info,
        'total': cost_owner + cost_angajati + costuri_fixe + profit_necesar,
    }


def calculateRevenueNeeded(total_costs_ron, margin_pct):
    if margin_pct <= 0:
        return 0
    return total_costs_ron / (margin_pct / 100)


def calculateProductMix(revenue_zilnica, basket, mix_pct, preturi):
    clienti_zi = revenue_zilnica / basket if basket > 0 else 0
    items = {}
    for prod, pct in mix_pct.items():
        venit_prod = revenue_zilnica * (pct / 100)
        items[prod] = venit_prod / preturi[prod] if preturi[prod] > 0 else 0
    return {'clienti_zi': clienti_zi, 'items': items}


def calculateMarginSensitivity(total_costs_ron, zile_lucratoare, marje=None):
    if marje is None:
        marje = [20, 22, 25, 28, 30]
    rows = []
    for m in marje:
        rev_lunar = calculateRevenueNeeded(total_costs_ron, m)
        rev_zilnic = rev_lunar / zile_lucratoare if zile_lucratoare > 0 else 0
        profit_ramas = rev_lunar * (m / 100) - total_costs_ron
        rows.append({
            'Marja (%)': m,
            'Venituri lunare (RON)': round(rev_lunar, 0),
            'Venituri zilnice (RON)': round(rev_zilnic, 0),
            'Profit ramas (RON)': round(max(0, profit_ramas), 0),
        })
    return rows


def formatCurrencyRON(val, decimale=0):
    return f"{val:,.{decimale}f}".replace(",", ".")


# ============================================================
# STEP 3: set_page_config (must be first Streamlit call)
# ============================================================
st.set_page_config(
    page_title="Calculator Profit Afacere 2026",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# STEP 4: Custom CSS
# ============================================================
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d6a4f 100%);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        color: white;
        margin: 4px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #52b788;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #b7e4c7;
        margin-top: 4px;
    }
    .section-box {
        background: #0e1117;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .total-row {
        font-weight: 700;
        color: #52b788;
    }
    .stDataFrame { font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# STEP 5: Input defaults + session_state init
# ============================================================
input_defaults = {
    'moneda': 'RON',
    'curs': CONFIG['CURS_EUR_RON_DEFAULT'],
    'net_salariu': 6500.0,
    'net_dividende': 4000.0,
    'nr_angajati': 1,
    'salariu_angajat_1': float(CONFIG['SALARIU_MINIM_BRUT']),
    'chirie_teren': 2000.0,
    'chirie_container': 1500.0,
    'contabilitate': 500.0,
    'utilitati': 700.0,
    'combustibil': 800.0,
    'leasing': 1500.0,
    'alte_costuri': 1000.0,
    'margin_procent': 25,
    'include_cass': True,
    'zile_lucratoare': 30,
    'valoare_cos': 12.0,
    'pret_apa': 3.59,
    'pret_suc': 6.19,
    'pret_dulciuri': 5.49,
    'pret_tigari': 30.0,
    'mix_apa': 35.0,
    'mix_suc': 25.0,
    'mix_dulciuri': 30.0,
    'mix_tigari': 10.0,
}

# Add per-employee defaults for up to 10 employees
for i in range(2, 11):
    input_defaults[f'salariu_angajat_{i}'] = float(CONFIG['SALARIU_MINIM_BRUT'])

for key, val in input_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

if 'version_to_load' not in st.session_state:
    st.session_state.version_to_load = None

if 'history' not in st.session_state:
    st.session_state.history = load_history()

if 'limba' not in st.session_state:
    st.session_state.limba = 'RO'

if 'version_saved_msg' not in st.session_state:
    st.session_state.version_saved_msg = False

# ============================================================
# STEP 6: Load version BEFORE any widgets
# ============================================================

def load_version_into_state(version_data):
    """Run BEFORE any widgets. Restores saved version into session_state."""
    if 'widget_values' in version_data:
        st.session_state.moneda = version_data.get('moneda', 'RON')
        st.session_state.curs = version_data.get('curs', CONFIG['CURS_EUR_RON_DEFAULT'])
        for key, val in version_data['widget_values'].items():
            st.session_state[key] = val
    else:
        # backward compat
        st.session_state.moneda = 'RON'
        st.session_state.curs = CONFIG['CURS_EUR_RON_DEFAULT']
        for key in input_defaults:
            if key in version_data.get('params', {}):
                st.session_state[key] = version_data['params'][key]


if st.session_state.version_to_load is not None:
    load_version_into_state(st.session_state.version_to_load)
    st.session_state.version_to_load = None

# Get translations
t = TRANSLATIONS[st.session_state.get('limba', 'RO')]

# ============================================================
# STEP 7: Sidebar
# ============================================================
with st.sidebar:
    st.title(f"⚙️ {t['settings']}")

    limba = st.radio(t['language'], ["RO", "EN"], horizontal=True, key='limba')
    # Update translations after potential change
    t = TRANSLATIONS[limba]

    st.divider()

    moneda = st.radio(t['currency'], ["RON", "EUR"], horizontal=True, key='moneda')
    sym = "RON" if moneda == "RON" else "€"

    if moneda == "EUR":
        curs = st.number_input(
            t['eur_rate'],
            min_value=1.0,
            max_value=20.0,
            step=0.01,
            format="%.2f",
            key='curs'
        )
    else:
        curs = CONFIG['CURS_EUR_RON_DEFAULT']

    st.divider()

    include_cass = st.toggle(t['include_cass'], key='include_cass')

    st.divider()

    if st.button(t['reset_btn'], width='stretch'):
        # Skip widget-bound keys from sidebar (widgets manage their own state via key parameter)
        widget_keys = {'moneda', 'curs', 'include_cass', 'limba'}
        for key, val in input_defaults.items():
            if key not in widget_keys:
                st.session_state[key] = val
        st.rerun()

    if st.button(t['load_example_btn'], width='stretch'):
        st.session_state.version_to_load = {
            'widget_values': input_defaults.copy(),
            'moneda': 'RON',
            'curs': CONFIG['CURS_EUR_RON_DEFAULT'],
        }
        st.rerun()

# ============================================================
# HELPER: conversion functions (defined after sidebar so
# moneda and curs variables are available)
# ============================================================

def to_ron(val):
    return val * curs if moneda == "EUR" else val


def from_ron(val):
    return val / curs if moneda == "EUR" else val

# ============================================================
# STEP 8: Main content — Input widgets
# ============================================================
st.title(t['title'])
st.caption(t['subtitle'])

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # --- A. Owner ---
    with st.expander(t['owner_section'], expanded=True):
        net_sal_label = f"{t['net_salary']} ({sym}/lună)" if moneda == "RON" else f"{t['net_salary']} ({sym}/month)"
        net_salariu_disp = st.number_input(
            net_sal_label,
            min_value=0.0,
            step=100.0,
            format="%.2f",
            key='net_salariu'
        )
        net_div_label = f"{t['net_dividends']} ({sym}/lună)" if moneda == "RON" else f"{t['net_dividends']} ({sym}/month)"
        net_dividende_disp = st.number_input(
            net_div_label,
            min_value=0.0,
            step=100.0,
            format="%.2f",
            key='net_dividende'
        )

    # --- B. Angajați ---
    with st.expander(t['employees_section'], expanded=True):
        nr_angajati = st.number_input(
            t['num_employees'],
            min_value=0,
            max_value=10,
            step=1,
            key='nr_angajati'
        )

        salarii_angajati_disp = []
        for i in range(1, int(nr_angajati) + 1):
            wage_key = f'salariu_angajat_{i}'
            if wage_key not in st.session_state:
                st.session_state[wage_key] = float(CONFIG['SALARIU_MINIM_BRUT'])

            use_min = st.checkbox(
                f"{t['use_min_wage']} — Angajat {i}",
                value=(st.session_state[wage_key] == float(CONFIG['SALARIU_MINIM_BRUT'])),
                key=f'use_min_{i}'
            )
            if use_min:
                st.session_state[wage_key] = float(CONFIG['SALARIU_MINIM_BRUT'])
                st.caption(f"Angajat {i}: {sym} {from_ron(CONFIG['SALARIU_MINIM_BRUT']):.2f} brut")
                salarii_angajati_disp.append(float(CONFIG['SALARIU_MINIM_BRUT']))
            else:
                sal = st.number_input(
                    f"{t['employee_gross']} {i} ({sym})",
                    min_value=float(CONFIG['SALARIU_MINIM_BRUT']),
                    step=100.0,
                    format="%.2f",
                    key=wage_key
                )
                salarii_angajati_disp.append(to_ron(sal))

    # --- C. Costuri fixe ---
    with st.expander(t['fixed_costs_section'], expanded=True):
        fc_cols = st.columns(2)
        with fc_cols[0]:
            chirie_teren_d = st.number_input(f"{t['chirie_teren']} ({sym})", min_value=0.0, step=50.0, format="%.0f", key='chirie_teren')
            chirie_container_d = st.number_input(f"{t['chirie_container']} ({sym})", min_value=0.0, step=50.0, format="%.0f", key='chirie_container')
            contabilitate_d = st.number_input(f"{t['contabilitate']} ({sym})", min_value=0.0, step=50.0, format="%.0f", key='contabilitate')
            utilitati_d = st.number_input(f"{t['utilitati']} ({sym})", min_value=0.0, step=50.0, format="%.0f", key='utilitati')
        with fc_cols[1]:
            combustibil_d = st.number_input(f"{t['combustibil']} ({sym})", min_value=0.0, step=50.0, format="%.0f", key='combustibil')
            leasing_d = st.number_input(f"{t['leasing']} ({sym})", min_value=0.0, step=50.0, format="%.0f", key='leasing')
            alte_costuri_d = st.number_input(f"{t['alte_costuri']} ({sym})", min_value=0.0, step=50.0, format="%.0f", key='alte_costuri')

        total_fixe_disp = (chirie_teren_d + chirie_container_d + contabilitate_d +
                           utilitati_d + combustibil_d + leasing_d + alte_costuri_d)
        st.success(f"**{t['total_fixed']}: {sym} {total_fixe_disp:,.0f}**")

with col_right:
    # --- D. Business params ---
    with st.expander(t['business_section'], expanded=True):
        margin_procent = st.slider(
            f"{t['margin']} (%)",
            min_value=1,
            max_value=99,
            step=1,
            key='margin_procent'
        )
        zile_lucratoare = st.number_input(
            t['working_days'],
            min_value=1,
            max_value=31,
            step=1,
            key='zile_lucratoare'
        )
        valoare_cos_d = st.number_input(
            f"{t['basket']} ({sym})",
            min_value=1.0,
            step=0.5,
            format="%.2f",
            key='valoare_cos'
        )

    # --- E. Product Mix ---
    with st.expander(t['products_section'], expanded=True):
        st.subheader(t['prices_header'])
        pr_cols = st.columns(2)
        with pr_cols[0]:
            pret_apa_d = st.number_input(f"{t['pret_apa']} ({sym})", min_value=0.01, step=0.10, format="%.2f", key='pret_apa')
            pret_suc_d = st.number_input(f"{t['pret_suc']} ({sym})", min_value=0.01, step=0.10, format="%.2f", key='pret_suc')
        with pr_cols[1]:
            pret_dulciuri_d = st.number_input(f"{t['pret_dulciuri']} ({sym})", min_value=0.01, step=0.10, format="%.2f", key='pret_dulciuri')
            pret_tigari_d = st.number_input(f"{t['pret_tigari']} ({sym})", min_value=0.01, step=0.50, format="%.2f", key='pret_tigari')

        st.subheader(t['mix_header'])
        mx_cols = st.columns(2)
        with mx_cols[0]:
            mix_apa_d = st.number_input(t['mix_apa'], min_value=0.0, max_value=100.0, step=1.0, format="%.1f", key='mix_apa')
            mix_suc_d = st.number_input(t['mix_suc'], min_value=0.0, max_value=100.0, step=1.0, format="%.1f", key='mix_suc')
        with mx_cols[1]:
            mix_dulciuri_d = st.number_input(t['mix_dulciuri'], min_value=0.0, max_value=100.0, step=1.0, format="%.1f", key='mix_dulciuri')
            mix_tigari_d = st.number_input(t['mix_tigari'], min_value=0.0, max_value=100.0, step=1.0, format="%.1f", key='mix_tigari')

        suma_mix = mix_apa_d + mix_suc_d + mix_dulciuri_d + mix_tigari_d
        if abs(suma_mix - 100.0) < 0.01:
            st.success(f"✅ Mix total: {suma_mix:.1f}%")
        else:
            st.error(f"{t['error_mix']} (curent: {suma_mix:.1f}%)")

# ============================================================
# STEP 9: Calculations
# ============================================================

# Convert displayed values to RON for calculations
net_salariu_ron = to_ron(st.session_state.get('net_salariu', input_defaults['net_salariu']))
net_dividende_ron = to_ron(st.session_state.get('net_dividende', input_defaults['net_dividende']))
valoare_cos_ron = to_ron(st.session_state.get('valoare_cos', input_defaults['valoare_cos']))
chirie_teren_ron = to_ron(st.session_state.get('chirie_teren', input_defaults['chirie_teren']))
chirie_container_ron = to_ron(st.session_state.get('chirie_container', input_defaults['chirie_container']))
contabilitate_ron = to_ron(st.session_state.get('contabilitate', input_defaults['contabilitate']))
utilitati_ron = to_ron(st.session_state.get('utilitati', input_defaults['utilitati']))
combustibil_ron = to_ron(st.session_state.get('combustibil', input_defaults['combustibil']))
leasing_ron = to_ron(st.session_state.get('leasing', input_defaults['leasing']))
alte_costuri_ron = to_ron(st.session_state.get('alte_costuri', input_defaults['alte_costuri']))

pret_apa_ron = to_ron(st.session_state.get('pret_apa', input_defaults['pret_apa']))
pret_suc_ron = to_ron(st.session_state.get('pret_suc', input_defaults['pret_suc']))
pret_dulciuri_ron = to_ron(st.session_state.get('pret_dulciuri', input_defaults['pret_dulciuri']))
pret_tigari_ron = to_ron(st.session_state.get('pret_tigari', input_defaults['pret_tigari']))

_nr_angajati = int(st.session_state.get('nr_angajati', input_defaults['nr_angajati']))
salarii_angajati_ron = []
for i in range(1, _nr_angajati + 1):
    wage_key = f'salariu_angajat_{i}'
    sal_disp = st.session_state.get(wage_key, float(CONFIG['SALARIU_MINIM_BRUT']))
    salarii_angajati_ron.append(to_ron(sal_disp))

params_ron = {
    'net_salariu': net_salariu_ron,
    'net_dividende': net_dividende_ron,
    'nr_angajati': _nr_angajati,
    'salarii_angajati': salarii_angajati_ron,
    'chirie_teren': chirie_teren_ron,
    'chirie_container': chirie_container_ron,
    'contabilitate': contabilitate_ron,
    'utilitati': utilitati_ron,
    'combustibil': combustibil_ron,
    'leasing': leasing_ron,
    'alte_costuri': alte_costuri_ron,
    'include_cass': bool(st.session_state.get('include_cass', input_defaults['include_cass'])),
}

_margin = float(st.session_state.get('margin_procent', input_defaults['margin_procent']))
_zile = int(st.session_state.get('zile_lucratoare', input_defaults['zile_lucratoare']))
_mix_apa = float(st.session_state.get('mix_apa', input_defaults['mix_apa']))
_mix_suc = float(st.session_state.get('mix_suc', input_defaults['mix_suc']))
_mix_dulciuri = float(st.session_state.get('mix_dulciuri', input_defaults['mix_dulciuri']))
_mix_tigari = float(st.session_state.get('mix_tigari', input_defaults['mix_tigari']))

costs = calculateTotalCosts(params_ron)
revenue_lunar_ron = calculateRevenueNeeded(costs['total'], _margin)
revenue_zilnic_ron = revenue_lunar_ron / _zile if _zile > 0 else 0

mix_pct = {'apa': _mix_apa, 'suc': _mix_suc, 'dulciuri': _mix_dulciuri, 'tigari': _mix_tigari}
preturi_ron = {'apa': pret_apa_ron, 'suc': pret_suc_ron, 'dulciuri': pret_dulciuri_ron, 'tigari': pret_tigari_ron}
mix_result = calculateProductMix(revenue_zilnic_ron, valoare_cos_ron, mix_pct, preturi_ron)

clienti_zi = mix_result['clienti_zi']
produse_zi = sum(mix_result['items'].values())

owner_emp_cost = calculateEmployeeCost(costs['gross_owner'])

results_dict = {
    'revenue_lunar_ron': revenue_lunar_ron,
    'revenue_zilnic_ron': revenue_zilnic_ron,
    'clienti_zi': clienti_zi,
    'produse_zi': produse_zi,
    'total_costuri': costs['total'],
    'margin_procent': _margin,
}

# ============================================================
# Validations / Warnings
# ============================================================
st.divider()

if _margin < 15:
    st.warning(t['warning_margin_low'])
if _margin > 40:
    st.warning(t['warning_margin_high'])
if _mix_tigari > 50:
    st.warning(t['warning_tigari'])
if clienti_zi > 500:
    st.warning(t['warning_clienti'])
if _zile <= 0:
    st.error(t['error_zile'])

# ============================================================
# STEP 9 cont.: Display results
# ============================================================
st.subheader(t['results_title'])

# Summary metric cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{t['monthly_revenue']}</div>
        <div class="metric-value">{sym} {from_ron(revenue_lunar_ron):,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{t['daily_revenue']}</div>
        <div class="metric-value">{sym} {from_ron(revenue_zilnic_ron):,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{t['clients_day']}</div>
        <div class="metric-value">{clienti_zi:.0f}</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{t['items_day']}</div>
        <div class="metric-value">{produse_zi:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Breakdown columns
bd_col1, bd_col2 = st.columns(2)

with bd_col1:
    # Owner salary breakdown
    with st.expander(t['breakdown_owner'], expanded=True):
        gross_owner_ron = costs['gross_owner']
        cam_owner = gross_owner_ron * CONFIG['CAM_ANGAJATOR']
        data_owner = {
            'Element': [
                t['net'], t['cas'], t['cass'], t['tax'],
                t['gross'], t['cam'], t['employer_cost']
            ],
            f'Valoare ({sym})': [
                f"{from_ron(owner_emp_cost['net']):,.2f}",
                f"{from_ron(owner_emp_cost['cas']):,.2f}",
                f"{from_ron(owner_emp_cost['cass']):,.2f}",
                f"{from_ron(owner_emp_cost['impozit']):,.2f}",
                f"{from_ron(gross_owner_ron):,.2f}",
                f"{from_ron(cam_owner):,.2f}",
                f"{from_ron(costs['cost_owner']):,.2f}",
            ]
        }
        st.dataframe(pd.DataFrame(data_owner), hide_index=True, width='stretch')

    # Dividend breakdown
    with st.expander(t['breakdown_dividends'], expanded=True):
        div_info = costs['div_info']
        pretax = calculatePretaxProfitForDividends(div_info['brut_lunar'])
        data_div = {
            'Element': [
                t['dividends_net'],
                t['dividends_cass'],
                t['dividends_gross'],
                t['dividends_tax'],
                t['pretax_profit'],
            ],
            f'Valoare ({sym}/lună)': [
                f"{from_ron(net_dividende_ron):,.2f}",
                f"{from_ron(div_info['cass_lunar']):,.2f}",
                f"{from_ron(div_info['brut_lunar']):,.2f}",
                f"{from_ron(div_info['impozit_dividende']):,.2f}",
                f"{from_ron(pretax):,.2f}",
            ]
        }
        st.dataframe(pd.DataFrame(data_div), hide_index=True, width='stretch')

with bd_col2:
    # Employee costs breakdown
    with st.expander(t['breakdown_employees'], expanded=True):
        if _nr_angajati == 0:
            st.info("Fără angajați" if limba == 'RO' else "No employees")
        else:
            emp_rows = []
            for idx_e, sal_brut in enumerate(salarii_angajati_ron, 1):
                emp_cost = calculateEmployerCost(sal_brut)
                emp_rows.append({
                    'Angajat': f"#{idx_e}",
                    f'Brut ({sym})': f"{from_ron(sal_brut):,.0f}",
                    f'Cost angajator ({sym})': f"{from_ron(emp_cost):,.0f}",
                })
            emp_rows.append({
                'Angajat': t['total'],
                f'Brut ({sym})': '',
                f'Cost angajator ({sym})': f"{from_ron(costs['cost_angajati']):,.0f}",
            })
            st.dataframe(pd.DataFrame(emp_rows), hide_index=True, width='stretch')

    # Fixed costs breakdown
    with st.expander(t['breakdown_fixed'], expanded=True):
        fixe_items = [
            (t['chirie_teren'], chirie_teren_ron),
            (t['chirie_container'], chirie_container_ron),
            (t['contabilitate'], contabilitate_ron),
            (t['utilitati'], utilitati_ron),
            (t['combustibil'], combustibil_ron),
            (t['leasing'], leasing_ron),
            (t['alte_costuri'], alte_costuri_ron),
        ]
        fixe_rows = [{'Cost': name, f'Valoare ({sym})': f"{from_ron(v):,.0f}"} for name, v in fixe_items]
        fixe_rows.append({'Cost': t['total'], f'Valoare ({sym})': f"{from_ron(costs['costuri_fixe']):,.0f}"})
        st.dataframe(pd.DataFrame(fixe_rows), hide_index=True, width='stretch')

# Total costs summary
with st.expander(t['breakdown_total'], expanded=True):
    total_rows = [
        (t['employer_cost'] + " owner", costs['cost_owner']),
        (t['breakdown_employees'].replace('🔍 ', ''), costs['cost_angajati']),
        (t['breakdown_fixed'].replace('🔍 ', ''), costs['costuri_fixe']),
        (t['pretax_profit'] + " dividende", costs['profit_necesar_dividende']),
    ]
    total_data = {'Element': [], f'Valoare ({sym}/lună)': []}
    for name, val in total_rows:
        total_data['Element'].append(name)
        total_data[f'Valoare ({sym}/lună)'].append(f"{from_ron(val):,.2f}")
    total_data['Element'].append(f"**{t['total']}**")
    total_data[f'Valoare ({sym}/lună)'].append(f"**{from_ron(costs['total']):,.2f}**")
    st.dataframe(pd.DataFrame(total_data), hide_index=True, width='stretch')
    st.info(f"**{t['revenue_needed']} ({_margin:.0f}% {t['margin_pct']}): {sym} {from_ron(revenue_lunar_ron):,.0f}/lună**")

# Product mix daily output
with st.expander(t['product_mix_output'], expanded=True):
    pm_data = {
        'Produs': ['Apă', 'Suc', 'Dulciuri', 'Țigări'],
        'Mix (%)': [f"{v:.1f}%" for v in [_mix_apa, _mix_suc, _mix_dulciuri, _mix_tigari]],
        f'Preț ({sym})': [
            f"{from_ron(pret_apa_ron):.2f}",
            f"{from_ron(pret_suc_ron):.2f}",
            f"{from_ron(pret_dulciuri_ron):.2f}",
            f"{from_ron(pret_tigari_ron):.2f}",
        ],
        'Unități/zi': [
            f"{mix_result['items']['apa']:.0f}",
            f"{mix_result['items']['suc']:.0f}",
            f"{mix_result['items']['dulciuri']:.0f}",
            f"{mix_result['items']['tigari']:.0f}",
        ],
        f'Venit/zi ({sym})': [
            f"{from_ron(revenue_zilnic_ron * _mix_apa / 100):,.2f}",
            f"{from_ron(revenue_zilnic_ron * _mix_suc / 100):,.2f}",
            f"{from_ron(revenue_zilnic_ron * _mix_dulciuri / 100):,.2f}",
            f"{from_ron(revenue_zilnic_ron * _mix_tigari / 100):,.2f}",
        ],
    }
    st.dataframe(pd.DataFrame(pm_data), hide_index=True, width='stretch')
    st.metric(t['clients_day'], f"{clienti_zi:.0f}")

st.divider()

# Sensitivity table
with st.expander(t['sensitivity_table'], expanded=False):
    sens_rows = calculateMarginSensitivity(costs['total'], _zile)
    sens_df_data = []
    for row in sens_rows:
        net_in_hand_ron = (row['Profit ramas (RON)'] +
                           net_salariu_ron + net_dividende_ron)
        sens_df_data.append({
            t['margin_pct']: f"{row['Marja (%)']:.0f}%",
            f"{t['monthly_revenue']} ({sym})": f"{from_ron(row['Venituri lunare (RON)']):,.0f}",
            f"{t['daily_revenue']} ({sym})": f"{from_ron(row['Venituri zilnice (RON)']):,.0f}",
            f"{t['profit_remaining']} ({sym})": f"{from_ron(row['Profit ramas (RON)']):,.0f}",
        })
    st.dataframe(pd.DataFrame(sens_df_data), hide_index=True, width='stretch')

# Dividends comparison table
with st.expander(t['dividends_table'], expanded=False):
    div_scenarios = [0, 4000, 5000, 8000, 10000]
    div_rows = []
    for sc_net in div_scenarios:
        sc_info = calculateGrossDividendsNeeded(sc_net, include_cass)
        sc_pretax = calculatePretaxProfitForDividends(sc_info['brut_lunar'])
        sc_rev = calculateRevenueNeeded(
            calculateTotalCosts({**params_ron, 'net_dividende': sc_net})['total'],
            _margin
        )
        div_rows.append({
            f"Net ({sym}/lună)": f"{from_ron(sc_net):,.0f}",
            f"Anual ({sym})": f"{from_ron(sc_net * 12):,.0f}",
            f"Plafon CASS ({sym})": f"{from_ron(sc_info['cass_info']['plafon']):,.0f}",
            f"CASS lunar ({sym})": f"{from_ron(sc_info['cass_lunar']):,.2f}",
            f"Brut ({sym}/lună)": f"{from_ron(sc_info['brut_lunar']):,.2f}",
            f"Profit pre-tax ({sym}/lună)": f"{from_ron(sc_pretax):,.2f}",
            f"Venituri necesare ({sym}/lună)": f"{from_ron(sc_rev):,.0f}",
        })
    st.dataframe(pd.DataFrame(div_rows), hide_index=True, width='stretch')

# Fixed costs comparison table
with st.expander(t['fixed_costs_comparison'], expanded=False):
    fc_scenarios = [5000, 8500, 10000]
    fc_rows = []
    for sc_fixe in fc_scenarios:
        sc_total = calculateTotalCosts({**params_ron, 'chirie_teren': sc_fixe, 'chirie_container': 0,
                                        'contabilitate': 0, 'utilitati': 0, 'combustibil': 0,
                                        'leasing': 0, 'alte_costuri': 0})
        sc_rev = calculateRevenueNeeded(sc_total['total'], _margin)
        fc_rows.append({
            f"Costuri fixe ({sym}/lună)": f"{from_ron(sc_fixe):,.0f}",
            f"Total costuri ({sym}/lună)": f"{from_ron(sc_total['total']):,.0f}",
            f"Venituri necesare ({sym}/lună)": f"{from_ron(sc_rev):,.0f}",
            f"Venituri/zi ({sym})": f"{from_ron(sc_rev / _zile if _zile > 0 else 0):,.0f}",
        })
    st.dataframe(pd.DataFrame(fc_rows), hide_index=True, width='stretch')

# Download current report CSV
current_report_rows = [
    ('Venituri lunare necesare (RON)', f"{revenue_lunar_ron:,.2f}"),
    ('Venituri zilnice (RON)', f"{revenue_zilnic_ron:,.2f}"),
    ('Clienți/zi', f"{clienti_zi:.1f}"),
    ('Produse/zi', f"{produse_zi:.1f}"),
    ('Total costuri (RON)', f"{costs['total']:,.2f}"),
    ('Marja (%)', f"{_margin:.1f}"),
    ('Cost owner (RON)', f"{costs['cost_owner']:,.2f}"),
    ('Cost angajați total (RON)', f"{costs['cost_angajati']:,.2f}"),
    ('Costuri fixe total (RON)', f"{costs['costuri_fixe']:,.2f}"),
    ('Profit pre-tax dividende (RON)', f"{costs['profit_necesar_dividende']:,.2f}"),
]
csv_current = "Element,Valoare\n" + "\n".join(f'"{r[0]}","{r[1]}"' for r in current_report_rows)
st.download_button(
    t['download_current'],
    data=csv_current.encode('utf-8-sig'),
    file_name=f"raport_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv",
)

# ============================================================
# STEP 10: Save / Load versions section
# ============================================================
st.divider()
st.subheader(t['save_section'])

if st.session_state.version_saved_msg:
    st.success(t['saved_ok'])
    st.session_state.version_saved_msg = False

sv_col1, sv_col2 = st.columns([3, 1])
with sv_col1:
    version_name = st.text_input(t['version_name'], value="", key='version_name_input')
with sv_col2:
    st.write("")
    st.write("")
    if st.button(t['save_btn'], width='stretch'):
        widget_values = {}
        for key in input_defaults:
            widget_values[key] = st.session_state.get(key, input_defaults[key])

        entry = {
            'timestamp': datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            'name': version_name or f"Versiune {len(st.session_state.history) + 1}",
            'moneda': moneda,
            'curs': curs,
            'widget_values': widget_values,
            'params': params_ron,
            'results': results_dict,
        }
        st.session_state.history.append(entry)
        save_history(st.session_state.history)
        st.session_state.version_saved_msg = True
        st.rerun()

# Display saved versions
if not st.session_state.history:
    st.info(t['no_versions'])
else:
    for idx, ver in enumerate(reversed(st.session_state.history)):
        actual_idx = len(st.session_state.history) - 1 - idx
        with st.container():
            vc1, vc2, vc3, vc4 = st.columns([3, 1, 1, 1])
            with vc1:
                ver_cur = ver.get('moneda', 'RON')
                ver_rev = ver.get('results', {}).get('revenue_lunar_ron', 0)
                ver_margin = ver.get('results', {}).get('margin_procent', 0)
                ver_rev_display = ver_rev / ver.get('curs', 5.10) if ver_cur == 'EUR' else ver_rev
                st.write(f"**{ver['name']}** — {ver['timestamp']}  |  "
                         f"Venituri: {ver_cur} {ver_rev_display:,.0f}/lună  |  "
                         f"Marja: {ver_margin:.0f}%")
            with vc2:
                if st.button(t['load_btn'], key=f"load_{actual_idx}", width='stretch'):
                    st.session_state.version_to_load = ver
                    st.rerun()
            with vc3:
                # Download CSV for this version
                ver_rows = [
                    ('Versiune', ver['name']),
                    ('Data', ver['timestamp']),
                    ('Venituri lunare necesare (RON)', f"{ver.get('results', {}).get('revenue_lunar_ron', 0):,.2f}"),
                    ('Total costuri (RON)', f"{ver.get('results', {}).get('total_costuri', 0):,.2f}"),
                    ('Marja (%)', f"{ver.get('results', {}).get('margin_procent', 0):.1f}"),
                ]
                ver_params = ver.get('params', {})
                for pk, pv in ver_params.items():
                    if not isinstance(pv, list):
                        ver_rows.append((pk, str(pv)))
                csv_ver = "Element,Valoare\n" + "\n".join(f'"{r[0]}","{r[1]}"' for r in ver_rows)
                st.download_button(
                    t['download_version'],
                    data=csv_ver.encode('utf-8-sig'),
                    file_name=f"versiune_{actual_idx}_{ver['name'].replace(' ', '_')}.csv",
                    mime="text/csv",
                    key=f"dl_{actual_idx}",
                )
            with vc4:
                if st.button(t['delete_btn'], key=f"delete_{actual_idx}", width='stretch'):
                    st.session_state.history.pop(actual_idx)
                    save_history(st.session_state.history)
                    st.rerun()

    # Comparison CSV if more than 1 version
    if len(st.session_state.history) > 1:
        st.divider()
        comp_rows = []
        for ver in st.session_state.history:
            res = ver.get('results', {})
            comp_rows.append({
                'Versiune': ver['name'],
                'Data': ver['timestamp'],
                'Moneda': ver.get('moneda', 'RON'),
                'Venituri lunare (RON)': res.get('revenue_lunar_ron', 0),
                'Venituri zilnice (RON)': res.get('revenue_zilnic_ron', 0),
                'Clienti/zi': res.get('clienti_zi', 0),
                'Total costuri (RON)': res.get('total_costuri', 0),
                'Marja (%)': res.get('margin_procent', 0),
            })
        comp_df = pd.DataFrame(comp_rows)
        csv_comp = comp_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            t['download_comparison'],
            data=csv_comp.encode('utf-8-sig'),
            file_name=f"comparatie_versiuni_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

st.divider()
st.caption("Calculator Afacere v1.0 | România 2026 | Fiscal rules: SRL standard, CASS plafoane iulie 2026")
