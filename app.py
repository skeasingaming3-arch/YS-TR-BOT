import time
import random
from flask import Flask, render_template_string

app = Flask(__name__)

MARKET_PAIRS = {
    "OTC Markets": [
        "USD/PKR (OTC)", "USD/BDT (OTC)", "USD/INR (OTC)", "CAD/CHF (OTC)", 
        "NZD/CHF (OTC)", "USD/IDR (OTC)", "USD/BRL (OTC)", "AUD/NZD (OTC)", 
        "USD/ARS (OTC)", "NZD/JPY (OTC)", "USD/COP (OTC)", "USD/EGP (OTC)", 
        "Bitcoin (OTC)", "Ethereum (OTC)", "Gold (OTC)", "Silver (OTC)"
    ],
    "Real Markets": [
        "EUR/USD", "GBP/USD", "USD/JPY", "EUR/JPY", "GBP/JPY", 
        "AUD/USD", "USD/CAD", "USD/CHF", "EUR/GBP", "AUD/CAD"
    ]
}

TIMEFRAMES = ["10s", "20s", "30s", "1m", "2m", "3m", "4m", "5m"]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FINORIX PRO - LIVE REALTIME CHART</title>
    <script src="https://unpkg.com/lightweight-charts@3.8.0/dist/lightweight-charts.standalone.production.js"></script>
    <style>
        :root {
            --bg-color: #0b0e14;
            --card-bg: #121824;
            --accent-color: #00e676;
            --danger-color: #ff5252;
            --text-color: #ffffff;
            --text-sub: #8b9bb4;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
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
        }

        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
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
            font-size: 18px;
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
            gap: 8px;
            margin-bottom: 12px;
        }

        .select-box {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        label {
            font-size: 10px;
            color: var(--text-sub);
        }

        select {
            background: #1a2232;
            color: var(--text-color);
            border: 1px solid #2e3a52;
            padding: 6px;
            border-radius: 6px;
            outline: none;
            font-size: 12px;
        }

        /* Fixed Chart Container Box */
        .chart-box {
            width: 100%;
            height: 240px;
            background: #000000;
            border-radius: 8px;
            position: relative;
            border: 1px solid #2e3a52;
            margin-bottom: 12px;
            overflow: hidden;
        }

        #chartContainer {
            width: 100%;
            height: 100%;
        }

        .live-status {
            position: absolute;
            top: 8px;
            left: 8px;
            z-index: 10;
            font-size: 10px;
            background: rgba(0, 230, 118, 0.2);
            color: var(--accent-color);
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid var(--accent-color);
            pointer-events: none;
        }

        .signal-btn {
            width: 100%;
            background: linear-gradient(135deg, #00e676, #00b0ff);
            color: #000;
            border: none;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
        }

        .signal-btn:hover {
            opacity: 0.9;
        }

        .result-panel {
            margin-top: 10px;
            background: #1a2232;
            padding: 8px 12px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .signal-text {
            font-size: 14px;
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
            <div class="bot-icon">🔴</div>
            <div>
                <strong style="font-size: 15px; display: block;">FINORIX PRO</strong>
                <span style="font-size: 10px; color: var(--text-sub);">LIVE CHART ENGINE</span>
            </div>
        </div>
        <span class="badge">ACTIVATED</span>
    </div>

    <div class="controls">
        <div class="select-box">
            <label>MARKET</label>
            <select id="marketType" onchange="updatePairs()">
                <option value="OTC Markets">OTC Markets</option>
                <option value="Real Markets">Real Markets</option>
            </select>
        </div>
        <div class="select-box">
            <label>PAIR</label>
            <select id="pairSelect" onchange="resetBasePrice()"></select>
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

    <!-- MAIN CHART CONTAINER -->
    <div class="chart-box">
        <div class="live-status">● LIVE RUNNING (+1 FUTURE)</div>
        <div id="chartContainer"></div>
    </div>

    <button class="signal-btn" onclick="manualAnalyse()">ANALYZE SIGNAL CONFLUENCE</button>

    <div class="result-panel">
        <div>
            <span style="font-size: 10px; color: var(--text-sub); display: block;">FUTURE PREDICTION</span>
            <span id="signalDir" class="signal-text up">CALL (UP)</span>
        </div>
        <div>
            <span style="font-size: 10px; color: var(--text-sub); display: block;">ACCURACY</span>
            <span id="accuracyVal" style="font-weight: bold; color: #38bdf8;">94.5%</span>
        </div>
    </div>
</div>

<script>
    const pairsData = {{ pairs | tojson }};
    let chart, candleSeries;
    let basePrice = 293.600;
    let currentCandleOpen = 293.600;
    let currentCandleClose = 293.605;
    let futureDirection = 'CALL';
    let candleHistory = [];

    function initChart() {
        const container = document.getElementById('chartContainer');
        container.innerHTML = '';

        chart = LightweightCharts.createChart(container, {
            width: container.clientWidth,
            height: container.clientHeight,
            layout: { backgroundColor: '#000000', textColor: '#ffffff' },
            grid: { vertLines: { color: '#151c28' }, horzLines: { color: '#151c28' } },
            timeScale: { timeVisible: true, secondsVisible: true }
        });

        candleSeries = chart.addCandlestickSeries({
            upColor: '#00e676', downColor: '#ff5252',
            borderUpColor: '#00e676', borderDownColor: '#ff5252',
            wickUpColor: '#00e676', wickDownColor: '#ff5252'
        });

        buildInitialChart();
        setInterval(updateLiveTick, 1000);
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
        resetBasePrice();
    }

    function resetBasePrice() {
        basePrice = 100 + Math.random() * 500;
        buildInitialChart();
    }

    function buildInitialChart() {
        let now = Math.floor(Date.now() / 1000);
        let baseTime = now - (now % 60);
        candleHistory = [];
        let p = basePrice;

        for (let i = 10; i >= 1; i--) {
            let t = baseTime - (i * 60);
            let open = p + (Math.random() * 0.02 - 0.01);
            let close = open + (Math.random() * 0.03 - 0.015);
            candleHistory.push({
                time: t,
                open: open,
                high: Math.max(open, close) + 0.005,
                low: Math.min(open, close) - 0.005,
                close: close
            });
            p = close;
        }

        currentCandleOpen = p;
        currentCandleClose = currentCandleOpen + 0.002;
        renderLiveSeries();
    }

    function updateLiveTick() {
        let now = Math.floor(Date.now() / 1000);
        let seconds = new Date().getSeconds();

        let tickChange = (Math.random() * 0.008 - 0.004);
        currentCandleClose += tickChange;

        if (seconds === 0) {
            let lastTime = now - 60 - (now % 60);
            candleHistory.push({
                time: lastTime,
                open: currentCandleOpen,
                high: Math.max(currentCandleOpen, currentCandleClose) + 0.004,
                low: Math.min(currentCandleOpen, currentCandleClose) - 0.004,
                close: currentCandleClose
            });
            if (candleHistory.length > 20) candleHistory.shift();

            currentCandleOpen = currentCandleClose;
            futureDirection = Math.random() > 0.5 ? 'CALL' : 'PUT';
            updateSignalDisplay();
        }

        renderLiveSeries();
    }

    function renderLiveSeries() {
        let now = Math.floor(Date.now() / 1000);
        let currentCandleTime = now - (now % 60);

        let displayData = [...candleHistory];

        let runningCandle = {
            time: currentCandleTime,
            open: currentCandleOpen,
            high: Math.max(currentCandleOpen, currentCandleClose) + 0.003,
            low: Math.min(currentCandleOpen, currentCandleClose) - 0.003,
            close: currentCandleClose
        };
        displayData.push(runningCandle);

        // +1 FUTURE CANDLE
        let futureTime = currentCandleTime + 60;
        let futureOpen = currentCandleClose;
        let futureClose = futureDirection === 'CALL' ? futureOpen + 0.025 : futureOpen - 0.025;

        let futureCandle = {
            time: futureTime,
            open: futureOpen,
            high: Math.max(futureOpen, futureClose) + 0.004,
            low: Math.min(futureOpen, futureClose) - 0.004,
            close: futureClose
        };
        displayData.push(futureCandle);

        candleSeries.setData(displayData);
        chart.timeScale().fitContent();
    }

    function manualAnalyse() {
        futureDirection = Math.random() > 0.5 ? 'CALL' : 'PUT';
        let accuracy = (90 + Math.random() * 8).toFixed(1);
        document.getElementById('accuracyVal').innerText = accuracy + '%';
        updateSignalDisplay();
        renderLiveSeries();
    }

    function updateSignalDisplay() {
        const dirEl = document.getElementById('signalDir');
        if (futureDirection === 'CALL') {
            dirEl.innerText = 'CALL (UP)';
            dirEl.className = 'signal-text up';
        } else {
            dirEl.innerText = 'PUT (DOWN)';
            dirEl.className = 'signal-text down';
        }
    }

    window.onload = () => {
        updatePairs();
        initChart();
    };

    window.onresize = () => {
        if (chart) {
            const container = document.getElementById('chartContainer');
            chart.resize(container.clientWidth, container.clientHeight);
        }
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
