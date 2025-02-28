#include "stepper_ctrl.h"
#include "config.h"

// Create an instance of AccelStepper in DRIVER mode (using STEP and DIR pins)
AccelStepper stepper1(AccelStepper::DRIVER, M1STEPPIN, M1DIRPIN);

// Global variables for step calculation
static int micro_step_res = 2;        // Default microstepping resolution (2 = half-step)
static float default_step_angle = 0.9;  // Effective step angle in degrees per microstep
                                      // (For a 1.8° motor, half-stepping gives 0.9° per step)
static float step_angle = 1;            // Calculated effective step angle

/**
 * @brief Checks a character mode and returns the corresponding microstep resolution.
 */
int stepper_check_steps(char mode)
{
    const char mode_values[] = {'1', '2', '3', '4', '5', '6'};
    const int step_values[] = {1, 2, 4, 8, 16, 32};
    for (int i = 0; i < (int)sizeof(mode_values); i++) {
        if (mode == mode_values[i]) {
            return step_values[i];
        }
    }
    return -1;
}

/**
 * @brief Sets the microstepping resolution and recalculates the effective step angle.
 */
void stepper_set_steps(int _micro_step_res)
{
    micro_step_res = _micro_step_res;
    step_angle = default_step_angle / micro_step_res;
}

/**
 * @brief Initializes the stepper motor driver.
 */
void stepper_init()
{
    stepper1.setMaxSpeed(1500);      // Set maximum speed (adjust as needed)
    stepper1.setAcceleration(1500);  // Set acceleration (adjust as needed)
    stepper_set_steps(micro_step_res);

    // Configure the enable pin and disable the driver by default
    pinMode(M1EN, OUTPUT);
    digitalWrite(M1EN, HIGH);
}

/**
 * @brief Manually sets the current position as 0°.
 */
void manual_set_zero()
{
    stepper1.setCurrentPosition(0);
}

/**
 * @brief Moves the stepper motor to the specified angle (in degrees).
 */
void move_to_angle(float angle)
{
    // Calculate the number of steps for the desired angle
    long steps = (long)round(angle / step_angle);
    
#if STEPPER_DEBUG_EN
    Serial.print("Calculated steps for ");
    Serial.print(angle);
    Serial.print("°: ");
    Serial.println(steps);
#endif

    // Enable the motor driver
    digitalWrite(M1EN, LOW);
    // Move to the target position (blocking call)
    stepper1.moveTo(steps);
    stepper1.runToPosition();
    // Optionally disable the driver after movement
    digitalWrite(M1EN, HIGH);
}
