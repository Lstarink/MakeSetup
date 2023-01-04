# -*- coding: utf-8 -*-
"""
Created on Thu May  5 13:03:25 2022

@author: lstar
"""
import numpy as np
import helpers
import pygmsh
from ogs5py import OGS



import settings

class GramMatrix:
    def __init__(self, tubes, grid_size, intersection_matrix):
        self.intersection_matrix = intersection_matrix
        self.grid_size = grid_size
        self.tubes = tubes
        self.gram_matrix = np.zeros([len(tubes), len(tubes)])
        self.resolution = settings.matrix_integration_setting
        GramMatrix.MakeGramMatrix_pygmsh(self)

    def MakeGramMatrix_pygmsh(self):
        previous_configurations = []
        volume_intersect = 0
        for m, tube_1 in enumerate(self.tubes):
            print("Gram matrix calculated for: " + str(100*m/len(self.tubes)) + "%")
            for n, tube_2 in enumerate(self.tubes):
                dot_unit_vectors = np.dot(tube_1.line.unit_vector, tube_2.line.unit_vector)
                if (m != n):
                    if (abs(np.dot(tube_1.line.unit_vector, tube_2.line.unit_vector)) < 0.999):
                        does_intersect, offset = GramMatrix.CanIntersect(self, tube_1, tube_2)
                        if does_intersect:
                            volume_intersect = GramMatrix.TubesVolumeIntersectMesh(tube_1, tube_2)
                else:
                    volume_intersect = tube_1.volume
                denominator = tube_1.area * tube_2.area * tube_1.line.length * tube_2.line.length
                self.gram_matrix[m][n] = volume_intersect * dot_unit_vectors / denominator
        try:
            np.save('..\output\calculations_' + settings.Name_of_calculation + '\gramMatrix.npy', self.gram_matrix)
        except FileExistsError:
            print("Gram Matrix already exists in this directory")

    def TubesVolumeIntersectMesh(tube_1, tube_2):
        with pygmsh.occ.Geometry() as geom:
            geom.characteristic_length_max = tube_1.width/settings.mesh_density
            cylinders = [
                geom.add_cylinder(tube_1.line.A, tube_1.line.unit_vector*tube_1.line.length, tube_1.width/2),
                geom.add_cylinder(tube_2.line.A, tube_2.line.unit_vector*tube_2.line.length, tube_2.width/2),
            ]
            try:
                geom.boolean_intersection(cylinders)
                mesh = geom.generate_mesh()
                volume_intersect = np.sum(helpers.compute_volume(mesh))
            except RuntimeError:
                volume_intersect = 0

        if settings.view_mesh:
            model = OGS()
            # generate example above
            model.msh.import_mesh(mesh, import_dim=3)
            model.msh.show()

        return volume_intersect

    def CanIntersect(self, tube_1, tube_2):
        line1 = tube_1.line
        line2 = tube_2.line
        # find point closest to both lines
        rounding = 5
        dA = np.array([line1.A[0] - line2.A[0],
                       line1.A[1] - line2.A[1],
                       line1.A[2] - line2.A[2]])

        unitVectorMatrix = np.array([[-line1.unit_vector[0], line2.unit_vector[0]],
                                     [-line1.unit_vector[1], line2.unit_vector[1]],
                                     [-line1.unit_vector[2], line2.unit_vector[2]]])

        # locVector = np.linalg.solve(unitVectorMatrix,dA)
        B__2 = np.matmul(np.transpose(unitVectorMatrix), unitVectorMatrix)
        B__2_inverse = np.linalg.inv(B__2)
        B__3 = np.matmul(B__2_inverse, np.transpose(unitVectorMatrix))
        locVector = np.matmul(B__3, dA)
        intersectionLocation1 = np.array([round((line1.A[0] + line1.unit_vector[0] * locVector[0]), rounding),
                                          round((line1.A[1] + line1.unit_vector[1] * locVector[0]), rounding),
                                          round((line1.A[2] + line1.unit_vector[2] * locVector[0]), rounding)])

        intersectionLocation2 = np.array([round((line2.A[0] + line2.unit_vector[0] * locVector[1]), rounding),
                                          round((line2.A[1] + line2.unit_vector[1] * locVector[1]), rounding),
                                          round((line2.A[2] + line2.unit_vector[2] * locVector[1]), rounding)])

        closest_point = (intersectionLocation1 + intersectionLocation2) / 2

        if (np.linalg.norm(intersectionLocation1 - intersectionLocation2) < tube_1.width * 2) and self.grid_size.PointInGrid(intersectionLocation1):
            can_intersect = True
        else:
            can_intersect = False
        return can_intersect, np.linalg.norm(intersectionLocation1 - intersectionLocation2)
            
