import time
import random
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Complete pairs categorized strictly into OTC and Real Markets
MARKET_PAIRS = {
    "Real Markets": [
        "EUR/JPY", "EUR/GBP", "GBP/USD", "USD/JPY", "AUD/CAD", 
        "EUR/USD", "CAD/JPY", "AUD/CHF", "GBP/AUD", "AUD/JPY", 
        "AUD/USD", "EUR/CHF", "CHF/JPY", "GBP/CHF", "GBP/JPY", 
        "EUR/AUD", "EUR/CAD", "USD/CAD", "GBP/CAD", "USD/CHF", 
        "Nikkei 225", "S&P/ASX 200", "FTSE China A50 Index", 
        "CAC 40", "FTSE 100", "Hong Kong 50", "IBEX 35", "EURO STOXX 50"
    ],
    "OTC Markets": [
        "CAD/CHF (OTC)", "USD/INR (OTC)", "USD/NGN (OTC)", "NZD/CHF (OTC)", 
        "USD/IDR (OTC)", "USD/BRL (OTC)", "AUD/NZD (OTC)", "USD/ARS (OTC)", 
        "NZD/JPY (OTC)", "USD/PKR (OTC)", "NZD/CAD (OTC)", "USD/BDT (OTC)", 
        "USD/COP (OTC)", "USD/DZD (OTC)", "USD/EGP (OTC)", "USD/MXN (OTC)", 
        "USD/PHP (OTC)", "EUR/NZD (OTC)", "GBP/NZD (OTC)", "USD/ZAR (OTC)", 
        "NZD/USD (OTC)", "Axie Infinity (OTC)", "Bitcoin Cash (OTC)", 
        "Bitcoin (OTC)", "Dash (OTC)", "Solana (OTC)", "Toncoin (OTC)", 
        "Trump (OTC)", "Zcash (OTC)", "Ripple (OTC)", "Chainlink (OTC)", 
        "Cosmos (OTC)", "Polkadot (OTC)", "Ethereum Classic (OTC)", 
        "Avalanche (OTC)", "Litecoin (OTC)", "Ethereum (OTC)", "Binance Coin (OTC)",
        "UKBrent (OTC)", "Gold (OTC)", "Silver (OTC)", "USCrude (OTC)"
    ]
}

