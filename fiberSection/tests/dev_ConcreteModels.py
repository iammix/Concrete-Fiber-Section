import materials


def dev_ParabolicEC2():
    concrete = materials.Concrete_ParabolicLinearEC2(16, 1.0, 1.0, 0.002, 0.0035, 1)
    concrete.test()


def dev_Popovics():
    concrete = materials.Concrete_Popovics(22360.7, 20, 0.002, 0.0035)
    concrete.test()


if __name__ == "__main__":
    dev_Popovics()
