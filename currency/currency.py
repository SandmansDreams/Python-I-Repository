class Currency:
    def __init__(self, creation_value): # Initiallizer
        self.value = creation_value

    def __str__(self) -> str: # String representation
        return str(self.value)

    def __repr__(self) -> str: # Debug representation
        return f"Currency(value = {self.value})"

    def __mul__(self, num) -> "Currency": # Multiply
        return Currency(self.value * float(num))
 
    def __truediv__(self, num) -> "Currency": # Divide (float potential)
        return Currency(self.value / float(num))

    def __iadd__(self, num) -> "Currency": # In-place addition
        self.value += float(num)
        return self

    def __isub__(self, num) -> "Currency": # In-place subtraction
        self.value -= float(num)
        return self

    def __le__(self, other: "Currency") -> bool: # Less than or equal
        return self <= other

    def __ge__(self, other: "Currency") -> bool: # Greater than or equal
        return self >= other

    def __int__(self) -> int: # Convert self to int
        return int(self.value)

    def __float__(self) -> float: # Convert self to float
        return float(self.value)

    def convert_usd(self, usd: str | float | int | None = None): # Convert to USD
        # 1 USD = 5 value
        if usd == None: # If nothing is provided, convert TO USD
            return self.value / 5
        else: # If something is provied, convert FROM USD
            return Currency(5 * float(usd))

    def accrue_compount_interest(self, rate, compunds_per_period, periods) -> "Currency": # Gives the value after a time period of compound interet
        return Currency(self.value * (1 + (rate / compunds_per_period)) ** compunds_per_period * periods)

    
