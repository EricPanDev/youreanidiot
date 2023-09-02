def generate_bar(percent):
    length = 18
    filled = "▰"
    empty = "▱"

    def roundup(num):
        return ((round(num)) if round(num) > num else (round(num) + 1))
    def rounddown(num):
        return ((round(num)) if round(num) < num else (round(num) - 1))

    bar = ""
    for i in range(rounddown(percent * length)):
        bar += filled
    for i in range(rounddown((1-percent) * length)):
        bar += empty
    return "▰" + bar