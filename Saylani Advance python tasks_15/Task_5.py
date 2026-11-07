def _tokenize(expr):
    tokens, i, n = [], 0, len(expr)
    while i < n:
        ch = expr[i]
        if ch.isspace():
            i += 1
        elif ch in "+-*/()":
            tokens.append(ch)
            i += 1
        elif ch in "0123456789":                 
            j = i
            while j < n and expr[j] in "0123456789":
                j += 1
            tokens.append(int(expr[i:j]))
            i = j
        else:
            raise ValueError(f"Invalid character {ch!r} at position {i}")
    return tokens


def calculate(expr):
    PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "neg": 3}   
    nums, ops = [], []                                   

    def apply_top():
        op = ops.pop()
        if op == "neg":
            nums.append(-nums.pop())
            return
        b, a = nums.pop(), nums.pop()
        if op == "+":
            nums.append(a + b)
        elif op == "-":
            nums.append(a - b)
        elif op == "*":
            nums.append(a * b)
        else:
            if b == 0:
                raise ZeroDivisionError("Division by zero in expression")
            nums.append(a / b)

    expect_operand = True    

    for tok in _tokenize(expr):
        if isinstance(tok, int):
            if not expect_operand:
                raise ValueError("Malformed expression: missing operator before number")
            nums.append(tok)
            expect_operand = False

        elif tok == "(":
            if not expect_operand:
                raise ValueError("Malformed expression: missing operator before '('")
            ops.append("(")

        elif tok == ")":
            if expect_operand:
                raise ValueError("Malformed expression: missing operand before ')'")
            while ops and ops[-1] != "(":
                apply_top()
            if not ops:
                raise ValueError("Malformed expression: unmatched ')'")
            ops.pop()                                    
            expect_operand = False

        else:                                         
            if expect_operand:
                if tok == "-":                           
                    ops.append("neg")
                    continue
                raise ValueError(f"Malformed expression: unexpected {tok!r}")
            while ops and ops[-1] != "(" and PREC[ops[-1]] >= PREC[tok]:
                apply_top()
            ops.append(tok)
            expect_operand = True

    if expect_operand:
        raise ValueError("Malformed expression: empty or ends with an operator")
    while ops:
        if ops[-1] == "(":
            raise ValueError("Malformed expression: unmatched '('")
        apply_top()
    return float(nums[0])