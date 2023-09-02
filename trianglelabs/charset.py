def change_font(text, charset):
    ascii_charset = list("""abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890~!@#$%^&*()_+`-=[]\{}|;':",./<>?""")
    fancy_charset = list(charset)

    new = {ascii_charset[i]: fancy_charset[i] for i in range(len(ascii_charset))}
    new_text = "".join([(new[char] if char in new else char) for char in text])

    return new_text