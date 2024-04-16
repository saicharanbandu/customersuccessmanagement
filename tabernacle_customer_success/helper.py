from decimal import Decimal, ROUND_HALF_UP

def formatINR(number):
    s, *d = str(number).partition(".")
    r = ",".join([s[x - 2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    if d[1] == '00':
        return "".join([r])
    else:
        return "".join([r] + d)


def formatINRCash(amount):

    def truncate_float(number, places):
        return int(number * (10**places)) / 10**places

    thousand = 1000
    lakh = 100000
    crore = 10000000

    if amount < thousand:
        return amount

    if thousand <= amount < lakh:
        return formatINR(amount)

    if lakh <= amount < crore:
        return str(truncate_float((amount / crore) * 100, 2)) + " lac"

    if amount > crore:
        return str(truncate_float(amount / crore, 2)) + " cr"


def INRWords(amount):
    assert (0 <= amount)
    d = {
        0: 'Zero',
        1: 'One',
        2: 'Two',
        3: 'Three',
        4: 'Four',
        5: 'Five',
        6: 'Six',
        7: 'Seven',
        8: 'Eight',
        9: 'Nine',
        10: 'Ten',
        11: 'Eleven',
        12: 'Twelve',
        13: 'Thirteen',
        14: 'Fourteen',
        15: 'Fifteen',
        16: 'Sixteen',
        17: 'Seventeen',
        18: 'Eighteen',
        19: 'Nineteen',
        20: 'Twenty',
        30: 'Thirty',
        40: 'Forty',
        50: 'Fifty',
        60: 'Sixty',
        70: 'Seventy',
        80: 'Eighty',
        90: 'Ninety'
    }
    h = [100, 'Hundred', 'Hundred']
    t = [h[0] * 10, 'Thousand', 'Thousand']
    l = [t[0] * 100, 'Lakh', 'Lakh']
    c = [l[0] * 100, 'Crore', 'Crore']
    if amount < 20:
        return d[amount]
    if amount < 100:
        div_, mod_ = divmod(amount, 10)
        return d[amount] if mod_ == 0 else d[div_ * 10] + '-' + d[mod_]
    else:
        if amount < t[0]:
            divisor, word1, word2 = h
        elif amount < l[0]:
            divisor, word1, word2 = t
        elif amount < c[0]:
            divisor, word1, word2 = l
        else:
            divisor, word1, word2 = c
        div_, mod_ = divmod(amount, divisor)
        if mod_ == 0:
            return '{} {}'.format(INRWords(div_), word1)
        else:
            return '{} {} {}'.format(INRWords(div_), word2, INRWords(mod_))


def get_discounted_amount(number, percentage):
    number = Decimal(number)
    discount_percentage_decimal = Decimal(percentage)
    discount_amount = (discount_percentage_decimal / Decimal(100)) * number
    discounted_price = number - discount_amount
    return discounted_price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)