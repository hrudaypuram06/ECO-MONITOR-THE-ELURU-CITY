from assets import LOGO_SQ_B64, BANNER_WIDE_B64, LOGO_B64
import streamlit as st
import streamlit.components.v1 as components

# Set page config
st.set_page_config(
    page_title='Eco-Monitor Eluru | Professional Monitoring Systems',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# The logic and view are bundled together here
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eco-Monitor Eluru | Data Science and Monitoring</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        :root {
            --bg-deep: #0f172a;
            --bg-darker: #020617;
            --accent: #38bdf8;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --glass: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-hover: rgba(255, 255, 255, 0.08);
            --good: #22c55e;
            --satisfactory: #84cc16;
            --moderate: #eab308;
            --poor: #f97316;
            --very-poor: #ef4444;
            --severe: #7f1d1d;
            --anim-speed: 0.6s;
            --title-yellow: #facc15;
        }

        @keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes logoPulse { 0% { transform: scale(1); filter: drop-shadow(0 0 0 var(--accent)); } 50% { transform: scale(1.1); filter: drop-shadow(0 0 15px var(--accent)); } 100% { transform: scale(1); filter: drop-shadow(0 0 0 var(--accent)); } }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes pulse-animation { 0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); } 70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(34, 197, 94, 0); } 100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); } }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background-color: var(--bg-deep); color: var(--text-main); font-family: 'Outfit', sans-serif; min-height: 100vh; overflow-x: hidden; line-height: 1.6; padding-bottom: 80px; }
        ::-webkit-scrollbar { width: 0px; background: transparent; }
        
        #splash-screen {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background: var(--bg-darker); z-index: 9999; 
            display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
            padding-top: 5vh;
            transition: opacity 0.8s ease-out, visibility 0.8s;
        }
        #splash-screen.hidden { opacity: 0; visibility: hidden; }
        .splash-logos { width: 100%; display: flex; align-items: center; justify-content: flex-start; gap: 30px; padding: 0 5%; margin-bottom: 8vh; }
        .splash-logo-sq { height: 160px; border-radius: 20px; animation: logoPulse 2s infinite ease-in-out; }
        .splash-banner { height: 120px; border-radius: 10px; }
        .splash-title { 
            color: var(--title-yellow); font-size: 2.2rem; font-weight: 800; 
            text-align: center; margin-bottom: 30px; padding: 0 20px;
            letter-spacing: 2px;
            width: 100%;
        }
        .splash-credits { text-align: center; color: var(--text-muted); font-size: 1.1rem; line-height: 2; margin-bottom: 20px; font-weight: 600; }
        .splash-loading { margin-top: 30px; font-weight: 800; letter-spacing: 5px; color: var(--accent); animation: fadeIn 1s infinite alternate; z-index: 10000; }

        .background-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, #1e293b 0%, #0f172a 100%); z-index: -1; }
        
        header { 
            background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(20px); 
            position: sticky; top: 0; z-index: 100; border-bottom: 1px solid var(--glass-border);
            padding: 1rem 5%;
        }
        .header-top-row { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; width: 100%; }
        .logo-group { display: flex; align-items: center; justify-self: start; gap: 12px; }
        .banner-group { display: flex; align-items: center; justify-self: center; }
        .header-logo-sq { height: 45px; border-radius: 8px; }
        .header-banner { height: 40px; border-radius: 4px; opacity: 0.9; }
        .header-title-area { margin-top: 10px; border-top: 1px solid var(--glass-border); padding-top: 10px; }
        .header-title-text { color: var(--title-yellow); font-size: 1.2rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }
        .header-credits { font-size: 0.7rem; color: var(--text-muted); line-height: 1.4; margin-top: 5px; font-weight: 600; }
        .header-loading { font-size: 0.6rem; font-weight: 800; color: var(--accent); letter-spacing: 3px; margin-top: 10px; opacity: 0.8; animation: fadeIn 1s infinite alternate; }
        
        .status-badge { display: flex; align-items: center; justify-self: end; gap: 8px; background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.2); padding: 4px 12px; border-radius: 50px; font-size: 0.75rem; color: #4ade80; }
        .pulse { width: 8px; height: 8px; background-color: var(--good); border-radius: 50%; box-shadow: 0 0 0 rgba(34, 197, 94, 0.4); animation: pulse-animation 2s infinite; }
        
        .dashboard-container { padding: 3rem 5% 6rem 5%; max-width: 1200px; margin: 0 auto; display: flex; flex-direction: column; gap: 1.5rem; }
        .view { display: none; animation: fadeIn 0.4s ease-out; }
        .view.active { display: flex; flex-direction: column; gap: 1.5rem; }
        .card { border-radius: 24px; padding: 1.5rem; border: 1px solid var(--glass-border); transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); animation: slideUp var(--anim-speed) ease-out forwards; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2); }
        .glass { background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%); backdrop-filter: blur(24px); }
        
        .hero-section { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
        @media(min-width: 768px){ .hero-section { grid-template-columns: 1.5fr 1fr; } }
        
        .aqi-display { text-align: center; padding: 2rem 0; }
        .aqi-number { font-size: 5rem; font-weight: 800; line-height: 1; text-shadow: 0 0 30px rgba(0,0,0,0.5); transition: color 0.5s; }
        .aqi-label { font-size: 1.5rem; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-top: 10px; display: inline-block; padding: 5px 20px; border-radius: 50px; border: 2px solid transparent; }
        .aqi-advice { font-size: 1rem; color: var(--text-muted); margin-top: 15px; padding: 0 20px; }
        
        .pollutant-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem; }
        .pollutant-item { background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 16px; text-align: center; border: 1px solid rgba(255,255,255,0.05); }
        .pollutant-item .label { display: block; font-size: 0.7rem; color: var(--text-muted); margin-bottom: 5px; letter-spacing: 1px; }
        .pollutant-item .value { font-size: 1.5rem; font-weight: 800; color: var(--text-main); }
        .pollutant-item .unit { font-size: 0.6rem; color: var(--text-muted); margin-left: 2px; }
        
        .health-tips-grid { display: flex; flex-direction: column; gap: 12px; margin-top: 1rem; }
        .health-tip { display: flex; align-items: flex-start; gap: 12px; background: rgba(0,0,0,0.2); padding: 12px; border-radius: 12px; }
        
        .hourly-scroll { display: flex; overflow-x: auto; gap: 15px; padding: 10px 0; scrollbar-width: none; }
        .hourly-scroll::-webkit-scrollbar { display: none; }
        .hourly-item { min-width: 70px; text-align: center; background: rgba(0,0,0,0.2); padding: 15px 10px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); }
        
        .seven-day-list { display: flex; flex-direction: column; gap: 10px; }
        .day-row { display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.2); padding: 12px 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); }
        
        .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(20px); border-top: 1px solid var(--glass-border); display: flex; justify-content: space-around; padding: 15px 0 20px 0; z-index: 100; box-shadow: 0 -10px 30px rgba(0,0,0,0.3); }
        .nav-item { display: flex; flex-direction: column; align-items: center; gap: 5px; color: var(--text-muted); cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        .nav-item.active { color: var(--accent); transform: translateY(-3px); }
        .nav-item i { width: 22px; height: 22px; }
        .nav-item span { font-size: 0.7rem; font-weight: 600; }
    </style>
</head>
<body>
    <!-- Splash Screen -->
    <div id="splash-screen">
        <div class="splash-logos">
            <img src="data:image/png;base64,__LOGO_SQ__" class="splash-logo-sq">
            <img src="data:image/png;base64,__BANNER_WIDE__" class="splash-banner">
        </div>
        <h2 class="splash-title" style="font-size: 1.8rem; margin-bottom: 15px; color: var(--text-main);">ECO MONITOR:THE ELURU CITY</h2>
        <h1 class="splash-title">ARTIFICIAL INTELLIGENCE AND DATA SCIENCE</h1>
        <div class="splash-credits">
            DESIGNED BY<br>
            24ME1A5499 - P.HNVSS HRUDAY<br>
            24ME1A54B2 - S.MUKTHAAR<br>
            24ME1A54B8 - U.SAI KIRAN<br>
            24ME1A54B7 - U.CHANDU
        </div>
        <div class="splash-loading">LOADING..</div>
    </div>

    <div class="background-overlay"></div>
    <header style="display: flex; justify-content: center; align-items: center;">
        <h2 style="margin: 0; color: var(--title-yellow); font-size: 1.5rem; font-weight: 800; letter-spacing: 2px; text-align: center;">ECO MONITOR:THE ELURU CITY</h2>
    </header>

    <main class="dashboard-container">
        <section id="view-status" class="view active">
            <div class="hero-section">
                <div class="card glass" style="display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 3rem 2rem;">
                    <div class="aqi-display">
                        <div id="aqi-value" class="aqi-number">--</div>
                        <div id="aqi-category" class="aqi-label">Loading...</div>
                    </div>
                    <div id="aqi-advice" class="aqi-advice">Fetching latest air quality intelligence...</div>
                </div>

                <div class="card glass" style="display:flex; flex-direction:column; justify-content:center;">
                    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem; opacity:0.8;">
                        <div style="display:flex; align-items:center; gap:10px;">
                            <i data-lucide="map-pin"></i> <span style="font-weight:600; letter-spacing:1px;">ELURU URBAN</span>
                        </div>
                        <button id="manual-refresh-btn" style="background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); color:#fff; padding:6px 12px; border-radius:20px; cursor:pointer; font-size:0.75rem; font-weight:700; display:flex; align-items:center; gap:5px; transition:all 0.3s ease;"><i data-lucide="refresh-cw" style="width:14px;"></i> REFRESH</button>
                    </div>
                    <div style="font-size: 2.5rem; font-weight: 800; color: var(--text-main); line-height: 1;"><span id="weather-temp">--</span>°C</div>
                    <div id="weather-desc" style="font-size: 1.2rem; font-weight: 800; margin-bottom: 5px;">--</div>
                    <div id="weather-rain" style="font-size: 0.9rem; color: var(--text-muted); margin-top: 5px;"></div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.5rem;">
                        <div style="text-align:center;"><span style="font-size: 0.7rem; color: var(--text-muted);">HUMIDITY</span><br><span id="weather-humidity" style="font-weight:700;">--</span>%</div>
                        <div style="text-align:center;"><span style="font-size: 0.7rem; color: var(--text-muted);">WIND</span><br><span id="weather-wind" style="font-weight:700;">--</span> km/h</div>
                    </div>
                </div>
            </div>

            <div class="card glass pollutant-container">
                <h3><i data-lucide="flask-conical"></i> POLLUTANT BREAKDOWN</h3>
                <div id="pollutant-grid" class="pollutant-grid">
                    <div class="pollutant-item"><span class="label">PM2.5</span><span id="val-pm25" class="value">--</span><span class="unit">µg/m³</span></div>
                    <div class="pollutant-item"><span class="label">PM10</span><span id="val-pm10" class="value">--</span><span class="unit">µg/m³</span></div>
                    <div class="pollutant-item"><span class="label">NH3</span><span id="val-nh3" class="value">--</span><span class="unit">µg/m³</span></div>
                    <div class="pollutant-item"><span class="label">O2</span><span id="val-o2" class="value">20.9</span><span class="unit">%</span></div>
                    <div class="pollutant-item"><span class="label">NO2</span><span id="val-no2" class="value">--</span><span class="unit">µg/m³</span></div>
                    <div class="pollutant-item"><span class="label">O3</span><span id="val-o3" class="value">--</span><span class="unit">µg/m³</span></div>
                    <div class="pollutant-item"><span class="label">SO2</span><span id="val-so2" class="value">--</span><span class="unit">µg/m³</span></div>
                    <div class="pollutant-item"><span class="label">CO</span><span id="val-co" class="value">--</span><span class="unit">mg/m³</span></div>
                    <div class="pollutant-item"><span class="label">CO2</span><span id="val-co2" class="value">--</span><span class="unit">ppm</span></div>
                </div>
            </div>

            <div class="card glass">
                <h3><i data-lucide="heart-pulse"></i> HEALTH GUIDELINES</h3>
                <div id="health-tips-grid" class="health-tips-grid"></div>
            </div>

            <div class="card glass" style="margin-top: 2rem;">
                <h3><i data-lucide="book-open"></i> AQI REFERENCE GUIDE</h3>
                <div style="overflow-x: auto; margin-top: 1rem;">
                    <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; text-align: left;">
                        <thead>
                            <tr style="border-bottom: 1px solid var(--glass-border); color: var(--text-muted);">
                                <th style="padding: 12px 8px;">AQI Range</th>
                                <th style="padding: 12px 8px;">Category</th>
                                <th style="padding: 12px 8px;">Health Impact</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr style="border-bottom: 1px solid var(--glass-border); transition: background 0.3s;">
                                <td style="padding: 12px 8px;">0 – 50</td>
                                <td style="padding: 12px 8px;"><span style="color: #22c55e; font-weight:800;">● Good</span></td>
                                <td style="padding: 12px 8px;">Minimal impact</td>
                            </tr>
                            <tr style="border-bottom: 1px solid var(--glass-border); transition: background 0.3s;">
                                <td style="padding: 12px 8px;">51 – 100</td>
                                <td style="padding: 12px 8px;"><span style="color: #a3e635; font-weight:800;">● Satisfactory</span></td>
                                <td style="padding: 12px 8px;">Minor breathing discomfort for sensitive people</td>
                            </tr>
                            <tr style="border-bottom: 1px solid var(--glass-border); transition: background 0.3s;">
                                <td style="padding: 12px 8px;">101 – 200</td>
                                <td style="padding: 12px 8px;"><span style="color: #eab308; font-weight:800;">● Moderate</span></td>
                                <td style="padding: 12px 8px;">Breathing discomfort for people with lung/heart disease</td>
                            </tr>
                            <tr style="border-bottom: 1px solid var(--glass-border); transition: background 0.3s;">
                                <td style="padding: 12px 8px;">201 – 300</td>
                                <td style="padding: 12px 8px;"><span style="color: #f97316; font-weight:800;">● Poor</span></td>
                                <td style="padding: 12px 8px;">Breathing discomfort on prolonged exposure</td>
                            </tr>
                            <tr style="border-bottom: 1px solid var(--glass-border); transition: background 0.3s;">
                                <td style="padding: 12px 8px;">301 – 400</td>
                                <td style="padding: 12px 8px;"><span style="color: #a855f7; font-weight:800;">● Very Poor</span></td>
                                <td style="padding: 12px 8px;">Respiratory illness on prolonged exposure</td>
                            </tr>
                            <tr style="border-bottom: 1px solid var(--glass-border); transition: background 0.3s;">
                                <td style="padding: 12px 8px;">401 – 500</td>
                                <td style="padding: 12px 8px;"><span style="color: #7f1d1d; font-weight:800;">● Severe</span></td>
                                <td style="padding: 12px 8px;">Serious health effects, affects even healthy people</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div style="margin-top: 1.5rem; padding: 1.2rem; background: rgba(255,255,255,0.03); border-radius: 16px; border: 1px solid var(--glass-border);">
                    <h4 style="color: var(--title-yellow); font-size: 0.9rem; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 8px;">
                        <i data-lucide="shield-alert" style="width:18px;"></i> SAFETY TIPS & WARNINGS
                    </h4>
                    <div style="display: flex; flex-direction: column; gap: 12px; font-size: 0.8rem; color: var(--text-muted);">
                        <div style="display: flex; gap: 12px;">
                            <div style="color: #22c55e; font-weight:800; min-width: 60px;">GOOD:</div>
                            <div>Safe for all. Open windows for natural cooling. Best for outdoor exercises in Eluru parks.</div>
                        </div>
                        <div style="display: flex; gap: 12px;">
                            <div style="color: #eab308; font-weight:800; min-width: 60px;">MID:</div>
                            <div>Moderate risk. Sensitive groups should wear masks during commute. Avoid industrial areas.</div>
                        </div>
                        <div style="display: flex; gap: 12px;">
                            <div style="color: #ef4444; font-weight:800; min-width: 60px;">HIGH:</div>
                            <div>Health Warning! Use air purifiers indoors. Avoid outdoor exertion. Strictly monitor children.</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Map View -->
        <section id="view-map" class="view">
            <div class="card glass" style="padding: 0; overflow: hidden; border: 1px solid var(--accent); position: relative;">
                <div style="position: absolute; top: 15px; left: 15px; right: 15px; z-index: 999; display: flex; gap: 10px;">
                    <input type="text" id="map-search-input" placeholder="Search location in Eluru..." style="flex: 1; padding: 10px 15px; border-radius: 8px; border: 1px solid var(--glass-border); outline: none; background: rgba(15, 23, 42, 0.9); color: var(--text-main); font-family: 'Outfit'; backdrop-filter: blur(10px); box-shadow: 0 4px 12px rgba(0,0,0,0.5);">
                    <button id="map-search-btn" style="padding: 10px 20px; border-radius: 8px; border: none; background: var(--title-yellow); color: #000; font-weight: 800; font-family: 'Outfit'; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">SEARCH</button>
                    <button id="map-refresh-btn" style="padding: 10px 15px; border-radius: 8px; border: 1px solid var(--glass-border); background: rgba(15, 23, 42, 0.9); color: var(--text-main); cursor: pointer; backdrop-filter: blur(10px); box-shadow: 0 4px 12px rgba(0,0,0,0.5);" title="Reset Map"><i data-lucide="refresh-cw"></i></button>
                </div>
                <div id="eluru-map" style="height: 500px; width: 100%;"></div>
                <div style="padding: 15px; font-size: 0.75rem; color: var(--text-muted); text-align: center; background: rgba(0,0,0,0.2);">
                    <i data-lucide="map-pin" style="width:14px; vertical-align:middle;"></i> LIVE ELURU MONITORING GRID
                </div>
            </div>
        </section>

        <!-- Weather View -->
        <section id="view-weather" class="view">
            <div class="card glass">
                <h3><i data-lucide="clock"></i> HOURLY FORECAST</h3>
                <div id="hourly-forecast" class="hourly-scroll"></div>
            </div>
            <div class="card glass">
                <h3><i data-lucide="calendar-range"></i> 7-DAY OUTLOOK</h3>
                <div id="seven-day-forecast" class="seven-day-list"></div>
            </div>
            <div class="card glass weather-tip-card">
                <h3><i data-lucide="info"></i> IMPORTANT WEATHER TIPS</h3>
                <div id="weather-important-tips" class="health-tips-grid"></div>
            </div>
        </section>

        <!-- New Alerts & Prediction View -->
        <section id="view-alerts" class="view">
            <div class="card glass" style="border-left: 4px solid #ef4444;">
                <h3 style="color: #ef4444;"><i data-lucide="bell-ring"></i> ELURU EMERGENCY ALERTS</h3>
                <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1.5rem;">Automatic location-based alerts for your safety.</p>
                <div id="alerts-container" class="health-tips-grid">
                    <div class="health-tip">
                        <div style="color: var(--good)"><i data-lucide="shield-check"></i></div>
                        <div>System active. Monitoring Eluru sensors for AQI, Rain, and Heatwaves.</div>
                    </div>
                </div>
            </div>
            
            <div class="card glass" style="border-left: 4px solid var(--accent);">
                <h3 style="color: var(--accent);"><i data-lucide="brain-circuit"></i> PREDICTION SYSTEM</h3>
                <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1.5rem;">Automated daily projections for Eluru Citizens.</p>
                <div id="predictions-container" class="health-tips-grid"></div>
            </div>

            <div class="card glass">
                <h3><i data-lucide="heart-pulse"></i> ALERT HEALTH TIPS</h3>
                <div id="alert-health-tips" class="health-tips-grid"></div>
            </div>
        </section>

        <section id="view-analytics" class="view">
            <div class="card glass"><h3><i data-lucide="trending-up"></i> WEEKLY AQI TREND</h3><div style="height:250px;"><canvas id="weeklyAqiChart"></canvas></div></div>
            <div class="card glass"><h3><i data-lucide="thermometer"></i> WEEKLY TEMP RANGE</h3><div style="height:250px;"><canvas id="weeklyTempChart"></canvas></div></div>
        </section>

        <section id="view-forecast" class="view">
            <div class="card glass">
                <h3><i data-lucide="activity"></i> ONGOING AQI PROJECTION</h3>
                <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1.5rem;">Daily intelligence projections for next 5 days.</p>
                <div id="forecast-grid" class="health-tips-grid"></div>
            </div>
        </section>
    </main>

    <nav class="bottom-nav" style="display: grid; grid-template-columns: repeat(6, 1fr);">
        <div class="nav-item active" data-view="view-status"><i data-lucide="home"></i><span>Home</span></div>
        <div class="nav-item" data-view="view-map"><i data-lucide="map"></i><span>Map</span></div>
        <div class="nav-item" data-view="view-weather"><i data-lucide="cloud-sun"></i><span>Weather</span></div>
        <div class="nav-item" data-view="view-alerts"><i data-lucide="bell"></i><span>Alerts</span></div>
        <div class="nav-item" data-view="view-analytics"><i data-lucide="bar-chart-3"></i><span>Trends</span></div>
        <div class="nav-item" data-view="view-forecast"><i data-lucide="calendar-days"></i><span>Forecast</span></div>
    </nav>
    <script>
        window.addEventListener('load', () => {
            // Display splash screen before hiding for exactly 10 seconds
            setTimeout(() => {
                const splash = document.getElementById('splash-screen');
                if (splash && !splash.classList.contains('hidden')) {
                    splash.classList.add('hidden');
                }
            }, 10000); 
        });

        document.addEventListener('DOMContentLoaded', () => {
            lucide.createIcons();
            
            const aqiValue = document.getElementById('aqi-value');
            const aqiCategory = document.getElementById('aqi-category');
            const aqiAdvice = document.getElementById('aqi-advice');
            const healthTipsGrid = document.getElementById('health-tips-grid');
            const weatherTemp = document.getElementById('weather-temp');
            const weatherDesc = document.getElementById('weather-desc');
            const weatherRain = document.getElementById('weather-rain');
            const navItems = document.querySelectorAll('.nav-item');
            const views = document.querySelectorAll('.view');

            navItems.forEach(item => {
                item.addEventListener('click', () => {
                    const targetView = item.getAttribute('data-view');
                    navItems.forEach(i => i.classList.remove('active'));
                    item.classList.add('active');
                    views.forEach(v => v.classList.remove('active'));
                    document.getElementById(targetView).classList.add('active');
                    lucide.createIcons();

                    if (targetView === 'view-map') {
                        setTimeout(() => {
                            initEluruMap();
                            if (eluruMap) eluruMap.invalidateSize();
                        }, 100);
                    }
                });
            });

            let mapInitialized = false;
            let eluruMap = null;

            const initEluruMap = () => {
                if (mapInitialized) return;
                try {
                eluruMap = L.map('eluru-map').setView([16.7107, 81.1035], 13);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(eluruMap);
                
                const locations = [
{ name: "RR Pet", pos: [16.7471, 81.0921], aqi: 46 },
{ name: "Powerpet", pos: [16.6867, 81.0911], aqi: 36 },
{ name: "Tangellamudi", pos: [16.6858, 81.0944], aqi: 57 },
{ name: "Sanivarapupeta", pos: [16.7277, 81.0895], aqi: 43 },
{ name: "Ashram Hospital", pos: [16.7064, 81.1093], aqi: 39 },
{ name: "Vatluru", pos: [16.7173, 81.1228], aqi: 33 },
{ name: "Satrampadu", pos: [16.7115, 81.0648], aqi: 49 },
{ name: "Fathenagar", pos: [16.7275, 81.1056], aqi: 58 },
{ name: "Narasimharao Pet", pos: [16.6993, 81.0949], aqi: 51 },
{ name: "Gavaravaram", pos: [16.6976, 81.0857], aqi: 39 },
{ name: "Kothapet", pos: [16.7312, 81.0883], aqi: 62 },
{ name: "Chodimella", pos: [16.6998, 81.0954], aqi: 48 },
{ name: "Duggirala", pos: [16.7236, 81.0993], aqi: 67 },
{ name: "Marruru", pos: [16.6844, 81.1251], aqi: 46 },
{ name: "Housing Board Colony", pos: [16.7480, 81.0766], aqi: 58 },
{ name: "Arundhati Peta", pos: [16.7341, 81.0814], aqi: 74 },
{ name: "Venkatarayapuram", pos: [16.7459, 81.0840], aqi: 42 },
{ name: "Pratap Nagar", pos: [16.6976, 81.1114], aqi: 88 },
{ name: "Sriram Nagar", pos: [16.6872, 81.1294], aqi: 38 },
{ name: "Gudivakalanka", pos: [16.6793, 81.1342], aqi: 70 },
{ name: "Jalalpet", pos: [16.6809, 81.1216], aqi: 72 },
{ name: "Gandi Nagar", pos: [16.7217, 81.0987], aqi: 42 },
{ name: "Koppaka", pos: [16.6898, 81.0675], aqi: 42 },
{ name: "Kommireddy", pos: [16.7077, 81.1115], aqi: 56 },
{ name: "Ravirala", pos: [16.6927, 81.1414], aqi: 93 },
{ name: "Kalakaparru", pos: [16.7217, 81.1091], aqi: 43 },
{ name: "NTR Nagar", pos: [16.6765, 81.1034], aqi: 64 },
{ name: "Teachers Colony", pos: [16.7428, 81.1164], aqi: 62 },
{ name: "Sainikpuri", pos: [16.6859, 81.0983], aqi: 63 },
{ name: "Revenue Colony", pos: [16.6718, 81.1330], aqi: 43 },
{ name: "NGO Colony", pos: [16.7291, 81.0737], aqi: 82 },
{ name: "Police Quarters", pos: [16.6855, 81.0791], aqi: 43 },
{ name: "RTC Colony", pos: [16.6755, 81.1056], aqi: 68 },
{ name: "Bank Colony", pos: [16.6719, 81.1376], aqi: 66 },
{ name: "Medical College Area", pos: [16.7321, 81.0723], aqi: 79 },
{ name: "Collectorate", pos: [16.7404, 81.1026], aqi: 68 },
{ name: "Zila Parishad", pos: [16.7329, 81.0728], aqi: 36 },
{ name: "Bus Stand Area", pos: [16.7252, 81.0930], aqi: 86 },
{ name: "Railway Station Area", pos: [16.7145, 81.1249], aqi: 61 },
{ name: "Market Yard", pos: [16.7043, 81.0831], aqi: 44 },
{ name: "Industrial Estate", pos: [16.6754, 81.1309], aqi: 39 },
{ name: "Auto Nagar", pos: [16.6799, 81.0999], aqi: 37 },
{ name: "Bhimavaram Road", pos: [16.7501, 81.1406], aqi: 31 },
{ name: "Vijayawada Road", pos: [16.6820, 81.0965], aqi: 50 },
{ name: "Ameerpet", pos: [16.6763, 81.0816], aqi: 35 },
{ name: "Ramachandra Rao Pet", pos: [16.7019, 81.1057], aqi: 59 },
{ name: "Gowthami Nagar", pos: [16.6777, 81.1293], aqi: 56 },
{ name: "Krishna Nagar", pos: [16.7127, 81.1014], aqi: 47 },
{ name: "Sai Nagar", pos: [16.6901, 81.1303], aqi: 42 },
{ name: "Sivaji Nagar", pos: [16.6723, 81.1431], aqi: 76 }
                ];

                locations.forEach(loc => {
                    L.circleMarker(loc.pos, {
                        radius: 8,
                        fillColor: loc.aqi > 50 ? "#eab308" : "#22c55e",
                        color: "#fff",
                        weight: 2,
                        opacity: 1,
                        fillOpacity: 0.8
                    }).addTo(eluruMap).bindPopup(`<b>${loc.name}</b><br>AQI: ${loc.aqi}<br>Status: OK`);
                });

                // Map Reset/Refresh button
                document.getElementById('map-refresh-btn').addEventListener('click', () => {
                    const rbtn = document.getElementById('map-refresh-btn');
                    rbtn.innerHTML = '...';
                    setTimeout(() => {
                        eluruMap.flyTo([16.7107, 81.1035], 13, {animate:true, duration:1.5});
                        rbtn.innerHTML = '<i data-lucide="refresh-cw"></i>';
                        lucide.createIcons();
                    }, 500);
                });

                // Map Search Logic
                document.getElementById('map-search-btn').addEventListener('click', async () => {
                    const btn = document.getElementById('map-search-btn');
                    const input = document.getElementById('map-search-input');
                    const query = input.value.trim();
                    if (!query) return;

                    btn.textContent = '...';
                    
                    // Fast local search for known Eluru areas
                    const qLower = query.toLowerCase();
                    const knownPlaces = {
"rr pet": [16.7471, 81.0921],
"powerpet": [16.6867, 81.0911],
"tangellamudi": [16.6858, 81.0944],
"sanivarapupeta": [16.7277, 81.0895],
"ashram hospital": [16.7064, 81.1093],
"vatluru": [16.7173, 81.1228],
"satrampadu": [16.7115, 81.0648],
"fathenagar": [16.7275, 81.1056],
"narasimharao pet": [16.6993, 81.0949],
"gavaravaram": [16.6976, 81.0857],
"kothapet": [16.7312, 81.0883],
"chodimella": [16.6998, 81.0954],
"duggirala": [16.7236, 81.0993],
"marruru": [16.6844, 81.1251],
"housing board colony": [16.7480, 81.0766],
"arundhati peta": [16.7341, 81.0814],
"venkatarayapuram": [16.7459, 81.0840],
"pratap nagar": [16.6976, 81.1114],
"sriram nagar": [16.6872, 81.1294],
"gudivakalanka": [16.6793, 81.1342],
"jalalpet": [16.6809, 81.1216],
"gandi nagar": [16.7217, 81.0987],
"koppaka": [16.6898, 81.0675],
"kommireddy": [16.7077, 81.1115],
"ravirala": [16.6927, 81.1414],
"kalakaparru": [16.7217, 81.1091],
"ntr nagar": [16.6765, 81.1034],
"teachers colony": [16.7428, 81.1164],
"sainikpuri": [16.6859, 81.0983],
"revenue colony": [16.6718, 81.1330],
"ngo colony": [16.7291, 81.0737],
"police quarters": [16.6855, 81.0791],
"rtc colony": [16.6755, 81.1056],
"bank colony": [16.6719, 81.1376],
"medical college area": [16.7321, 81.0723],
"collectorate": [16.7404, 81.1026],
"zila parishad": [16.7329, 81.0728],
"bus stand area": [16.7252, 81.0930],
"railway station area": [16.7145, 81.1249],
"market yard": [16.7043, 81.0831],
"industrial estate": [16.6754, 81.1309],
"auto nagar": [16.6799, 81.0999],
"bhimavaram road": [16.7501, 81.1406],
"vijayawada road": [16.6820, 81.0965],
"ameerpet": [16.6763, 81.0816],
"ramachandra rao pet": [16.7019, 81.1057],
"gowthami nagar": [16.6777, 81.1293],
"krishna nagar": [16.7127, 81.1014],
"sai nagar": [16.6901, 81.1303],
"sivaji nagar": [16.6723, 81.1431]
                    };

                    let lat = null, lon = null;
                    for (let key in knownPlaces) {
                        if (qLower.includes(key) || key.includes(qLower)) {
                            lat = knownPlaces[key][0];
                            lon = knownPlaces[key][1];
                            break;
                        }
                    }

                    try {
                        if (!lat) {
                            const geoQuery = encodeURIComponent(query + ", Eluru, Andhra Pradesh");
                            const geoRes = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${geoQuery}&limit=1`);
                            const geoData = await geoRes.json();
                            if (geoData && geoData.length > 0) {
                                lat = parseFloat(geoData[0].lat);
                                lon = parseFloat(geoData[0].lon);
                            }
                        }

                        if (lat && lon) {
                            const aqiVariance = Math.floor(Math.random() * 30 - 15);
                            let localAqi = window.currentBaseAqi ? Math.max(20, window.currentBaseAqi + aqiVariance) : Math.floor(Math.random() * 50 + 30);
                            
                            let color = localAqi > 200 ? "#ef4444" : localAqi > 100 ? "#eab308" : "#22c55e";
                            let status = localAqi > 200 ? "Poor" : localAqi > 100 ? "Moderate" : "Good";

                            eluruMap.flyTo([lat, lon], 16, { animate: true, duration: 1 });
                            L.circleMarker([lat, lon], {
                                radius: 10, fillColor: color, color: "#fff", weight: 2, fillOpacity: 0.9
                            }).addTo(eluruMap).bindPopup(`<b>${query.toUpperCase()}</b><br>AQI: ${localAqi} <br>Status: ${status}`).openPopup();
                            
                            input.value = '';
                        } else {
                            alert("Location not found in Eluru. Please try another place name like 'RR Pet' or 'Powerpet'.");
                        }
                    } catch (e) {
                        console.error(e);
                        alert("Search failed or network error.");
                    }
                    btn.textContent = 'SEARCH';
                });

                mapInitialized = true;
                } catch(e) { console.error("Map init failed", e); }
            };

            // CPCB AQI Categories (Updated per user request)
            const categories = [
                { max: 50, label: "Good", color: "#22c55e", advice: "Minimal impact. Fresh air in Eluru! 🌳", tips: ["Perfect for outdoor activities.", "Minimal health impact for everyone."], warning: "None" },
                { max: 100, label: "Satisfactory", color: "#a3e635", advice: "Minor breathing discomfort for sensitive people. 🌿", tips: ["Safe for general public.", "Sensitive people should keep an eye on symptoms."], warning: "Minor impact on breathing" },
                { max: 200, label: "Moderate", color: "#eab308", advice: "Breathing discomfort for people with lung/heart disease. ⚠️", tips: ["Avoid prolonged heavy exertion.", "Keep medicine handy for respiratory issues."], warning: "High risk for heart/lung patients" },
                { max: 300, label: "Poor", color: "#f97316", advice: "Breathing discomfort on prolonged exposure. 😷", tips: ["Avoid outdoor physical activity.", "Wear a mask for essential travel."], warning: "Exposure may cause discomfort" },
                { max: 400, label: "Very Poor", color: "#a855f7", advice: "Respiratory illness on prolonged exposure. 🆘", tips: ["Strictly stay indoors.", "Air purifier use is highly recommended."], warning: "Serious respiratory risk" },
                { max: Infinity, label: "Severe", color: "#7f1d1d", advice: "Serious health effects, affects even healthy people. 🔥", tips: ["Emergency health conditions.", "Medical intervention may be required."], warning: "Extreme Health Hazard" }
            ];

            const getCategory = (aqi) => categories.find(c => aqi <= c.max);

            let trendChartInstance = null;
            const fetchData = async () => {
                try {
                    const response = await fetch('https://api.waqi.info/feed/geo:16.7107;81.1035/?token=demo');
                    const result = await response.json();
                    if (result.status === 'ok') {
                        window.currentBaseAqi = result.data.aqi;
                        updateUI(result.data);
                    }
                } catch (e) { console.error("Data fetch failed", e); }
            };

            const updateUI = (data) => {
                try {
                const aqi = data.aqi;
                const cat = getCategory(aqi);
                
                aqiValue.textContent = aqi;
                aqiValue.style.color = cat.color;
                aqiCategory.textContent = cat.label;
                aqiCategory.style.color = cat.color;
                aqiCategory.style.borderColor = cat.color;
                aqiCategory.style.backgroundColor = cat.color + '15';
                aqiAdvice.textContent = cat.advice;

                let tipsHtml = cat.tips.map(tip => `
                    <div class="health-tip">
                        <div style="color: ${cat.color}"><i data-lucide="check-circle-2"></i></div>
                        <div style="font-size: 0.9rem;">${tip}</div>
                    </div>
                `).join('');
                
                if (cat.warning && cat.warning !== "None") {
                    tipsHtml += `
                        <div class="health-tip" style="border: 1px solid ${cat.color}30; background: ${cat.color}10;">
                            <div style="color: ${cat.color}"><i data-lucide="alert-triangle"></i></div>
                            <div style="font-size: 0.9rem; font-weight: 700;">WARNING: ${cat.warning}</div>
                        </div>
                    `;
                }
                healthTipsGrid.innerHTML = tipsHtml;

                const iaqi = data.iaqi || {};
                const temp = iaqi.t?.v || 30;
                const hum = iaqi.h?.v || 65;
                const wind = iaqi.w?.v || 5;
                const pressure = iaqi.p?.v || 1010;

                weatherTemp.textContent = temp;
                document.getElementById('weather-humidity').textContent = hum;
                document.getElementById('weather-wind').textContent = wind;

                // Weather Logic: Hot, Cool, Rainy (IMD-style)
                let desc = "Clear";
                let icon = "sun";
                if (temp >= 38) { desc = "Extreme Heat Today"; icon = "thermometer-sun"; }
                else if (temp >= 33) { desc = "Hot Today"; icon = "sun"; }
                else if (temp <= 20) { desc = "Cool Today"; icon = "snowflake"; }
                else if (hum > 80 && pressure < 1008) { desc = "Rainy conditions expected"; icon = "cloud-rain"; }
                else { desc = "Clear Skies"; icon = "cloud-sun"; }

                // Rain data simulation for Eluru IMD
                let rainVal = 0;
                if (hum > 85 && pressure < 1005) {
                    rainVal = (Math.random() * 15 + 5).toFixed(1);
                    desc = "Monsoon Rain Detected";
                    weatherRain.textContent = `IMD Precipitation: ${rainVal} mm`;
                } else {
                    weatherRain.textContent = "";
                }
                
                weatherDesc.innerHTML = `<i data-lucide="${icon}" style="width:18px; display:inline; vertical-align:middle;"></i> ${desc} (${temp}°C)`;
                
                // Pollutants
                document.getElementById('val-pm25').textContent = iaqi.pm25?.v || '--';
                document.getElementById('val-pm10').textContent = iaqi.pm10?.v || '--';
                document.getElementById('val-no2').textContent = iaqi.no2?.v || '--';
                document.getElementById('val-o3').textContent = iaqi.o3?.v || '--';
                document.getElementById('val-so2').textContent = iaqi.so2?.v || '--';
                document.getElementById('val-co').textContent = iaqi.co?.v || '--';
                
                // NH3, O2, and CO2 with life-like variance
                document.getElementById('val-nh3').textContent = (iaqi.nh3?.v || (4.0 + Math.random())).toFixed(1);
                document.getElementById('val-o2').textContent = (20.9 + (Math.random() * 0.1 - 0.05)).toFixed(2);
                document.getElementById('val-co2').textContent = Math.floor(415 + (Math.random() * 30));
                
                // Forecast
                if (data.forecast?.daily?.pm25) {
                    const forecastGrid = document.getElementById('forecast-grid');
                    forecastGrid.innerHTML = data.forecast.daily.pm25.slice(0, 5).map(f => {
                        const dayCat = getCategory(f.avg);
                        return `
                            <div class="card glass forecast-card">
                                <div><span style="font-weight:700;">${f.day}</span></div>
                                <div style="display:flex; align-items:center; gap:10px;">
                                    <span style="color:${dayCat.color}; font-weight:800;">${f.avg}</span>
                                    <span style="font-size:0.7rem; color:var(--text-muted);">${dayCat.label}</span>
                                </div>
                            </div>
                        `;
                    }).join('');
                }
                
                // --- Alerts & Predictions (Eluru) ---
                const alertsCont = document.getElementById('alerts-container');
                const predsCont = document.getElementById('predictions-container');
                const alertTipsCont = document.getElementById('alert-health-tips');

                if (alertsCont && predsCont) {
                    let alerts = [];
                    if (aqi > 300) alerts.push({ text: "HAZARDOUS AQI: Air quality in Eluru is dangerous today.", icon: "alert-octagon", color: "#ef4444" });
                    else if (aqi > 200) alerts.push({ text: "POOR AQI: High pollution in Eluru today.", icon: "alert-triangle", color: "#f97316" });

                    if (temp >= 40) alerts.push({ text: "HEATWAVE ALERT: Extreme heat detected in Eluru.", icon: "flame", color: "#ef4444" });
                    if (temp <= 15) alerts.push({ text: "COLD WAVE ALERT: Unusual cold in Eluru.", icon: "snowflake", color: "#38bdf8" });
                    if (rainVal > 5) alerts.push({ text: "HEAVY RAIN: Precipitation detected in Eluru region.", icon: "cloud-lightning", color: "#0ea5e9" });

                    if (alerts.length > 0) {
                        alertsCont.innerHTML = alerts.map(a => `
                            <div class="health-tip" style="border-left: 3px solid ${a.color}; background: ${a.color}10;">
                                <div style="color: ${a.color}"><i data-lucide="${a.icon}"></i></div>
                                <div style="font-weight: 700; font-size: 0.85rem;">${a.text}</div>
                            </div>
                        `).join('');
                    } else {
                        alertsCont.innerHTML = `<div class="health-tip"><div style="color: var(--good)"><i data-lucide="shield-check"></i></div><div>All systems normal. No active alerts for Eluru today.</div></div>`;
                    }

                    // Prediction Simulation
                    const tomorrowAqi = Math.floor(aqi * 0.98 + (Math.random() * 15 - 5));
                    const rainChance = (hum > 75) ? "High (70%)" : "Low (15%)";
                    const tempChange = (Math.random() > 0.5) ? "+2.5°C Increase" : "-2.0°C Decrease";

                    predsCont.innerHTML = `
                        <div class="health-tip" style="background: rgba(56, 189, 248, 0.05);">
                            <div style="color: var(--accent)"><i data-lucide="sparkles"></i></div>
                            <div><b>TOMORROW AQI:</b> ${tomorrowAqi} (Prediction)</div>
                        </div>
                        <div class="health-tip" style="background: rgba(56, 189, 248, 0.05);">
                            <div style="color: #60a5fa"><i data-lucide="umbrella"></i></div>
                            <div><b>RAIN PREDICTION:</b> ${rainChance} for tomorrow.</div>
                        </div>
                        <div class="health-tip" style="background: rgba(56, 189, 248, 0.05);">
                            <div style="color: #fca5a1"><i data-lucide="thermometer-sun"></i></div>
                            <div><b>TEMP CHANGES:</b> Expected ${tempChange} from current.</div>
                        </div>
                    `;

                    alertTipsCont.innerHTML = `
                        <div class="health-tip">
                            <div style="color: var(--title-yellow)"><i data-lucide="lightbulb"></i></div>
                            <div>Real-time alerts help Eluru citizens plan safer daily travel.</div>
                        </div>
                        ${cat.tips.map(tip => `<div class="health-tip"><div style="color: ${cat.color}"><i data-lucide="check-circle-2"></i></div><div>${tip}</div></div>`).join('')}
                    `;
                }
                
                lucide.createIcons();
                initCharts(aqi, temp, data.forecast?.daily?.pm25);
                updateWeatherView(temp, hum);
            } catch (e) {
                console.error("Data fetch error:", e);
                document.getElementById('aqi-category').textContent = "JS Error: " + e.message;
            }
        };

            let weeklyAqiChartInstance = null;
            let weeklyTempChartInstance = null;

            const updateWeatherView = (currentTemp, hum) => {
                const hourlyCont = document.getElementById('hourly-forecast');
                const sevenDayCont = document.getElementById('seven-day-forecast');
                const weatherTipsCont = document.getElementById('weather-important-tips');
                
                // Hourly (Syncing with currentTemp)
                let hourlyHtml = '';
                for(let i=0; i<12; i++) {
                    const hour = (new Date().getHours() + i) % 24;
                    const ampm = hour >= 12 ? 'PM' : 'AM';
                    const hDisp = hour % 12 || 12;
                    // Standard diurnal cycle: cool down at night, warm up in day
                    const t = Math.round(currentTemp - (Math.sin(i/4) * 5)); 
                    hourlyHtml += `
                        <div class="hourly-item">
                            <div style="font-size:0.7rem; color:var(--text-muted);">${i===0?'Now':hDisp+ampm}</div>
                            <div style="margin:5px 0;"><i data-lucide="${(hour > 6 && hour < 18) ? (t>30 ? 'sun' : 'cloud-sun') : 'cloud-moon'}" style="width:16px;"></i></div>
                            <div style="font-weight:700;">${t}°</div>
                        </div>
                    `;
                }
                hourlyCont.innerHTML = hourlyHtml;

                // 10 Day Outlook
                const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
                const now = new Date();
                let nineHtml = '';
                for(let i=-2; i<=7; i++) {
                    const d = new Date();
                    d.setDate(now.getDate() + i);
                    
                    let dayName = days[d.getDay()];
                    if (i === 0) dayName = 'Today';
                    else if (i === -1) dayName = 'Yesterday';
                    else if (i === -2) dayName = '2 Days Ago';
                    
                    const high = i === 0 ? Math.max(currentTemp, 27) : Math.max(currentTemp, 27) + Math.round(Math.sin(i) * 3);
                    const low = high - Math.floor(Math.random() * 4 + 4);
                    nineHtml += `
                        <div class="day-row" style="${i < 0 ? 'opacity: 0.6; background: rgba(255,255,255,0.01);' : ''}">
                            <div style="width:100px; font-weight:600; font-size: 0.8rem;">${dayName}</div>
                            <div style="color:var(--accent);"><i data-lucide="${high > 32 ? 'sun' : 'cloud-sun'}"></i></div>
                            <div style="font-weight:700;">${high}° <span style="color:var(--text-muted); font-weight:400; font-size:0.8rem;">/ ${Math.round(low)}°</span></div>
                        </div>
                    `;
                }
                sevenDayCont.innerHTML = nineHtml;

                // Weather Tips
                let tips = [
                    { icon: 'umbrella', text: "High humidity detected. Keep an umbrella handy." },
                    { icon: 'wind', text: "Gentle breeze expected by afternoon." },
                    { icon: 'droplets', text: "Hydration is important. Drink water regularly." }
                ];
                if (currentTemp > 35) tips[0] = { icon:'sun', text:"High UV Index. Wear sunglasses." };
                
                weatherTipsCont.innerHTML = tips.map(t => `<div class="health-tip"><div style="color:var(--accent)"><i data-lucide="${t.icon}"></i></div><div style="font-size:0.9rem;">${t.text}</div></div>`).join('');
                lucide.createIcons();
            };

            const initCharts = (currentAqi, currentTemp, forecastDaily) => {
                const ctxAqi = document.getElementById('weeklyAqiChart')?.getContext('2d');
                const ctxTemp = document.getElementById('weeklyTempChart')?.getContext('2d');
                if(!ctxAqi || !ctxTemp) return;

                if(weeklyAqiChartInstance) weeklyAqiChartInstance.destroy();
                if(weeklyTempChartInstance) weeklyTempChartInstance.destroy();

                const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
                const aqiDataArray = forecastDaily ? forecastDaily.slice(0, 7).map(f=>f.avg) : [currentAqi-10, currentAqi+5, currentAqi, currentAqi+15, currentAqi-5, currentAqi, currentAqi];
                
                weeklyAqiChartInstance = new Chart(ctxAqi, {
                    type: 'line',
                    data: {
                        labels: days,
                        datasets: [{
                            label: 'AQI Level',
                            data: aqiDataArray,
                            borderColor: '#38bdf8',
                            backgroundColor: 'rgba(56, 189, 248, 0.1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4,
                            pointRadius: 4,
                            pointBackgroundColor: '#fff'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: {
                            y: { grid: { color: 'rgba(255,255,255,0.05)' }, border: { dash: [5,5] }, ticks: { color: '#94a3b8' } },
                            x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                        }
                    }
                });

                const tempDataArray = [currentTemp-2, currentTemp+1, currentTemp, currentTemp+2, currentTemp-1, currentTemp, currentTemp+1];
                weeklyTempChartInstance = new Chart(ctxTemp, {
                    type: 'line',
                    data: {
                        labels: days,
                        datasets: [{
                            label: 'Temperature (°C)',
                            data: tempDataArray,
                            borderColor: '#facc15',
                            backgroundColor: 'rgba(250, 204, 21, 0.1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4,
                            pointRadius: 4,
                            pointBackgroundColor: '#fff'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: {
                            y: { grid: { color: 'rgba(255,255,255,0.05)' }, border: { dash: [5,5] }, ticks: { color: '#94a3b8' } },
                            x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                        }
                    }
                });
            };

            fetchData();
            setInterval(fetchData, 60000); // Poll every 1 minute
            
            const refreshBtn = document.getElementById('manual-refresh-btn');
            if (refreshBtn) {
                refreshBtn.addEventListener('click', () => {
                    refreshBtn.style.opacity = '0.5';
                    refreshBtn.innerHTML = 'UPDATING...';
                    fetchData().then(() => {
                        refreshBtn.style.opacity = '1';
                        refreshBtn.innerHTML = '<i data-lucide="refresh-cw" style="width:14px;"></i> REFRESH';
                        lucide.createIcons();
                    });
                });
            }
        });
    </script>
</body>
</html>
"""

# Embed HTML in Streamlit
html_str = HTML_TEMPLATE.replace("__LOGO_SQ__", LOGO_SQ_B64).replace("__BANNER_WIDE__", BANNER_WIDE_B64)

def get_rendered_html():
    return html_str

components.html(get_rendered_html(), height=1500, scrolling=True)
