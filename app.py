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
        'title': 'Calculator Profit Afacere 2026',
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
        'total_in_mana': 'Total în mână (lunar)',
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
        'impozit_profit': 'Impozit profit firmă (16%)',
        'pretax_profit': 'Profit pre-tax necesar firmei',
        'deductibil': 'Deductibil',
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
        'financial_statement_title': '📋 Situație Financiară Completă — Owner',
        'period_title': '📅 Calcul Total pentru O Perioadă',
        'period_type': 'Tip perioadă',
        'period_months': 'Luni',
        'period_years': 'Ani',
        'period_value': 'Număr',
        'total_earned': 'Total câstigat',
        'period_summary': 'Rezumat Perioadă',
    },
    'EN': {
        'title': 'Business Profit Calculator 2026',
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
        'total_in_mana': 'Total in hand (monthly)',
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
        'impozit_profit': 'Corporate income tax (16%)',
        'pretax_profit': 'Required pre-tax profit (company)',
        'deductibil': 'Deductible',
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
        'financial_statement_title': '📋 Complete Financial Statement — Owner',
        'period_title': '📅 Calculate Total for a Period',
        'period_type': 'Period type',
        'period_months': 'Months',
        'period_years': 'Years',
        'period_value': 'Number',
        'total_earned': 'Total earned',
        'period_summary': 'Period Summary',
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


def calculateDividendCASS(dividende_brute_anuale_ron, include_cass):
    """Selectează plafonul CASS pe baza dividendelor BRUTE anuale (venitul realizat)."""
    if not include_cass or dividende_brute_anuale_ron <= 0:
        return {'plafon': 0, 'cass_anual': 0, 'cass_lunar': 0}

    if dividende_brute_anuale_ron <= CONFIG['CASS_PLAFON_6SAL']:
        plafon = CONFIG['CASS_PLAFON_6SAL']
    elif dividende_brute_anuale_ron <= CONFIG['CASS_PLAFON_12SAL']:
        plafon = CONFIG['CASS_PLAFON_12SAL']
    else:
        plafon = CONFIG['CASS_PLAFON_24SAL']

    cass_anual = plafon * CONFIG['COTA_CASS_DIVIDENDE']
    return {'plafon': plafon, 'cass_anual': cass_anual, 'cass_lunar': cass_anual / 12}


def calculateGrossDividendsNeeded(net_dividende_lunar_ron, include_cass):
    # Iterative: estimate gross, determine CASS threshold from gross, recalculate.
    # First pass: estimate gross without CASS to get approximate brut for threshold selection
    brut_estimat = net_dividende_lunar_ron / (1 - CONFIG['COTA_IMPOZIT_DIVIDENDE'])
    cass_info = calculateDividendCASS(brut_estimat * 12, include_cass)
    # Second pass: recalculate gross including the correct CASS
    brut = (net_dividende_lunar_ron + cass_info['cass_lunar']) / (1 - CONFIG['COTA_IMPOZIT_DIVIDENDE'])
    # Re-check threshold with final gross (may shift plafon)
    cass_info = calculateDividendCASS(brut * 12, include_cass)
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


def calculateMarginSensitivity(total_costs_ron, zile_lucratoare, current_margin, marje=None):
    if marje is None:
        marje = [20, 22, 25, 28, 30]
    # Fix: use fixed revenue (from current margin) so "profit ramas" shows
    # how much MORE or LESS profit each alternative margin would yield.
    rev_fixed = calculateRevenueNeeded(total_costs_ron, current_margin)
    rows = []
    for m in marje:
        rev_breakeven = calculateRevenueNeeded(total_costs_ron, m)
        rev_zilnic = rev_breakeven / zile_lucratoare if zile_lucratoare > 0 else 0
        # Profit remaining if you hit the SAME revenue but at margin m
        profit_ramas = rev_fixed * (m / 100) - total_costs_ron
        rows.append({
            'Marja (%)': m,
            'Venituri lunare (RON)': round(rev_breakeven, 0),
            'Venituri zilnice (RON)': round(rev_zilnic, 0),
            'Profit ramas (RON)': round(profit_ramas, 0),
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
# Note: 'moneda', 'curs', 'include_cass', 'limba' are widget-bound — not included here
input_defaults = {
    'net_salariu': 0.0,
    'net_dividende': 6500.0,
    'nr_angajati': 1,
    'salariu_angajat_1': float(CONFIG['SALARIU_MINIM_BRUT']),
    'chirie_teren': 4000.0,
    'chirie_locatie': 3000.0,
    'contabilitate': 500.0,
    'utilitati': 1000.0,
    'combustibil': 400.0,
    'leasing': 1500.0,
    'alte_costuri': 500.0,
    'margin_procent': 25,
    'zile_lucratoare': 22,
    'valoare_cos': 20.0,
    'pret_apa': 3.59,
    'pret_suc': 6.19,
    'pret_dulciuri': 5.49,
    'pret_tigari': 0.0,
    'mix_apa': 35.0,
    'mix_suc': 35.0,
    'mix_dulciuri': 30.0,
    'mix_tigari': 0.0,
}

# Add per-employee defaults for up to 10 employees
for i in range(2, 11):
    input_defaults[f'salariu_angajat_{i}'] = float(CONFIG['SALARIU_MINIM_BRUT'])

# Define monetary keys early — needed for conversion BEFORE widget init loop
_MONETARY_KEYS = [
    'net_salariu', 'net_dividende', 'valoare_cos',
    'chirie_teren', 'chirie_container', 'contabilitate',
    'utilitati', 'combustibil', 'leasing', 'alte_costuri',
    'pret_apa', 'pret_suc', 'pret_dulciuri', 'pret_tigari',
] + [f'salariu_angajat_{i}' for i in range(1, 11)]

if 'curs' not in st.session_state:
    st.session_state.curs = CONFIG['CURS_EUR_RON_DEFAULT']

if 'moneda' not in st.session_state:
    st.session_state['moneda'] = 'RON'

if '_prev_moneda' not in st.session_state:
    st.session_state['_prev_moneda'] = st.session_state.get('moneda', 'RON')

# Perform currency conversion HERE — before the widget init loop and WITHOUT
# st.rerun(). Using st.rerun() from STEP 7b (after sidebar, before main widgets)
# causes Streamlit to clean up session_state keys for unrendered widget-bound
# keys (e.g. 'zile_lucratoare'), resetting them to defaults on the next run.
_curr_moneda = st.session_state.get('moneda', 'RON')
_prev_moneda_chk = st.session_state.get('_prev_moneda', _curr_moneda)
if _prev_moneda_chk != _curr_moneda:
    _rate = st.session_state.curs
    if _curr_moneda == 'EUR':  # RON → EUR: divide
        for _k in _MONETARY_KEYS:
            if _k in st.session_state:
                st.session_state[_k] = round(st.session_state[_k] / _rate, 4)
    else:  # EUR → RON: multiply
        for _k in _MONETARY_KEYS:
            if _k in st.session_state:
                st.session_state[_k] = round(st.session_state[_k] * _rate, 4)
    st.session_state['_prev_moneda'] = _curr_moneda
st.session_state['_prev_moneda'] = _curr_moneda

# Initialize input fields; monetary keys already have converted values if applicable
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

if 'period_type' not in st.session_state:
    st.session_state.period_type = 'months'

if 'period_value' not in st.session_state:
    st.session_state.period_value = 12

if '_reset_pending' not in st.session_state:
    st.session_state['_reset_pending'] = False

# Process pending reset BEFORE any widgets are instantiated
if st.session_state['_reset_pending']:
    # Reset all input fields to defaults
    for key, val in input_defaults.items():
        st.session_state[key] = val
    # Also reset employee salaries
    for i in range(1, 11):
        key = f'salariu_angajat_{i}'
        if key in input_defaults:
            st.session_state[key] = input_defaults[key]
    st.session_state.curs = CONFIG['CURS_EUR_RON_DEFAULT']
    st.session_state['_prev_moneda'] = 'RON'
    st.session_state.moneda = 'RON'
    st.session_state['_reset_pending'] = False
    # No st.rerun() here — reset block runs before all widgets, so the script
    # continues and every widget renders immediately with the new session_state values.

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
    # Sync _prev_moneda so currency detection doesn't fire a spurious conversion
    st.session_state['_prev_moneda'] = st.session_state.moneda


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
    sym = "RON" if st.session_state.moneda == "RON" else "€"

    if moneda == "EUR":
        curs_input = st.number_input(
            t['eur_rate'],
            min_value=1.0,
            max_value=20.0,
            step=0.01,
            format="%.2f",
            value=st.session_state.curs,
            key='curs'
        )
    else:
        # Do NOT overwrite curs here — preserve it for correct round-trip conversion
        st.caption(f"{t['eur_rate']}: 1 EUR = {st.session_state.curs:.2f} RON")

    st.divider()

    include_cass = st.toggle(t['include_cass'], key='include_cass')

    st.divider()

    if st.button(t['reset_btn'], width='stretch'):
        st.session_state['_reset_pending'] = True
        st.rerun()

    if st.button(t['load_example_btn'], width='stretch'):
        st.session_state.version_to_load = {
            'widget_values': input_defaults.copy(),
            'moneda': 'RON',
            'curs': CONFIG['CURS_EUR_RON_DEFAULT'],
        }
        st.session_state['_prev_moneda'] = 'RON'
        st.rerun()

# Currency conversion is now handled in STEP 5, before widget init.
# _prev_moneda is already synchronized there — nothing to do here.

# ============================================================
# HELPER: conversion functions
# ============================================================

def to_ron(val):
    return val * st.session_state.curs if st.session_state.moneda == "EUR" else val


def from_ron(val):
    return val / st.session_state.curs if st.session_state.moneda == "EUR" else val

# ============================================================
# STEP 8: Main content — Input widgets
# ============================================================
st.title(t['title'])
st.caption(t['subtitle'])

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # --- A. Owner ---
    with st.expander(t['owner_section'], expanded=True):
        net_sal_label = f"{t['net_salary']} ({sym}/lună)" if st.session_state.moneda == "RON" else f"{t['net_salary']} ({sym}/month)"
        net_salariu_disp = st.number_input(
            net_sal_label,
            min_value=0.0,
            step=100.0,
            format="%.2f",
            key='net_salariu'
        )
        net_div_label = f"{t['net_dividends']} ({sym}/lună)" if st.session_state.moneda == "RON" else f"{t['net_dividends']} ({sym}/month)"
        net_dividende_disp = st.number_input(
            net_div_label,
            min_value=0.0,
            step=100.0,
            format="%.2f",
            key='net_dividende'
        )
        # Display total in mana (in hand)
        total_in_mana_disp = net_salariu_disp + net_dividende_disp
        st.divider()
        st.metric(
            label=t['total_in_mana'],
            value=f"{sym} {total_in_mana_disp:,.2f}"
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
            _min_wage_disp = from_ron(CONFIG['SALARIU_MINIM_BRUT'])
            if wage_key not in st.session_state:
                st.session_state[wage_key] = _min_wage_disp

            use_min = st.checkbox(
                f"{t['use_min_wage']} — Angajat {i}",
                value=(abs(st.session_state[wage_key] - _min_wage_disp) < 1.0),
                key=f'use_min_{i}'
            )
            if use_min:
                st.session_state[wage_key] = _min_wage_disp
                st.caption(f"Angajat {i}: {sym} {_min_wage_disp:.2f} brut")
                salarii_angajati_disp.append(to_ron(_min_wage_disp))
            else:
                sal = st.number_input(
                    f"{t['employee_gross']} {i} ({sym})",
                    min_value=_min_wage_disp,
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
    'include_cass': bool(st.session_state.get('include_cass', True)),
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

# Calculate total in mana
total_in_mana_ron = net_salariu_ron + net_dividende_ron

# Summary metric cards (with total in mana as first/primary)
c0, c1, c2, c3, c4 = st.columns(5)
with c0:
    st.markdown(f"""
    <div class="metric-card" style="border: 3px solid #1f77b4; background-color: #f0f8ff;">
        <div class="metric-label" style="color: #1f77b4; font-weight: bold;">{t['total_in_mana']}</div>
        <div class="metric-value" style="color: #1f77b4; font-size: 1.4em;">{sym} {from_ron(total_in_mana_ron):,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
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

# ============================================================
# Full Financial Statement (P&L waterfall for owner)
# ============================================================
with st.expander(t['financial_statement_title'], expanded=True):
    _fs         = costs['div_info']
    _pretax     = costs['profit_necesar_dividende']
    _imp_profit = _pretax * CONFIG['COTA_IMPOZIT_PROFIT']
    _div_brut   = _fs['brut_lunar']
    _imp_div    = _fs['impozit_dividende']
    _cass_div   = _fs['cass_lunar']
    _cogs       = revenue_lunar_ron * (1.0 - _margin / 100.0)
    _gross_p    = revenue_lunar_ron - _cogs
    _cam_own    = costs['gross_owner'] * CONFIG['CAM_ANGAJATOR']

    def _fv(ron): return f"{sym}&nbsp;{from_ron(abs(ron)):,.0f}"
    def _fp(ron): return f"{ron / revenue_lunar_ron * 100:.1f}%" if revenue_lunar_ron > 0 else ""

    _r = (limba == 'RO')

    # Pre-compute all translated labels (avoids backslash in f-string expressions)
    _L = {
        'col_elem'  : 'Element'                               if _r else 'Item',
        'col_luna'  : f"{sym}/lun\u0103"                      if _r else f"{sym}/month",
        'col_pct'   : '%\u00a0Ven.'                           if _r else '%\u00a0Rev.',
        'col_nota'  : 'Not\u0103'                             if _r else 'Note',
        's_venit'   : '\U0001f4b0 VENITURI'                   if _r else '\U0001f4b0 REVENUE',
        'rev_brut'  : 'Venituri lunare brute'                 if _r else 'Monthly gross revenue',
        'cogs'      : '\u00a0\u00a0\u2212 Cost marf\u0103\u00a0/\u00a0achizi\u021bie (COGS)'
                                                              if _r else '\u00a0\u00a0\u2212 Cost of goods (COGS)',
        'cogs_nt'   : f"la marj\u0103 {_margin:.0f}%"        if _r else f"at margin {_margin:.0f}%",
        'gp'        : '= Profit brut comercial'               if _r else '= Gross commercial profit',
        's_ded'     : '\U0001f50d CHELTUIELI DEDUCTIBILE FIRM\u0102'
                                                              if _r else '\U0001f50d DEDUCTIBLE BUSINESS EXPENSES',
        'co_lbl'    : '\u00a0\u00a0\u2212 Cost angajator Owner'
                                                              if _r else '\u00a0\u00a0\u2212 Owner employer cost',
        'co_sub'    : f"(brut {_fv(costs['gross_owner'])} + CAM {_fv(_cam_own)})",
        'co_nt'     : '\u2705 deductibil\u00a0100%'           if _r else '\u2705 100%\u00a0deductible',
        'ca_lbl'    : '\u00a0\u00a0\u2212 Cost angajatori angaja\u021bi'
                                                              if _r else '\u00a0\u00a0\u2212 Employee employer costs',
        'ca_nt'     : '\u2705 deductibil\u00a0100%'           if _r else '\u2705 100%\u00a0deductible',
        'cf_lbl'    : '\u00a0\u00a0\u2212 Costuri fixe totale' if _r else '\u00a0\u00a0\u2212 Total fixed costs',
        'cf_nt'     : '\u2705 deductibil\u00a0~100%'          if _r else '\u2705 ~100%\u00a0deductible',
        'pi'        : '= Profit impozabil'                    if _r else '= Taxable profit',
        's_tax'     : '\U0001f3db IMPOZIT PE PROFIT (firm\u0103)'
                                                              if _r else '\U0001f3db CORPORATE INCOME TAX',
        'ip_lbl'    : '\u00a0\u00a0\u2212 Impozit pe profit (16%)'
                                                              if _r else '\u00a0\u00a0\u2212 Corporate income tax (16%)',
        'ip_nt'     : 'D100 trimestrial'                      if _r else 'D100 quarterly',
        'db_lbl'    : '= Dividende brute (profit net firm\u0103)'
                                                              if _r else '= Gross dividends (company net profit)',
        'db_nt'     : 'distribuite c\u0103tre owner'          if _r else 'distributed to owner',
        's_div'     : '\U0001f4b8 IMPOZITE PE DIVIDENDE (owner)'
                                                              if _r else '\U0001f4b8 DIVIDEND TAXES (owner)',
        'idiv_lbl'  : '\u00a0\u00a0\u2212 Impozit dividende (16%)'
                                                              if _r else '\u00a0\u00a0\u2212 Dividend tax (16%)',
        'cass_lbl'  : '\u00a0\u00a0\u2212 CASS dividende'    if _r else '\u00a0\u00a0\u2212 CASS on dividends',
        'cass_nt'   : (f"plafon {sym}\u00a0{from_ron(_fs['cass_info']['plafon']):,.0f}/an"
                       if _cass_div > 0 else '\u2014')        if _r
                      else (f"ceiling {sym}\u00a0{from_ron(_fs['cass_info']['plafon']):,.0f}/yr"
                            if _cass_div > 0 else '\u2014'),
        'dn_lbl'    : '= Dividende nete \xeen m\xe2n\u0103'  if _r else '= Net dividends in hand',
        's_sal'     : '\U0001f464 SALARIU OWNER \u2014 re\u021binute din brut'
                                                              if _r else '\U0001f464 OWNER SALARY \u2014 withholdings',
        'gb_lbl'    : '\u00a0\u00a0Salariu brut'             if _r else '\u00a0\u00a0Gross salary',
        'gb_nt'     : 'baz\u0103 calcul'                     if _r else 'calculation base',
        'cas_lbl'   : '\u00a0\u00a0\u00a0\u00a0\u2212 CAS angajat (25%)'
                                                              if _r else '\u00a0\u00a0\u00a0\u00a0\u2212 Employee CAS (25%)',
        'cas_nt'    : 're\u021binut din brut'                 if _r else 'withheld from gross',
        'cass2_lbl' : '\u00a0\u00a0\u00a0\u00a0\u2212 CASS angajat (10%)'
                                                              if _r else '\u00a0\u00a0\u00a0\u00a0\u2212 Employee CASS (10%)',
        'iv_lbl'    : '\u00a0\u00a0\u00a0\u00a0\u2212 Impozit venit (10%)'
                                                              if _r else '\u00a0\u00a0\u00a0\u00a0\u2212 Income tax (10%)',
        'sn_lbl'    : '= Salariu net'                        if _r else '= Net salary',
        'tot_lbl'   : '\u2705 TOTAL NET \xcen M\xc2N\u0102 / LUN\u0102'
                                                              if _r else '\u2705 TOTAL NET IN HAND / MONTH',
        'tot_nt'    : 'salariu net + dividende nete'         if _r else 'net salary + net dividends',
    }

    _row_angajati = ""
    if costs['cost_angajati'] > 0:
        _row_angajati = (
            f"<tr>"
            f"<td>{_L['ca_lbl']}</td>"
            f"<td class='fst-val fst-neg'>&#8722;{_fv(costs['cost_angajati'])}</td>"
            f"<td class='fst-pct'>{_fp(costs['cost_angajati'])}</td>"
            f"<td class='fst-nt'>{_L['ca_nt']}</td>"
            f"</tr>"
        )

    _css = """<style>
.fst{width:100%;border-collapse:collapse;font-size:.88rem;}
.fst td{padding:5px 10px;border-bottom:1px solid rgba(128,128,128,.12);vertical-align:middle;}
.fst-sec td{background:#1e3a5f;color:#e8f4fd;font-weight:700;padding:7px 10px;letter-spacing:.04em;}
.fst-sub td{background:#0d3b27;color:#52b788;font-weight:700;border-top:1.5px solid #52b788;padding:6px 10px;}
.fst-tot td{background:#1a3d1a;color:#ffd700;font-weight:700;font-size:1rem;border-top:3px solid #ffd700;padding:8px 10px;}
.fst-neg{color:#ff7b72;}
.fst-pos{color:#56d364;}
.fst-val{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums;}
.fst-pct{text-align:right;color:#8b949e;font-size:.8rem;white-space:nowrap;}
.fst-nt{color:#8b949e;font-size:.8rem;}
.fst th{background:#152a3e;color:#b7e4c7;text-align:right;padding:7px 10px;font-weight:600;}
.fst th:first-child{text-align:left;}
</style>"""

    _thead = (
        f"<table class='fst'><thead><tr>"
        f"<th style='text-align:left;min-width:240px;'>{_L['col_elem']}</th>"
        f"<th>{_L['col_luna']}</th>"
        f"<th>{_L['col_pct']}</th>"
        f"<th style='text-align:left;'>{_L['col_nota']}</th>"
        f"</tr></thead><tbody>"
    )

    _rows = (
        # ── REVENUE ─────────────────────────────────────────────────────
        f"<tr class='fst-sec'><td colspan='4'>{_L['s_venit']}</td></tr>"
        f"<tr><td>{_L['rev_brut']}</td>"
        f"<td class='fst-val fst-pos'>+{_fv(revenue_lunar_ron)}</td>"
        f"<td class='fst-pct'>100.0%</td><td class='fst-nt'>&mdash;</td></tr>"
        f"<tr><td>{_L['cogs']}</td>"
        f"<td class='fst-val fst-neg'>&#8722;{_fv(_cogs)}</td>"
        f"<td class='fst-pct'>{_fp(_cogs)}</td>"
        f"<td class='fst-nt'>{_L['cogs_nt']}</td></tr>"
        f"<tr class='fst-sub'><td>{_L['gp']}</td>"
        f"<td class='fst-val'>{_fv(_gross_p)}</td>"
        f"<td class='fst-pct'>{_fp(_gross_p)}</td><td></td></tr>"
        # ── DEDUCTIBLE COSTS ────────────────────────────────────────────
        f"<tr class='fst-sec'><td colspan='4'>{_L['s_ded']}</td></tr>"
        f"<tr><td>{_L['co_lbl']}&nbsp;<span style='color:#8b949e;font-size:.8rem;'>{_L['co_sub']}</span></td>"
        f"<td class='fst-val fst-neg'>&#8722;{_fv(costs['cost_owner'])}</td>"
        f"<td class='fst-pct'>{_fp(costs['cost_owner'])}</td>"
        f"<td class='fst-nt'>{_L['co_nt']}</td></tr>"
        f"{_row_angajati}"
        f"<tr><td>{_L['cf_lbl']}</td>"
        f"<td class='fst-val fst-neg'>&#8722;{_fv(costs['costuri_fixe'])}</td>"
        f"<td class='fst-pct'>{_fp(costs['costuri_fixe'])}</td>"
        f"<td class='fst-nt'>{_L['cf_nt']}</td></tr>"
        f"<tr class='fst-sub'><td>{_L['pi']}</td>"
        f"<td class='fst-val'>{_fv(_pretax)}</td>"
        f"<td class='fst-pct'>{_fp(_pretax)}</td><td></td></tr>"
        # ── CORPORATE TAX ───────────────────────────────────────────────
        f"<tr class='fst-sec'><td colspan='4'>{_L['s_tax']}</td></tr>"
        f"<tr><td>{_L['ip_lbl']}</td>"
        f"<td class='fst-val fst-neg'>&#8722;{_fv(_imp_profit)}</td>"
        f"<td class='fst-pct'>{_fp(_imp_profit)}</td>"
        f"<td class='fst-nt'>{_L['ip_nt']}</td></tr>"
        f"<tr class='fst-sub'><td>{_L['db_lbl']}</td>"
        f"<td class='fst-val'>{_fv(_div_brut)}</td>"
        f"<td class='fst-pct'>{_fp(_div_brut)}</td>"
        f"<td class='fst-nt'>{_L['db_nt']}</td></tr>"
        # ── DIVIDEND TAXES ──────────────────────────────────────────────
        f"<tr class='fst-sec'><td colspan='4'>{_L['s_div']}</td></tr>"
        f"<tr><td>{_L['idiv_lbl']}</td>"
        f"<td class='fst-val fst-neg'>&#8722;{_fv(_imp_div)}</td>"
        f"<td class='fst-pct'>{_fp(_imp_div)}</td><td></td></tr>"
        f"<tr><td>{_L['cass_lbl']}</td>"
        f"<td class='fst-val fst-neg'>&#8722;{_fv(_cass_div)}</td>"
        f"<td class='fst-pct'>{_fp(_cass_div)}</td>"
        f"<td class='fst-nt'>{_L['cass_nt']}</td></tr>"
        f"<tr class='fst-sub'><td>{_L['dn_lbl']}</td>"
        f"<td class='fst-val'>{_fv(net_dividende_ron)}</td>"
        f"<td class='fst-pct'>{_fp(net_dividende_ron)}</td><td></td></tr>"
        # ── OWNER SALARY ────────────────────────────────────────────────
        f"<tr class='fst-sec'><td colspan='4'>{_L['s_sal']}</td></tr>"
        f"<tr><td>{_L['gb_lbl']}</td>"
        f"<td class='fst-val'>{_fv(costs['gross_owner'])}</td>"
        f"<td class='fst-pct'>{_fp(costs['gross_owner'])}</td>"
        f"<td class='fst-nt'>{_L['gb_nt']}</td></tr>"
        f"<tr><td>{_L['cas_lbl']}</td>"
        f"<td class='fst-val fst-neg'>&#8722;{_fv(owner_emp_cost['cas'])}</td>"
        f"<td class='fst-pct'>{_fp(owner_emp_cost['cas'])}</td>"
        f"<td class='fst-nt'>{_L['cas_nt']}</td></tr>"
        f"<tr><td>{_L['cass2_lbl']}</td>"
        f"<td class='fst-val fst-neg'>&#8722;{_fv(owner_emp_cost['cass'])}</td>"
        f"<td class='fst-pct'>{_fp(owner_emp_cost['cass'])}</td>"
        f"<td class='fst-nt'>{_L['cas_nt']}</td></tr>"
        f"<tr><td>{_L['iv_lbl']}</td>"
        f"<td class='fst-val fst-neg'>&#8722;{_fv(owner_emp_cost['impozit'])}</td>"
        f"<td class='fst-pct'>{_fp(owner_emp_cost['impozit'])}</td>"
        f"<td class='fst-nt'>{_L['cas_nt']}</td></tr>"
        f"<tr class='fst-sub'><td>{_L['sn_lbl']}</td>"
        f"<td class='fst-val'>{_fv(net_salariu_ron)}</td>"
        f"<td class='fst-pct'>{_fp(net_salariu_ron)}</td><td></td></tr>"
        # ── TOTAL ────────────────────────────────────────────────────────
        f"<tr class='fst-tot'><td>{_L['tot_lbl']}</td>"
        f"<td class='fst-val'>{_fv(total_in_mana_ron)}</td>"
        f"<td class='fst-pct'>{_fp(total_in_mana_ron)}</td>"
        f"<td class='fst-nt'>{_L['tot_nt']}</td></tr>"
    )

    st.markdown(_css + _thead + _rows + "</tbody></table>", unsafe_allow_html=True)


# ============================================================
# Period calculation section
# ============================================================
with st.expander(t['period_title'], expanded=False):
    period_col1, period_col2 = st.columns([2, 2])
    
    with period_col1:
        period_type = st.radio(
            t['period_type'],
            options=['months', 'years'],
            format_func=lambda x: t['period_months'] if x == 'months' else t['period_years'],
            horizontal=True,
            key='period_type'
        )
    
    with period_col2:
        max_val = 60 if period_type == 'months' else 5
        period_value = st.number_input(
            t['period_value'],
            min_value=1,
            max_value=max_val,
            step=1,
            key='period_value'
        )
    
    # Calculate total months
    total_months = period_value if period_type == 'months' else period_value * 12
    
    # Calculate net income for the period (what you keep in hand)
    total_net_salary_period = net_salariu_ron * total_months
    total_net_dividends_period = net_dividende_ron * total_months
    total_net_in_hand = total_net_salary_period + total_net_dividends_period
    
    # Display period summary
    st.divider()
    per_c1, per_c2, per_c3 = st.columns(3)
    
    with per_c1:
        st.metric(
            f"👤 {('Salariu net' if limba == 'RO' else 'Net Salary')}",
            f"{sym} {from_ron(total_net_salary_period):,.0f}",
            f"{total_months} {'luni' if limba == 'RO' else 'months'}"
        )
    
    with per_c2:
        st.metric(
            f"💰 {('Dividende net' if limba == 'RO' else 'Net Dividends')}",
            f"{sym} {from_ron(total_net_dividends_period):,.0f}",
            f"{total_months} {'luni' if limba == 'RO' else 'months'}"
        )
    
    with per_c3:
        st.metric(
            f"✅ {('Total în mână' if limba == 'RO' else 'Total in Hand')}",
            f"{sym} {from_ron(total_net_in_hand):,.0f}",
        )
    
    # Detailed breakdown table for the period
    st.subheader(t['period_summary'])
    period_data = {
        ('Salariu net/lună' if limba == 'RO' else 'Net salary/month'): f"{sym} {from_ron(net_salariu_ron):,.0f}",
        ('Dividende net/lună' if limba == 'RO' else 'Net dividends/month'): f"{sym} {from_ron(net_dividende_ron):,.0f}",
        ('Perioada (luni)' if limba == 'RO' else 'Period (months)'): f"{total_months}",
        ('Salariu total' if limba == 'RO' else 'Total salary'): f"{sym} {from_ron(total_net_salary_period):,.0f}",
        ('Dividende total' if limba == 'RO' else 'Total dividends'): f"{sym} {from_ron(total_net_dividends_period):,.0f}",
        ('Total în mână' if limba == 'RO' else 'Total in hand'): f"**{sym} {from_ron(total_net_in_hand):,.0f}**",
    }
    period_df = pd.DataFrame(list(period_data.items()), columns=['Parametru' if limba == 'RO' else 'Parameter', 'Valoare' if limba == 'RO' else 'Value'])
    st.dataframe(period_df, hide_index=True, width='stretch')

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
        impozit_profit_ron = pretax - div_info['brut_lunar']
        data_div = {
            'Element': [
                t['dividends_net'],
                t['dividends_cass'],
                t['dividends_tax'],
                t['dividends_gross'],
                t['impozit_profit'],
                t['pretax_profit'],
            ],
            f'Valoare ({sym}/lună)': [
                f"{from_ron(net_dividende_ron):,.2f}",
                f"{from_ron(div_info['cass_lunar']):,.2f}",
                f"{from_ron(div_info['impozit_dividende']):,.2f}",
                f"{from_ron(div_info['brut_lunar']):,.2f}",
                f"{from_ron(impozit_profit_ron):,.2f}",
                f"{from_ron(pretax):,.2f}",
            ]
        }
        st.dataframe(pd.DataFrame(data_div), hide_index=True, width='stretch')
        if limba == 'RO':
            st.caption("📌 Flux: Net dorit + CASS + Impozit div. = **Dividende brute** → ÷ 0,84 = **Profit pre-tax** (din care 16% impozit pe profit se plătește trimestrial prin D100)")
        else:
            st.caption("📌 Flow: Desired net + CASS + Div. tax = **Gross dividends** → ÷ 0.84 = **Pre-tax profit** (16% corporate tax paid quarterly via D100)")

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
        _ded_partial = '⚠️ parțial' if limba == 'RO' else '⚠️ partial'
        fixe_items = [
            (t['chirie_teren'],     chirie_teren_ron,     '✅ 100%'),
            (t['chirie_container'], chirie_container_ron, '✅ 100%'),
            (t['contabilitate'],    contabilitate_ron,    '✅ 100%'),
            (t['utilitati'],        utilitati_ron,        '✅ 100%'),
            (t['combustibil'],      combustibil_ron,      '✅ 100% (documente)'),
            (t['leasing'],          leasing_ron,          '✅ 100%'),
            (t['alte_costuri'],     alte_costuri_ron,     _ded_partial),
        ]
        fixe_rows = [
            {'Cost': name, f'Valoare ({sym})': f"{from_ron(v):,.0f}", t['deductibil']: ded}
            for name, v, ded in fixe_items
        ]
        fixe_rows.append({'Cost': t['total'], f'Valoare ({sym})': f"{from_ron(costs['costuri_fixe']):,.0f}", t['deductibil']: ''})
        st.dataframe(pd.DataFrame(fixe_rows), hide_index=True, width='stretch')

# Total costs summary
with st.expander(t['breakdown_total'], expanded=True):
    _pretax_label = t['pretax_profit'] if 'pretax_profit' in t else 'Profit pre-tax'
    total_rows = [
        (f"✅ {t['employer_cost']} owner", costs['cost_owner']),
        (f"✅ {t['breakdown_employees'].replace('🔍 ', '')}", costs['cost_angajati']),
        (f"✅ {t['breakdown_fixed'].replace('🔍 ', '')}", costs['costuri_fixe']),
        (f"📊 {_pretax_label}", costs['profit_necesar_dividende']),
    ]
    total_data = {'Element': [], f'Valoare ({sym}/lună)': []}
    for name, val in total_rows:
        total_data['Element'].append(name)
        total_data[f'Valoare ({sym}/lună)'].append(f"{from_ron(val):,.2f}")
    total_data['Element'].append(f"**{t['total']}**")
    total_data[f'Valoare ({sym}/lună)'].append(f"**{from_ron(costs['total']):,.2f}**")
    st.dataframe(pd.DataFrame(total_data), hide_index=True, width='stretch')
    if limba == 'RO':
        st.caption("✅ = cheltuieli deductibile fiscal | 📊 = profit pre-tax (include impozit firmă 16% + dividende — nedeductibil)")
    else:
        st.caption("✅ = tax-deductible costs | 📊 = pre-tax profit (includes 16% corporate tax + dividends — not deductible)")
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
    sens_rows = calculateMarginSensitivity(costs['total'], _zile, _margin)
    sens_df_data = []
    for row in sens_rows:
        net_in_hand_ron = (row['Profit ramas (RON)'] +
                           net_salariu_ron + net_dividende_ron)
        sens_df_data.append({
            t['margin_pct']: f"{row['Marja (%)']:.0f}%",
            f"{t['monthly_revenue']} ({sym})": f"{from_ron(row['Venituri lunare (RON)']):,.0f}",
            f"{t['daily_revenue']} ({sym})": f"{from_ron(row['Venituri zilnice (RON)']):,.0f}",
            f"{t['profit_remaining']} ({sym})": f"{from_ron(row['Profit ramas (RON)']):,.0f}",
            f"{t['net_in_hand']} ({sym})": f"{from_ron(net_in_hand_ron):,.0f}",
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
    (f'Venituri lunare necesare ({sym})', f"{from_ron(revenue_lunar_ron):,.2f}"),
    (f'Venituri zilnice ({sym})', f"{from_ron(revenue_zilnic_ron):,.2f}"),
    ('Clienți/zi', f"{clienti_zi:.1f}"),
    ('Produse/zi', f"{produse_zi:.1f}"),
    (f'Total costuri ({sym})', f"{from_ron(costs['total']):,.2f}"),
    ('Marja (%)', f"{_margin:.1f}"),
    (f'Cost owner ({sym})', f"{from_ron(costs['cost_owner']):,.2f}"),
    (f'Cost angajați total ({sym})', f"{from_ron(costs['cost_angajati']):,.2f}"),
    (f'Costuri fixe total ({sym})', f"{from_ron(costs['costuri_fixe']):,.2f}"),
    (f'Profit pre-tax dividende ({sym})', f"{from_ron(costs['profit_necesar_dividende']):,.2f}"),
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
            'curs': st.session_state.curs,
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
                    (f'Venituri lunare necesare ({sym})', f"{from_ron(ver.get('results', {}).get('revenue_lunar_ron', 0)):,.2f}"),
                    (f'Total costuri ({sym})', f"{from_ron(ver.get('results', {}).get('total_costuri', 0)):,.2f}"),
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


# ============================================================
# BONUS: Container Analysis Feature
# ============================================================
st.divider()

with st.expander("📦 **Analiză Cost-Beneficiu Container** — Merită container mai mare?", expanded=False):
    st.markdown("""
Calculează dacă upgradul la container mai mare decurează:
- **Cost săptămânal/lunar** pentru deplasări la aprovizionare
- **Discount compărături** en-gros
- **Creștere coș mediu** datorită mai multor produse
""")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### Scenariu A — Container Curent")
        suprafata_a = st.number_input("Suprafață (m²)", min_value=5, max_value=100, value=20, step=1, key='sup_a')
        deplasari_a = st.number_input("Deplasări/lună", min_value=1, max_value=30, value=12, step=1, key='depl_a')
        ore_per = st.number_input("Ore/deplasare", min_value=0.5, max_value=10.0, value=3.0, step=0.5, key='ore')
        cost_ora_default = net_salariu_ron / (_zile * 8) if _zile > 0 else 0
        cost_ora = st.number_input(f"Cost/oră (default: {from_ron(cost_ora_default):.0f} {sym})", min_value=0.0, value=from_ron(cost_ora_default), step=10.0, key='costura')
    
    with col_b:
        st.markdown("#### Scenariu B — Container Nou (Mai Mare)")
        suprafata_b = st.number_input("Suprafață nouă (m²)", min_value=5, max_value=100, value=40, step=1, key='sup_b')
        deplasari_b = st.number_input("Deplasări/lună (en-gros)", min_value=1, max_value=30, value=4, step=1, key='depl_b')
        chirie_noua = st.number_input(f"Chirie nouă ({sym}/lună)", min_value=0.0, value=from_ron(chirie_container_ron * 1.5), step=100.0, key='chir_n', format="%.0f")
        discount = st.number_input("Discount marfă (%)", min_value=0.0, max_value=30.0, value=5.0, step=0.5, key='disc')
        cos_inc = st.number_input("Creștere coș (%)", min_value=0.0, max_value=50.0, value=10.0, step=1.0, key='cos_inc')
    
    # Calculations (convert back to RON for internal calculations)
    cost_ora_ron = to_ron(cost_ora)
    cost_timp_a = ore_per * deplasari_a * cost_ora_ron
    cost_timp_b = ore_per * deplasari_b * cost_ora_ron
    
    marja_b = _margin + (discount / 100) * (1 - _margin / 100) * 100
    
    # Scenarios
    params_a = {**params_ron, 'chirie_container': chirie_container_ron}
    params_a['chirie_teren'] += cost_timp_a
    
    chirie_noua_ron = to_ron(chirie_noua)
    params_b = {**params_ron, 'chirie_container': chirie_noua_ron}
    params_b['chirie_teren'] += cost_timp_b
    
    costs_a = calculateTotalCosts(params_a)
    costs_b = calculateTotalCosts(params_b)
    
    rev_a = calculateRevenueNeeded(costs_a['total'], _margin)
    rev_b = calculateRevenueNeeded(costs_b['total'], marja_b)
    
    # Display comparison
    st.markdown("---")
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric("Venituri necesare A", f"{sym} {from_ron(rev_a):,.0f}/lună")
    with col_res2:
        st.metric("Venituri necesare B", f"{sym} {from_ron(rev_b):,.0f}/lună")
    
    delta = rev_a - rev_b
    if abs(delta) < rev_a * 0.05:
        st.info("🟡 Indiferent — diferența < 5%")
    elif delta > 0:
        st.success(f"🟢 Container nou e mai eficient — {sym} {from_ron(delta):,.0f}/lună mai puțin necesar")
    else:
        st.warning(f"🔴 Container curent e mai bun — {sym} {from_ron(abs(delta)):,.0f}/lună mai mult cu container nou")

st.divider()
st.caption("Calculator Afacere v1.0 | România 2026 | Fiscal rules: SRL standard, CASS plafoane iulie 2026")
