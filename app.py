"""
Compact mobile Kate prototype.

Visualises engine.py only. Customer figures are not written back to disk.
Completeness percentages are illustrative visual values for the demo.
"""

import json
from html import escape
from pathlib import Path

import streamlit as st

from engine import evaluate_customer


st.set_page_config(page_title="Kate", layout="centered")

st.markdown(
    """
    <style>
    header[data-testid="stHeader"],
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    #MainMenu,
    footer {
        display: none;
    }
    .stApp,
    [data-testid="stAppViewContainer"],
    section.main,
    .block-container {
        height: auto !important;
        overflow: visible !important;
    }
    .stApp {
        background: #e6e7eb;
    }
    .block-container {
        max-width: 480px;
        background: transparent;
        border: none;
        box-shadow: none;
        margin: 0.65rem auto 1.5rem auto;
        padding: 0.35rem 0.6rem 1.2rem 0.6rem;
    }
    .st-key-phone_device {
        background: #121214;
        border-radius: 48px;
        box-shadow:
            0 0 0 1px rgba(255, 255, 255, 0.22),
            0 18px 42px rgba(16, 18, 24, 0.2);
        box-sizing: border-box;
        margin: 0.35rem auto 0.4rem auto;
        max-width: 430px;
        padding: 14px 15px 16px;
        width: 430px;
    }
    .st-key-phone_screen {
        background: #f7fbfe;
        border-radius: 38px;
        box-sizing: border-box;
        padding: 2.7rem 0.72rem 0.35rem;
        position: relative;
        width: 100%;
    }
    .st-key-phone_screen::before {
        background: #050505;
        border-radius: 18px;
        content: "";
        height: 26px;
        left: 50%;
        pointer-events: none;
        position: absolute;
        top: 0.62rem;
        transform: translateX(-50%);
        width: 108px;
        z-index: 2;
    }
    .st-key-phone_screen::after {
        background: #1c1c1e;
        border-radius: 4px;
        content: "";
        display: block;
        flex: 0 0 auto;
        height: 4px;
        margin: 0.65rem auto 0.2rem;
        width: 112px;
    }
    @media (max-width: 520px) {
        .st-key-phone_device {
            border-radius: 32px;
            max-width: 100%;
            padding: 8px 8px 12px;
            width: 100%;
        }
        .st-key-phone_screen {
            border-radius: 26px;
            padding-top: 2.75rem;
        }
        .footer-note {
            white-space: normal !important;
        }
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0.65rem;
    }
    div[data-testid="stElementContainer"] {
        margin-bottom: 0.15rem;
    }
    .app-header {
        align-items: center;
        border-bottom: 1px solid #e3eef6;
        display: flex;
        justify-content: space-between;
        margin: 0 0 0.35rem 0;
        padding: 0.15rem 0.1rem 0.55rem 0.1rem;
        position: static;
    }
    .app-header .icon {
        color: #0077b6;
        flex: 0 0 1.5rem;
        font-size: 1.05rem;
        line-height: 1;
    }
    .app-header .icon.right {
        text-align: right;
    }
    .app-header .mid {
        flex: 1 1 auto;
        min-width: 0;
        text-align: center;
    }
    .app-header .name {
        color: #003865;
        display: block;
        font-size: 1.02rem;
        font-weight: 750;
        line-height: 1.2;
    }
    .app-header .sub {
        color: #8aa0b3;
        display: block;
        font-size: 0.68rem;
        line-height: 1.2;
        margin-top: 0.1rem;
    }
    .screen-title {
        color: #003865;
        font-size: 1.05rem;
        font-weight: 750;
        line-height: 1.3;
        margin: 0.15rem 0 0.45rem 0;
    }
    .msg {
        margin: 0.15rem 0 0.35rem 0;
    }
    .bubble {
        background: #e7f4fc;
        border-radius: 6px 16px 16px 16px;
        color: #16324f;
        font-size: 0.9rem;
        line-height: 1.45;
        max-width: 100%;
        overflow-wrap: anywhere;
        padding: 0.7rem 0.8rem;
    }
    .bubble p {
        margin: 0 0 0.55rem 0;
    }
    .bubble p:last-child {
        margin-bottom: 0;
    }
    .msg.user {
        text-align: right;
    }
    .user-bubble {
        background: #ffffff;
        border: 1.5px solid #00aeef;
        border-radius: 16px 16px 6px 16px;
        color: #003865;
        display: inline-block;
        font-size: 0.86rem;
        line-height: 1.35;
        max-width: 85%;
        overflow-wrap: anywhere;
        padding: 0.45rem 0.7rem;
        text-align: left;
    }
    .txn-card, .sheet, .complete-card {
        background: #ffffff;
        border: 1px solid #e3eef6;
        border-radius: 16px;
        box-shadow: 0 1px 2px rgba(0, 56, 101, 0.04);
        margin: 0.35rem 0 0.7rem 0;
        padding: 0.35rem 0.8rem 0.5rem 0.8rem;
    }
    .complete-card {
        align-items: center;
        display: flex;
        gap: 0.8rem;
        padding: 0.85rem 0.8rem;
    }
    .ring {
        background: conic-gradient(#12a36a calc(var(--pct) * 1%), #e6eef5 0);
        border-radius: 50%;
        flex: 0 0 74px;
        height: 74px;
        width: 74px;
        display: grid;
        place-items: center;
    }
    .ring span {
        align-items: center;
        background: #ffffff;
        border-radius: 50%;
        color: #003865;
        display: flex;
        font-size: 0.82rem;
        font-weight: 750;
        height: 54px;
        justify-content: center;
        width: 54px;
    }
    .complete-copy {
        flex: 1 1 auto;
        min-width: 0;
    }
    .complete-copy strong {
        color: #003865;
        display: block;
        font-size: 0.84rem;
        line-height: 1.3;
        margin-bottom: 0.25rem;
    }
    .complete-copy p {
        color: #5d7386;
        font-size: 0.75rem;
        line-height: 1.4;
        margin: 0;
    }
    .txn-row, .status-row {
        align-items: flex-start;
        border-top: 1px solid #e8f0f6;
        display: flex;
        gap: 0.65rem;
        justify-content: space-between;
        padding: 0.62rem 0;
    }
    .txn-card .txn-row:first-child,
    .sheet .group + .status-row,
    .sheet .prov-head + .prov-row {
        border-top: none;
    }
    .txn-row span, .status-label, .status-row span {
        color: #16324f;
        flex: 1 1 auto;
        font-size: 0.84rem;
        line-height: 1.35;
        min-width: 0;
        overflow-wrap: anywhere;
    }
    .txn-row strong {
        color: #003865;
        flex: 0 0 auto;
        font-size: 0.86rem;
        line-height: 1.35;
    }
    .badge {
        border-radius: 999px;
        flex: 0 1 auto;
        font-size: 0.7rem;
        line-height: 1.3;
        max-width: 48%;
        overflow-wrap: anywhere;
        padding: 0.18rem 0.5rem;
        text-align: center;
    }
    .badge.ok {
        background: #e8f8ef;
        color: #0e8a52;
    }
    .badge.warn {
        background: #fff6e5;
        color: #b26a00;
    }
    .badge.unknown {
        background: #fdeeee;
        color: #c24545;
    }
    .group {
        color: #003865;
        font-size: 0.78rem;
        font-weight: 750;
        line-height: 1.3;
        padding: 0.45rem 0 0.15rem 0;
    }
    .prov-head, .prov-row {
        align-items: start;
        column-gap: 0.55rem;
        display: grid;
        grid-template-columns: minmax(0, 1.35fr) minmax(0, 0.85fr) minmax(0, 0.95fr);
        padding: 0.45rem 0;
    }
    .prov-row {
        border-top: 1px solid #e8f0f6;
    }
    .prov-head span, .prov-row span {
        line-height: 1.35;
        min-width: 0;
        overflow-wrap: anywhere;
    }
    .prov-head span {
        color: #8aa0b3;
        font-size: 0.68rem;
        font-weight: 700;
    }
    .prov-row span {
        color: #16324f;
        font-size: 0.8rem;
    }
    .prov-row span:nth-child(2),
    .prov-row span:nth-child(3),
    .prov-head span:nth-child(2),
    .prov-head span:nth-child(3) {
        text-align: right;
    }
    .missing-list {
        margin: 0.15rem 0 0.2rem 0;
        padding: 0;
    }
    .missing-list li {
        color: #16324f;
        font-size: 0.8rem;
        line-height: 1.4;
        margin: 0.35rem 0;
        overflow-wrap: anywhere;
    }
    .note, .control-note {
        color: #5d7386;
        font-size: 0.78rem;
        line-height: 1.45;
        margin: 0.2rem 0 0.45rem 0;
        overflow-wrap: anywhere;
    }
    .footer-note {
        clear: both;
        color: #8aa0b3 !important;
        font-size: 0.68rem !important;
        font-weight: 400;
        letter-spacing: 0;
        line-height: 1.2 !important;
        margin: 0.55rem 0 0.1rem 0;
        padding-top: 0.15rem;
        position: static;
        text-align: center;
        white-space: nowrap;
    }
    div[data-testid="stExpander"] {
        background: #ffffff;
        border: 1px solid #d7dbe2;
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(20, 24, 32, 0.06);
        margin: 0 auto 0.85rem auto;
        max-width: 430px;
    }
    div[data-testid="stExpander"] details,
    div[data-testid="stExpander"] summary {
        background: #ffffff !important;
        color: #16324f !important;
    }
    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary p,
    div[data-testid="stExpander"] summary span {
        color: #16324f !important;
    }
    div[data-testid="stExpander"] details {
        background: transparent;
        border: none;
        overflow: hidden;
    }
    div[data-testid="stExpander"] details:not([open]) [data-testid="stExpanderDetails"] {
        display: none !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    div[data-testid="stNumberInput"] {
        margin-bottom: 0.15rem;
    }
    div[data-testid="stNumberInput"] label p {
        font-size: 0.78rem;
        line-height: 1.3;
        white-space: normal;
    }
    div[data-testid="stColumn"] {
        flex: 1 1 0px !important;
        min-width: 0 !important;
        width: auto !important;
    }
    button[data-testid="stBaseButton-secondary"],
    button[data-testid="stBaseButton-primary"] {
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 650;
        height: auto !important;
        line-height: 1.25;
        min-height: 2.35rem;
        padding: 0.35rem 0.7rem;
        white-space: normal !important;
    }
    button[data-testid="stBaseButton-secondary"] {
        background: #ffffff;
        border: 1.5px solid #7ec8ea;
        color: #0077b6;
    }
    button[data-testid="stBaseButton-primary"] {
        background: #00aeef;
        border: 1.5px solid #00aeef;
        color: #ffffff;
    }
    div[data-testid="stHorizontalBlock"] {
        align-items: stretch;
        background: transparent;
        border: none;
        flex-wrap: nowrap !important;
        gap: 0.45rem;
        margin: 0;
        padding: 0;
        position: static !important;
    }
    .st-key-nav_bar {
        background: #eef5fb;
        border-radius: 14px;
        margin: 0.15rem 0 0.45rem 0;
        padding: 0.22rem;
        position: static;
    }
    .st-key-nav_bar button {
        background: transparent !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: none !important;
        color: #5d7386 !important;
        font-size: 0.68rem !important;
        min-height: 2.15rem !important;
        padding: 0.28rem 0.12rem !important;
    }
    .st-key-nav_bar button[data-testid="stBaseButton-primary"] {
        background: #ffffff !important;
        color: #0077b6 !important;
        box-shadow: 0 1px 3px rgba(0, 56, 101, 0.08) !important;
    }
    .st-key-option_grid {
        margin-top: 0.15rem;
    }
    .st-key-option_grid button {
        margin-bottom: 0.15rem;
    }
    .st-key-acquire_cards button {
        background: #ffffff !important;
        border: 1.5px solid #d5e8f5 !important;
        border-radius: 16px !important;
        color: #003865 !important;
        margin-bottom: 0.45rem;
        min-height: 3.5rem !important;
        text-align: left !important;
    }
    .complete-copy p.purpose-flag {
        color: #0077b6;
        font-size: 0.72rem;
        font-weight: 750;
        letter-spacing: 0.03em;
        margin: 0.15rem 0;
    }
    .future-tag {
        color: #8aa0b3;
        font-size: 0.68rem;
        font-weight: 750;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    div[data-testid="stCheckbox"] label,
    div[data-testid="stCheckbox"] p,
    div[data-testid="stNumberInput"] label p,
    div[data-testid="stSelectbox"] label p,
    div[data-testid="stCaptionContainer"] p,
    div[data-testid="stSliderTickBar"] p {
        color: #16324f !important;
    }
    div[data-testid="stNumberInput"] input {
        background: #ffffff !important;
        color: #16324f !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_customers():
    data_path = Path(__file__).with_name("customers.json")
    with data_path.open(encoding="utf-8") as customer_file:
        return json.load(customer_file)


def format_euro(amount):
    return f"€{amount:,.0f}"


def format_months(months):
    return f"{months:.1f} months"


def updated_lucas_picture(customer, context):
    """Demo-only view after Lucas shares context. Nothing is saved to disk."""
    combined_income = context["external_income"]
    combined_expenses = (
        customer["essential_expenses"]
        + customer["discretionary_expenses"]
        + context["external_expenses"]
    )
    combined_savings = customer["kbc_savings"] + context["external_savings"]
    monthly_flexibility = combined_income - combined_expenses

    emergency_fund_coverage = None
    if combined_expenses > 0:
        emergency_fund_coverage = combined_savings / combined_expenses

    return monthly_flexibility, emergency_fund_coverage


def kate_follow_up(monthly_flexibility, emergency_fund_coverage):
    if (
        monthly_flexibility > 200
        and emergency_fund_coverage is not None
        and emergency_fund_coverage >= 1
    ):
        return (
            "You appear to have regular monthly flexibility and an established "
            "financial buffer. Would you like to explore your longer-term savings goals?"
        )
    return (
        "Your current financial flexibility or buffer appears limited. Would you "
        "like help reviewing your savings goals or recurring expenses?"
    )


def blank_profile():
    return {
        "transfer_purpose": None,
        "context_choice": None,
        "manual": None,
        "simulated_savings": None,
        "reviewed": False,
        "emma_stage": None,
        "savings_goal": False,
    }


def set_view(name):
    st.session_state["view"] = name


def profile_for(name):
    profiles = st.session_state.setdefault("profiles", {})
    if name not in profiles:
        profiles[name] = blank_profile()
    return profiles[name]


def update_profile(name, **fields):
    profile = profile_for(name)
    profile.update(fields)
    st.session_state["profiles"][name] = profile


def set_transfer(name, choice):
    update_profile(name, transfer_purpose=choice)


def set_context_choice(name, choice):
    update_profile(name, context_choice=choice)


def set_emma_stage(stage):
    update_profile("Emma", emma_stage=stage)


def set_savings_goal():
    update_profile("Emma", emma_stage="goal", savings_goal=True)


def simulate_connection(name):
    update_profile(name, simulated_savings=25000)


def reset_demo():
    name = st.session_state.get("demo_customer", "Emma")
    st.session_state.setdefault("profiles", {})
    st.session_state["profiles"][name] = blank_profile()
    for suffix in (
        "ext_income",
        "ext_expenses",
        "ext_savings",
        "whatif_savings",
        "whatif_only",
    ):
        st.session_state.pop(f"{name}_{suffix}", None)
    st.session_state["view"] = "KATE"


def kate_bubble(paragraphs):
    if isinstance(paragraphs, str):
        paragraphs = [paragraphs]
    body = "".join(f"<p>{escape(paragraph)}</p>" for paragraph in paragraphs)
    st.markdown(
        f'<div class="msg"><div class="bubble">{body}</div></div>',
        unsafe_allow_html=True,
    )


def user_bubble(text):
    st.markdown(
        (
            '<div class="msg user"><div class="user-bubble">'
            f"{escape(text)}</div></div>"
        ),
        unsafe_allow_html=True,
    )


def provenance_rows(title, rows):
    """rows are (label, value, source). Each cell wraps inside its column."""
    lines = [
        f'<div class="group">{escape(title)}</div>',
        (
            '<div class="prov-head"><span>Item</span>'
            "<span>Value</span><span>Source</span></div>"
        ),
    ]
    for label, value, source in rows:
        lines.append(
            '<div class="prov-row"><span>'
            f"{escape(label)}</span><span>{escape(value)}</span>"
            f"<span>{escape(source)}</span></div>"
        )
    st.markdown(f'<div class="sheet">{"".join(lines)}</div>', unsafe_allow_html=True)


def status_sheet(title, rows, tone):
    """rows are (label, provenance). The badge sits beside the label and wraps."""
    lines = [f'<div class="group">{escape(title)}</div>']
    for label, provenance in rows:
        lines.append(
            '<div class="status-row"><span class="status-label">'
            f"{escape(label)}</span>"
            f'<span class="badge {tone}">{escape(provenance)}</span></div>'
        )
    st.markdown(f'<div class="sheet">{"".join(lines)}</div>', unsafe_allow_html=True)


def savings_context_status(customer, profile, visibility):
    """Illustrative indicator for this savings-guidance purpose only."""
    manual = profile.get("manual")
    simulated = profile.get("simulated_savings")
    purpose = profile.get("transfer_purpose")
    purpose_known = purpose not in (None, "Skip")
    has_external_savings = simulated is not None or (
        manual is not None and "external_savings" in manual
    )

    if visibility == "HIGH":
        return 90, "MORE COMPLETE"
    if has_external_savings and purpose_known:
        return 85, "MORE COMPLETE"
    if has_external_savings:
        return 75, "MORE COMPLETE"
    if purpose_known:
        return 55, "INCOMPLETE"
    return 40, "INCOMPLETE"


def context_groups(customer, profile, visibility):
    """Rows that matter for savings guidance. Irrelevant gaps stay out of the way."""
    confirmed = [("KBC savings", "KBC data")]
    needs_context = []

    if visibility == "HIGH":
        if customer.get("salary_detected_at_kbc"):
            confirmed.insert(0, ("Income", "KBC data"))
        if customer.get("living_expenses_detected_at_kbc"):
            confirmed.append(("Regular expenses", "KBC data"))
        return confirmed, needs_context

    transfer = customer.get("recurring_external_transfer") or 0
    if transfer:
        confirmed.append((f"Recurring {format_euro(transfer)} transfer", "KBC data"))

    purpose = profile.get("transfer_purpose")
    if purpose and purpose != "Skip":
        confirmed.append((f"Recurring transfer purpose: {purpose}", "Confirmed by you"))
    else:
        needs_context.append(("Purpose of recurring transfer", "Unknown"))

    manual = profile.get("manual")
    simulated = profile.get("simulated_savings")
    if simulated is not None:
        confirmed.append(
            (f"External savings: {format_euro(simulated)}", "Simulated Open Banking data")
        )
    elif manual is not None:
        confirmed.append(
            (
                f"External savings: {format_euro(manual['external_savings'])}",
                "Provided by you",
            )
        )
        confirmed.append(
            (
                f"External income: {format_euro(manual['external_income'])}",
                "Provided by you",
            )
        )
        confirmed.append(
            (
                f"External expenses: {format_euro(manual['external_expenses'])}",
                "Provided by you",
            )
        )
    else:
        needs_context.append(("External savings", "Not provided"))

    return confirmed, needs_context


def render_header():
    st.markdown(
        """
        <div class="app-header">
            <span class="icon">←</span>
            <span class="mid">
                <span class="name">Kate</span>
                <span class="sub">Financial guidance</span>
            </span>
            <span class="icon right">⋮</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_nav():
    view = st.session_state["view"]
    labels = (
        ("Kate", "KATE"),
        ("My context", "MY CONTEXT"),
        ("What if?", "WHAT IF?"),
        ("Why?", "WHY?"),
    )
    with st.container(key="nav_bar"):
        columns = st.columns(4)
        for column, (label, value) in zip(columns, labels):
            with column:
                st.button(
                    label,
                    key=f"nav_{value}",
                    on_click=set_view,
                    args=(value,),
                    type="primary" if view == value else "secondary",
                    use_container_width=True,
                )


def render_kate(customer, result, profile):
    name = customer["name"]
    if name == "Lucas" and result["action"] == "ASK":
        render_lucas_conversation(customer, profile)
        return

    if name == "Emma":
        render_emma(result, profile)
        return

    kate_bubble(result["guidance"])
    if name == "Sophie":
        render_sophie(profile)


def render_emma(result, profile):
    stage = profile.get("emma_stage")
    if stage is None:
        kate_bubble(result["guidance"])
        with st.container(key="option_grid"):
            st.button(
                "Explore savings goals",
                key="emma_explore",
                on_click=set_emma_stage,
                args=("explore",),
                use_container_width=True,
            )
            st.button(
                "Review my context",
                key="emma_review",
                on_click=set_view,
                args=("MY CONTEXT",),
                use_container_width=True,
            )
            st.button(
                "Why this suggestion?",
                key="emma_why",
                on_click=set_view,
                args=("WHY?",),
                use_container_width=True,
            )
        return

    user_bubble("Explore savings goals")
    kate_bubble(
        "Based on the financial picture available to me, you appear to have "
        "regular monthly flexibility and an established buffer. I can help you "
        "explore a savings goal without assuming anything about finances you "
        "may hold elsewhere."
    )
    if stage == "goal":
        user_bubble("Set a savings goal")
        kate_bubble(
            "I've noted that you'd like to set a savings goal. This prototype "
            "doesn't create a product or move any money."
        )
        return

    st.button(
        "Set a savings goal",
        key="emma_set_goal",
        on_click=set_savings_goal,
        use_container_width=True,
    )


def note_sophie():
    update_profile("Sophie", sophie_note=True)


def render_sophie(profile):
    if profile.get("sophie_note"):
        user_bubble("Build my buffer")
        kate_bubble(
            "Let's look at building a savings buffer from the picture KBC can already see."
        )
    with st.container(key="option_grid"):
        st.button(
            "Build my buffer",
            key="sophie_buffer",
            on_click=note_sophie,
            use_container_width=True,
        )
        st.button(
            "Review expenses",
            key="sophie_expenses",
            on_click=set_view,
            args=("WHY?",),
            use_container_width=True,
        )
        st.button(
            "Why this suggestion?",
            key="sophie_why",
            on_click=set_view,
            args=("WHY?",),
            use_container_width=True,
        )


def render_lucas_conversation(customer, profile):
    name = customer["name"]
    purpose = profile.get("transfer_purpose")
    choice = profile.get("context_choice")

    # The category is stored only after Lucas taps it. It is not treated as income.
    kate_bubble(
        "We noticed a recurring €1,000 transfer to another financial institution. "
        "Would adding some context about this transfer help us make your financial "
        "picture more accurate?"
    )
    st.markdown(
        (
            '<div class="txn-card">'
            '<div class="txn-row"><span>Recurring transfer</span><strong>'
            f'{format_euro(customer["recurring_external_transfer"])} / month</strong></div>'
            '<div class="txn-row"><span>To another financial institution</span>'
            "<strong>Monthly</strong></div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )
    kate_bubble("What is this transfer mainly for?")

    if not purpose:
        render_transfer_options(name)
        return

    user_bubble(purpose)
    if purpose != "Skip":
        kate_bubble(
            "Thanks. I've recorded that category as confirmed by you. "
            "I won't infer anything beyond what you selected."
        )
    else:
        kate_bubble(
            "That's fine. I won't assign a purpose to this transfer."
        )

    kate_bubble(
        "More context may improve this savings guidance. Connecting an account "
        "could make this overview more complete for this purpose. You can also "
        "enter only what you choose, or leave external information unknown."
    )

    if choice is None:
        render_acquisition_choices(name)
        return

    if choice == "connect":
        user_bubble("Connect an account")
        render_open_banking(customer, profile)
    elif choice == "manual":
        user_bubble("Enter manually")
        render_manual_context(customer, profile)
    else:
        user_bubble("Continue without it")
        kate_bubble(
            "I'll keep external information unknown. I won't fill those gaps in for you."
        )


def render_transfer_options(name):
    options = (
        ("Savings", "Investment"),
        ("Loan repayment", "Household transfer"),
        ("Other", "Skip"),
    )
    with st.container(key="option_grid"):
        for left, right in options:
            left_col, right_col = st.columns(2)
            with left_col:
                st.button(
                    left,
                    key=f"transfer_{left}",
                    on_click=set_transfer,
                    args=(name, left),
                    use_container_width=True,
                )
            with right_col:
                st.button(
                    right,
                    key=f"transfer_{right}",
                    on_click=set_transfer,
                    args=(name, right),
                    use_container_width=True,
                )


def render_acquisition_choices(name):
    with st.container(key="acquire_cards"):
        st.button(
            "Connect an account\nUse Open Banking for this purpose",
            key="choose_connect",
            on_click=set_context_choice,
            args=(name, "connect"),
            use_container_width=True,
        )
        st.button(
            "Enter manually\nProvide only the information you choose",
            key="choose_manual",
            on_click=set_context_choice,
            args=(name, "manual"),
            use_container_width=True,
        )
        st.button(
            "Continue without it\nKeep external information unknown",
            key="choose_skip",
            on_click=set_context_choice,
            args=(name, "skip"),
            use_container_width=True,
        )


def render_open_banking(customer, profile):
    st.markdown(
        (
            '<div class="sheet"><div class="group">Open Banking connection — prototype</div>'
            "<p class=\"note\">In a production experience, you could securely select "
            "an external account to use for this specific purpose. Nothing here "
            "connects to a real bank.</p></div>"
        ),
        unsafe_allow_html=True,
    )
    if profile.get("simulated_savings") is None:
        st.button(
            "Simulate account connection",
            key="simulate_connection",
            on_click=simulate_connection,
            args=(customer["name"],),
            use_container_width=True,
        )
        return

    kate_bubble(
        "The simulated connection adds €25,000 of external savings for this "
        "savings guidance. This is fictional prototype data, not a live bank "
        "connection. I still won't treat the recurring transfer as income."
    )
    provenance_rows(
        "Simulated for this purpose",
        [
            ("External savings", "€25,000", "Simulated Open Banking data"),
        ],
    )


def render_manual_context(customer, profile):
    name = customer["name"]
    st.markdown(
        '<p class="note">Information provided by you</p>',
        unsafe_allow_html=True,
    )
    for field, label in (
        ("ext_income", "Approximate monthly income managed elsewhere"),
        ("ext_expenses", "Approximate monthly expenses managed elsewhere"),
        ("ext_savings", "Approximate savings held elsewhere"),
    ):
        key = f"{name}_{field}"
        if key not in st.session_state:
            st.session_state[key] = 0
        st.number_input(label, min_value=0, step=100, key=key)

    if st.button("Update my context", key="update_context", use_container_width=True):
        update_profile(
            name,
            manual={
                "external_income": st.session_state[f"{name}_ext_income"],
                "external_expenses": st.session_state[f"{name}_ext_expenses"],
                "external_savings": st.session_state[f"{name}_ext_savings"],
            },
        )
        st.rerun()

    manual = profile.get("manual")
    if not manual:
        return

    flexibility, coverage = updated_lucas_picture(customer, manual)
    coverage_text = (
        format_months(coverage) if coverage is not None else "Not enough information"
    )
    kate_bubble(
        [
            (
                "Thanks — that gives me a clearer picture. Based on the information "
                "you've shared, I can now provide guidance that better reflects your "
                "overall financial situation."
            ),
            kate_follow_up(flexibility, coverage),
        ]
    )
    provenance_rows(
        "Information provided by you",
        [
            ("Income elsewhere", format_euro(manual["external_income"]), "Provided by you"),
            (
                "Expenses elsewhere",
                format_euro(manual["external_expenses"]),
                "Provided by you",
            ),
            (
                "Savings elsewhere",
                format_euro(manual["external_savings"]),
                "Provided by you",
            ),
            ("Monthly flexibility", format_euro(flexibility), "Calculated"),
            ("Emergency fund coverage", coverage_text, "Calculated"),
        ],
    )


def render_my_context(customer, result, profile):
    if not profile.get("reviewed"):
        update_profile(customer["name"], reviewed=True)
        profile = profile_for(customer["name"])

    st.markdown(
        '<p class="screen-title">Your financial context</p>',
        unsafe_allow_html=True,
    )
    percent, status = savings_context_status(
        customer, profile, result["visibility"]
    )
    st.markdown(
        (
            '<div class="complete-card">'
            f'<div class="ring" style="--pct: {percent}"><span>{percent}%</span></div>'
            '<div class="complete-copy">'
            "<strong>Context for savings guidance</strong>"
            f'<p class="purpose-flag">{escape(status)}</p>'
            "<p>Shows how complete the information available for this guidance is.</p>"
            "<p>Prototype completeness indicator.</p>"
            "</div></div>"
        ),
        unsafe_allow_html=True,
    )

    confirmed, needs_context = context_groups(customer, profile, result["visibility"])
    status_sheet("Confirmed", confirmed, "ok")
    if needs_context:
        status_sheet("Needs context", needs_context, "warn")
    st.markdown(
        (
            '<p class="control-note">You control your financial context. '
            "Unknown details that are not needed for this guidance are left unknown.</p>"
        ),
        unsafe_allow_html=True,
    )
    render_rewards(profile)


def render_rewards(profile):
    def mark(done):
        return "✓" if done else "○"

    transfer_done = profile.get("transfer_purpose") not in (None, "Skip")
    lines = [
        f"{mark(profile.get('reviewed'))} Reviewed your financial context",
        f"{mark(transfer_done)} Confirmed a recurring transfer",
        f"{mark(profile.get('savings_goal'))} Created a savings goal",
    ]
    items = "".join(f'<div class="status-row"><span>{escape(line)}</span></div>' for line in lines)
    st.markdown(
        (
            '<div class="sheet"><p class="future-tag">Future concept</p>'
            '<div class="group">Kate Rewards</div>'
            '<p class="note">Complete useful financial actions and unlock relevant '
            "partner benefits.</p>"
            f"{items}"
            '<div class="group">Example reward</div>'
            '<p class="note">Partner cashback or benefit</p>'
            "<p class=\"note\">Rewards would be optional and should not require "
            "customers to provide information that is unnecessary for the service "
            "they want to use.</p></div>"
        ),
        unsafe_allow_html=True,
    )


def render_what_if(customer):
    name = customer["name"]
    savings_key = f"{name}_whatif_savings"
    only_key = f"{name}_whatif_only"
    if savings_key not in st.session_state:
        st.session_state[savings_key] = 20000
    if only_key not in st.session_state:
        st.session_state[only_key] = True

    st.markdown('<p class="screen-title">What if?</p>', unsafe_allow_html=True)
    kate_bubble("Explore a scenario without changing your financial context.")
    st.markdown(
        (
            '<p class="note">Values used here are temporary and are not added '
            "to your financial context.</p>"
        ),
        unsafe_allow_html=True,
    )
    temporary = st.slider(
        "External savings",
        min_value=0,
        max_value=50000,
        step=1000,
        key=savings_key,
    )
    st.caption("€0 — €50,000")
    use_temporary = st.checkbox("Use for this simulation only", key=only_key)
    considered = temporary if use_temporary else 0
    total = customer["kbc_savings"] + considered
    provenance_rows(
        "Available savings considered in this scenario",
        [
            ("KBC savings", format_euro(customer["kbc_savings"]), "KBC data"),
            (
                "Temporary external savings",
                format_euro(considered),
                "Temporary simulation input",
            ),
            ("Total savings considered", format_euro(total), "Calculated"),
        ],
    )
    kate_bubble(
        "This scenario uses the temporary value above. It has not been added "
        "to your financial context."
    )


def render_why(customer, result, profile):
    st.markdown(
        '<p class="screen-title">Why am I seeing this?</p>',
        unsafe_allow_html=True,
    )
    manual = profile.get("manual")
    simulated = profile.get("simulated_savings")
    low_visibility = result["visibility"] == "LOW" and not manual and simulated is None

    if low_visibility:
        st.markdown(
            (
                '<p class="note">Kate asked for context because the information '
                "available for this guidance was incomplete. Calculated figures "
                "from that partial picture are not shown.</p>"
            ),
            unsafe_allow_html=True,
        )
        rows = [("KBC savings", format_euro(customer["kbc_savings"]), "KBC data")]
        transfer = customer.get("recurring_external_transfer")
        if isinstance(transfer, (int, float)) and transfer > 0:
            rows.append(("Recurring transfer", f"{format_euro(transfer)} / month", "KBC data"))
        purpose = profile.get("transfer_purpose")
        if purpose and purpose != "Skip":
            rows.append(("Transfer purpose", purpose, "Confirmed by you"))
        provenance_rows("What Kate can use", rows)
        missing = ["External savings — Unknown"]
        if not purpose or purpose == "Skip":
            missing.insert(0, "Purpose of the recurring transfer — Unknown")
        items = "".join(f"<li>{escape(line)}</li>" for line in missing)
        st.markdown(
            (
                '<div class="sheet"><div class="group">Still missing for this guidance</div>'
                f'<ul class="missing-list">{items}</ul></div>'
            ),
            unsafe_allow_html=True,
        )
    else:
        rows = [("KBC savings", format_euro(customer["kbc_savings"]), "KBC data")]
        if result["visibility"] == "HIGH":
            rows = [
                ("Income", format_euro(customer["monthly_income"]), "KBC data"),
                (
                    "Essential expenses",
                    format_euro(customer["essential_expenses"]),
                    "KBC data",
                ),
                ("KBC savings", format_euro(customer["kbc_savings"]), "KBC data"),
            ]
            flexibility = result["displayed_monthly_flexibility"]
            coverage = result["displayed_emergency_fund_months"]
            if flexibility is not None:
                rows.append(("Monthly flexibility", format_euro(flexibility), "Calculated"))
            if coverage is not None:
                rows.append(
                    ("Emergency fund coverage", format_months(coverage), "Calculated")
                )
        else:
            purpose = profile.get("transfer_purpose")
            if purpose and purpose != "Skip":
                rows.append(("Transfer purpose", purpose, "Confirmed by you"))
            if simulated is not None:
                rows.append(
                    ("External savings", format_euro(simulated), "Simulated Open Banking data")
                )
            if manual is not None:
                rows.extend(
                    [
                        (
                            "External income",
                            format_euro(manual["external_income"]),
                            "Provided by you",
                        ),
                        (
                            "External expenses",
                            format_euro(manual["external_expenses"]),
                            "Provided by you",
                        ),
                        (
                            "External savings",
                            format_euro(manual["external_savings"]),
                            "Provided by you",
                        ),
                    ]
                )
                flexibility, coverage = updated_lucas_picture(customer, manual)
                rows.append(("Monthly flexibility", format_euro(flexibility), "Calculated"))
                if coverage is not None:
                    rows.append(
                        (
                            "Emergency fund coverage",
                            format_months(coverage),
                            "Calculated",
                        )
                    )
        provenance_rows("What Kate used", rows)

    st.markdown(
        (
            '<p class="note">What if? values are temporary simulation inputs and '
            "are not part of this context. Kate adapts her guidance based on the "
            "information available for this purpose, and on how complete that "
            "information appears to be.</p>"
        ),
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        (
            '<p class="footer-note">Hackathon prototype • Fictional data • '
            "Illustrative guidance</p>"
        ),
        unsafe_allow_html=True,
    )


if "view" not in st.session_state:
    st.session_state["view"] = "KATE"
if "profiles" not in st.session_state:
    st.session_state["profiles"] = {}

customers = load_customers()
customers_by_name = {customer["name"]: customer for customer in customers}

with st.expander("Demo controls", expanded=True):
    st.markdown('<p class="note">Prototype only</p>', unsafe_allow_html=True)
    selected_name = st.selectbox(
        "Demo customer",
        list(customers_by_name),
        key="demo_customer",
    )
    st.button(
        "Reset demo",
        key="reset_demo",
        on_click=reset_demo,
        use_container_width=True,
    )

if st.session_state.get("active_customer") != selected_name:
    if st.session_state.get("active_customer") is not None:
        st.session_state["view"] = "KATE"
    st.session_state["active_customer"] = selected_name

customer = customers_by_name[selected_name]
profile = profile_for(selected_name)
result = evaluate_customer(customer)

with st.container(key="phone_device"):
    with st.container(key="phone_screen"):
        render_header()
        render_nav()

        view = st.session_state["view"]
        if view == "MY CONTEXT":
            render_my_context(customer, result, profile)
        elif view == "WHAT IF?":
            render_what_if(customer)
        elif view == "WHY?":
            render_why(customer, result, profile)
        else:
            render_kate(customer, result, profile)

        render_footer()
