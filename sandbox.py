

try:
    print("1")
    raise Exception()
    print("2")
except Exception as e:
    print("3")
    raise
finally:
    print("4")
