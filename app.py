import numpy as np  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import plotly.graph_objects as go  # type: ignore
import streamlit as st  # type: ignore
import io
import time

# ---------- Page Config ----------
st.set_page_config(page_title="Wind Turbine Pro Designer", layout="wide")

# ---------- Custom Full Background CSS ----------
st.markdown("""
    <style>
        html, body, .stApp {
            height: 100%;
            margin: 0;
            padding: 0;
             background: linear-gradient(-45deg, #ed8b8b, #d29ed7, #90f7e2, #d1868c);
            background-size: 400% 400%;
            animation: gradientBG 20s ease infinite;
            color: white;
        }

        .block-container {
            padding: 2rem;
        }

        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        .stButton>button {
            background: linear-gradient(to right, #e53935, #d81b60);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            padding: 0.6em 1.2em;
            transition: transform 0.3s ease;
        }

        .stButton>button:hover {
            transform: scale(1.05);
        }

        .footer {
            text-align: center;
            font-weight: bold;
            padding-top: 30px;
            color: #fff;
        }

       .stApp {
            background-color: #111111;
            color: rgb(57, 48, 48);
        }

  @keyframes greyOutlineGlow {
    0% {
        text-shadow: 
            0 0 2px #f9f9f9, 
            0 0 4px #fdfafa, 
            0 0 6px #f9f5f5,
            1px 1px 2px #faf9f9;
    }
    50% {
        text-shadow: 
            0 0 4px #fefefe, 
            0 0 6px #fffefe, 
            0 0 10px #fdfdfd,
            1px 1px 3px #ffffff;
    }
    100% {
        text-shadow: 
            0 0 2px #fdfcfc, 
            0 0 4px #ffffff, 
            0 0 6px #ffffff,
            1px 1px 2px #ffffff;
    }
}

@keyframes yellowRedLine {
    0% {
        background: linear-gradient(to right, yellow, red);
        width: 0%;
    }
    50% {
        background: linear-gradient(to right, yellow, red);
        width: 80%;
    }
    100% {
        background: linear-gradient(to right, yellow, red);
        width: 0%;
    }
}

h1, h2, h3, h4, h5, h6 {
    color: #1a1a1a !important;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 900;
    text-align: center;
    letter-spacing: 1px;
    animation: greyOutlineGlow 2.5s infinite ease-in-out;
    margin-top: 25px;
    margin-bottom: 40px;
    position: relative;
}

h1::after, h2::after, h3::after, h4::after, h5::after, h6::after {
    content: "";
    display: block;
    height: 6px;
    margin: 10px auto 0;
    border-radius: 10px;
    animation: yellowRedLine 3s infinite ease-in-out;
}
            .energy-label {
    color: red;
    font-weight: bold;
    font-size: 22px;
    margin-bottom: 8px;
}

.energy-value {
    color: yellow;
    font-weight: bold;
    font-size: 24px;
    text-shadow:
        0 0 5px #FFD700,
        0 0 10px #FFD700,
        0 0 20px #FFA500;
    display: inline-block;
    margin-left: 10px;
}
            



             label, .stSelectbox label, .stSlider label, .stRadio label, .stNumberInput label {
        font-size: 17px !important;
        font-weight: 600 !important;
    }
    .stSelectbox div[data-baseweb="select"] * {
        font-size: 17px !important;
    }
    .stSlider .css-14pt78w, .stNumberInput input, .stRadio div[role="radiogroup"] {
        font-size: 17px !important;
    }
            







    </style>
""", unsafe_allow_html=True)

# ---------- Heading ----------
st.markdown("<h1 style='text-align: center; color: #2ecc71;'>Wind Turbine Power Calculator & 3D Visualizer</h1>", unsafe_allow_html=True)

# ---------- Inputs ----------

col1, col2, col3 = st.columns(3)
with col1:
    blade_length = st.slider("Blade Length (m)", 5.0, 60.0, 25.0)
    rpm = st.slider("Rotational Speed (RPM)", 10, 70, 30)
    material = st.selectbox("Blade Material", ["Fiberglass", "Carbon Fiber", "Aluminum", "Plastic"])
with col2:
    num_blades = st.selectbox("Number of Blades", [2, 3, 4])
    wind_speed = st.slider("Wind Speed (m/s)", 3.0, 25.0, 12.0)
    air_density = st.number_input("Air Density (kg/m³)", 1.0, 1.5, 1.225)
with col3:
    power_coefficient = st.slider("Power Coefficient (Cp)", 0.1, 0.59, 0.4)
    calc_option = st.radio("Adjust Calculation", ["Base", "Add (+10%)", "Subtract (-10%)"])

