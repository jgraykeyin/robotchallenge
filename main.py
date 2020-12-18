looking_for_target = False
looking_for_people = False

room_a = 1
room_b = 3
room_c = 2
room_d = 1


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
        vision_ctrl.detect_marker_and_aim(rm_define.marker_number_one)

        print("Fire")

        vision_ctrl.disable_detection(rm_define.vision_detection_marker)


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

    vision_ctrl.set_marker_detection_distance(3)

    # Set Speeds
    gimbal_ctrl.set_rotate_speed(30)
    chassis_ctrl.set_trans_speed(0.8)


def fire_mode(direction_in, direction_out, meters):
    global looking_for_target

    # Rotate and move into room
    # chassis_ctrl.rotate_with_degree(direction_in, 90)
    # gimbal_ctrl.recenter()
    # chassis_ctrl.move_with_distance(0, meters)

    # Enable marker detection
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)

    looking_for_target = True

    while looking_for_target == True:
        gimbal_ctrl.pitch_ctrl(0)
        gimbal_ctrl.yaw_ctrl(250)
        gimbal_ctrl.yaw_ctrl(-250)

    # Disable marker detection
    vision_ctrl.disable_detection(rm_define.vision_detection_marker)

    media_ctrl.play_sound(rm_define.media_custom_audio_2, wait_for_complete=False)
    gun_ctrl.set_fire_count(8)
    gun_ctrl.fire_once()

    # Send the drone back out the room
    # chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180)
    # chassis_ctrl.move_with_distance(0, meters)

    # Turn left
    # chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)


def search_mode():
    global looking_for_people
    gimbal_ctrl.recenter()

    vision_ctrl.enable_detection(rm_define.vision_detection_people)
    looking_for_people = True

    while looking_for_people == True:
        gimbal_ctrl.pitch_ctrl(10)
        gimbal_ctrl.yaw_ctrl(250)
        gimbal_ctrl.yaw_ctrl(-250)

    vision_ctrl.disable_detection(rm_define.vision_detection_people)
    media_ctrl.play_sound(rm_define.media_custom_audio_3, wait_for_complete=False)
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 150, rm_define.effect_flash)
    led_ctrl.set_top_led(rm_define.armor_top_all, 161, 255, 69, rm_define.effect_flash)


