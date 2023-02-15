try:
    import os
    import gstools as gs
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.tri as tri
    import meshio
    import meshzoo
except Exception:
    print('Не установлен какой либо пакет из требуемых\nПроверьте файл "requirements.txt" и загрузите библиотеки окружения')


# 2.1 Randrom Field generation
# Very Simple Example
def gaus_covar_exemp():
    x = y = range(100)
    model = gs.Gaussian(dim=2, var=1, len_scale=10)
    srf = gs.SRF(model, seed=20170519)
    field = srf.structured([x, y])
    srf.plot()


# Creating an Ensemble of Fields
def many_feilds():
    x = y = range(100)
    model = gs.Gaussian(dim=2, var=1, len_scale=10)
    srf = gs.SRF(model)
    srf.set_pos([x, y], 'structured')
    ens_no = 4
    for i in range(ens_no):
        srf(seed=i, store=f'field_{i}')
    _, ax = plt.subplots(2, 2, sharex=True, sharey=True)
    ax = ax.flatten()
    for i in range(ens_no):
        ax[i].imshow(srf[i].T, origin='lower')
    plt.show()


# Creating Fancier Fields
def unusual_field():
    x = y = np.arange(100)
    model = gs.Exponential(dim=2, var=1, len_scale=[12.0, 3.0], angles=np.pi / 8)
    srf = gs.SRF(model, seed=20170519)
    srf.structured([x, y])
    srf.plot()


# Using an Unstructured Grid
def unstructured_grid():
    seed = gs.random.MasterRNG(19970221)
    rng = np.random.RandomState(seed())
    x = rng.randint(0, 100, size=10000)
    y = rng.randint(0, 100, size=10000)
    model = gs.Exponential(dim=2, var=1, len_scale=[12, 3], angles=np.pi / 8)
    srf = gs.SRF(model, seed=20170519)
    field = srf((x, y))
    srf.vtk_export("field")
    ax = srf.plot()
    ax.set_aspect("equal")


# Generating Fields on Meshes
def meshes_fields():
    points, cells = meshzoo.ngon(6, 4)  # создание триангулированного шестиугольника с помощью meshzoo
    mesh = meshio.Mesh(points, {"triangle": cells})
    fields_no = 12
    # настройка модели
    model = gs.Gaussian(dim=2, len_scale=0.5)
    srf = gs.SRF(model, mean=1)
    for i in range(fields_no):
        srf.mesh(mesh, points="centroids", name=f"c_field_{i}", seed=i)
    for i in range(fields_no):
        srf.mesh(mesh, points="points", name=f"p-field-{i}", seed=i)
    triangulation = tri.Triangulation(points[:, 0], points[:, 1], cells)
    # настройка фигуры в матплот
    cols = 4
    rows = int(np.ceil(fields_no / cols))
    fig = plt.figure(figsize=[2 * cols, 2 * rows])
    for i, field in enumerate(mesh.cell_data, 1):
        ax = fig.add_subplot(rows, cols, i)
        ax.tripcolor(triangulation, mesh.cell_data[field][0])
        ax.triplot(triangulation, linewidth=0.5, color="k")
        ax.set_aspect("equal")
    fig.tight_layout()
    plt.show()


# 2.2. The Covariance Model
# Introductory example
def introductory():
    class Gau(gs.CovModel):
        def cor(self, h):
            return np.exp(-(h**2))
    model = Gau(dim=2, var=2.0, len_scale=10)
    model.plot()


# Anisotropy and Rotation
def anisotropy():
    model = gs.Gaussian(dim=3, var=2.0, len_scale=[10, 5, 4])
    model.plot("vario_spatial")
    print("Представления анизотрапии:")
    print("Анизатропные коэффициенты: ", model.anis)
    print("Основная шкала длины: ", model.len_scale)
    print("Вся шкала длины: ", model.len_scale_vec)


# Rotation Angles
def rotation():
    model = gs.Gaussian(dim=3, var=2.0, len_scale=[10, 2], angles=2.5)
    model.plot("vario_spatial")
    print("Углы поворота", model.angles)


# Additional Parameters
def additional():
    class Stab(gs.CovModel):
        def default_opt_arg(self):
            return {"alpha": 1.5}

        def cor(self, h):
            return np.exp(-(h**self.alpha))
    model1 = Stab(dim=2, var=2.0, len_scale=10)
    model2 = Stab(dim=2, var=2.0, len_scale=10, alpha=0.5)
    ax = model1.plot()
    model2.plot(ax=ax)


def main():
    message = """
    Выберите какой пример хотите вывести:
    2.1 Randrom Field generation
        1 - Very Simple Example
        2 - Creating an Ensemble of Fields
        3 - Creating Fancier Fields
        4 - Using an Unstructured Grid
        5 - Generating Fields on Meshes
    2.2. The Covariance Model
        6 - Introductory example
        7 - Anisotropy and Rotation
        8 - Rotation Angles
        9 - Additional Parameters
    """
    os.system('cls||clear')
    print(message)
    try:
        choise = int(input('> '))
    except ValueError as e:
        return main()
    match choise:
        case 1:
            return gaus_covar_exemp()
        case 2:
            return many_feilds()
        case 3:
            return unusual_field()
        case 4:
            return unstructured_grid()
        case 5:
            return meshes_fields()
        case 6:
            return introductory()
        case 7:
            return anisotropy()
        case 8:
            return rotation()
        case 9:
            return additional()
        case _:
            return main()


if __name__ == '__main__':
    main()
    # a = input()  # Если программа моментально закрывается то уберите символ "#" в начале данной строки
