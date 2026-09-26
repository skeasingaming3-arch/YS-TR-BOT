from flask import Flask, render_template_string, jsonify
import time
import random

app = Flask(__name__)

# Complete Pairs (Real & OTC)
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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FINORIX PRO SOFTWARE</title>
    <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: #0b0e14;
            color: #ffffff;
            font-family: 'Segoe UI', Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 10px;
        }

        /* Screen Wrapper mimicking live trading layout */
        .live-screen {
            width: 100%;
            max-width: 420px;
            height: 700px;
            background: #111622;
            border-radius: 12px;
            position: relative;
            overflow: hidden;
            border: 1px solid #1e293b;
            display: flex;
            flex-direction: column;
        }

        /* Top Header Info */
        .top-bar {
            padding: 10px 15px;
            background: #182030;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            border-bottom: 1px solid #2a364f;
        }

        /* Main Chart Area */
        .main-chart {
            flex: 1;
            position: relative;
            background: #000;
        }

        #mainChartContainer {
            width: 100%;
            height: 100%;
        }

        /* Floating Bot Window (Finorix Pro) as in the screenshot */
        .finorix-bot-overlay {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            background: rgba(18, 24, 38, 0.95);
            border: 1px solid #00e676;
            border-radius: 12px;
            padding: 12px;
            box-shadow: 0 0 15px rgba(0, 230, 118, 0.3);
            backdrop-filter: blur(5px);
        }

        .bot-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }

        .bot-title {
            font-size: 14px;
            font-weight: bold;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .status-badge {
            font-size: 10px;
            background: #ff5252;
            color: #fff;
            padding: 2px 6px;
            border-radius: 4px;
        }

        .status-badge.active {
            background: #00e676;
            color: #000;
            font-weight: bold;
        }

        .pair-info {
            font-size: 12px;
            color: #8b9bb4;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
        }

        /* Inner Mini Chart showing +1 Future Candle */
        .inner-chart-box {
            width: 100%;
            height: 120px;
            background: #000000;
            border-radius: 8px;
            border: 1px solid #2a364f;
            overflow: hidden;
            position: relative;
        }

        #botChartContainer {
            width: 100%;
            height: 100%;
        }

        .action-btn {
            width: 100%;
            margin-top: 10px;
            background: linear-gradient(135deg, #00e676, #00b0ff);
            color: #000;
            font-weight: bold;
            border: none;
            padding: 8px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
        }
    </style>
</head>
<body>

<div class="live-screen">
    <!-- Top Bar -->
    <div class="top-bar">
        <span>UTC+6 <strong id="clock">00:00:00</strong></span>
        <span style="color: #00e676;">LIVE MARKET ACTIVE</span>
    </div>

    <!-- Main Chart -->
    <div class="main-chart">
        <div id="mainChartContainer"></div>
    </div>

    <!-- Finorix Pro Floating Overlay -->
    <div class="finorix-bot-overlay">
        <div class="bot-header">
            <div class="bot-title">
                <span>🔴🔴</span>
                <span>FINORIX PRO</span>
            </div>
            <span class="status-badge active" id="actBadge">Activated</span>
        </div>

        <div class="pair-info">
            <span id="pairName">USD/PKR (OTC) 1m</span>
            <span id="timerCountdown" style="color: #00e676; font-weight: bold;">00:53</span>
        </div>

        <!-- Bot Inner Chart (+1 Future Candle Engine) -->
        <div class="inner-chart-box">
            <div id="botChartContainer"></div>
        </div>

        <button class="action-btn" onclick="triggerPrediction()">GENERATE PREDICTION (+1 CANDLE)</button>
    </div>
</div>

<script>
    let mainChart, mainSeries, botChart, botSeries;
    let basePrice = 293.600;
    let predictedDir = 'UP';

    function initCharts() {
        // Main Chart Setup
        const mainContainer = document.getElementById('mainChartContainer');
        mainChart = LightweightCharts.createChart(mainContainer, {
            layout: { backgroundColor: '#0b0e14', textColor: '#8b9bb4' },
            grid: { vertLines: { color: '#182030' }, horzLines: { color: '#182030' } },
            timeScale: { timeVisible: true, secondsVisible: true }
        });

        mainSeries = mainChart.addCandlestickSeries({
            upColor: '#00e676', downColor: '#ff5252',
            borderUpColor: '#00e676', borderDownColor: '#ff5252',
            wickUpColor: '#00e676', wickDownColor: '#ff5252'
        });

        // Bot Inner Chart Setup
        const botContainer = document.getElementById('botChartContainer');
        botChart = LightweightCharts.createChart(botContainer, {
            layout: { backgroundColor: '#000000', textColor: '#ffffff' },
            grid: { vertLines: { color: '#111' }, horzLines: { color: '#111' } },
            timeScale: { timeVisible: true, secondsVisible: true }
        });

        botSeries = botChart.addCandlestickSeries({
            upColor: '#00e676', downColor: '#ff5252',
            borderUpColor: '#00e676', borderDownColor: '#ff5252',
            wickUpColor: '#00e676', wickDownColor: '#ff5252'
        });

        updateChartData();
    }

    function updateChartData() {
        let now = Math.floor(Date.now() / 1000);
        let mainData = [];
        let botData = [];

        // Generate past 5 candles
        let p = basePrice;
        for (let i = 5; i >= 1; i--) {
            let t = now - (i * 60);
            let open = p + (Math.random() * 0.02 - 0.01);
            let close = open + (Math.random() * 0.03 - 0.015);
            let candle = {
                time: t,
                open: open,
                high: Math.max(open, close) + 0.005,
                low: Math.min(open, close) - 0.005,
                close: close
            };
            mainData.push(candle);
            botData.push(candle);
            p = close;
        }

        // Current Running Candle
        let currentOpen = p;
        let currentClose = currentOpen + (Math.random() * 0.01);
        let currentCandle = {
            time: now,
            open: currentOpen,
            high: currentClose + 0.003,
            low: currentOpen - 0.002,
            close: currentClose
        };

        mainData.push(currentCandle);
        botData.push(currentCandle);

        // +1 FUTURE PREDICTED CANDLE IN BOT CHART ONLY
        let futureTime = now + 60;
        let futureOpen = currentClose;
        let futureClose = predictedDir === 'UP' ? futureOpen + 0.025 : futureOpen - 0.025;

        botData.push({
            time: futureTime,
            open: futureOpen,
            high: Math.max(futureOpen, futureClose) + 0.004,
            low: Math.min(futureOpen, futureClose) - 0.004,
            close: futureClose
        });

        mainSeries.setData(mainData);
        botSeries.setData(botData);

        mainChart.timeScale().fitContent();
        botChart.timeScale().fitContent();
    }

    function updateClock() {
        let d = new Date();
        document.getElementById('clock').innerText = d.toTimeString().split(' ')[0];
        
        let seconds = 60 - d.getSeconds();
        let secStr = seconds < 10 ? '0' + seconds : seconds;
        document.getElementById('timerCountdown').innerText = '00:' + secStr;

        // Auto shift candles every 60 seconds
        if (seconds === 60 || seconds === 0) {
            updateChartData();
        }
    }

    function triggerPrediction() {
        predictedDir = Math.random() > 0.5 ? 'UP' : 'DOWN';
        updateChartData();
    }

    setInterval(updateClock, 1000);

    window.onload = () => {
        initCharts();
    };
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
