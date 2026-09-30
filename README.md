# Gyro Boy — self-balancing LEGO EV3 robot

Gyro Boy is a two-wheel self-balancing robot built with the LEGO® MINDSTORMS® Education EV3 Core Set. A LEGO EV3 gyro sensor measures body tilt and angular velocity. The controller continually changes both wheel speeds to keep the robot's centre of mass above its wheel axle.

This repository contains the Python program recovered from the original EV3 project, reproducible hardware and deployment instructions, an explanation of the control physics, and a tuning/troubleshooting guide.

> **Runtime note:** the recovered code runs directly on the EV3 with `ev3dev2`. It is not currently a ROS node and does not require ROS. See [ROS status](#ros-status) for details.

## What you need

- LEGO MINDSTORMS Education EV3 Core Set (45544), assembled as the official Gyro Boy model
- EV3 Intelligent Brick
- Two EV3 Large Motors
- One EV3 Gyro Sensor
- A microSD/microSDHC card, 2–32 GB (ev3dev warns that cards larger than 32 GB are unsupported)
- A computer, card reader, and USB/Bluetooth/Wi-Fi connection to the EV3
- A clear, level, non-slip test area

Use LEGO Education's official [Gyro Boy building instructions](https://assets.education.lego.com/v3/assets/blt293eea581807678a/blt9b683d3a8c4c4078/5f8801eba0ee6b216678e013/ev3-model-core-set-gyro-boy.pdf?locale=en-us). LEGO also publishes a short [original program description](https://assets.education.lego.com/v3/assets/blt293eea581807678a/blt6442d49d724f3570/5f8803d01c5db60f7d0ae38e/ev3-program-description-gyroboy.pdf?locale=en-us). Those copyrighted documents are linked rather than copied into this repository.

## Wiring

| Component | EV3 port |
| --- | --- |
| Left Large Motor | Output A |
| Right Large Motor | Output D |
| Gyro Sensor | Input 3 |

The program assumes this exact layout. If your build uses other ports, change the constants in the imports and device constructors near the top of [`main.py`](main.py).

## Install ev3dev

1. Follow the official [ev3dev EV3 setup guide](https://docs.ev3dev.org/en/ev3dev-stretch/getting-started/ev3.html): download the EV3 image, flash it to a microSD card, insert the card, and boot the brick.
2. Connect the EV3 by USB, Bluetooth, or a compatible USB Wi-Fi adapter.
3. Connect over SSH. The documented default is:

   ```sh
   ssh robot@ev3dev.local
   ```

4. Confirm that Python 3 and `ev3dev2` are available:

   ```sh
   python3 -c "import ev3dev2; print('ev3dev2 ready')"
   ```

The ev3dev image normally includes the Python bindings. If the import fails and the brick has Internet access, install the pinned dependency with `python3 -m pip install -r requirements.txt`.

## Deploy and run

### Option A: VS Code

Install Visual Studio Code and the **ev3dev-browser** extension, open this repository, connect the extension to the brick, open `main.py`, and run the included **Download and run current file on EV3** configuration. VS Code with ev3dev-browser is the development environment recommended by ev3dev.

### Option B: SCP and SSH

From this repository on your computer:

```sh
scp main.py robot@ev3dev.local:/home/robot/gyro-boy/
ssh robot@ev3dev.local
cd /home/robot/gyro-boy
chmod +x main.py
./main.py
```

## Safe start procedure

1. Put the robot on a level, non-slip surface with room to move.
2. Make sure the wheels rotate freely and all cables are clear of them.
3. Hold the robot upright and **completely motionless**. LEGO documents that the gyro must remain still during connection/start-up; motion here causes drift.
4. Start `main.py`. Keep holding it still during the first beep and calibration samples (about 0.8 seconds).
5. After the second beep, give the robot light support and release it gently.
6. Be ready to catch the upper frame without touching the wheels.
7. Stop with `Ctrl+C`. The `finally` block turns both motors off. A tilt beyond 35° also stops the program.

Never test near stairs, table edges, faces, loose hair, or fragile objects. Disconnect power before changing the mechanism.

## How it balances

The upright robot behaves approximately like an inverted pendulum: gravity increases any small lean, so the equilibrium is naturally unstable. The controller observes four state signals on each loop:

```text
power = 15.0 × tilt angle
      +  1.15 × angular rate
      +  0.08 × average motor position
      +  0.12 × average motor speed
```

- **Tilt angle** supplies the main restoring action.
- **Angular rate** damps fast falling and oscillation.
- **Motor position** discourages the robot from continually rolling away from its start point.
- **Motor speed** adds wheel-motion damping.

The result is clamped to the `-100..100` percent range accepted by `Motor.on()`. The loop targets a 5 ms interval, although Linux scheduling and EV3 I/O mean the real rate will vary. Read [Control theory](docs/CONTROL_THEORY.md) for a fuller explanation.

## Tuning for another build

The included gains and `BALANCE_OFFSET = -2.5` were tuned for the recovered build; they are not universal LEGO values. Wheel diameter, gearing, cable placement, battery mass/charge, frame stiffness, tyre friction, and centre-of-mass position all affect the result.

Start with [the tuning guide](docs/TUNING.md). Change one value at a time, use small adjustments, and keep a hand ready to catch the frame. If the wheels accelerate in the direction of the fall, change `DIRECTION` from `1.0` to `-1.0` before attempting any other tuning.

## ROS status

The source folder supplied for this repository contained only `main.py` and a VS Code ev3dev launch configuration. The program imports `ev3dev2` directly and contains no ROS package, node, messages, topics, launch file, or dependency manifest. Therefore this version is accurately described as an **ev3dev/Python project**, even if ROS was used elsewhere in the original experiment.

A future ROS integration could wrap sensor readings and motor commands in a node, but it should specify the ROS distribution, where the ROS master runs, message interfaces, timing requirements, and a safe behaviour on lost communication. A network-dependent outer loop should not replace the brick-local balance loop without real-time and fail-safe validation.

## Repository layout

```text
.
├── .vscode/launch.json       # ev3dev-browser deployment configuration
├── docs/
│   ├── CONTROL_THEORY.md     # physics and state-feedback explanation
│   ├── TROUBLESHOOTING.md    # symptom-based fault finding
│   └── TUNING.md             # safe gain/offset tuning workflow
├── main.py                   # on-brick balancing controller
├── requirements.txt          # documented Python dependency
├── CONTRIBUTING.md
└── LICENSE
```

## References

- [LEGO Education EV3 building instructions and resources](https://education.lego.com/en-us/product-resources/mindstorms-ev3/downloads/building-instructions/)
- [LEGO EV3 user guide — gyro sensor behaviour and stillness requirement](https://assets.education.lego.com/v3/assets/blt293eea581807678a/blta17299b86de85c10/5f8806b7ed5ccb12e4342e8e/ev3_user_guide_engb.pdf?locale=en-gb)
- [ev3dev setup for LEGO MINDSTORMS EV3](https://docs.ev3dev.org/en/ev3dev-stretch/getting-started/ev3.html)
- [`python-ev3dev2` gyro sensor API](https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/sensors.html#gyro-sensor)
- [`python-ev3dev2` motor API](https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html)

## License and trademarks

The original code and repository documentation are released under the [MIT License](LICENSE). LEGO®, MINDSTORMS®, and EV3 are trademarks of the LEGO Group, which does not sponsor, authorize, or endorse this project.
