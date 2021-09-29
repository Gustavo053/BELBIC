a = 2


def test(a):
    a = a + 1
    return a


def main():
    a = 3

    a = test(a)
    print(a)


main()
