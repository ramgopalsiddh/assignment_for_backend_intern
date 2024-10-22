def calculate_equal_split(amount, participants):
    return amount / len(participants)

def calculate_exact_split(amounts):
    return amounts  # Already split

def calculate_percentage_split(amount, percentages):
    return [amount * (percentage / 100) for percentage in percentages]
