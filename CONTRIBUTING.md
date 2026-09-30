# Contributing

Contributions that improve repeatability, safety, documentation, or tested hardware support are welcome.

Before opening a change:

1. Keep the balance loop self-contained on the EV3 unless the new design includes a documented communication-loss fail-safe.
2. Do not label gain values as universal or official without a primary source.
3. Document the exact EV3/ev3dev version and mechanical changes used for hardware testing.
4. Keep motor shutdown in a `finally` block and retain a fall threshold.
5. Run `python -m py_compile main.py` for syntax validation.

For tuning reports, include the wheel size, gearing, battery, added mass, control values, test surface, approximate run duration, and whether the result was reproduced across multiple starts.
