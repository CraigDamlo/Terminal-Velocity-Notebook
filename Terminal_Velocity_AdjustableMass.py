import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import math
    return math, mo


@app.cell
def _(mo):
    mass = mo.ui.slider(1,1000)
    mass
    return (mass,)


@app.cell
def _():
    # Define parameters
    gravity = 9.81  # m/s^2 (acceleration due to gravity)
    density_air = 1.225  # kg/m^3 (density of air)
    drag_coefficient = 0.5  # (dimensionless, typical value for spheres)
    area = 0.25  # m^2 (cross-sectional area of the object)
    return area, density_air, drag_coefficient, gravity


@app.cell
def _(area, density_air, drag_coefficient, gravity, mass, math):
    # Calculate terminal velocity
    terminal_velocity = math.sqrt((2 * mass.value * gravity) / (density_air * drag_coefficient * area))
    return (terminal_velocity,)


@app.cell
def _(terminal_velocity):
    # Print the result
    print(f"The terminal velocity is: {terminal_velocity:.2f} m/s")
    return


if __name__ == "__main__":
    app.run()
