# Control theory

## Why two wheels can hold up a tall body

With its centre of mass above the axle, Gyro Boy is an inverted pendulum. Gravity produces a torque that makes a small lean grow rather than disappear. The wheels must move the support point underneath the falling centre of mass quickly enough to recover the upright position.

The program uses a linear state-feedback approximation around the upright position. It does not model every physical effect; tyre deformation, gearbox backlash, motor saturation, battery voltage, sensor drift, and software timing all make the real robot nonlinear.

## State variables

The controller uses four measurements:

| State | Source | Meaning |
| --- | --- | --- |
| `gyro_angle` | Gyro angle minus its start angle, plus balance offset | Body lean from the desired pose, in degrees |
| `gyro_rate` | Gyro rate minus measured stationary bias | How quickly the body is rotating, in degrees/second |
| `motor_position` | Mean of both motor encoders | Wheel displacement from the reset position, in tacho counts |
| `motor_speed` | Mean of both motor speeds | Wheel velocity, in tacho counts/second |

The feedback law is:

```text
u = direction × (K_angle θ + K_rate θ_dot + K_position x + K_speed x_dot)
```

where `u` is the requested motor speed percentage. The code clamps `u` to `[-100, 100]` because that is the valid percentage range used by `ev3dev2`.

The signs depend on how the motors and gyro are mounted. `DIRECTION` provides one deliberate place to reverse the complete correction.

## Calibration and offsets

At startup, the program averages 40 angular-rate samples to estimate stationary gyro bias. Subtracting that average reduces constant rate drift; it cannot remove temperature-dependent or time-varying drift. The start angle becomes the zero reference.

`BALANCE_OFFSET` moves the requested equilibrium away from the geometric sensor zero. This is useful when the assembled robot's mass is not perfectly centred over the axle. It should be adjusted only after gyro start-up and direction have been verified.

## Loop timing and saturation

The target sleep interval is 5 ms (nominally 200 Hz), but this is not a hard real-time loop. Sensor reads, sysfs access, motor writes, and Linux scheduling add latency and jitter. Changing the software stack or adding logging can therefore change stability even with identical gains.

Motor saturation matters too. Once the command reaches ±100%, the controller has no additional authority. A large initial lean, low battery, binding drivetrain, or heavy modification can make recovery physically impossible. The 35° fall threshold stops the motors after balance is clearly lost.

## State feedback versus a simple PID

A simple angle PID reacts to tilt error and its history. This controller instead feeds back measured body angle/rate and wheel position/speed separately. The terms still resemble proportional and derivative effects, but the wheel states help limit rolling drift as well as body fall. The four constants should be treated as a coupled set and tuned carefully.
