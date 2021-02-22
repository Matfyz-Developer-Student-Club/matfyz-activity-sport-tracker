def ordinal(number):
    if number <= 0:
        return 'none'
    tmp = number % 100
    if tmp >= 20:
        tmp = tmp % 10
    if tmp == 1:
        return str(number) + 'st'
    elif tmp == 2:
        return str(number) + 'nd'
    elif tmp == 3:
        return str(number) + 'rd'
    else:
        return str(number) + 'th'
