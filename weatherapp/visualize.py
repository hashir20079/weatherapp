import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_cloud_with_sun(ax, center_x, center_y, scale=1.0, zorder=3):
    """Draws a vector cloud with a sun behind it."""
    base_w, base_h = 0.8 * scale, 0.3 * scale
    cloud_base = patches.FancyBboxPatch(
        (center_x - base_w / 2, center_y - base_h / 2),
        base_w, base_h,
        boxstyle="round,pad=0.05,rounding_size=0.1",
        facecolor='#ffffff', edgecolor='none', zorder=zorder
    )
    ax.add_patch(cloud_base)
    
    puffs = [
        (center_x - 0.2 * scale, center_y + 0.1 * scale, 0.22 * scale),
        (center_x + 0.1 * scale, center_y + 0.15 * scale, 0.25 * scale),
        (center_x + 0.25 * scale, center_y, 0.18 * scale)
    ]
    for px, py, pr in puffs:
        circle = patches.Circle((px, py), pr, facecolor='#ffffff', edgecolor='none', zorder=zorder)
        ax.add_patch(circle)
        
    sun = patches.Circle((center_x + 0.2, center_y + 0.25), 0.18, facecolor='#fde047', edgecolor='none', zorder=zorder-1)
    ax.add_patch(sun)

def draw_sun(ax, center_x, center_y, zorder=3):
    """Draws a clear sun icon."""
    sun = patches.Circle((center_x, center_y), 0.22, facecolor='#fde047', edgecolor='none', zorder=zorder)
    ax.add_patch(sun)

def plot_weather_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT city, temp, humidity, wind_speed, description, sunrise, sunset FROM weather_records")
    rows = cursor.fetchall()

    if not rows:
        print("⚠️ No data to visualize.")
        return

    num_cities = len(rows)
    fig, axes = plt.subplots(1, num_cities, figsize=(5.5 * num_cities, 8.2))
    
    if num_cities == 1:
        axes = [axes]

    fig.patch.set_facecolor('#3a6375')

    for idx, (city, temp, humidity, wind_speed, desc, sunrise, sunset) in enumerate(rows):
        ax = axes[idx]
        ax.set_facecolor('#3a6375')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # --- CARD CONTAINER ---
        card = patches.FancyBboxPatch(
            (0.5, 0.4), 9.0, 9.2,
            boxstyle="round,pad=0.2,rounding_size=0.4",
            facecolor='#062c3b',
            edgecolor='#0f4c61',
            linewidth=1.2,
            zorder=1
        )
        ax.add_patch(card)

        # --- HEADER ---
        ax.text(5.0, 8.8, "Wednesday, July 22", color='#8fa3af', fontsize=11, ha='center', zorder=2)
        ax.text(5.0, 8.1, f"{city.title()}", color='#ffffff', fontsize=18, fontweight='bold', ha='center', zorder=2)

        # --- METRICS LIST (With PKT Timezone Label) ---
        metrics = [
            ("Temperature", f"{temp}°C"),
            ("Wind", f"{wind_speed} m/s"),
            ("Humidity", f"{humidity}%"),
            ("Atm pressure", "756 mmHg"),
            ("Water", f"{round(temp - 4, 2)}°"),
            ("Sunrise", f"{sunrise} PKT"),
            ("Sunset", f"{sunset} PKT")
        ]

        y_start = 7.1
        y_step = 0.52
        for m_idx, (label, val) in enumerate(metrics):
            y_pos = y_start - (m_idx * y_step)
            ax.text(1.2, y_pos, label, color='#8fa3af', fontsize=11, ha='left', va='center', zorder=2)
            ax.text(8.8, y_pos, val, color='#ffffff', fontsize=10, fontweight='bold', ha='right', va='center', zorder=2)

        # Divider line
        ax.plot([1.0, 9.0], [3.3, 3.3], color='#0f4c61', linewidth=1, zorder=2)

        # --- CLEAN ANIMATED WIND STREAKS ---
        num_streaks = int(min(max(wind_speed, 1), 3))
        for w in range(num_streaks):
            y_streak = 2.8 + (w * 0.15)
            ax.plot([6.5, 8.2], [y_streak, y_streak],
                    color='#38bdf8', linestyle='-', linewidth=1.5, alpha=0.6, zorder=2)

        # --- HORIZONTAL 4-PIECE DAY FORECAST (With PKT Timezone Label) ---
        forecasts = [
            ("Morning PKT", f"{temp+1}°", "cloud_sun"),
            ("Midday PKT", f"{temp+3}°", "sun"),
            ("Evening PKT", f"{temp}°", "cloud_sun"),
            ("Night PKT", f"{temp-1}°", "sun")
        ]

        x_coords = [2.0, 4.0, 6.0, 8.0]
        for f_idx, (time_str, temp_str, icon_type) in enumerate(forecasts):
            cx = x_coords[f_idx]
            
            if icon_type == "cloud_sun":
                draw_cloud_with_sun(ax, center_x=cx, center_y=2.0, scale=0.8, zorder=3)
            elif icon_type == "sun":
                draw_sun(ax, center_x=cx, center_y=2.0, zorder=3)

            ax.text(cx, 1.3, time_str, color='#8fa3af', fontsize=9, ha='center', va='center', zorder=3)
            ax.text(cx, 0.8, temp_str, color='#ffffff', fontsize=12, fontweight='bold', ha='center', va='center', zorder=3)

    plt.tight_layout()
    plt.show()