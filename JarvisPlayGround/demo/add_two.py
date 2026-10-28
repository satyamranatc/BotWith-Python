def add_two(a, b):
    """Return the sum of two numbers."""
    return a + b

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        try:
            a = float(sys.argv[1])
            b = float(sys.argv[2])
            print(add_two(a, b))
        except ValueError:
            print("Please provide two numeric arguments.")
    else:
        print("Usage: python add_two.py <num1> <num2>")
