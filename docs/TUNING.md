# Tuning guide

Balancing gains are specific to the mechanical build. Work on a level, non-slip floor with a clear area, keep a hand ready to catch the upper frame, and stop after repeated motor saturation or hot motors.

## Before changing gains

1. Rebuild against LEGO's official Gyro Boy instructions and tighten loose axle/frame connections.
2. Confirm left motor A, right motor D, and gyro input 3.
3. Route cables so they do not pull the body or touch a wheel.
4. Charge the battery.
5. Keep the gyro completely still through boot and the program's initial calibration.
6. Confirm the tyres turn freely and both encoders change consistently.

## Direction test

Support the robot with its wheels just touching the floor. Lean the top a few degrees forward. The wheels should drive forward, toward the fall, to move the axle back underneath the centre of mass. If they drive away from the fall, stop immediately and set:

```python
DIRECTION = -1.0
```

Do not attempt to compensate for a reversed direction by changing individual gains.

## Find the balance offset

If the robot consistently rolls one way while remaining nearly upright, its natural balance point differs from gyro zero. Adjust `BALANCE_OFFSET` in steps of roughly 0.25–0.5°. Reverse the last change if rolling gets worse. Avoid using a large offset to hide a twisted frame, dragging cable, mismatched motor, or sloped floor.

## Adjust one gain at a time

Keep a written log of values and behaviour.

| Symptom | First value to inspect | Typical experiment |
| --- | --- | --- |
| Falls without a strong enough correction | `K_GYRO_ANGLE` | Increase slightly |
| Rapid fore/aft oscillation | `K_GYRO_RATE` | Increase slightly for more damping |
| Sluggish response that cannot catch a fall | `K_GYRO_RATE` or angle gain | Undo excessive damping; then test a small angle-gain increase |
| Balances but rolls steadily away | `BALANCE_OFFSET` first | Correct offset before position gain |
| Slowly wanders far from start | `K_MOTOR_POSITION` | Increase slightly |
| Wheel motion is poorly damped | `K_MOTOR_SPEED` | Increase slightly |

Use changes of about 5–10% for gains, then test several starts. Mechanical backlash and gyro drift cause run-to-run variation, so do not judge from one attempt.

## Record a known-good configuration

For every stable build, record:

- wheel diameter and any gearing;
- battery type and approximate charge;
- added mass and its location;
- all four gains, offset, and direction;
- average balance duration and test surface;
- software/image version.

That record is more useful than calling any one set of gains “official,” because a change in mass distribution or drivetrain can invalidate them.
