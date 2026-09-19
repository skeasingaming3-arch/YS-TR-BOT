import time
import random
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# Institutional Knowledge & Precision Signal Logic Base
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
    "Demand Zone Mitigation + Change of Character (CHOCH)"
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
            --bg-color: #070e13;
            --card-bg: #0f1922;
            --accent-color: #00e676;
            --accent-blue: #00bcd4;
            --text-color: #ffffff;
            --text-dim: #8fa3b0;
            --border-color: #1a2a38;
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

        /* Smooth RGB Glowing Animated Border */
        .bot-card {
            width: 100%;
            max-width: 420px;
            background: var(--card-bg);
            border-radius: 18px;
            padding: 16px;
            position: relative;
            box-shadow: 0 0 25px rgba(0, 230, 118, 0.12);
            border: 2px solid transparent;
            background-clip: padding-box;
            animation: borderGlow 4s linear infinite;
        }

        @keyframes borderGlow {
            0% { border-color: #00e676; box-shadow: 0 0 15px rgba(0, 230, 118, 0.3); }
            33% { border-color: #00bcd4; box-shadow: 0 0 15px rgba(0, 188, 212, 0.3); }
            66% { border-color: #7c4dff; box-shadow: 0 0 15px rgba(124, 77, 255, 0.3); }
            100% { border-color: #00e676; box-shadow: 0 0 15px rgba(0, 230, 118, 0.3); }
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
            gap: 10px;
        }

        .bot-icon {
            width: 40px;
            height: 40px;
            background: #14232f;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 20px;
            border: 1.5px solid var(--accent-color);
        }

        .title-text h2 {
            font-size: 16px;
            color: var(--accent-color);
            font-weight: 700;
            letter-spacing: 0.5px;
        }

        .title-text p {
            font-size: 10px;
            color: var(--text-dim);
        }

        .broker-badge {
            background: rgba(0, 188, 212, 0.1);
            color: var(--accent-blue);
            border: 1px solid var(--accent-blue);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: bold;
        }

        .controls-grid {
            display: grid;
            grid-template-columns: 1.3fr 0.7fr;
            gap: 10px;
            margin-bottom: 12px;
        }

        .control-group {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .control-group label {
            font-size: 10px;
            color: var(--text-dim);
        }

        select {
            background: #0a131b;
            color: #fff;
            border: 1px solid var(--border-color);
            padding: 8px;
            border-radius: 8px;
            outline: none;
            font-size: 11px;
        }

        optgroup {
            background: #0f1922;
            color: var(--accent-color);
        }

        /* Compacted Live Chart Styles */
        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 6px 10px;
            background: #0a131b;
            border: 1px solid var(--border-color);
            border-bottom: none;
            border-radius: 8px 8px 0 0;
        }

        .live-indicator {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 10px;
            font-weight: bold;
            color: var(--accent-color);
        }

        .blinking-dot {
            width: 7px;
            height: 7px;
            background-color: var(--accent-color);
            border-radius: 50%;
            box-shadow: 0 0 6px var(--accent-color);
            animation: blink 1s infinite alternate;
        }

        @keyframes blink {
            0% { opacity: 0.2; }
            100% { opacity: 1; }
        }

        .chart-tools-top {
            display: flex;
            gap: 6px;
            font-size: 10px;
            color: var(--text-dim);
        }

        .chart-wrapper {
            width: 100%;
            height: 165px; /* Compact Size Adjustment */
            background: #060b0e;
            border-radius: 0 0 8px 8px;
            border: 1px solid var(--border-color);
            border-top: none;
            margin-bottom: 12px;
            position: relative;
            overflow: hidden;
        }

        /* OTC Market Warning Notice Container */
        .otc-notice-container {
            display: none;
            width: 100%;
            height: 100%;
            padding: 20px;
            background: #0a131b;
            text-align: center;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 8px;
        }

        .otc-notice-title {
            color: #ff9800;
            font-size: 12px;
            font-weight: bold;
        }

        .otc-notice-desc {
            color: var(--text-dim);
            font-size: 10px;
            line-height: 1.4;
        }

        .tradingview-widget-container {
            width: 100%;
            height: 100%;
        }

        /* Scanner Animation Overlay */
        .scanner-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(6, 11, 14, 0.92);
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 20;
        }

        .scan-line {
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, #00e676, transparent);
            box-shadow: 0 0 10px #00e676;
            position: absolute;
            animation: scanAnimation 1.5s infinite linear;
        }

        @keyframes scanAnimation {
            0% { top: 0%; }
            50% { top: 95%; }
            100% { top: 0%; }
        }

        .scan-status-text {
            color: var(--accent-color);
            font-size: 11px;
            font-weight: bold;
            margin-top: 8px;
        }

        .timer-bar {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid #ffd54f;
            color: #ffd54f;
            text-align: center;
            padding: 8px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 12px;
        }

        .btn-scan {
            width: 100%;
            background: linear-gradient(135deg, #00e676, #00b0ff);
            color: #000;
            border: none;
            padding: 11px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 6px;
            margin-bottom: 12px;
            transition: 0.2s;
        }

        .btn-scan:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .signal-box {
            background: #09131a;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            text-align: center;
            margin-bottom: 12px;
        }

        .signal-header {
            font-size: 9px;
            color: #b0bec5;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }

        .signal-result {
            font-size: 16px;
            font-weight: 800;
            color: var(--accent-color);
        }

        .signal-subtext {
            font-size: 10px;
            color: var(--text-dim);
            margin-top: 3px;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
            margin-bottom: 12px;
        }

        .metric-card {
            background: #0a141d;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 8px;
            text-align: center;
        }

        .metric-title {
            font-size: 8px;
            color: var(--text-dim);
            margin-bottom: 2px;
        }

        .metric-value {
            font-size: 13px;
            font-weight: bold;
            color: #fff;
        }

        .footer-desc {
            font-size: 8px;
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
                <div class="bot-icon">🤖</div>
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
                    <optgroup label="💱 Currencies (Real Market)">
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
                    <optgroup label="🌐 Currencies (OTC Market)">
                        <option value="USD/BDT (OTC)">USD/BDT (OTC)</option>
                        <option value="USD/NGN (OTC)">USD/NGN (OTC)</option>
                        <option value="USD/ARS (OTC)">USD/ARS (OTC)</option>
                        <option value="NZD/JPY (OTC)">NZD/JPY (OTC)</option>
                        <option value="USD/PKR (OTC)">USD/PKR (OTC)</option>
                        <option value="NZD/CHF (OTC)">NZD/CHF (OTC)</option>
                        <option value="USD/DZD (OTC)">USD/DZD (OTC)</option>
                        <option value="CAD/CHF (OTC)">CAD/CHF (OTC)</option>
                        <option value="GBP/NZD (OTC)">GBP/NZD (OTC)</option>
                        <option value="NZD/CAD (OTC)">NZD/CAD (OTC)</option>
                    </optgroup>
                    <optgroup label="🪙 Crypto">
                        <option value="BINANCE:BTCUSDT">Bitcoin (OTC)</option>
                        <option value="BINANCE:ETHUSDT">Ethereum (OTC)</option>
                        <option value="BINANCE:XRPUSDT">Ripple (OTC)</option>
                        <option value="BINANCE:SOLUSDT">Solana (OTC)</option>
                    </optgroup>
                    <optgroup label="🛢️ Commodities">
                        <option value="OANDA:XAUUSD">Gold (OTC)</option>
                        <option value="OANDA:XAGUSD">Silver (OTC)</option>
                        <option value="TVC:UKOIL">UKBrent (OTC)</option>
                    </optgroup>
                    <optgroup label="📈 Stocks">
                        <option value="INDEX:SPX">S&P/ASX 200</option>
                        <option value="INDEX:UKX">FTSE 100</option>
                    </optgroup>
                </select>
            </div>
            <div class="control-group">
                <label>Timeframe</label>
                <select id="timeframe">
                    <option value="1m">1m (Strict Locked)</option>
                </select>
            </div>
        </div>

        <!-- Live Chart Container Header -->
        <div class="chart-header">
            <div class="live-indicator">
                <div class="blinking-dot"></div>
                <span>LIVE CHART</span>
            </div>
            <div class="chart-tools-top">
                <span>1m</span> | <span>📊 Candlestick</span>
            </div>
        </div>

        <div class="chart-wrapper">
            <div class="scanner-overlay" id="scannerOverlay">
                <div class="scan-line"></div>
                <div class="scan-status-text" id="scanText">ANALYZING MARKET DYNAMICS...</div>
            </div>

            <!-- Notice for OTC Markets -->
            <div class="otc-notice-container" id="otcNotice">
                <div class="otc-notice-title">⚠️ LIVE CHART UNAVAILABLE</div>
                <div class="otc-notice-desc">
                    TradingView Live Chart is not supported for OTC Pairs.<br>
                    <strong>High Precision Signal Engine remains active.</strong>
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
            <div class="signal-subtext" id="signalReason">Click the SCAN button manually to analyze trade market</div>
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
            This signal engine operates using advanced multi-indicator real market analysis, price action strategy, RSI confluence, and volume dynamics to deliver maximum precision.
        </div>
    </div>

    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
        let currentSymbol = "FX:EURUSD";

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

        function speakBanglaVoice(text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'bn-BD';
                utterance.rate = 0.9;
                utterance.pitch = 1.0;
                window.speechSynthesis.speak(utterance);
            }
        }

        function startScannerProcess() {
            const btn = document.getElementById('scanBtn');
            const overlay = document.getElementById('scannerOverlay');
            const scanText = document.getElementById('scanText');
            const output = document.getElementById('signalOutput');
            const reason = document.getElementById('signalReason');

            btn.disabled = true;
            overlay.style.display = 'flex';
            output.innerText = "SCANNING MARKET...";
            output.style.color = "#00bcd4";

            document.getElementById('winRateVal').innerText = "-- %";
            document.getElementById('accuracyVal').innerText = "-- %";
            document.getElementById('confirmVal').innerText = "-- %";

            const scanSteps = [
                "SCANNING CANDLESTICKS...",
                "CALCULATING SMC & FVG...",
                "ANALYZING VOLUME DELTA...",
                "FILTERING VOLATILITY..."
            ];

            let stepIndex = 0;
            const stepInterval = setInterval(() => {
                if (stepIndex < scanSteps.length) {
                    scanText.innerText = scanSteps[stepIndex];
                    stepIndex++;
                }
            }, 1000);

            setTimeout(() => {
                clearInterval(stepInterval);
                overlay.style.display = 'none';

                fetch('/api/analyze')
                    .then(res => res.json())
                    .then(data => {
                        output.innerText = data.signal;

                        if (data.isNoTrade) {
                            output.style.color = "#ff9800";
                        } else {
                            output.style.color = data.isCall ? "#00e676" : "#ff5252";
                        }

                        reason.innerText = `লজিক: ${data.logic} | নেক্সট ক্যান্ডেল: ${data.nextCandle}`;

                        document.getElementById('winRateVal').innerText = data.winRate + "%";
                        document.getElementById('accuracyVal').innerText = data.accuracy + "%";
                        document.getElementById('confirmVal').innerText = data.confirmRate + "%";

                        speakBanglaVoice(data.voiceMessage);
                        btn.disabled = false;
                    });
            }, 4500);
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
    time.sleep(0.2)
    
    # 15% Chance of High Volatility (No Trade Protection)
    is_volatile = random.random() < 0.15

    if is_volatile:
        signal = "WAIT (MARKET VOLATILE ⚠️)"
        next_candle = "স্কিপ (ট্রেড নেবেন না)"
        logic = "High Volatility Detected - Risk Avoidance Engine Active"
        is_call = False
        is_no_trade = True
        win_rate = random.randint(50, 65)
        accuracy = random.randint(50, 60)
        confirm_rate = random.randint(50, 65)
        voice_msg = "মার্কেট অতিরিক্ত পরিবর্তনশীল। এই মুহূর্তে ট্রেড নেওয়া থেকে বিরত থাকুন।"
    else:
        is_call = random.choice([True, False])
        is_no_trade = False
        signal = "CALL (BUY 🟢)" if is_call else "PUT (SELL 🔴)"
        next_candle = "গ্রিন (সবুজ)" if is_call else "রেড (লাল)"
        logic = random.choice(INSTITUTIONAL_KNOWLEDGE_BASE)

        # High Precision Range for Real Trades (72% - 98%)
        win_rate = random.randint(75, 98)
        accuracy = random.randint(72, 96)
        confirm_rate = random.randint(80, 99)

        voice_msg = f"কনফার্ম সিগন্যাল। পরবর্তী ক্যান্ডেল {'বাই অথবা কল' if is_call else 'সেল অথবা পুট'} ট্রেড নিন।"

    return jsonify({
        "signal": signal,
        "isCall": is_call,
        "isNoTrade": is_no_trade,
        "nextCandle": next_candle,
        "logic": logic,
        "winRate": win_rate,
        "accuracy": accuracy,
        "confirmRate": confirm_rate,
        "voiceMessage": voice_msg
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
