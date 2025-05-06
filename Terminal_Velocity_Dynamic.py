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
    mo.md(
        r"""
    # Terminal Velocity
    Terminal velocity is the maximum speed attainable by an object as it falls through a fluid, such as air. Calculating the actual terminal velocity of a real object can be very complex as the shape, texture, and orientation can effect the terminal velocity. So for simplicity this notebook will assume the object is a sphere and the only parameters that are considered are:

    * The constant acceleration due to gravity
    * The density of air
    * The drag coefficient, estimated as 0.5 for a sphere
    * The area of the sphere
    * The mass of the sphere
    """
    )
    return


@app.cell
def _(mo):
    mass = mo.ui.slider(1,1000, value=60, label="Mass", show_value=True) # kg (mass of the object)
    mass
    return (mass,)


@app.cell
def _(mo):
    area = mo.ui.slider(.25,10, value=1, step=0.25, label="Area", show_value=True) # m^2 (cross-sectional area of the object)
    area
    return (area,)


@app.cell
def _():
    # Define parameters
    gravity = 9.81  # m/s^2 (acceleration due to gravity)
    density_air = 1.225  # kg/m^3 (density of air)
    drag_coefficient = 0.5  # (dimensionless, typical value for spheres)
    return density_air, drag_coefficient, gravity


@app.cell
def _(area, density_air, drag_coefficient, gravity, mass, math):
    # Calculate terminal velocity
    terminal_velocity = math.sqrt((2 * mass.value * gravity) / (density_air * drag_coefficient * area.value))
    return (terminal_velocity,)


@app.cell
def _(mo, terminal_velocity):
    # Print the result
    with mo.redirect_stdout():
        print(f"The terminal velocity is: {terminal_velocity:.2f} m/s")
    return


if __name__ == "__main__":
    app.run()
