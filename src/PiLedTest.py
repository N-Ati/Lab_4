import RPi.GPIO as GPIO  # Import RPi.GPIO module
from time import sleep, time
from hal import hal_input_switch  # Import the custom module for switch reading

# Initialize the GPIO for the switch
hal_input_switch.init()

# Set up GPIO pin for LED
LED_PIN = 24  # GPIO 24 for LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# State variable to track the last switch position
last_switch_position = None
right_position_start_time = None

try:
    while True:
        # Read the current position of the switch
        current_switch_position = hal_input_switch.read_slide_switch()

        if current_switch_position == 1:
            # Switch is in the left position
            right_position_start_time = None  # Reset timer for right position
            # Blink the LED at 5Hz (0.1s interval)
            GPIO.output(LED_PIN, GPIO.HIGH)
            sleep(0.1)
            GPIO.output(LED_PIN, GPIO.LOW)
            sleep(0.1)

        elif current_switch_position == 0:
            # Switch is in the right position
            if last_switch_position != 0:
                # Reset the timer when switching to the right position
                right_position_start_time = time()

            # Blink at 10Hz only within the first 5 seconds
            if right_position_start_time and time() - right_position_start_time < 5:
                GPIO.output(LED_PIN, GPIO.HIGH)
                sleep(0.05)
                GPIO.output(LED_PIN, GPIO.LOW)
                sleep(0.05)
            else:
                # Turn the LED off after 5 seconds
                GPIO.output(LED_PIN, GPIO.LOW)

        # Update the last switch position
        last_switch_position = current_switch_position

except KeyboardInterrupt:
    # Clean up GPIO settings when interrupted
    GPIO.cleanup()
