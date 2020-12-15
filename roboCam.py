
#From Point C turn back around 180 degrees to face the way you came in.
chassis_ctrl.rotate_with_degree(rm_define.clockwise, 180)

#Move back to point B from point C (4.3 metres distance)
chassis_ctrl.move_with_distance(0, 4.3)

#Rotate left 90 degrees once at point B. After this you are now now facing point D.
chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)

#Move to point D from point B (9.2 metres distance)
chassis_ctrl.move_with_distance(0, 9.2)