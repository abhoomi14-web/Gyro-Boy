# Troubleshooting

## Program cannot find a motor or sensor

- Check motor cables on outputs A and D and the gyro on input 3.
- Use the EV3 port view to confirm each device is detected.
- Check for damaged/loose RJ12-style connectors.
- If you intentionally used other ports, update `main.py`.

## `ModuleNotFoundError: ev3dev2`

Run the program on the EV3's ev3dev operating system, not on the development computer. Confirm `python3 -c "import ev3dev2"`. If the module is absent, install `python-ev3dev2` on the brick or use an ev3dev image that includes it.

## Gyro value changes while the robot is still

Power down, keep the sensor and brick still, reseat the gyro cable, and boot again without moving the robot. LEGO specifically requires the gyro to remain motionless during connection and EV3 startup. Also keep it still during this program's calibration phase.

Small drift can remain; the code averages rate samples at startup. Persistent large drift can indicate movement during startup, a loose sensor, temperature change, cable trouble, or a faulty sensor.

## Robot drives into the fall

Stop immediately. Change `DIRECTION` from `1.0` to `-1.0` (or vice versa), then repeat the supported direction test in [TUNING.md](TUNING.md).

## Robot instantly runs at full speed

- Verify direction first.
- Hold the body closer to its real balance point before release.
- Check that the gyro is mounted on the intended axis.
- Verify motor encoder readings and that both wheels turn freely.
- Restore the repository's starting gains if experimental values are loaded.

## Robot oscillates violently

The angle response may be too aggressive or angular-rate damping too weak. Make small gain changes using [TUNING.md](TUNING.md). Also check frame flex, gearbox backlash, loose wheels, low battery, and a slippery floor.

## Robot balances but keeps rolling

Adjust `BALANCE_OFFSET` in small steps. Check the test surface with a level and ensure cables are not pulling the body. Only then consider the position feedback gain.

## Motors stop after a large tilt

This is expected fall protection. The program exits when the measured lean exceeds 35°. Return the robot upright and still, then restart it so gyro bias and the start angle are sampled again.

## `Permission denied` when starting `./main.py`

Run `chmod +x main.py`, or invoke it as `python3 main.py`.
