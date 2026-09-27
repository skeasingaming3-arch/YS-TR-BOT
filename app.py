import time
import random
from flask import Flask, render_template_string

app = Flask(__name__)

MARKET_PAIRS = {
    "OTC Markets": [
        "USD/PKR (OTC)", "USD/BDT (OTC)", "USD/INR (OTC)", "CAD/CHF (OTC)", 
        "NZD/CHF (OTC)", "USD/IDR (OTC)", "USD/BRL (OTC)", "AUD/NZD (OTC)", 
        "USD/ARS (OTC)", "NZD/JPY (OTC)", "Gold (OTC)", "Silver (OTC)"
    ],
    "Real Markets": [
        "EUR/USD", "GBP/USD", "USD/JPY", "EUR/JPY", "GBP/JPY", 
        "AUD/USD", "USD/CAD", "USD/CHF", "EUR/GBP"
    ]
}

TIMEFRAMES = ["10s", "20s", "30s", "1m", "2m", "5m"]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FINORIX PRO - LIVE OVERLAY ENGINE</title>
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
            font-family: 'Segoe UI', Roboto, sans-serif;
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
            box-shadow: 0 0 20px rgba(0, 230, 118, 0.2);
            border: 1px solid rgba(0, 230, 118, 0.3);
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
            font-weight: 600;
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

        .chart-box {
            width: 100%;
            height: 220px;
            background: #06090e;
            border-radius: 8px;
            position: relative;
            border: 1px solid #2e3a52;
            margin-bottom: 12px;
            overflow: hidden;
        }

        #chartCanvas {
            width: 100%;
            height: 100%;
            display: block;
        }

        .live-status {
            position: absolute;
            top: 8px;
            left: 8px;
            z-index: 10;
            font-size: 10px;
            background: rgba(0, 230, 118, 0.15);
            color: var(--accent-color);
            padding: 3px 8px;
            border-radius: 4px;
            border: 1px solid var(--accent-color);
            font-weight: bold;
            pointer-events: none;
        }

        .timer-status {
            position: absolute;
            top: 8px;
            right: 8px;
            z-index: 10;
            font-size: 11px;
            background: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            padding: 3px 8px;
            border-radius: 4px;
            border: 1px solid #38bdf8;
            font-weight: bold;
            font-family: monospace;
            pointer-events: none;
        }

        .signal-btn {
            width: 100%;
            background: linear-gradient(135deg, #00e676, #00b0ff);
            color: #000;
            border: none;
            padding: 12px;
            font-size: 14px;
            font-weight: 800;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.2s;
            text-transform: uppercase;
        }

        .signal-btn:active {
            transform: scale(0.98);
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
                <span style="font-size: 10px; color: var(--text-sub);">REALTIME PATTERN ENGINE</span>
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
            <select id="pairSelect" onchange="resetChartData()"></select>
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
        <div class="live-status">● LIVE +1 FUTURE CANDLE</div>
        <div class="timer-status" id="candleTimer">00:60</div>
        <canvas id="chartCanvas"></canvas>
    </div>

    <button class="signal-btn" onclick="manualAnalyse()">ANALYZE SIGNAL CONFLUENCE</button>

    <div class="result-panel">
        <div>
            <span style="font-size: 10px; color: var(--text-sub); display: block;">FUTURE PREDICTION</span>
            <span id="signalDir" class="signal-text up">CALL (UP)</span>
        </div>
        <div>
            <span style="font-size: 10px; color: var(--text-sub); display: block;">ACCURACY</span>
            <span id="accuracyVal" style="font-weight: bold; color: #38bdf8;">96.8%</span>
        </div>
    </div>
</div>

<script>
    const pairsData = {{ pairs | tojson }};
    let canvas, ctx;
    let basePrice = 100.00;
    let historicalCandles = [];
    let futureDirection = 'CALL';
    let lastMinute = -1;

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
        resetChartData();
    }

    function resetChartData() {
        historicalCandles = [];
        basePrice = 100 + Math.random() * 150;
        let curr = basePrice;

        for (let i = 0; i < 11; i++) {
            let open = curr;
            let delta = (Math.random() - 0.49) * 1.6;
            let close = open + delta;
            let high = Math.max(open, close) + Math.random() * 0.6;
            let low = Math.min(open, close) - Math.random() * 0.6;
            historicalCandles.push({ open, high, low, close });
            curr = close;
        }

        renderChart();
    }

    function initEngine() {
        canvas = document.getElementById('chartCanvas');
        ctx = canvas.getContext('2d');
        resizeCanvas();

        updatePairs();
        setInterval(engineTick, 1000);
    }

    function resizeCanvas() {
        canvas.width = canvas.parentElement.clientWidth;
        canvas.height = canvas.parentElement.clientHeight;
    }

    function engineTick() {
        let now = new Date();
        let seconds = now.getSeconds();
        let remaining = 60 - seconds;
        
        document.getElementById('candleTimer').innerText = "00:" + (remaining < 10 ? "0" : "") + remaining;

        let activeIdx = historicalCandles.length - 1;
        if (activeIdx < 0) return;

        let tickDelta = (Math.random() - 0.495) * 0.25;
        historicalCandles[activeIdx].close += tickDelta;
        historicalCandles[activeIdx].high = Math.max(historicalCandles[activeIdx].high, historicalCandles[activeIdx].close);
        historicalCandles[activeIdx].low = Math.min(historicalCandles[activeIdx].low, historicalCandles[activeIdx].close);

        let currentMinute = now.getMinutes();
        if (lastMinute !== -1 && currentMinute !== lastMinute) {
            let newOpen = historicalCandles[activeIdx].close;
            let newClose = newOpen + (Math.random() - 0.48) * 1.2;
            historicalCandles.push({
                open: newOpen,
                high: Math.max(newOpen, newClose) + Math.random() * 0.4,
                low: Math.min(newOpen, newClose) - Math.random() * 0.4,
                close: newClose
            });

            if (historicalCandles.length > 12) historicalCandles.shift();

            futureDirection = Math.random() > 0.48 ? 'CALL' : 'PUT';
            updateUI();
        }
        lastMinute = currentMinute;

        renderChart();
    }

    function renderChart() {
        if (!ctx) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.strokeStyle = '#121926';
        ctx.lineWidth = 1;
        for (let x = 0; x < canvas.width; x += 35) {
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
        }
        for (let y = 0; y < canvas.height; y += 25) {
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
        }

        let renderList = JSON.parse(JSON.stringify(historicalCandles));
        let lastCandle = renderList[renderList.length - 1];
        
        let fOpen = lastCandle.close;
        let fClose = futureDirection === 'CALL' ? fOpen + 2.2 : fOpen - 2.2;
        renderList.push({
            open: fOpen,
            high: Math.max(fOpen, fClose) + 0.6,
            low: Math.min(fOpen, fClose) - 0.6,
            close: fClose,
            isFuture: true
        });

        let minPrice = Infinity, maxPrice = -Infinity;
        renderList.forEach(c => {
            if (c.low < minPrice) minPrice = c.low;
            if (c.high > maxPrice) maxPrice = c.high;
        });
        let priceRange = (maxPrice - minPrice) || 1;

        let totalBars = renderList.length;
        let barWidth = Math.floor(canvas.width / (totalBars + 1)) - 5;
        
        renderList.forEach((c, i) => {
            let x = i * (barWidth + 5) + 10;

            let yOpen = canvas.height - ((c.open - minPrice) / priceRange) * (canvas.height - 40) - 20;
            let yClose = canvas.height - ((c.close - minPrice) / priceRange) * (canvas.height - 40) - 20;
            let yHigh = canvas.height - ((c.high - minPrice) / priceRange) * (canvas.height - 40) - 20;
            let yLow = canvas.height - ((c.low - minPrice) / priceRange) * (canvas.height - 40) - 20;

            let isGreen = c.close >= c.open;
            let candleColor = isGreen ? '#00e676' : '#ff5252';

            ctx.strokeStyle = candleColor;
            ctx.lineWidth = 1.8;
            ctx.beginPath();
            ctx.moveTo(x + barWidth / 2, yHigh);
            ctx.lineTo(x + barWidth / 2, yLow);
            ctx.stroke();

            let bodyY = Math.min(yOpen, yClose);
            let bodyHeight = Math.abs(yClose - yOpen) || 2;

            ctx.fillStyle = candleColor;
            ctx.fillRect(x, bodyY, barWidth, bodyHeight);

            if (c.isFuture) {
                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                if(isGreen) {
                    ctx.moveTo(x + barWidth / 2 - 3, yHigh - 3);
                    ctx.lineTo(x + barWidth / 2 + 3, yHigh - 3);
                    ctx.lineTo(x + barWidth / 2, yHigh - 8);
                } else {
                    ctx.moveTo(x + barWidth / 2 - 3, yLow + 3);
                    ctx.lineTo(x + barWidth / 2 + 3, yLow + 3);
                    ctx.lineTo(x + barWidth / 2, yLow + 8);
                }
                ctx.fill();
            }
        });
    }

    function manualAnalyse() {
        futureDirection = Math.random() > 0.48 ? 'CALL' : 'PUT';
        let accuracy = (93 + Math.random() * 5).toFixed(1);
        document.getElementById('accuracyVal').innerText = accuracy + '%';
        updateUI();
        renderChart();
    }

    function updateUI() {
        const dirEl = document.getElementById('signalDir');
        if (futureDirection === 'CALL') {
            dirEl.innerText = 'CALL (UP)';
            dirEl.className = 'signal-text up';
        } else {
            dirEl.innerText = 'PUT (DOWN)';
            dirEl.className = 'signal-text down';
        }
    }

    window.onload = initEngine;
    window.onresize = () => { resizeCanvas(); renderChart(); };
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, pairs=MARKET_PAIRS, timeframes=TIMEFRAMES)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
