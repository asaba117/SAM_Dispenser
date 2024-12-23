#in state 1, light 1 is green.
#in starte 2, no lights
#in state 3, light 2 is green, and light 5 blinks green
#in state 4, light 3 is red and light 5 blinks red
#in state 5, light 4 is green


#map
#led 1 is on nurses controller - it marks when the machine has meds
#LED 2 is on Nurses, green for successfully dispensed
#LED 3 is on nurses, red for failed to dispense
#LED 4 is on nurses, green for meds taken

#LED 5 is on devise, blinking green means take you pills. blinking red means theres and error go get the nurse


# ------------------------
# Constants
# ------------------------

# State Constants
STATE_IDLE = 0
STATE_LOADED = 1
STATE_DISPENSING = 2
STATE_DISPENSED = 3
STATE_ERROR = 4
STATE_TAKEN = 5

# Color Constants
COLOR_OFF = 0x000000
COLOR_GREEN = 0x00FF00
COLOR_RED = 0xFF0000

# Other Constants
THRESHOLD_JUMP = 10      # Sound level change to detect a jump/drop
FRAME_DURATION = 300     # Frame duration in milliseconds

# ------------------------
# Global Variables
# ------------------------

state = STATE_IDLE          # Current state of the state machine
previous_state = -1         # Store the last state for comparison
start_time_error = 0        # Timestamp to calculate error timeout
baseline_threshold = 0      # Baseline sound level for threshold comparison
last_frame_time = control.millis()  # Initialize the last frame time
current_time = 0            # Current time in milliseconds
end_time = 0                # End time for error sound
end_time2 = 0               # End time for success sound
current_sound_level = 0     # Real-time sound level from the microphone

# ------------------------
# LED Control Functions
# ------------------------

def turn_on_light(light_index, color):
    # Turn off all lights and turn on specified light with given color.
    BLiXel.blixels_off()
    BLiXel.set_pixel_colour(BLiXel.blixel_index(light_index), color)

def blink_light(light_index, color):
    # Blink specified light with given color.
    BLiXel.set_pixel_colour(BLiXel.blixel_index(light_index), color)
    basic.pause(100)
    BLiXel.set_pixel_colour(BLiXel.blixel_index(light_index), COLOR_OFF)
    basic.pause(100)

# ------------------------
# Sound Functions
# ------------------------

def play_error_sound():
    global end_time
    # Play an error sound for 3 seconds (State 4: Error).
    end_time = control.millis() + 3000
    while control.millis() < end_time:
        music.ring_tone(262)  # Play C4
        basic.pause(200)
        music.rest(music.beat(BeatFraction.QUARTER))
        basic.pause(200)
    music.stop_all_sounds()

def play_success_sound():
    global end_time2
    # Play a success sound for 3 seconds (State 5: Taken).
    end_time2 = control.millis() + 3000
    while control.millis() < end_time2:
        music.play_melody("C E G C5 - - - - ", 120)
        basic.pause(200)
    music.stop_all_sounds()

# ------------------------
# Button Handlers
# ------------------------

def on_button_pressed_a():
    global state, start_time_error, baseline_threshold, wieght_found
    # Handle Button A press to start dispensing (Transition from Loaded to Dispensing).
    if state == STATE_LOADED:
        state = STATE_DISPENSING
        bBoard_Motor.motor_left_timed(50, 3000)  # Run motor for 3 seconds
        start_time_error = control.millis()
        #baseline_threshold = bBoard_Mic.mic_sound_level()


input.on_button_pressed(Button.A, on_button_pressed_a)

wieght_found = 0 

def sim_weightsensor():
    global wieght_found
    basic.show_string(str(wieght_found))
    if input.button_is_pressed(Button.B):
        wieght_found = 1;
    else:
        wieght_found = 0;
basic.forever(sim_weightsensor)

def on_button_refill_pressed():
    global state, start_time_error, baseline_threshold
    # Handle refilling/resetting logic when refill button is pressed.
    if state in [STATE_IDLE, STATE_ERROR, STATE_TAKEN]:
        state = STATE_LOADED
        start_time_error = 0
        #baseline_threshold = 0
        BLiXel.blixels_off()

def check_refilled_button():
    # Check if the refill button (TouchPin.P0) is pressed and reset the system.
    if input.pin_is_pressed(TouchPin.P0):
        on_button_refill_pressed()

# ------------------------
# State Transition Function
# ------------------------

def on_state_transition():
    # Handle actions upon entering a new state.
    BLiXel.blixels_off()  # Turn off all lights at the beginning of any state transition
    if state == STATE_IDLE:
        pass  # No lights in State 0
    elif state == STATE_LOADED:
        turn_on_light(BLiXelIndex.ONE, COLOR_GREEN)  # State 1: Light 1 is green
    elif state == STATE_DISPENSING:
        pass  # State 2: No lights
    elif state == STATE_DISPENSED:
        turn_on_light(BLiXelIndex.TWO, COLOR_GREEN)  # State 3: Light 2 is green
    elif state == STATE_ERROR:
        turn_on_light(BLiXelIndex.THREE, COLOR_RED)  # State 4: Light 3 is red
        play_error_sound()
    elif state == STATE_TAKEN:
        turn_on_light(BLiXelIndex.FOUR, COLOR_GREEN)  # State 5: Light 4 is green
        play_success_sound()

# ------------------------
# State Loop Function (executed once per frame)
# ------------------------

def while_in_state():
    global state, current_sound_level, wieght_found
    # Execute actions based on the current state.
    if state == STATE_IDLE:
        pass  # No specific actions
    elif state == STATE_LOADED:
        pass  # No specific actions
    elif state == STATE_DISPENSING:
        # Poll current sound level - not working
        #current_sound_level = bBoard_Mic.mic_sound_level()
        #basic.show_string(str(current_sound_level))
        sim_weightsensor();
        if control.millis() - start_time_error > 5000:
            state = STATE_ERROR
       # elif current_sound_level > baseline_threshold + THRESHOLD_JUMP: --- not working with sound
        #    state = STATE_DISPENSED
        elif wieght_found == 1:
            state = STATE_DISPENSED
    elif state == STATE_DISPENSED:
        # State 3: Light 2 is green (already turned on), blink Light 3 green
        blink_light(BLiXelIndex.FIVE, COLOR_GREEN)
        # Poll current sound level - does not work right too hard to maintain noise 
        #current_sound_level = bBoard_Mic.mic_sound_level()
       # if current_sound_level < baseline_threshold + THRESHOLD_JUMP :
        if wieght_found == 0 :
            state = STATE_TAKEN
    elif state == STATE_ERROR:
        # State 4: Light 3 is red (already turned on), blink Light 3 red
        blink_light(BLiXelIndex.FIVE, COLOR_RED)
    elif state == STATE_TAKEN:
        pass  # No specific actions

# ------------------------
# State Machine Logic
# ------------------------

def state_machine():
    # Main state machine logic to handle transitions and checks.
    check_refilled_button()

# ------------------------
# Main Loops
# ------------------------

def on_forever():
    global current_time, last_frame_time
    # Loop to execute state actions based on frame timing.
    current_time = control.millis()
    if current_time - last_frame_time >= FRAME_DURATION:
        last_frame_time = current_time
        while_in_state()

basic.forever(on_forever)

def on_forever2():
    global previous_state
    # Main loop to check for state changes and handle transitions.
    if state != previous_state:
        on_state_transition()
        previous_state = state
    state_machine()

basic.forever(on_forever2)

