import numpy as np
import plotly.graph_objects as go

def plot_z_transform(b, a, r_min=0, r_max=2, num_points=100):
    """
    Generates and plots an interactive 3D magnitude response of a filter in the z-domain.

    Args:
        b (list or array): Numerator coefficients of the filter transfer function.
        a (list or array): Denominator coefficients of the filter transfer function.
        r_min (float): Minimum radius for the plot (default 0).
        r_max (float): Maximum radius for the plot (default 2, to show outside unit circle).
        num_points (int): Number of points in each dimension of the grid.
    """
    # 1. Create a grid of points in the complex z-plane
    # The z-plane is a polar plane: z = r * exp(j*omega)
    r = np.linspace(r_min, r_max, num_points)
    theta = np.linspace(0, 2 * np.pi, num_points)
    R, THETA = np.meshgrid(r, theta)
    
    # Convert polar coordinates to Cartesian coordinates for plotting (X, Y)
    X = R * np.cos(THETA)
    Y = R * np.sin(THETA)
    
    # Create the complex Z values
    Z_complex = -R * np.exp(1j * THETA)
    
    # 2. Calculate the filter's magnitude response |H(z)|
    # H(z) = B(z) / A(z), where B(z) and A(z) are polynomials of z
    B_z = np.polyval(b, Z_complex)
    A_z = np.polyval(a, Z_complex)
    
    # Handle potential division by zero if z is a pole location
    H_z = B_z / A_z
    magnitude_response = np.abs(H_z)

    # Limit magnitude to prevent excessive peaks at poles for better visualization
    magnitude_response = np.clip(magnitude_response, 0, 10) 
    
    # 3. Create the interactive 3D plot using Plotly
    fig = go.Figure(data=[go.Surface(x=X, y=Y, z=magnitude_response, colorscale='Viridis')])
    
    # Add unit circle on the X-Y plane for reference
    unit_circle_theta = np.linspace(0, 2 * np.pi, 100)
    unit_circle_x = np.cos(unit_circle_theta)
    unit_circle_y = np.sin(unit_circle_theta)
    unit_circle_z = np.zeros_like(unit_circle_theta)
    
    fig.add_trace(go.Scatter3d(
        x=unit_circle_x, y=unit_circle_y, z=unit_circle_z,
        mode='lines',
        name='Unit Circle',
        line=dict(color='red', width=3, dash='dash')
    ))
    
    # Update layout
    fig.update_layout(
        title='Interactive 3D Magnitude Response of a Digital Filter in the Z-Domain',
        scene=dict(
            xaxis_title='Real Axis',
            yaxis_title='Imaginary Axis',
            zaxis_title='Magnitude |H(z)|'
        ),
        width=900,
        height=700
    )
    
    fig.show()