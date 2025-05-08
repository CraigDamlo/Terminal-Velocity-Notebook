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
    height = mo.ui.slider(1,100, value=10, step=1, label="Drop Height", show_value=True) # km (height the object will be dropped from)
    height
    return (height,)


@app.cell
def _():
    # Simulation parameters
    dt = 0.1  # Time step in seconds
    max_time = 200  # Maximum simulation time in seconds
    return dt, max_time


@app.cell
def _(dt, height, max_time, np):
    # Initialize arrays
    time_points = np.arange(0, max_time, dt)
    velocities = np.zeros_like(time_points)
    heights = np.zeros_like(time_points)
    
    # Set initial conditions
    heights[0] = height.value
    velocities[0] = 0
    return heights, time_points, velocities


@app.cell
def _(
    air_density_e,
    area,
    drag_coefficient,
    dt,
    gravity_e,
    heights,
    mass,
    plt,
    terminal_velocity,
    terminal_velocity_e,
    time_points,
    velocities,
):
    def __():

        # Simulation loop
        for i in range(1, len(time_points)):
            # Calculate drag force
            drag_force = .5 * air_density_e * velocities[i-1]**2 * drag_coefficient * area
        
            # Net force (gravity minus drag)
            net_force = mass * gravity_e - drag_force
        
            # Acceleration
            acceleration = net_force / mass
        
            # Update velocity
            velocities[i] = velocities[i-1] + acceleration * dt
        
            # Ensure velocity doesn't exceed terminal velocity
            # This is a physical constraint due to air resistance
            if velocities[i] > terminal_velocity_e:
                velocities[i] = terminal_velocity_e
        
            # Update position
            heights[i] = heights[i-1] - velocities[i-1] * dt
        
            # Check if shpere has hit the ground
            if heights[i] <= 0:
                # Truncate arrays at this point
                time_points = time_points[:i+1]
                velocities = velocities[:i+1]
                heights = heights[:i+1]
                print(f"Ball hits the ground after {time_points[-1]:.2f} seconds")
                break
    
        # Create the velocity plot
        fig = plt.figure(figsize=(10, 6))
        plt.plot(time_points, velocities, 'b-', linewidth=2, label='Velocity')
        plt.axhline(y=terminal_velocity, color='r', linestyle='--', 
                   label=f'Terminal Velocity: {terminal_velocity:.2f} m/s')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Velocity (m/s)')
        plt.title('Velocity of Ball Dropped from 100 km')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
    
        # Return the figure - Marimo handles this appropriately
        return fig
    return


if __name__ == "__main__":
    app.run()
