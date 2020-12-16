looking_for_target = False
looking_for_people = False

room_a = 1
room_b = 2
room_c = 3


# Marker 1: Put out fire
# Marker 2: Ignore Room
# Marker 3: Scan for person and play sound / exit

# Use this function to do specific code when it detects a human
def vision_recognized_people(msg):
    global looking_for_people
    if looking_for_people:
        print("PERSON FOUND!")
        looking_for_people = False


def vision_recognized_marker_number_one(msg):
    global looking_for_target
    if looking_for_target:
        print("Target One Found")
        looking_for_target = False
        media_ctrl.play_sound(rm_define.media_sound_recognize_success)
        print("Initiate Fire sequence")


def vision_recognized_marker_number_two(msg):
    global looking_for_target
    if looking_for_target:
        print("Target Two Found")
        looking_for_target = False
        media_ctrl.play_sound(rm_define.media_sound_recognize_success)
        print("Do not enter room")


def vision_recognized_marker_number_three(msg):
    global looking_for_target
    if looking_for_target:
        print("Target Three Found")
        looking_for_target = False
        media_ctrl.play_sound(rm_define.media_sound_recognize_success)
        print("Scan for person and exit room")


def init_robot_settings():
    print("Robot Starting")
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    gimbal_ctrl.recenter()

    vision_ctrl.set_marker_detection_distance(2)

    # Set Speeds
    gimbal_ctrl.set_rotate_speed(30)


def fire_mode(direction_in, direction_out, meters):
    # Rotate and move into room
    chassis_ctrl.rotate_with_degree(direction_in, 90)
    gimbal_ctrl.recenter()
    chassis_ctrl.move_with_distance(0, meters)

    # Enable marker detection
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    looking_for_target = True
    media_ctrl.play_sound(rm_define.media_sound_scanning)

    while looking_for_target == True:
        gimbal_ctrl.pitch_ctrl(0)
        gimbal_ctrl.yaw_ctrl(250)
        gimbal_ctrl.yaw_ctrl(-250)

    # Disable marker detection
    vision_ctrl.disable_detection(rm_define.vision_detection_marker)

    # Send the drone back out the room
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180)
    chassis_ctrl.move_with_distance(0, meters)

    # Turn left
    chassis_ctrl.rotate_with_degree(direction_out, 90)


def start():
    global looking_for_target
    global looking_for_people
    global room_a
    global room_b
    global room_c

    init_robot_settings()

    # Travel to Room A
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 2.4)

    if room_a == 1:

        # Run through the fire-mode function.
        # We're passing the turn direction into the room, turn direction out of the room, and distance into room
        fire_mode(rm_define.anticlockwise, rm_define.anticlockwise, 4.3)


    elif room_a == 2:

        # Ignore the room and continue on
        pass


    elif room_a == 3:
        # This will need to be code for detecting a person and escorting them back to the beginning
        # Move into the room, enable vision detection, detect human, leave room, go back to start.
        # Until we get some code we'll just pass
        pass

    # Continue to Room B
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 4.2)

    # Turn left at the end of the hallway
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)

    # Keep moving toward Room B
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 2.2)

    # Room B: React based on the marker
    if room_b == 1:

        # Run the fire-mode function
        fire_mode(rm_define.anticlockwise, rm_define.anticlockwise, 2.6)


    # If it's #2 we just ignore it and keep on moving
    elif room_b == 2:
        pass


    elif room_b == 3:
        # This will need to be code for detecting a person and escorting them back to the beginning
        # Move into the room, enable vision detection, detect human, leave room, go back to start.
        # Until we get some code we'll just pass
        pass

    # Continue on to Room 3
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 3.9)

    if room_c == 1:

        # Initiate the fire_mode function
        fire_mode(rm_define.anticlockwise, rm_define.clockwise, 4.7)


    elif room_c == 2:

        # Ignore this room and turn around
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180)

    elif room_c == 3:

        # This will need to be code for detecting a person and escorting them back to the beginning
        # Move into the room, enable vision detection, detect human, leave room, go back to start.
        # Until we get some code we'll just pass
        pass

    # Go home!
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 1.1)

    # Turn right
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)

    # Continue to the end
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 1.6)

    gimbal_ctrl.recenter()
    media_ctrl.play_sound(rm_define.media_sound_attacked)

    print("Program ending...")




