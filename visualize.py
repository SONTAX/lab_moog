import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.use('TkAgg')


def visualize(mesh):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(len(mesh.faces)):
        X = np.zeros(len(mesh.faces[i].verts))
        Y = np.zeros(len(mesh.faces[i].verts))
        Z = np.zeros(len(mesh.faces[i].verts))
        for j in range(len(mesh.faces[i].verts)):
            X[j] = mesh.faces[i].verts[j].coords.x
            Y[j] = mesh.faces[i].verts[j].coords.y
            Z[j] = mesh.faces[i].verts[j].coords.z

            v1 = mesh.faces[i].verts[j].coords
            v2 = mesh.faces[i].verts[j + 1 if j != len(mesh.faces[i].verts) - 1 else 0].coords

            xsc = np.linspace(v1.x, v2.x, 2)
            ysc = np.linspace(v1.y, v2.y, 2)
            zsc = np.linspace(v1.z, v2.z, 2)

            ax.plot3D(xsc, ysc, zsc, color='blue')

        X = X.reshape((1, len(mesh.faces[i].verts), 1))
        Y = Y.reshape((1, len(mesh.faces[i].verts), 1))
        Z = Z.reshape((1, len(mesh.faces[i].verts), 1))
        ax.scatter(X, Y, Z, color='purple')

    plt.show()
