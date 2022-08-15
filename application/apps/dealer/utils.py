def is_cpf_valid(value):

    def based_digit_calc(cpf, amount_of_digits):
        first_9_digits = slice(0, amount_of_digits)
        reversed = slice(-1, -(amount_of_digits + 1), -1)

        return sum(
            [(index + 2) * int(d) for index, d in enumerate(cpf[first_9_digits][reversed])]
        )

    try:
        cpf = ''.join(filter(str.isdigit, value))

        sum_first_9_digits = based_digit_calc(cpf, 9)
        digit_10 = 0 if sum_first_9_digits % 11 < 2 else 11 - sum_first_9_digits % 11

        if str(digit_10) == cpf[9]:
            sum_first_10_digits = based_digit_calc(cpf, 10)
            digit_11 = 0 if sum_first_10_digits % 11 < 2 else 11 - sum_first_10_digits % 11
            return str(digit_11) == cpf[10]

    except Exception:
        raise ValueError('Invalid CPF pattern')

    return False
