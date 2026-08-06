import re


def extract_amount(text):

    # Find prices like:
    # 45.80
    # 45,80
    # 45.80 €

    amounts = re.findall(
        r"\d+[,.]\d{2}",
        text
    )


    if amounts:

        values = []

        for amount in amounts:

            amount = amount.replace(
                ",",
                "."
            )

            values.append(
                float(amount)
            )


        # Usually the biggest number is the total

        return max(values)


    return 0



def extract_date(text):

    # Examples:
    # 03/08/2026
    # 03-08-2026

    match = re.search(
        r"\d{2}[/-]\d{2}[/-]\d{4}",
        text
    )


    if match:

        return match.group()


    return ""



def extract_merchant(text):

    lines = text.split("\n")


    for line in lines:

        line = line.strip()


        if len(line) > 3:

            # First useful line is often merchant

            return line


    return "Unknown"



def detect_category(text):

    text = text.lower()


    if any(word in text for word in [
        "carrefour",
        "leclerc",
        "auchan",
        "market"
    ]):

        return "Food"


    if any(word in text for word in [
        "shell",
        "total",
        "essence",
        "fuel"
    ]):

        return "Transport"


    if any(word in text for word in [
        "amazon",
        "fnac"
    ]):

        return "Shopping"


    return "Other"



def parse_receipt(text):


    expense = {

        "date": extract_date(text),

        "merchant": extract_merchant(text),

        "category": detect_category(text),

        "amount": extract_amount(text),

        "description": "Automatic parsing"

    }


    return expense