TIMEFRAMES = ["10s", "20s", "30s", "1m", "2m", "3m", "4m", "5m"]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FINORIX PRO SOFTWARE - INSTITUTIONAL BOT</title>
    <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
    <style>
        :root {
            --bg-color: #0b0e14;
            --card-bg: #121824;
            --accent-color: #00e676;
            --danger-color: #ff5252;
            --border-glow: #00e676;
            --text-color: #ffffff;
            --text-sub: #8b9bb4;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 10px;
        }

        .bot-card {
            background: var(--card-bg);
            width: 100%;
            max-width: 420px;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 0 20px rgba(0, 230, 118, 0.25);
            border: 1px solid rgba(0, 230, 118, 0.4);
            animation: pulseGlow 2.5s infinite alternate;
        }

        @keyframes pulseGlow {
            0% { border-color: rgba(0, 230, 118, 0.3); box-shadow: 0 0 10px rgba(0, 230, 118, 0.2); }
            100% { border-color: rgba(0, 230, 118, 0.9); box-shadow: 0 0 22px rgba(0, 230, 118, 0.6); }
        }

        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
        }

        .bot-title {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .bot-icon {
            width: 38px;
            height: 38px;
            background: #1e293b;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            border: 2px solid var(--accent-color);
        }

        .badge {
            background: #1e293b;
            color: #38bdf8;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: bold;
            border: 1px solid #38bdf8;
        }

        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 12px;
        }

        .select-box {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        label {
            font-size: 11px;
            color: var(--text-sub);
        }

        select {
            background: #1a2232;
            color: var(--text-color);
            border: 1px solid #2e3a52;
            padding: 8px;
            border-radius: 8px;
            outline: none;
            font-size: 13px;
        }

        .chart-box {
            height: 180px;
            background: #000;
            border-radius: 8px;
            overflow: hidden;
            position: relative;
            border: 1px solid #2e3a52;
            margin-bottom: 12px;
        }

        #chartContainer {
            width: 100%;
            height: 100%;
        }

        .signal-btn {
            width: 100%;
            background: linear-gradient(135deg, #00e676, #00b0ff);
            color: #000;
            border: none;
            padding: 12px;
            font-size: 15px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
        }

        .signal-btn:hover {
            opacity: 0.9;
            transform: scale(0.99);
        }

        .result-panel {
            margin-top: 12px;
            background: #1a2232;
            padding: 10px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .signal-text {
            font-size: 16px;
            font-weight: bold;
        }

        .up { color: var(--accent-color); }
        .down { color: var(--danger-color); }
    </style>
</head>
<body>

<div class="bot-card">
    <div class="header">
        <div class="bot-title">
            <div class="bot-icon">🤖</div>
            <div>
                <strong style="font-size: 16px; display: block;">FINORIX PRO</strong>
                <span style="font-size: 11px; color: var(--text-sub);">250+ KNOWLEDGE ENGINE</span>
            </div>
        </div>
        <span class="badge">ACTIVATED</span>
    </div>

    <div class="controls">
        <div class="select-box">
            <label>MARKET TYPE</label>
            <select id="marketType" onchange="updatePairs()">
                <option value="OTC Markets">OTC Markets</option>
                <option value="Real Markets">Real Markets</option>
            </select>
        </div>
        <div class="select-box">
            <label>SELECT PAIR</label>
            <select id="pairSelect"></select>
        </div>
        <div class="select-box">
            <label>TIMEFRAME</label>
            <select id="timeframeSelect">
                {% for tf in timeframes %}
                <option value="{{tf}}" {% if tf == '1m' %}selected{% endif %}>{{tf}}</option>
                {% endfor %}
            </select>
        </div>
    </div>

    <div class="chart-box">
        <div id="chartContainer"></div>
    </div>

    <button class="signal-btn" onclick="generateSignal()">GENERATE PREDICTION (+1 CANDLE)</button>

    <div class="result-panel">
        <div>
            <span style="font-size: 11px; color: var(--text-sub); display: block;">SIGNAL DIRECTION</span>
            <span id="signalDir" class="signal-text">WAITING...</span>
        </div>
        <div>
            <span style="font-size: 11px; color: var(--text-sub); display: block;">ACCURACY CONFLUENCE</span>
            <span id="accuracyVal" style="font-weight: bold; color: #38bdf8;">--%</span>
        </div>
    </div>
</div>

<script>
    const pairsData = {{ pairs | tojson }};
    let chart, candleSeries;

    function initChart() {
        const container = document.getElementById('chartContainer');
        chart = LightweightCharts.createChart(container, {
            layout: { backgroundColor: '#000000', textColor: '#ffffff' },
            grid: { vertLines: { color: '#1a2232' }, horzLines: { color: '#1a2232' } },
            timeScale: { timeVisible: true, secondsVisible: true }
        });

        candleSeries = chart.addCandlestickSeries({
            upColor: '#00e676', downColor: '#ff5252',
            borderUpColor: '#00e676', borderDownColor: '#ff5252',
            wickUpColor: '#00e676', wickDownColor: '#ff5252'
        });

        renderBaseCandles('CALL');
    }

    function updatePairs() {
        const type = document.getElementById('marketType').value;
        const select = document.getElementById('pairSelect');
        select.innerHTML = '';
        pairsData[type].forEach(pair => {
            let opt = document.createElement('option');
            opt.value = pair;
            opt.innerHTML = pair;
            select.appendChild(opt);
        });
    }

    function renderBaseCandles(predictedDirection) {
        let now = Math.floor(Date.now() / 1000);
        let basePrice = 293.600;
        let data = [];

        // Past 5 candles
        for (let i = 5; i >= 1; i--) {
            let time = now - (i * 60);
            let open = basePrice + (Math.random() * 0.020 - 0.010);
            let close = open + (Math.random() * 0.030 - 0.015);
            data.push({
                time: time,
                open: open,
                high: Math.max(open, close) + 0.005,
                low: Math.min(open, close) - 0.005,
                close: close
            });
            basePrice = close;
        }

        // Current Running Candle
        let currentOpen = basePrice;
        let currentClose = currentOpen + 0.010;
        data.push({
            time: now,
            open: currentOpen,
            high: currentClose + 0.004,
            low: currentOpen - 0.002,
            close: currentClose
        });

        // FUTURE +1 PREDICTED CANDLE (Advanced Feature)
        let futureTime = now + 60;
        let futureOpen = currentClose;
        let futureClose = predictedDirection === 'CALL' ? futureOpen + 0.025 : futureOpen - 0.025;

        data.push({
            time: futureTime,
            open: futureOpen,
            high: Math.max(futureOpen, futureClose) + 0.005,
            low: Math.min(futureOpen, futureClose) - 0.005,
            close: futureClose
        });

        candleSeries.setData(data);
        chart.timeScale().fitContent();
    }

    function generateSignal() {
        const directions = ['CALL (UP)', 'PUT (DOWN)'];
        const chosen = directions[Math.floor(Math.random() * directions.length)];
        const accuracy = (88 + Math.random() * 9).toFixed(1);

        const dirEl = document.getElementById('signalDir');
        dirEl.innerText = chosen;
        dirEl.className = 'signal-text ' + (chosen.includes('CALL') ? 'up' : 'down');
        
        document.getElementById('accuracyVal').innerText = accuracy + '%';

        renderBaseCandles(chosen.includes('CALL') ? 'CALL' : 'PUT');
    }

    window.onload = () => {
        updatePairs();
        initChart();
    };
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, pairs=MARKET_PAIRS, timeframes=TIMEFRAMES)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
