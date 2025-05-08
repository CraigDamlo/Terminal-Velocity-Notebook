import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium", app_title="Terminal Velocity")


@app.cell
def _():
    import marimo as mo
    import math
    import matplotlib.pyplot as plt
    import numpy as np
    return math, mo, np, plt


@app.cell
def _(mo):
    mo.md(
        r"""
    # Terminal Velocity
    Terminal velocity is the maximum speed attainable by an object as it falls through a fluid, such as air. Calculating the actual terminal velocity of a real object can be very complex as the shape, texture, and orientation can effect the terminal velocity. So for simplicity this notebook will assume the object is a sphere and the only parameters that are considered are:

    * The constant acceleration due to gravity
    * The density of air
    * The drag coefficient, estimated as 0.47 for a sphere
    * The area of the sphere
    * The mass of the sphere
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Calculate Terminal Velocity
    * Slide the mass slider up and down to change the mass (in kgs) of the sphere being dropped to see the effect on the terminal velocity
    * Slide the area slider to adjust the cross area(in m<sup>2</sup>)of the sphere being dropped to see the effect on the terminal velocity
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
    gravity_e = 9.81  # m/s^2 (acceleration due to gravity) on Earth
    gravity_m = 3.73 # m/s^2 (acceleration due to gravity) on Mars
    density_air_e = 1.225  # kg/m^3 (density of air) on Earth
    density_air_m = 0.020 # kg/m^3 (density of air) on Mars
    drag_coefficient = 0.47  # (dimensionless, typical value for spheres)
    return density_air_e, density_air_m, drag_coefficient, gravity_e, gravity_m


@app.cell
def _(area, density_air_e, drag_coefficient, gravity_e, mass, math):
    # Calculate terminal velocity on Earth
    terminal_velocity_e = math.sqrt((2 * mass.value * gravity_e) / (density_air_e * drag_coefficient * area.value))
    return (terminal_velocity_e,)


@app.cell
def _(area, density_air_m, drag_coefficient, gravity_m, mass, math):
    # Calculate terminal velocity on Mars
    terminal_velocity_m = math.sqrt((2 * mass.value * gravity_m) / (density_air_m * drag_coefficient * area.value))
    return (terminal_velocity_m,)


@app.cell
def _(mo):
    mo.md(r"""### Earth""")
    return


@app.cell
def _(mo, terminal_velocity_e):
    # Print the result for Earth
    with mo.redirect_stdout():
        print(f"The terminal velocity is: {terminal_velocity_e:.2f} m/s")
    return


@app.cell
def _(mo):
    mo.md(r"""### Mars""")
    return


@app.cell
def _(mo, terminal_velocity_m):
    # Print the result for Mars
    with mo.redirect_stdout():
        print(f"The terminal velocity is: {terminal_velocity_m:.2f} m/s")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Visualization
    So a shpere dropped from a specific hight doens't just jump to the terminal velocity, it takes time based on how strong gravity is. For examble on Earth in will fall 9.81 m/s^2, meaning each second it falls it gains 9.81 m/s untill it reaches terminal velocity; while on Mars it falls at 3.73 m/s^2.

    So if you don't drop it from a great enough height it will not reach terminal velocity before it hits the ground (height = 0). This charg will show you the speed of the sphere dropped from a height defined by the slider below (in kms) until it reaches the ground.
    """
    )
    return


@app.cell
def _(mo):
    height = mo.ui.slider(1,100000, value=10, step=1, label="Drop Height", show_value=True, orientation='vertical') # m (height the object will be dropped from)
    height
    return (height,)


@app.cell
def _():
    # Simulation parameters
    dt = 0.1  # Time step in seconds
    max_time = 2000  # Maximum simulation time in seconds
    return dt, max_time


@app.cell
def _():
    return


@app.cell
def _(
    area,
    density_air_e,
    drag_coefficient,
    dt,
    gravity_e,
    height,
    mass,
    max_time,
    np,
    plt,
    terminal_velocity_e,
):
    # Initialize arrays
    time_points_e = np.arange(0, max_time, dt)
    velocities_e = np.zeros_like(time_points_e)
    heights_e = np.zeros_like(time_points_e)

    # Set initial conditions
    heights_e[0] = height.value
    velocities_e[0] = 0

    # Simulation loop
    for i in range(1, len(time_points_e)):
        # Calculate drag force
        drag_force_e = .5 * density_air_e * velocities_e[i-1]**2 * drag_coefficient * area.value

        # Net force (gravity minus drag)
        net_force_e = mass.value * gravity_e - drag_force_e

        # Acceleration
        acceleration_e = net_force_e / mass.value

        # Update velocity
        velocities_e[i] = velocities_e[i-1] + acceleration_e * dt

        # Ensure velocity doesn't exceed terminal velocity
        # This is a physical constraint due to air resistance
        if velocities_e[i] > terminal_velocity_e:
            velocities_e[i] = terminal_velocity_e

        # Update position
        heights_e[i] = heights_e[i-1] - velocities_e[i-1] * dt

        # Check if shpere has hit the ground
        if heights_e[i] <= 0:
            # Truncate arrays at this point
            time_points_e = time_points_e[:i+1]
            velocities_e = velocities_e[:i+1]
            heights_e = heights_e[:i+1]
            print(f"The shpere did not reach terminal velocity and hit the ground after {time_points_e[-1]:.2f} seconds")
            break

    # Create the velocity plot
    fig = plt.figure(figsize=(10, 6))
    plt.plot(time_points_e, velocities_e, 'b-', linewidth=2, label='Velocity')
    plt.axhline(y=terminal_velocity_e, color='r', linestyle='--', 
                label=f'Terminal Velocity: {terminal_velocity_e:.2f} m/s')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Velocity (m/s)')
    plt.title(f"Velocity of Ball Dropped from {height.value} m above Earth")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.gca()

    return


@app.cell
def _(
    area,
    density_air_m,
    drag_coefficient,
    dt,
    gravity_m,
    height,
    mass,
    max_time,
    np,
    plt,
    terminal_velocity_m,
):
    # Initialize arrays
    time_points_m = np.arange(0, max_time, dt)
    velocities_m = np.zeros_like(time_points_m)
    heights_m = np.zeros_like(time_points_m)

    # Set initial conditions
    heights_m[0] = height.value
    velocities_m[0] = 0

    # Simulation loop
    for i2 in range(1, len(time_points_m)):
        # Calculate drag force
        drag_force_m = .5 * density_air_m * velocities_m[i2-1]**2 * drag_coefficient * area.value

        # Net force (gravity minus drag)
        net_force_m = mass.value * gravity_m - drag_force_m

        # Acceleration
        acceleration_m = net_force_m / mass.value

        # Update velocity
        velocities_m[i2] = velocities_m[i2-1] + acceleration_m * dt

        # Ensure velocity doesn't exceed terminal velocity
        # This is a physical constraint due to air resistance
        if velocities_m[i2] > terminal_velocity_m:
            velocities_m[i2] = terminal_velocity_m

        # Update position
        heights_m[i2] = heights_m[i2-1] - velocities_m[i2-1] * dt

        # Check if shpere has hit the ground
        if heights_m[i2] <= 0:
            # Truncate arrays at this point
            time_points_m = time_points_m[:i2+1]
            velocities_m = velocities_m[:i2+1]
            heights_m = heights_m[:i2+1]
            print(f"The shpere did not reach terminal velocity and hit the ground after {time_points_m[-1]:.2f} seconds")
            break

    # Create the velocity plot
    fig_m = plt.figure(figsize=(10, 6))
    plt.plot(time_points_m, velocities_m, 'b-', linewidth=2, label='Velocity')
    plt.axhline(y=terminal_velocity_m, color='r', linestyle='--', 
                label=f'Terminal Velocity: {terminal_velocity_m:.2f} m/s')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Velocity (m/s)')
    plt.title(f"Velocity of Ball Dropped from {height.value} m above Mars")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.gca()

    return


if __name__ == "__main__":
    app.run()
