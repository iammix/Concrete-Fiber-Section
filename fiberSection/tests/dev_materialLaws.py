import materials


def dev_ParabolicEC2():
    concrete = materials.Concrete_ParabolicLinearEC2(16, 1.0, 1.0, 0.002, 0.0035, 10)
    concrete.test()


def dev_Popovics():
    concrete = materials.Concrete_Popovics(22360.7, 20, 0.002, 0.0035)
    concrete.test()


def dev_ParkSampson():
    steel = materials.Steel_ParkSampson(200000, 400, 480, 0.01, 0.1)
    steel.test()


def dev_NonlinearEC2():
    concrete = materials.Concrete_NonlinearEC2(22, 0.002, 0.0035)
    concrete.test()


def dev_Concrete_ParabolicLinearGeneral():
    concrete = materials.Concrete_ParabolicLinearGeneral(200000, 22, 0.002, 0.0035, 1, 1.2, 0)
    concrete.test()


if __name__ == "__main__":
    dev_Concrete_ParabolicLinearGeneral()
