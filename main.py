#!/usr/bin/env python3
"""Balance a LEGO MINDSTORMS EV3 Gyro Boy using state feedback.

Hardware layout:
  * Left drive motor: output A
  * Right drive motor: output D
  * LEGO EV3 gyro sensor: input 3

Run this file on an EV3 brick booted into ev3dev. Keep the robot upright
and completely still while the program starts and samples gyro drift.
"""

import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_D, Motor
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sound import Sound


# State-feedback gains tuned for the original build. Different wheel sizes,
# mass distribution, batteries, or gearing can require new values.
K_GYRO_ANGLE = 15.0
K_GYRO_RATE = 1.15
K_MOTOR_POSITION = 0.08
K_MOTOR_SPEED = 0.12

# Compensates for the original robot's natural centre-of-mass lean, in degrees.
BALANCE_OFFSET = -2.5

# Change to -1.0 if the robot drives into a fall instead of correcting it.
DIRECTION = 1.0

CALIBRATION_SAMPLES = 40
CALIBRATION_INTERVAL_SECONDS = 0.02
CONTROL_INTERVAL_SECONDS = 0.005
FALL_ANGLE_DEGREES = 35.0


def clamp(value, minimum=-100.0, maximum=100.0):
    """Limit a motor command to the percentage accepted by ev3dev2."""
    return max(minimum, min(maximum, value))


def main():
    sound = Sound()
    motor_left = Motor(OUTPUT_A)
    motor_right = Motor(OUTPUT_D)
    gyro = GyroSensor(INPUT_3)

    motor_left.reset()
    motor_right.reset()
    gyro.mode = GyroSensor.MODE_GYRO_G_A
    time.sleep(0.5)

    print("Hold the robot upright and completely still...")
    sound.beep()

    # Estimate the stationary angular-rate bias (gyro drift).
    rate_bias = 0.0
    for _ in range(CALIBRATION_SAMPLES):
        _, angular_rate = gyro.angle_and_rate
        rate_bias += angular_rate
        time.sleep(CALIBRATION_INTERVAL_SECONDS)
    rate_bias /= CALIBRATION_SAMPLES

    # Read the angle without switching the sensor away from combined mode.
    start_angle, _ = gyro.angle_and_rate
    sound.beep()
    print("Balance control active. Release the robot gently.")

    try:
        while True:
            angle, angular_rate = gyro.angle_and_rate
            gyro_angle = (angle - start_angle) + BALANCE_OFFSET
            gyro_rate = angular_rate - rate_bias

            motor_position = (motor_left.position + motor_right.position) / 2.0
            motor_speed = (motor_left.speed + motor_right.speed) / 2.0

            power = (
                gyro_angle * K_GYRO_ANGLE
                + gyro_rate * K_GYRO_RATE
                + motor_position * K_MOTOR_POSITION
                + motor_speed * K_MOTOR_SPEED
            ) * DIRECTION

            motor_left.on(clamp(power))
            motor_right.on(clamp(power))

            if abs(gyro_angle) > FALL_ANGLE_DEGREES:
                print("Balance lost. Motors stopped safely.")
                break

            time.sleep(CONTROL_INTERVAL_SECONDS)
    finally:
        motor_left.off()
        motor_right.off()
        sound.beep()


if __name__ == "__main__":
    main()