def start():
    global looking_for_target
    global looking_for_people
    global room_a
    global room_b
    global room_c

    lastroom = False

    init_robot_settings()

    # Travel to Room A
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 2.4)

    print("Room A reached")

    if room_a == 1:

        # Run through the fire-mode function.
        # We're passing the turn direction into the room, turn direction out of the room, and distance into room
        # Rotate and move into room

        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)
        gimbal_ctrl.recenter()
        chassis_ctrl.move_with_distance(0, 2)

        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 45)
        chassis_ctrl.move_with_distance(0, 1.5)

        # Detect fire
        fire_mode(rm_define.anticlockwise, rm_define.anticlockwise, 2)

        # Send the drone back out the room
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180)
        chassis_ctrl.move_with_distance(0, 1.5)

        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45)
        chassis_ctrl.move_with_distance(0, 2)

        # Turn left
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)

    elif room_a == 2:

        # Ignore the room and continue on
        # Play a sound here
        media_ctrl.play_sound(rm_define.media_custom_audio_1, wait_for_complete=False)

    elif room_a == 3:
        # This will need to be code for detecting a person and escorting them back to the beginning
        # Move into the room, enable vision detection, detect human, leave room, go back to start.
        # Until we get some code we'll just pass
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)
        chassis_ctrl.move_with_distance(0, 2.5)

        # Enable person-search
        search_mode()

        # Leave the room
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180)
        chassis_ctrl.move_with_distance(0, 2.5)
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)

        # Travel back to start position
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 2.4)

        media_ctrl.play_sound(rm_define.media_custom_audio_0, wait_for_complete=False)

        # Turn around
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180)
        time.sleep(5)

        # Get back by Room A and carry on
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 2.4)

    # Continue to Room B
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 3.8)

    print("Hallway corner reached")

    # Turn left at the end of the hallway
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)

    # Keep moving toward Room B
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 2.3)

    print("Room B Reached")
    # Room B: React based on the marker
    if room_b == 1:
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)
        gimbal_ctrl.recenter()
        chassis_ctrl.move_with_distance(0, 2)

        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 45)
        chassis_ctrl.move_with_distance(0, 2)

        # Detect fire
        fire_mode(rm_define.anticlockwise, rm_define.anticlockwise, 2)

        # Send the drone back out the room
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180)
        chassis_ctrl.move_with_distance(0, 2)

        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45)
        chassis_ctrl.move_with_distance(0, 2)

        # Turn left
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)

    # If it's #2 we just ignore it and keep on moving
    elif room_b == 2:
        # Play sound here
        media_ctrl.play_sound(rm_define.media_custom_audio_1, wait_for_complete=False)


    elif room_b == 3:
        # This will need to be code for detecting a person and escorting them back to the beginning
        # Move into the room, enable vision detection, detect human, leave room, go back to start.
        # Until we get some code we'll just pass
        # While still facing down the hall turn 90 degrees so that you are now facing into room b
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)
        chassis_ctrl.move_with_distance(0, 2.4)

        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 45)
        chassis_ctrl.move_with_distance(0, 3)

        # Enable people-search mode
        search_mode()

        # Leave the room
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 180)
        chassis_ctrl.move_with_distance(0, 3.0)
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45)
        chassis_ctrl.move_with_distance(0, 2.6)

        # Out of the room, turn toward the end of the hallway
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)

        # Go home!
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 2.25)

        # Turn right at carpet-corner
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)

        # Continue to the end
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 1.6)

        # The robot should now be at the start, turn around and get back
        media_ctrl.play_sound(rm_define.media_custom_audio_0, wait_for_complete=False)

        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 180)
        time.sleep(5)

        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 1.6)
        # Turn at the carpet-corner
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)
        # Get back to position by room B
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 2.2)

    # Continue on to Room C
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 3.8)

    if room_c == 1:
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)
        gimbal_ctrl.recenter()
        chassis_ctrl.move_with_distance(0, 2)

        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45)
        chassis_ctrl.move_with_distance(0, 2)

        # Detect fire
        fire_mode(rm_define.anticlockwise, rm_define.anticlockwise, 2)

        # Send the drone back out the room
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180)
        chassis_ctrl.move_with_distance(0, 2)

        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 45)
        chassis_ctrl.move_with_distance(0, 2)

        # Turn left
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)

    elif room_c == 2:

        # Ignore this room and turn around
        # chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180
        media_ctrl.play_sound(rm_define.media_custom_audio_1, wait_for_complete=False)

    elif room_c == 3:

        # This will need to be code for detecting a person and escorting them back to the beginning
        # Move into the room, enable vision detection, detect human, leave room, go back to start.
        # Until we get some code we'll just pass
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)
        chassis_ctrl.move_with_distance(0, 4.7)

        search_mode()

        # Leave the room
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180)
        chassis_ctrl.move_with_distance(0, 4.7)
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)

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

        # The robot should now be at the start, turn around and get back
        media_ctrl.play_sound(rm_define.media_custom_audio_0, wait_for_complete=False)

        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 180)
        time.sleep(5)
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 1.6)
        # Turn at the carpet-corner
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)
        # Get back to position by room C
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 2.2)
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 3.85)

    # Continue to Room D
    chassis_ctrl.move_with_distance(0, 5.0)
    chassis_ctrl.move_with_distance(0, 5.0)

    if room_d == 1:
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)
        gimbal_ctrl.recenter()
        chassis_ctrl.move_with_distance(0, 2)

        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45)
        chassis_ctrl.move_with_distance(0, 2)

        # Detect fire
        fire_mode(rm_define.anticlockwise, rm_define.anticlockwise, 2)

        # Send the drone back out the room
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180)
        chassis_ctrl.move_with_distance(0, 2)

        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 45)
        chassis_ctrl.move_with_distance(0, 2)

        # Turn left
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)

    elif room_d == 2:
        media_ctrl.play_sound(rm_define.media_custom_audio_1, wait_for_complete=False)
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180)


    elif room_d == 3:
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)
        chassis_ctrl.move_with_distance(0, 4.7)

        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45)
        chassis_ctrl.move_with_distance(0, 2)

        search_mode()

        # Leave the room
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180)

        chassis_ctrl.move_with_distance(0, 2)
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 45)

        chassis_ctrl.move_with_distance(0, 4.7)
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)

        # Go home!
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 4.3)
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

        # The robot should now be at the start, turn around and get back
        media_ctrl.play_sound(rm_define.media_custom_audio_0, wait_for_complete=False)

        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 180)
        lastroom = True

    if lastroom == False:
        # Go home!
        chassis_ctrl.move_with_distance(0, 5.0)
        chassis_ctrl.move_with_distance(0, 4.3)
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

    print("Program ending...")




