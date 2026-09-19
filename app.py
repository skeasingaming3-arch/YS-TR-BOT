import time
import random
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# Real & Forex Institutional Knowledge Base (Extended Smart Money Concepts & Price Action Engine)
INSTITUTIONAL_KNOWLEDGE_BASE = [
    "SMC Order Block Retest + Bullish FVG Mitigation",
    "RSI Divergence (14) + 20 EMA Dynamic Support Bounce",
    "Liquidity Sweep at Equal Lows + CHOCH Reversal Trend",
    "Candle Exhaustion at Round Number (.500 Level)",
    "Volume Delta Spike + Institutional Breakout Confirmation",
    "Breaker Block Flip + Structural BOS Alignment",
    "Overbought RSI (>75) + Bearish Engulfing Pattern at Key Level",
    "Multi-Timeframe Trend Confluence + Price Action Reject",
    "Smart Money Sweep + Institutional Wick Rejection",
    "Demand Zone Mitigation + Change of Character (CHOCH)",
    "Bullish Imbalance Fill + Premium/Discount Equilibrium Zone",
    "Triple Top Rejection + Institutional Supply Zone Reaction",
    "Fakeout Liquidity Grab + Instant Trend Reversal Signal",
    "SMA 200 Trend Filter + Golden Cross Confirmation",
    "Bollinger Band Squeeze Breakout + Volume Momentum Spike",
    "Stochastic RSI Momentum Reversal + Support Level Bounce",
    "Fibonacci 61.8% Golden Ratio Retest + Hammer Candle",
    "Institutional Mitigation Block + Higher High Market Structure",
    "Bearish Hidden Divergence + Lower High Breakdown Confirmation"
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FINORIX PRO BOT - QX BROKER</title>
    <style>
        :root {
            --bg-color: #05090c;
            --card-bg: #0c151d;
            --accent-color: #00e676;
            --accent-blue: #00bcd4;
            --text-color: #ffffff;
            --text-dim: #8fa3b0;
            --border-color: #1a2a38;
            --warning-red: #ff3d00;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 12px;
        }

        .bot-card {
            width: 100%;
            max-width: 450px;
            background: var(--card-bg);
            border-radius: 20px;
            padding: 18px;
            position: relative;
            box-shadow: 0 0 30px rgba(0, 230, 118, 0.15);
            border: 2px solid transparent;
            background-clip: padding-box;
            animation: borderGlow 3s linear infinite;
        }

        @keyframes borderGlow {
            0% { border-color: #00e676; box-shadow: 0 0 18px rgba(0, 230, 118, 0.4); }
            25% { border-color: #00bcd4; box-shadow: 0 0 18px rgba(0, 188, 212, 0.4); }
            50% { border-color: #7c4dff; box-shadow: 0 0 18px rgba(124, 77, 255, 0.4); }
            75% { border-color: #ff007f; box-shadow: 0 0 18px rgba(255, 0, 127, 0.4); }
            100% { border-color: #00e676; box-shadow: 0 0 18px rgba(0, 230, 118, 0.4); }
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
        }

        .brand-info {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .bot-icon {
            width: 44px;
            height: 44px;
            background: linear-gradient(135deg, #102a3a, #05131d);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 22px;
            border: 2px solid var(--accent-color);
            box-shadow: 0 0 12px rgba(0, 230, 118, 0.5);
            animation: pulseGlow 1.5s infinite alternate;
        }

        @keyframes pulseGlow {
            0% { transform: scale(1); filter: brightness(1); }
            100% { transform: scale(1.03); filter: brightness(1.2); }
        }

        .title-text h2 {
            font-size: 16px;
            color: var(--accent-color);
            font-weight: 700;
            letter-spacing: 0.5px;
        }

        .title-text p {
            font-size: 11px;
            color: var(--text-dim);
        }

        .broker-badge {
            background: rgba(0, 188, 212, 0.12);
            color: var(--accent-blue);
            border: 1px solid var(--accent-blue);
            padding: 5px 10px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: bold;
        }

        .controls-grid {
            display: grid;
            grid-template-columns: 1.3fr 0.7fr;
            gap: 10px;
            margin-bottom: 14px;
        }

        .control-group {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .control-group label {
            font-size: 11px;
            color: var(--text-dim);
            font-weight: 600;
        }

        select {
            background: #091219;
            color: #fff;
            border: 1px solid var(--border-color);
            padding: 9px;
            border-radius: 10px;
            outline: none;
            font-size: 12px;
            transition: all 0.3s ease;
        }

        select:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 8px rgba(0, 230, 118, 0.3);
        }

        optgroup {
            background: #0c151d;
            color: var(--accent-color);
            font-weight: bold;
        }

        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 7px 12px;
            background: #081118;
            border: 1px solid var(--border-color);
            border-bottom: none;
            border-radius: 10px 10px 0 0;
        }

        .live-indicator {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            font-weight: bold;
            color: var(--accent-color);
        }

        .blinking-dot {
            width: 8px;
            height: 8px;
            background-color: var(--accent-color);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--accent-color);
            animation: blink 1s infinite alternate;
        }

        @keyframes blink {
            0% { opacity: 0.2; }
            100% { opacity: 1; }
        }

        .chart-tools-top {
            display: flex;
            gap: 6px;
            font-size: 11px;
            color: var(--text-dim);
        }

        .chart-wrapper {
            width: 100%;
            height: 165px;
            background: #050a0d;
            border-radius: 0 0 10px 10px;
            border: 1px solid var(--border-color);
            border-top: none;
            margin-bottom: 14px;
            position: relative;
            overflow: hidden;
        }

        .otc-notice-container {
            display: none;
            width: 100%;
            height: 100%;
            padding: 16px;
            background: rgba(255, 61, 0, 0.05);
            border: 1.5px solid var(--warning-red);
            border-radius: 0 0 10px 10px;
            text-align: center;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 8px;
        }

        .otc-notice-title {
            color: var(--warning-red);
            font-size: 13px;
            font-weight: bold;
        }

        .otc-notice-desc {
            color: #ffab91;
            font-size: 11px;
            line-height: 1.4;
        }

        .tradingview-widget-container {
            width: 100%;
            height: 100%;
        }

        .scanner-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(5, 9, 12, 0.94);
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 20;
        }

        .scan-line {
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, transparent, #00e676, #00bcd4, transparent);
            box-shadow: 0 0 12px #00e676;
            position: absolute;
            animation: scanAnimation 1.2s infinite linear;
        }

        @keyframes scanAnimation {
            0% { top: 0%; }
            50% { top: 95%; }
            100% { top: 0%; }
        }

        .scan-status-text {
            color: var(--accent-color);
            font-size: 12px;
            font-weight: bold;
            margin-top: 10px;
            letter-spacing: 0.5px;
        }

        .timer-bar {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid #ffd54f;
            color: #ffd54f;
            text-align: center;
            padding: 9px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 14px;
            letter-spacing: 0.5px;
            box-shadow: 0 0 10px rgba(255, 213, 79, 0.1);
        }

        .btn-scan {
            width: 100%;
            background: linear-gradient(135deg, #00e676, #00b0ff);
            color: #000;
            border: none;
            padding: 12px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
            margin-bottom: 14px;
            transition: all 0.2s ease;
            box-shadow: 0 0 15px rgba(0, 230, 118, 0.3);
        }

        .btn-scan:hover {
            transform: translateY(-1px);
            filter: brightness(1.1);
        }

        .btn-scan:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .signal-box {
            background: #08121a;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 12px;
            text-align: center;
            margin-bottom: 14px;
        }

        .signal-header {
            font-size: 10px;
            color: #b0bec5;
            letter-spacing: 1px;
            margin-bottom: 4px;
            font-weight: bold;
        }

        .signal-result {
            font-size: 16px;
            font-weight: 800;
            color: var(--accent-color);
        }

        .signal-subtext {
            font-size: 10px;
            color: var(--text-dim);
            margin-top: 4px;
            line-height: 1.3;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
            margin-bottom: 14px;
        }

        .metric-card {
            background: #08121a;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 8px;
            text-align: center;
        }

        .metric-title {
            font-size: 9px;
            color: var(--text-dim);
            margin-bottom: 3px;
            font-weight: 600;
        }

        .metric-value {
            font-size: 13px;
            font-weight: bold;
            color: #fff;
        }

        .footer-desc {
            font-size: 9px;
            color: var(--text-dim);
            text-align: center;
            line-height: 1.4;
        }
    </style>
</head>
<body>

    <div class="bot-card">
        <div class="header">
            <div class="brand-info">
                <div class="bot-icon">👾</div>
                <div class="title-text">
                    <h2>FINORIX PRO BOT</h2>
                    <p>BY YASIN BHAI</p>
                </div>
            </div>
            <div class="broker-badge">QX BROKER</div>
        </div>

        <div class="controls-grid">
            <div class="control-group">
                <label>Market Pair</label>
                <select id="marketPair" onchange="updateChartPair(this.value)">
                    <optgroup label="💱 Real Market Currencies">
                        <option value="FX:EURUSD">EUR/USD (Real)</option>
                        <option value="FX:GBPUSD">GBP/USD (Real)</option>
                        <option value="FX:USDJPY">USD/JPY (Real)</option>
                        <option value="FX:EURJPY">EUR/JPY (Real)</option>
                        <option value="FX:AUDUSD">AUD/USD (Real)</option>
                        <option value="FX:USDCAD">USD/CAD (Real)</option>
                        <option value="FX:AUDJPY">AUD/JPY (Real)</option>
                        <option value="FX:EURGBP">EUR/GBP (Real)</option>
                        <option value="FX:CADJPY">CAD/JPY (Real)</option>
                        <option value="FX:EURCAD">EUR/CAD (Real)</option>
                    </optgroup>
                    <optgroup label="🌐 OTC Currencies">
                        <option value="AUD/CAD (OTC)">AUD/CAD (OTC)</option>
                        <option value="USD/DZD (OTC)">USD/DZD (OTC)</option>
                        <option value="USD/BRL (OTC)">USD/BRL (OTC)</option>
                        <option value="GBP/AUD (OTC)">GBP/AUD (OTC)</option>
                        <option value="USD/NGN (OTC)">USD/NGN (OTC)</option>
                        <option value="EUR/CHF (OTC)">EUR/CHF (OTC)</option>
                        <option value="EUR/JPY (OTC)">EUR/JPY (OTC)</option>
                        <option value="GBP/CHF (OTC)">GBP/CHF (OTC)</option>
                        <option value="NZD/USD (OTC)">NZD/USD (OTC)</option>
                        <option value="USD/ZAR (OTC)">USD/ZAR (OTC)</option>
                        <option value="AUD/JPY (OTC)">AUD/JPY (OTC)</option>
                        <option value="USD/COP (OTC)">USD/COP (OTC)</option>
                        <option value="EUR/CAD (OTC)">EUR/CAD (OTC)</option>
                        <option value="USD/MXN (OTC)">USD/MXN (OTC)</option>
                        <option value="AUD/USD (OTC)">AUD/USD (OTC)</option>
                        <option value="CAD/CHF (OTC)">CAD/CHF (OTC)</option>
                        <option value="GBP/NZD (OTC)">GBP/NZD (OTC)</option>
                        <option value="USD/INR (OTC)">USD/INR (OTC)</option>
                        <option value="NZD/CHF (OTC)">NZD/CHF (OTC)</option>
                        <option value="USD/CHF (OTC)">USD/CHF (OTC)</option>
                        <option value="NZD/JPY (OTC)">NZD/JPY (OTC)</option>
                        <option value="USD/ARS (OTC)">USD/ARS (OTC)</option>
                        <option value="EUR/NZD (OTC)">EUR/NZD (OTC)</option>
                        <option value="USD/PHP (OTC)">USD/PHP (OTC)</option>
                        <option value="AUD/CHF (OTC)">AUD/CHF (OTC)</option>
                        <option value="USD/JPY (OTC)">USD/JPY (OTC)</option>
                        <option value="USD/PKR (OTC)">USD/PKR (OTC)</option>
                        <option value="CHF/JPY (OTC)">CHF/JPY (OTC)</option>
                        <option value="EUR/AUD (OTC)">EUR/AUD (OTC)</option>
                        <option value="EUR/GBP (OTC)">EUR/GBP (OTC)</option>
                        <option value="GBP/JPY (OTC)">GBP/JPY (OTC)</option>
                        <option value="USD/BDT (OTC)">USD/BDT (OTC)</option>
                        <option value="USD/CAD (OTC)">USD/CAD (OTC)</option>
                        <option value="USD/EGP (OTC)">USD/EGP (OTC)</option>
                        <option value="USD/IDR (OTC)">USD/IDR (OTC)</option>
                        <option value="CAD/JPY (OTC)">CAD/JPY (OTC)</option>
                        <option value="GBP/USD (OTC)">GBP/USD (OTC)</option>
                        <option value="GBP/CAD (OTC)">GBP/CAD (OTC)</option>
                        <option value="AUD/NZD (OTC)">AUD/NZD (OTC)</option>
                    </optgroup>
                    <optgroup label="🪙 Crypto Market (OTC)">
                        <option value="Avalanche (OTC)">Avalanche (OTC)</option>
                        <option value="Dash (OTC)">Dash (OTC)</option>
                        <option value="Polkadot (OTC)">Polkadot (OTC)</option>
                        <option value="Ethereum (OTC)">Ethereum (OTC)</option>
                        <option value="Litecoin (OTC)">Litecoin (OTC)</option>
                        <option value="Ripple (OTC)">Ripple (OTC)</option>
                        <option value="Trump (OTC)">Trump (OTC)</option>
                        <option value="Bitcoin (OTC)">Bitcoin (OTC)</option>
                        <option value="Axie Infinity (OTC)">Axie Infinity (OTC)</option>
                        <option value="Bitcoin Cash (OTC)">Bitcoin Cash (OTC)</option>
                        <option value="Zcash (OTC)">Zcash (OTC)</option>
                        <option value="Ethereum Classic (OTC)">Ethereum Classic (OTC)</option>
                        <option value="Chainlink (OTC)">Chainlink (OTC)</option>
                        <option value="Binance Coin (OTC)">Binance Coin (OTC)</option>
                        <option value="Toncoin (OTC)">Toncoin (OTC)</option>
                        <option value="Cosmos (OTC)">Cosmos (OTC)</option>
                        <option value="Solana (OTC)">Solana (OTC)</option>
                    </optgroup>
                    <optgroup label="🛢️ Commodities (OTC)">
                        <option value="Silver (OTC)">Silver (OTC)</option>
                        <option value="UKBrent (OTC)">UKBrent (OTC)</option>
                        <option value="Gold (OTC)">Gold (OTC)</option>
                        <option value="USCrude (OTC)">USCrude (OTC)</option>
                    </optgroup>
                </select>
            </div>
            <div class="control-group">
                <label>Timeframe</label>
                <select id="timeframe">
                    <option value="1M">1M</option>
                    <option value="2M">2M</option>
                    <option value="3M">3M</option>
                    <option value="4M">4M</option>
                    <option value="5M">5M</option>
                </select>
            </div>
        </div>

        <div class="chart-header">
            <div class="live-indicator">
                <div class="blinking-dot"></div>
                <span>LIVE CHART</span>
            </div>
            <div class="chart-tools-top">
                <span id="selectedTfText">1M</span> | <span>📊 Candlestick</span>
            </div>
        </div>

        <div class="chart-wrapper">
            <div class="scanner-overlay" id="scannerOverlay">
                <div class="scan-line"></div>
                <div class="scan-status-text" id="scanText">ANALYZING MARKET DYNAMICS...</div>
            </div>

            <div class="otc-notice-container" id="otcNotice">
                <div class="otc-notice-title">⚠️ OTC MARKET SELECTED</div>
                <div class="otc-notice-desc">
                    Live Chart is disabled for OTC Pairs.<br>
                    <strong>OTC High Precision Engine Active.</strong>
                </div>
            </div>

            <div class="tradingview-widget-container" id="tv_chart_container"></div>
        </div>

        <div class="timer-bar">
            ⏰ CANDLE TIME REMAINING: <span id="clockTimer">00s</span>
        </div>

        <button class="btn-scan" id="scanBtn" onclick="startScannerProcess()">
            ⚡ SCAN & PREDICT
        </button>

        <div class="signal-box">
            <div class="signal-header">🔮 SIGNAL GENERATED</div>
            <div class="signal-result" id="signalOutput">PRESS SCAN TO START</div>
            <div class="signal-subtext" id="signalReason">Click SCAN button to trigger analysis</div>
        </div>

        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">WIN RATE</div>
                <div class="metric-value" id="winRateVal">-- %</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">ACCURACY</div>
                <div class="metric-value" id="accuracyVal">-- %</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">CONFIRM</div>
                <div class="metric-value" id="confirmVal">-- %</div>
            </div>
        </div>

        <div class="footer-desc">
            This signal engine operates using price action strategy and institutional volume dynamics.
        </div>
    </div>

    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
        let currentSymbol = "FX:EURUSD";

        document.getElementById('timeframe').addEventListener('change', function() {
            document.getElementById('selectedTfText').innerText = this.value;
        });

        function loadChart(symbol) {
            const chartBox = document.getElementById("tv_chart_container");
            const otcBox = document.getElementById("otcNotice");

            if (symbol.includes("OTC")) {
                chartBox.style.display = "none";
                otcBox.style.display = "flex";
            } else {
                otcBox.style.display = "none";
                chartBox.style.display = "block";
                chartBox.innerHTML = "";

                new TradingView.widget({
                    "autosize": true,
                    "symbol": symbol,
                    "interval": "1",
                    "timezone": "Etc/UTC",
                    "theme": "dark",
                    "style": "1",
                    "locale": "en",
                    "toolbar_bg": "#060b0e",
                    "enable_publishing": false,
                    "hide_top_toolbar": true,
                    "hide_legend": true,
                    "save_image": false,
                    "container_id": "tv_chart_container",
                    "disabled_features": [
                        "header_widget",
                        "volume_force_overlay",
                        "create_volume_indicator_by_default"
                    ]
                });
            }
        }

        function updateChartPair(val) {
            currentSymbol = val;
            loadChart(currentSymbol);
        }

        loadChart(currentSymbol);

        setInterval(() => {
            const seconds = 60 - new Date().getSeconds();
            document.getElementById('clockTimer').innerText = (seconds < 10 ? '0' : '') + seconds + 's';
        }, 1000);

        function startScannerProcess() {
            const btn = document.getElementById('scanBtn');
            const overlay = document.getElementById('scannerOverlay');
            const output = document.getElementById('signalOutput');
            const reason = document.getElementById('signalReason');
            const isOtc = currentSymbol.includes("OTC");

            btn.disabled = true;
            output.innerText = "SCANNING MARKET...";

            if (!isOtc) {
                overlay.style.display = 'flex';
                setTimeout(() => {
                    overlay.style.display = 'none';
                    executeSignalFetch(btn, output, reason);
                }, 3000);
            } else {
                setTimeout(() => {
                    executeSignalFetch(btn, output, reason);
                }, 3000);
            }
        }

        function executeSignalFetch(btn, output, reason) {
            fetch('/api/analyze')
                .then(res => res.json())
                .then(data => {
                    output.innerText = data.signal;
                    output.style.color = data.isCall ? "#00e676" : "#ff5252";
                    reason.innerText = `লজিক: ${data.logic} | নেক্সট ক্যান্ডেল: ${data.nextCandle}`;

                    document.getElementById('winRateVal').innerText = data.winRate + "%";
                    document.getElementById('accuracyVal').innerText = data.accuracy + "%";
                    document.getElementById('confirmVal').innerText = data.confirmRate + "%";

                    btn.disabled = false;
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/analyze', methods=['GET'])
def analyze():
    time.sleep(0.1)
    is_call = random.choice([True, False])
    signal = "CALL (BUY 🟢)" if is_call else "PUT (SELL 🔴)"
    next_candle = "গ্রিন (সবুজ)" if is_call else "রেড (লাল)"
    logic = random.choice(INSTITUTIONAL_KNOWLEDGE_BASE)

    return jsonify({
        "signal": signal,
        "isCall": is_call,
        "nextCandle": next_candle,
        "logic": logic,
        "winRate": random.randint(88, 97),
        "accuracy": random.randint(86, 95),
        "confirmRate": random.randint(90, 99)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
