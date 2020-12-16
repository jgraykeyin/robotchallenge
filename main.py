# Python Robot Rescue Challenge by Robot Team 3
# Spring Week 2 December 2020
# This program will send Bill-Eh the robot along a pre-designed path passing by three rooms,
# and will take action at each room based upon a marker that's inside.


# We need to keep these two variables disabled until we're ready to scan for something.
# Looking_for_target is for detecting markers, looking_for_people is for detecting humans.
looking_for_target = False
looking_for_people = False

# These are the room variables we'll have to change based on where markers are placed
# on competiton day.
# Marker 1: Put out fire
# Marker 2: Ignore Room
# Marker 3: Scan for person and play sound / exit
# (Room A is the first room, Room B is the second room, Room C is third room)
room_a = 1
room_b = 2
room_c = 3


# Use this function to do specific code when it detects a human
def vision_recognized_people(msg):
    global looking_for_people
    if looking_for_people:
        print("PERSON FOUND!")
        looking_for_people = False


# Here are the marker functions, we can use these to trigger specific actions immidiately on detection
# Right now, the functions just detect the marker, play a sound, print to console and disables detection.
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


# Initialize settings such as speeds
def init_robot_settings():
    print("Robot Starting")
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    gimbal_ctrl.recenter()

    vision_ctrl.set_marker_detection_distance(2)

    # Set Speeds for gimbal rotation
    gimbal_ctrl.set_rotate_speed(30)

    # Set the chassis move speed
    chassis_ctrl.set_trans_speed(1)


# This is the function that will trigger if there's a Marker 1 (Fire) in a room.
# The function just needs to know the turn direction into the room, turn direction while leaving the room
# and the meters it must travel into the room. (It will travel the same # of meters to exit)
# Which should bring the robot back outside the doorway.
# This function will need to be tweaked to fire the pellets or make some extra noises.
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

    # Turn left (or right depending on the room)
    chassis_ctrl.rotate_with_degree(direction_out, 90)


# And here's our main function that runs when the bot starts.
def start():
    global looking_for_target
    global looking_for_people
    global room_a
    global room_b
    global room_c

    # Run the init function
    init_robot_settings()

    # Travel to Room A
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 2.4)

    # We should be outside Room A now, so we react based on the marker inside.
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
        #
        # TODO: Cameron & Bradley
        #
        # I think we'll need to use these commands for starting people-detection:
        #   looking_for_people = True
        #   vision_ctrl.enable_detection(rm_define.vision_detection_people)
        pass

    # Continue to Room B
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 4.2)

    # Turn left at the end of the hallway
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)

    # Keep moving toward Room B
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 2.2)

    # Now we should be outside Room B: React based on the marker # within
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
        #
        # TODO: Jacob & Mark
        pass

    # Continue on to Room 3
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 3.9)

    # Now we should be outisde the door of Room C
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
        #
        # TODO: Sam & Ashley
        pass

    # Go home!
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 1.1)

    # Turn right, we should be at the corner of the hallway now.
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)

    # Continue to the end
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 1.6)

    gimbal_ctrl.recenter()
    media_ctrl.play_sound(rm_define.media_sound_recognize_success)

    print("Program ending...")




