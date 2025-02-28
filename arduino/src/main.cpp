#include <Arduino.h>
#include "stepper_ctrl.h"
#include "config.h"

void ser_connection_check();

void setup() {
  Serial.begin(9600);
  Serial.println("4-Wire Stepper Control Initialized");

  // Initialize the stepper motor driver
  stepper_init();
}

void loop() {
  ser_connection_check();
  delay(1000);
}

/**
 * @brief Processes serial commands and calls the appropriate stepper function.
 */
void ser_connection_check()
{
  if (Serial.available())
  {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();  // Remove any trailing newline or carriage return characters

    Serial.print("Received Command: ");
    Serial.println(cmd);

    if (cmd == CHECK_CONN)
    {
      Serial.println("OK");
    }
    else if (cmd == SET_ZERO_CMD || cmd == SET_STEPPER_ZERO)
    {
      // Set manual zero position
      manual_set_zero();
      Serial.println("Zero position set.");
    }
    else if (cmd == SET_STEPPER_90P)
    {
      // Move to +90° relative to manual zero
      move_to_angle(90);
      Serial.println("Moved to +90°.");
    }
    else if (cmd == SET_STEPPER_90N)
    {
      // Move to -90° relative to manual zero
      move_to_angle(-90);
      Serial.println("Moved to -90°.");
    }
    else if (cmd == TURN_12_POS)
    {
      // For example, rotate to -90° (customize if needed)
      move_to_angle(-90);
      Serial.println("Turned to -90° (12 o'clock).");
    }
    else if (cmd == TURN_6_POS)
    {
      // For example, rotate to +90° (customize if needed)
      move_to_angle(90);
      Serial.println("Turned to +90° (6 o'clock).");
    }
    else if (cmd == TURN_9_POS)
    {
      // Return to 0° (manual zero)
      move_to_angle(0);
      Serial.println("Returned to 0°.");
    }
    else if (cmd.startsWith(SET_MICROSTEP))
    {
      // Example command: AT+CSTEP2 sets microstepping resolution to 2
      String val = cmd.substring(String(SET_MICROSTEP).length());
      val.trim();
      if (val.length() > 0)
      {
        char mChar = val.charAt(0);
        int micro = stepper_check_steps(mChar);
        if (micro != -1)
        {
          stepper_set_steps(micro);
          Serial.println("Microstepping set.");
        }
        else
        {
          Serial.println("ERROR: Invalid microstep value.");
        }
      }
      else
      {
        Serial.println("ERROR: No microstep value provided.");
      }
    }
    else if (cmd.startsWith(ANG_CMD))
    {
      // New command to set an arbitrary angle: e.g., AT+ANG=45
      String angleStr = cmd.substring(String(ANG_CMD).length());
      angleStr.trim();
      float angle = angleStr.toFloat();
      // Accept 0 as a valid angle
      if (angle != 0 || angleStr == "0")
      {
        move_to_angle(angle);
        Serial.print("Moved to ");
        Serial.print(angle);
        Serial.println("°.");
      }
      else
      {
        Serial.println("ERROR: Invalid angle value.");
      }
    }
    else
    {
      Serial.println("ERROR: Unknown command.");
    }
  }
}
