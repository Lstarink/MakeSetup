# -*- coding: utf-8 -*-
"""
Created on Tue May 10 19:42:47 2022

@author: lstar
"""

"""
Settings for what is used en where to save it
"""
recalculate_gram_matrix = True

FileName = '3D_setup2.csv'
Name_of_calculation = 'final_setup_new'
# generated_measurement_file = 'Speeds' + Name_of_calculation + '.npy'
# if generate_your_own_measurement:
#     measurement_file = generated_measurement_file
# else:
#     measurement_file = 'ZONDER_OBSTAKEL_back_and_forward.npy'

"""Settings for intersections"""
intersection_boundary_edge_x = 0.005 #meters, defines a boundary layer around the edge of the setup for which intersections will not be included, generally to exclude the sensors as intersections
intersection_boundary_edge_y = 0.005
intersection_boundary_edge_z = 0.000
use_only_full_rank_intersections = False


"""Settings for Gram Matrix"""
use_integration_for_gram_matrix = False
matrix_integration_setting = 20 #If used needs alot of calculation time, and value has to be set to at least 100
tube_width = 0.0225 #m
mesh_density = 5

"""Settings for plotting"""
#Pas alleen True of False aan!
plot_line_setup = False
plot_line_intersections = False
plot_tube_setup = False
plot_tube_setup_2d = False
view_mesh = False
# plot_u0 = False
# plot_original_field = False
# plot_intersection_field = False
# plot_interpolated = False
# plot_error = False and generate_your_own_measurement

# save_figures = quickplot #Letop hij slaat alleen onderstaande plotjes op en slaat ze alleen op als je de plot instelling ook op True hebt staan.
# only_combined = False
# plot_interpolated_resolution = 25  #bepaalt hoeveel pijlen er worden geplot. 11 houdt het overzichtelijk vindt ik, Maar hier kun je zelf mee spelen.
# plot_amount_of_interpolated_slices = 3 #Bepaalt hoeveel slices je te zien krijgt in x y en z richting
# inplane_error = True
# arrow_legenda = 1 #Bepaalt hoe groot het legenda pijltje rechtsbovenin is bij de plotjes. Zorg dat het dezelfde orde van grote heeft als je vector veld!
# arrow_legenda_string = r'$1.0\frac{m}{s}$' # Vul hier in wat je bij de regel hierboven heb gezet

# plot_field_sliced = quickplot
# plot_error_sliced = quickplot and generate_your_own_measurement
# show_sliced = False and plot_error_sliced
# calculate_error = True and generate_your_own_measurement

###Settings hieronder hebben jullie niet nodig!!

plot_tube_intersections = False and use_integration_for_gram_matrix