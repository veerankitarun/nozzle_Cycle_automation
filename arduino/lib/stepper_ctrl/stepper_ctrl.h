#ifndef STEPPER_CTRL_H
#define STEPPER_CTRL_H

#include <Arduino.h>
#include <AccelStepper.h>

/**
 * @brief Initializes the stepper motor driver.
 */
void stepper_init();

/**
 * @brief Manually sets the current motor position as 0°.
 *
 * Call this after you have physically positioned your motor to its known zero.
 */
void manual_set_zero();

/**
 * @brief Moves the stepper motor to the specified angle (in degrees).
 * The angle is relative to the manually set zero.
 *
 * @param angle The target angle in degrees.
 */
void move_to_angle(float angle);

/**
 * @brief Sets the microstepping resolution.
 *
 * The effective step angle is calculated as: default_step_angle / micro_step_res.
 *
 * @param micro_step_res The microstepping resolution (e.g., 1 for full step, 2 for half step, etc.)
 */
void stepper_set_steps(int micro_step_res);

/**
 * @brief Checks a character mode and returns the corresponding microstep resolution.
 *
 * @param mode A character between '1' and '6'.
 * @return The corresponding microstep value or -1 if invalid.
 */
int stepper_check_steps(char mode);

#endif // STEPPER_CTRL_H
