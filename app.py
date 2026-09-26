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
    <title>FINORIX PRO - LIVE REALTIME ENGINE</title>
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

        /* Chart Canvas Area Fix */
        .chart-box {
            width: 100%;
            height: 220px;
            background: #000000;
            border-radius: 8px;
            position: relative;
            border: 1px solid #2e3a52;
            margin-bottom: 12px;
            overflow: hidden;
        }

        #customChartCanvas {
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
                <span style="font-size: 10px; color: var(--text-sub);">CANVAS LIVE ENGINE</span>
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
            <select id="pairSelect" onchange="resetChart()"></select>
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

    <!-- CANVAS LIVE CHART CONTAINER -->
    <div class="chart-box">
        <div class="live-status">● LIVE +1 FUTURE CANDLE</div>
        <canvas id="customChartCanvas"></canvas>
    </div>

    <button class="signal-btn" onclick="manualAnalyse()">ANALYZE SIGNAL CONFLUENCE</button>

    <div class="result-panel">
        <div>
            <span style="font-size: 10px; color: var(--text-sub); display: block;">FUTURE PREDICTION</span>
            <span id="signalDir" class="signal-text up">CALL (UP)</span>
        </div>
        <div>
            <span style="font-size: 10px; color: var(--text-sub); display: block;">ACCURACY</span>
            <span id="accuracyVal" style="font-weight: bold; color: #38bdf8;">95.2%</span>
        </div>
    </div>
</div>

<script>
    const pairsData = {{ pairs | tojson }};
    let canvas, ctx;
    let basePrice = 200.0;
    let candles = [];
    let futureDirection = 'CALL';
    let timerCounter = 0;

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
        resetChart();
    }

    function resetChart() {
        basePrice = 100 + Math.random() * 300;
        candles = [];
        let p = basePrice;

        // Create 12 Historical Candles
        for (let i = 0; i < 12; i++) {
            let open = p;
            let close = open + (Math.random() * 4 - 2);
            let high = Math.max(open, close) + Math.random() * 1.5;
            let low = Math.min(open, close) - Math.random() * 1.5;
            candles.push({ open, high, low, close, isFuture: false });
            p = close;
        }

        renderCanvas();
    }

    function initCanvas() {
        canvas = document.getElementById('customChartCanvas');
        ctx = canvas.getContext('2d');
        resizeCanvas();

        updatePairs();
        setInterval(liveTick, 800); // Ticks every 800ms
    }

    function resizeCanvas() {
        canvas.width = canvas.parentElement.clientWidth;
        canvas.height = canvas.parentElement.clientHeight;
    }

    function liveTick() {
        if (candles.length === 0) return;

        timerCounter++;
        let lastRealIdx = candles.length - 1;
        
        // Simulating live tick movement on the active candle
        let tick = (Math.random() * 0.8 - 0.4);
        candles[lastRealIdx].close += tick;
        candles[lastRealIdx].high = Math.max(candles[lastRealIdx].high, candles[lastRealIdx].close);
        candles[lastRealIdx].low = Math.min(candles[lastRealIdx].low, candles[lastRealIdx].close);

        // Every 15 ticks shift candle & make new future prediction
        if (timerCounter % 15 === 0) {
            let newOpen = candles[lastRealIdx].close;
            let newClose = newOpen + (Math.random() * 3 - 1.5);
            candles.push({
                open: newOpen,
                high: Math.max(newOpen, newClose) + 1,
                low: Math.min(newOpen, newClose) - 1,
                close: newClose,
                isFuture: false
            });

            if (candles.length > 14) candles.shift();

            futureDirection = Math.random() > 0.5 ? 'CALL' : 'PUT';
            updateSignalUI();
        }

        renderCanvas();
    }

    function renderCanvas() {
        if (!ctx) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Background Grid
        ctx.strokeStyle = '#151c28';
        ctx.lineWidth = 1;
        for (let x = 0; x < canvas.width; x += 40) {
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
        }
        for (let y = 0; y < canvas.height; y += 30) {
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
        }

        // Build list including +1 Future Candle
        let displayCandles = JSON.parse(JSON.stringify(candles));
        let lastCandle = displayCandles[displayCandles.length - 1];
        
        let fOpen = lastCandle.close;
        let fClose = futureDirection === 'CALL' ? fOpen + 3.5 : fOpen - 3.5;
        displayCandles.push({
            open: fOpen,
            high: Math.max(fOpen, fClose) + 1,
            low: Math.min(fOpen, fClose) - 1,
            close: fClose,
            isFuture: true
        });

        // Min-Max Price Calculations
        let minP = Infinity, maxP = -Infinity;
        displayCandles.forEach(c => {
            if (c.low < minP) minP = c.low;
            if (c.high > maxP) maxP = c.high;
        });
        let priceRange = (maxP - minP) || 1;

        let candleWidth = Math.floor(canvas.width / (displayCandles.length + 1)) - 6;
        
        displayCandles.forEach((c, i) => {
            let x = i * (candleWidth + 6) + 12;

            // Map price to y coordinate
            let yOpen = canvas.height - ((c.open - minP) / priceRange) * (canvas.height - 40) - 20;
            let yClose = canvas.height - ((c.close - minP) / priceRange) * (canvas.height - 40) - 20;
            let yHigh = canvas.height - ((c.high - minP) / priceRange) * (canvas.height - 40) - 20;
            let yLow = canvas.height - ((c.low - minP) / priceRange) * (canvas.height - 40) - 20;

            let isGreen = c.close >= c.open;
            let color = isGreen ? '#00e676' : '#ff5252';

            // Wick
            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(x + candleWidth / 2, yHigh);
            ctx.lineTo(x + candleWidth / 2, yLow);
            ctx.stroke();

            // Candle Body
            ctx.fillStyle = color;
            let bodyHeight = Math.abs(yClose - yOpen) || 2;
            let bodyY = Math.min(yOpen, yClose);

            if (c.isFuture) {
                // Dashed border for Future Candle
                ctx.strokeStyle = color;
                ctx.lineWidth = 2;
                ctx.setLineDash([3, 3]);
                ctx.strokeRect(x, bodyY, candleWidth, bodyHeight);
                ctx.setLineDash([]);
                ctx.fillStyle = color + "44"; // Translucent fill
                ctx.fillRect(x, bodyY, candleWidth, bodyHeight);
            } else {
                ctx.fillRect(x, bodyY, candleWidth, bodyHeight);
            }
        });
    }

    function manualAnalyse() {
        futureDirection = Math.random() > 0.5 ? 'CALL' : 'PUT';
        let accuracy = (91 + Math.random() * 7).toFixed(1);
        document.getElementById('accuracyVal').innerText = accuracy + '%';
        updateSignalUI();
        renderCanvas();
    }

    function updateSignalUI() {
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
        initCanvas();
    };

    window.onresize = () => {
        resizeCanvas();
        renderCanvas();
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