# ---------- Calculations ----------
material_efficiency = {
    "Fiberglass": 0.95,
    "Carbon Fiber": 1.0,
    "Aluminum": 0.85,
    "Plastic": 0.75
}

tip_speed_ratio = (rpm * 2 * np.pi / 60) * blade_length / wind_speed
swept_area = np.pi * blade_length ** 2
base_power_output = 0.5 * air_density * swept_area * (wind_speed ** 3) * power_coefficient
material_factor = material_efficiency[material]
rpm_efficiency = rpm / 70
power_output = base_power_output * material_factor * rpm_efficiency

if calc_option == "Add (+10%)":
    power_output *= 1.10
elif calc_option == "Subtract (-10%)":
    power_output *= 0.90

energy_hour = power_output * 3600 / 1000
energy_day = energy_hour * 24
energy_month = energy_day * 30

# ---------- Output ----------
st.markdown("### Performance Overview")

col4, col5 = st.columns(2)
with col4:
    st.metric("Tip Speed Ratio", f"{tip_speed_ratio:.2f}")
    st.metric("Swept Area", f"{swept_area:.2f} m²")
    st.metric("Power Output", f"{power_output:.0f} W")
with col5:
    st.metric("Energy / Hour", f"{energy_hour:.2f} kWh")
    st.metric("Energy / Day", f"{energy_day:.2f} kWh")
    st.metric("Energy / Month", f"{energy_month:.2f} kWh")

# ---------- 3D Visualization ----------
theta = np.linspace(0, 2 * np.pi, 100)
colors = ["#f80505", "#3b00fd", "#000000"]
fig3d = go.Figure()

for i in range(num_blades):
    angle = i * (2 * np.pi / num_blades)
    x = blade_length * np.cos(theta) * np.cos(angle) - blade_length * 0.1 * np.sin(theta) * np.sin(angle)
    y = blade_length * np.cos(theta) * np.sin(angle) + blade_length * 0.1 * np.sin(theta) * np.cos(angle)
    z = blade_length * 0.15 * np.sin(2 * theta)

    fig3d.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(width=6, color=colors[i % len(colors)]),
        name=f"Blade {i+1}"
    ))

st.markdown("<h2 style='text-align: center; color: green;'>3D Wind Turbine Visualization</h2>", unsafe_allow_html=True)

fig3d.update_layout(
    scene=dict(
        aspectratio=dict(x=1, y=1, z=0.5),
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
    ),
    margin=dict(l=0, r=0, t=50, b=0),
    showlegend=True
)
st.plotly_chart(fig3d, use_container_width=True)

# ---------- 2D Animated Fan ----------
st.markdown("<h2 style='text-align: center; color: green;'>2D Wind Turbine Fan Rotation with Energy Display</h2><br><br>", unsafe_allow_html=True)

col_anim1, col_anim2 = st.columns([2, 1])

with col_anim1:
    rotation_speed_2d = st.slider("Rotation Speed (RPM)", 10, 120, 30)

    def draw_fan_frame(angle, num_blades=3):
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        hub = plt.Circle((0, 0), 0.08, color='black')
        ax.add_patch(hub)

        for i in range(num_blades):
            blade_angle = angle + (2 * np.pi / num_blades) * i
            x = [0, 1.2 * np.cos(blade_angle)]
            y = [0, 1.2 * np.sin(blade_angle)]
            ax.plot(x, y, color='blue', linewidth=6, solid_capstyle='round')

        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight')
        plt.close(fig)
        return buf

    fan_area = st.empty()
    angle = 0
    rps = rotation_speed_2d / 60
    angle_step = 2 * np.pi * rps / 30

    # Calculate dynamic values
    power_output_2d = (rotation_speed_2d * 0.5) ** 3  # Example formula
    energy_hour_2d = power_output_2d / 1000
    energy_day_2d = energy_hour_2d * 24

    for _ in range(30):
        img_buf = draw_fan_frame(angle, num_blades=3)
        fan_area.image(img_buf)
        angle += angle_step
        time.sleep(1 / 30)

with col_anim2:
    st.markdown("#### Energy & Power Generated:")
    st.markdown(f"""
    <div class='energy-label'>Power Output:<span class='energy-value'> {power_output_2d:.2f} W</span></div>
    <div class='energy-label'>Hourly Energy:<span class='energy-value'> {energy_hour_2d:.2f} kWh</span></div>
    <div class='energy-label'>Daily Energy:<span class='energy-value'> {energy_day_2d:.2f} kWh</span></div>
    """, unsafe_allow_html=True)
# ---------- Footer ----------
st.markdown("<div class='footer'>Made by Bilal Waseem</div>", unsafe_allow_html=True)
