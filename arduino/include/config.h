#ifndef CONFIG_H
#define CONFIG_H

// MOTOR
#define IN1_PIN         41
#define IN2_PIN         43

// STEPPER CONTROL (for driver-based control)
#define M1DIRPIN        7    // Motor X direction pin
#define M1STEPPIN       6    // Motor X step pin
#define M1EN            8    // Motor X enable pin

// DEBUG ENABLE (set to 1 to enable debug prints, 0 to disable)
#define MAIN_DEBUG_EN       0
#define STEPPER_DEBUG_EN    0

// MODULE ENABLE
#define STEPPER_EN      1

// OTHER CONFIGS (Serial command strings)
#define CHECK_CONN          "AT"
#define SET_ZERO_CMD        "AT+CZO"
#define SET_STEPPER_ZERO    "AT+CREF=0"
#define SET_STEPPER_90P     "AT+CREF=2"
#define SET_STEPPER_90N     "AT+CREF=1"
#define TURN_12_POS         "AT+TSTEPPER=1"
#define TURN_6_POS          "AT+TSTEPPER=2"
#define TURN_9_POS          "AT+TSTEPPER=0"
#define SET_MICROSTEP       "AT+CSTEP="

// New command to set an arbitrary angle
#define ANG_CMD             "AT+ANG="

#endif // CONFIG_H
