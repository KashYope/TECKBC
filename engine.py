"""
Transparent rule-based engine for the KBC hackathon prototype.

These thresholds and rules are illustrative hackathon prototype assumptions.
They are NOT KBC financial-advice rules.

The engine only uses figures supplied on the customer profile. It does not
treat missing external financial information as zero, and it does not turn a
recurring incoming transfer into income.
"""


def calculate_financial_metrics(customer):
    """Calculate a few simple figures from the amounts KBC can see."""
    # Illustrative prototype arithmetic, not a KBC advice formula.
    total_monthly_outgoings = (
        customer["essential_expenses"]
        + customer["discretionary_expenses"]
        + customer["monthly_debt_payments"]
    )
    monthly_flexibility = customer["monthly_income"] - total_monthly_outgoings

    metrics = {
        "total_monthly_outgoings": total_monthly_outgoings,
        "monthly_flexibility": monthly_flexibility,
    }

    # Only defined when essential expenses are actually above zero.
    # A missing or zero essential-expense figure is left unknown.
    # It is not stored as zero months of savings.
    essential_expenses = customer.get("essential_expenses")
    kbc_savings = customer.get("kbc_savings")
    if (
        essential_expenses is not None
        and essential_expenses > 0
        and kbc_savings is not None
    ):
        metrics["emergency_fund_months"] = kbc_savings / essential_expenses

    return metrics


def assess_visibility(customer):
    """
    Estimate how complete KBC's view of this customer is.

    Returns (visibility, reasons), where visibility is HIGH, MEDIUM, or LOW.

    A recurring incoming transfer is not treated as income.
    Missing activity outside KBC is not treated as zero resources.
    """
    salary_seen = customer.get("salary_detected_at_kbc") is True
    expenses_seen = customer.get("living_expenses_detected_at_kbc") is True

    # Unknown transfer data stays unknown. It is not read as "no transfer".
    transfer_amount = customer.get("recurring_external_transfer")
    direction = customer.get("external_transfer_direction")
    no_external_transfer = transfer_amount == 0
    has_external_transfer = (
        isinstance(transfer_amount, (int, float)) and transfer_amount > 0
    )

    if salary_seen and expenses_seen and no_external_transfer:
        return "HIGH", [
            "Salary is detected at KBC.",
            "Living expenses are detected at KBC.",
            "No recurring transfer to or from another bank is visible.",
        ]

    if (not salary_seen) and (not expenses_seen) and has_external_transfer:
        reasons = [
            "Salary is not detected at KBC.",
            "Living expenses are not detected at KBC.",
            "A recurring transfer with another bank is visible.",
            "Finances held outside KBC are not assumed to be zero.",
        ]
        # An incoming transfer can be a sweep or a top-up. It is not salary.
        if direction == "incoming":
            reasons.append(
                "The recurring incoming transfer is not treated as income."
            )
        return "LOW", reasons

    reasons = [
        "KBC can see some of this customer's finances, but not a complete picture."
    ]
    if salary_seen:
        reasons.append("Salary is detected at KBC.")
    else:
        reasons.append("Salary is not detected at KBC.")
    if expenses_seen:
        reasons.append("Living expenses are detected at KBC.")
    else:
        reasons.append("Living expenses are not detected at KBC.")
    if has_external_transfer:
        reasons.append("A recurring external transfer is visible.")
        if direction == "incoming":
            reasons.append(
                "The recurring incoming transfer is not treated as income."
            )
    elif no_external_transfer:
        reasons.append("No recurring external transfer is visible.")
    else:
        reasons.append(
            "Recurring external transfers are unknown and are not assumed to be zero."
        )
    return "MEDIUM", reasons


def decide_response(customer, metrics, visibility):
    """
    Choose ASK or ACT from visibility and the visible buffer.

    The 1-month and 200 flexibility cut-offs are illustrative hackathon
    prototype assumptions. They are NOT KBC financial-advice rules.
    """
    if visibility == "LOW":
        return {
            "action": "ASK",
            "guidance": (
                "It looks like KBC may only see part of your financial activity. "
                "Do you manage some of your day-to-day finances or savings elsewhere?"
            ),
            "reason": (
                "KBC should request context before making a personalised "
                "financial recommendation. Salary and day-to-day expenses are "
                "not visible here, and a recurring external transfer suggests "
                "activity elsewhere. Missing external finances are not treated "
                "as zero."
            ),
        }

    if visibility == "MEDIUM":
        return {
            "action": "ASK",
            "guidance": (
                "We may be missing part of your financial picture. Would you "
                "like to review what KBC currently understands about your finances?"
            ),
            "reason": (
                "More context would improve personalisation. The signals KBC "
                "can see are incomplete, so a recommendation would rest on a "
                "partial view."
            ),
        }

    # HIGH visibility: the visible salary and living costs are enough to
    # talk about the buffer. Still only an illustrative prototype rule.
    emergency_months = metrics.get("emergency_fund_months")
    flexibility = metrics.get("monthly_flexibility")
    limited_buffer = (
        emergency_months is not None and emergency_months < 1
    ) or (
        flexibility is not None and flexibility <= 200
    )

    if limited_buffer:
        return {
            "action": "ACT",
            "guidance": (
                "Your current financial buffer appears relatively limited. "
                "Would you like help building a savings buffer or reviewing "
                "recurring expenses?"
            ),
            "reason": (
                "KBC can see salary and living expenses, and no recurring "
                "external transfer. The visible emergency fund covers less "
                "than one month of essential expenses, or monthly flexibility "
                "is 200 or less. This 1-month / 200 cut-off is a hackathon "
                "prototype assumption, not a KBC advice rule."
            ),
        }

    return {
        "action": "ACT",
        "guidance": (
            "You appear to have a stable financial buffer and regular monthly "
            "flexibility. Would you like to explore your longer-term savings goals?"
        ),
        "reason": (
            "KBC can see salary and living expenses, and no recurring external "
            "transfer. The visible emergency fund covers at least one month of "
            "essential expenses and monthly flexibility is above 200. This "
            "cut-off is a hackathon prototype assumption, not a KBC advice rule."
        ),
    }


def evaluate_customer(customer):
    """Run metrics, visibility, and the response for one customer.

    When KBC has insufficient visibility, mathematically calculable values
    may still be misleading. The prototype therefore separates raw
    calculations from customer-facing financial assessments.
    """
    metrics = calculate_financial_metrics(customer)
    visibility, visibility_reasons = assess_visibility(customer)
    # ACT/ASK still uses the raw metrics. Only the displayed figures change.
    response = decide_response(customer, metrics, visibility)

    if visibility == "LOW":
        # Raw numbers stay in metrics, but they are not a full assessment.
        displayed_monthly_flexibility = None
        displayed_emergency_fund_months = None
        metric_confidence = "INSUFFICIENT"
    elif visibility == "MEDIUM":
        displayed_monthly_flexibility = metrics.get("monthly_flexibility")
        displayed_emergency_fund_months = metrics.get("emergency_fund_months")
        metric_confidence = "PARTIAL"
    else:
        displayed_monthly_flexibility = metrics.get("monthly_flexibility")
        displayed_emergency_fund_months = metrics.get("emergency_fund_months")
        metric_confidence = "HIGH"

    return {
        "metrics": metrics,
        "visibility": visibility,
        "visibility_reasons": visibility_reasons,
        "action": response["action"],
        "guidance": response["guidance"],
        "reason": response["reason"],
        "displayed_monthly_flexibility": displayed_monthly_flexibility,
        "displayed_emergency_fund_months": displayed_emergency_fund_months,
        "metric_confidence": metric_confidence,
    }
