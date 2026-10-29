DEPOSIT_MONTHS = {"small": 1, "medium": 2, "large": 3}


def rent_due(unit_size, months, is_climate, is_member):
    if unit_size not in DEPOSIT_MONTHS:
        raise ValueError("unknown unit size")
    if months < 0:
        raise ValueError("invalid months")
    covered = DEPOSIT_MONTHS[unit_size]
    if is_member and unit_size != "large":
        covered += 1
    extra = months - covered
    if extra <= 0:
        return 0
    if is_climate:
        rate = 120
    else:
        rate = 80
    if extra > 6:
        rate = rate - 10
        if is_climate:
            rate -= 5
    return extra * rate


def access_allowed(hour, visitors, is_owner):
    if is_owner:
        return visitors <= 4
    if hour < 6 or hour > 22:
        return False
    return visitors <= 2


def payment_status(days_to_due, is_autopay, has_prior_late):
    if is_autopay:
        cutoff = 0
    else:
        cutoff = 5
    if has_prior_late:
        cutoff += 10
    if days_to_due >= cutoff:
        return "current"
    elif days_to_due >= cutoff - 15:
        return "grace"
    return "lien"
