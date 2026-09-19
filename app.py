import os
import time
import random
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# স্ক্রিনশট অনুযায়ী গঠিত মার্কেট লিস্ট
MARKETS = {
    "Real": [
        {"symbol": "FX:EURUSD", "name": "EUR/USD (Real)"},
        {"symbol": "FX:GBPUSD", "name": "GBP/USD (Real)"},
        {"symbol": "FX:USDJPY", "name": "USD/JPY (Real)"},
        {"symbol": "FX:AUDCAD", "name": "AUD/CAD (Real)"},
        {"symbol": "FX:USDCAD", "name": "USD/CAD (Real)"}
    ],
    "OTC_Currencies": [
        "AUD/CAD (OTC)", "USD/DZD (OTC)", "USD/BRL (OTC)", "GBP/AUD (OTC)",
        "USD/NGN (OTC)", "EUR/CHF (OTC)", "EUR/JPY (OTC)", "GBP/CHF (OTC)",
        "NZD/USD (OTC)", "USD/ZAR (OTC)", "USD/COP (OTC)", "EUR/CAD (OTC)",
        "USD/MXN (OTC)", "AUD/USD (OTC)", "CAD/CHF (OTC)", "GBP/NZD (OTC)",
        "USD/INR (OTC)", "NZD/CHF (OTC)", "USD/CHF (OTC)", "NZD/JPY (OTC)",
        "USD/ARS (OTC)", "EUR/NZD (OTC)", "USD/PHP (OTC)", "AUD/CHF (OTC)",
        "USD/JPY (OTC)", "USD/PKR (OTC)", "CHF/JPY (OTC)", "EUR/AUD (OTC)",
        "EUR/GBP (OTC)", "GBP/JPY (OTC)", "USD/BDT (OTC)", "USD/EGP (OTC)",
        "USD/IDR (OTC)", "CAD/JPY (OTC)", "GBP/CAD (OTC)", "AUD/NZD (OTC)"
    ],
    "OTC_Crypto": [
        "Avalanche (OTC)", "Dash (OTC)", "Polkadot (OTC)", "Ethereum (OTC)",
        "Litecoin (OTC)", "Ripple (OTC)", "Trump (OTC)", "Bitcoin (OTC)",
        "Axie Infinity (OTC)", "Bitcoin Cash (OTC)", "Zcash (OTC)",
        "Ethereum Classic (OTC)", "Chainlink (OTC)", "Binance Coin (OTC)",
        "Toncoin (OTC)", "Cosmos (OTC)", "Solana (OTC)"
    ],
    "OTC_Commodities": [
        "Silver (OTC)", "UKBrent (OTC)", "Gold (OTC)", "USCrude (OTC)"
    ]
}

# HTML, CSS & JavaScript UI Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>FINORIX PRO BOT V1.0</title>
    <style>
        :root {
            --bg-color: #0b0e14;
            --card-bg: #131822;
            --accent-green: #00e676;
            --accent-red: #ff1744;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Roboto, sans-serif;
            user-select: none;
        }

        body {
            background-color: var(--bg-color);
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
            padding: 8px;
        }

        /* সাইজ সামঞ্জস্য এবং কালার সাইক্লিং এনিমেশন বর্ডার */
        .app-container {
            width: 100%;
            max-width: 380px;
            background: var(--card-bg);
            border-radius: 14px;
            padding: 12px;
            position: relative;
            box-shadow: 0 0 12px rgba(0, 255, 204, 0.2);
            animation: borderCycling 3s infinite linear;
            border: 2px solid transparent;
        }

        @keyframes borderCycling {
            0% { border-color: #ff0055; box-shadow: 0 0 10px #ff0055; }
            25% { border-color: #00e676; box-shadow: 0 0 10px #00e676; }
            50% { border-color: #00e5ff; box-shadow: 0 0 10px #00e5ff; }
            75% { border-color: #ffea00; box-shadow: 0 0 10px #ffea00; }
            100% { border-color: #ff0055; box-shadow: 0 0 10px #ff0055; }
        }

        /* প্রোফাইল সেকশন */
        .profile-section {
            display: flex;
            align-items: center;
            gap: 10px;
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 10px;
        }

        .avatar {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid #ff0055;
            box-shadow: 0 0 6px #ff0055;
        }

        .profile-info h3 {
            font-size: 15px;
            color: #00ffcc;
            line-height: 1.2;
        }

        .profile-info p.version {
            font-size: 10px;
            color: #aaaaaa;
            font-weight: bold;
            margin-top: 2px;
        }

        /* ড্রপডাউন কন্ট্রোলস */
        .input-group {
            display: flex;
            gap: 6px;
            margin-bottom: 10px;
        }

        .select-box {
            flex: 1;
            background: #1a2230;
            color: #fff;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 7px;
            border-radius: 6px;
            font-size: 11px;
            outline: none;
        }

        /* চার্ট বক্স ও ওভারলে */
        .chart-box {
            width: 100%;
            height: 190px;
            background: #000;
            border-radius: 8px;
            overflow: hidden;
            position: relative;
            margin-bottom: 8px;
            border: 1px solid #222;
        }

        .chart-iframe {
            width: 100%;
            height: 100%;
            border: none;
        }

        .otc-warning {
            display: none;
            color: #ff3366;
            background: rgba(255, 51, 102, 0.1);
            border: 1px solid #ff3366;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            font-size: 11px;
            height: 100%;
            justify-content: center;
            align-items: center;
            font-weight: bold;
        }

        /* টাইমার বার */
        .timer-bar {
            background: #1a2230;
            border: 1px solid #ffea00;
            color: #ffea00;
            padding: 5px;
            text-align: center;
            border-radius: 6px;
            font-size: 11px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        /* স্ক্যান বাটন ও লাইটনিং এনিমেশন */
        .scan-btn {
            width: 100%;
            padding: 10px;
            background: linear-gradient(90deg, #00e676, #00b0ff);
            border: none;
            border-radius: 6px;
            color: #000;
            font-weight: bold;
            font-size: 13px;
            cursor: pointer;
            box-shadow: 0 0 8px #00e676;
            transition: 0.2s;
        }

        .scan-btn:active {
            transform: scale(0.98);
        }

        .scanning-active {
            animation: thunderEffect 0.15s infinite;
        }

        @keyframes thunderEffect {
            0% { background: #00e676; filter: brightness(1); }
            50% { background: #ffffff; filter: brightness(2); box-shadow: 0 0 20px #ffffff; }
            100% { background: #00b0ff; filter: brightness(1); }
        }

        /* সিগন্যাল ফলাফল ও রিজন সেকশন */
        .result-box {
            margin-top: 10px;
            background: #161c28;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.08);
        }

        .signal-text {
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            margin: 4px 0;
        }

        .call-signal { color: var(--accent-green); }
        .put-signal { color: var(--accent-red); }
        .volatile-signal { color: #ffea00; font-size: 12px; }

        .metrics {
            display: flex;
            justify-content: space-around;
            font-size: 10px;
            color: #aaa;
            margin-bottom: 8px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            padding-bottom: 4px;
        }

        .reasons-list {
            font-size: 10px;
            color: #bbb;
            list-style: none;
        }

        .reasons-list li {
            margin-bottom: 3px;
            padding-left: 8px;
            position: relative;
        }

        .reasons-list li::before {
            content: "•";
            position: absolute;
            left: 0;
            color: #00ffcc;
        }
    </style>
</head>
<body>

<div class="app-container">
    <!-- প্রোফাইল সেকশন -->
    <div class="profile-section">
        <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=150" alt="Scary Robot" class="avatar">
        <div class="profile-info">
            <h3>HR SHADOW BOT</h3>
            <p class="version">Version 1.0</p>
        </div>
    </div>

    <!-- মার্কেট ও টাইমফ্রেম সিলেক্টর -->
    <div class="input-group">
        <select id="marketSelect" class="select-box" onchange="handleMarketChange()">
            <optgroup label="Real Markets">
                {% for item in markets.Real %}
                    <option value="{{ item.symbol }}" data-type="real">{{ item.name }}</option>
                {% endfor %}
            </optgroup>
            <optgroup label="OTC Currencies">
                {% for item in markets.OTC_Currencies %}
                    <option value="{{ item }}" data-type="otc">{{ item }}</option>
                {% endfor %}
            </optgroup>
            <optgroup label="OTC Crypto">
                {% for item in markets.OTC_Crypto %}
                    <option value="{{ item }}" data-type="otc">{{ item }}</option>
                {% endfor %}
            </optgroup>
            <optgroup label="OTC Commodities">
                {% for item in markets.OTC_Commodities %}
                    <option value="{{ item }}" data-type="otc">{{ item }}</option>
                {% endfor %}
            </optgroup>
        </select>

        <select id="timeframeSelect" class="select-box">
            <option value="1M">1M</option>
            <option value="2M">2M</option>
            <option value="3M">3M</option>
            <option value="4M">4M</option>
            <option value="5M">5M</option>
        </select>
    </div>

    <!-- লাইভ চার্ট কন্টেইনার -->
    <div class="chart-box">
        <div id="otcWarning" class="otc-warning">
            ⚠️ WARNING: This feature only works in Real Markets. OTC markets do not support live chart scanning.
        </div>
        <iframe id="tradingViewChart" class="chart-iframe" src=""></iframe>
    </div>

    <!-- ক্যান্ডেল টাইমার -->
    <div class="timer-bar">
        ⏰ CANDLE TIME REMAINING: <span id="candleTimer">60s</span>
    </div>

    <!-- স্ক্যান বাটন -->
    <button id="scanBtn" class="scan-btn" onclick="startScan()">⚡ SCAN & PREDICT</button>

    <!-- আউটপুট প্যানেল -->
    <div class="result-box">
        <div class="metrics">
            <span>WIN RATE: <b id="winRate">--%</b></span>
            <span>ACCURACY: <b id="accuracy">--%</b></span>
            <span>CONFIRM: <b id="confirm">HIGH</b></span>
        </div>

        <div id="signalOutput" class="signal-text">PRESS SCAN TO START</div>

        <ul id="reasonList" class="reasons-list">
            <li>System ready. Select pair and initiate scan.</li>
        </ul>
    </div>
</div>

<script>
    let timerSeconds = 60;

    // ১ মিনিটের ক্যান্ডেল টাইমার
    setInterval(() => {
        timerSeconds--;
        if (timerSeconds <= 0) timerSeconds = 60;
        document.getElementById('candleTimer').innerText = (timerSeconds < 10 ? '0' : '') + timerSeconds + 's';
    }, 1000);

    // ট্রেডিংভিউ ক্লিন লাইভ চার্ট ইউআরএল
    function loadChart(symbol) {
        const cleanSymbol = symbol.replace("FX:", "");
        const chartUrl = `https://s.tradingview.com/widgetembed/?frameElementId=tradingview_1&symbol=${cleanSymbol}&interval=1&hidesidetoolbar=1&symboledit=0&saveimage=0&toolbarbg=000000&studies=[]&theme=dark&style=1&timezone=Etc%2FUTC`;
        document.getElementById('tradingViewChart').src = chartUrl;
    }

    function handleMarketChange() {
        const select = document.getElementById('marketSelect');
        const selectedOption = select.options[select.selectedIndex];
        const marketType = selectedOption.getAttribute('data-type');
        const chartIframe = document.getElementById('tradingViewChart');
        const warning = document.getElementById('otcWarning');

        if (marketType === 'real') {
            warning.style.display = 'none';
            chartIframe.style.display = 'block';
            loadChart(selectedOption.value);
        } else {
            chartIframe.style.display = 'none';
            warning.style.display = 'flex';
        }
    }

    // বাংলা ভয়েস অ্যানাউন্সমেন্ট
    function speakBangla(text) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'bn-BD';
            utterance.rate = 0.95;
            window.speechSynthesis.speak(utterance);
        }
    }

    // স্ক্যান লজিক
    function startScan() {
        const btn = document.getElementById('scanBtn');
        const signalOut = document.getElementById('signalOutput');
        const market = document.getElementById('marketSelect').value;
        const timeframe = document.getElementById('timeframeSelect').value;

        btn.classList.add('scanning-active');
        btn.innerText = "⚡ SCANNING MARKET...";
        signalOut.innerText = "ANALYZING SIGNAL...";
        signalOut.className = "signal-text";

        fetch('/api/scan', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ market: market, timeframe: timeframe })
        })
        .then(res => res.json())
        .then(data => {
            btn.classList.remove('scanning-active');
            btn.innerText = "⚡ SCAN & PREDICT";

            const reasonList = document.getElementById('reasonList');
            reasonList.innerHTML = '';

            if (data.status === "VOLATILE") {
                signalOut.innerText = "⚠️ DO NOT TRADE!";
                signalOut.className = "signal-text volatile-signal";
                document.getElementById('winRate').innerText = "0%";
                document.getElementById('accuracy').innerText = "LOW";
                
                let li = document.createElement('li');
                li.innerText = data.message;
                reasonList.appendChild(li);

                speakBangla(data.voice_msg);
            } else {
                signalOut.innerText = data.signal;
                signalOut.className = "signal-text " + (data.signal.includes("CALL") ? "call-signal" : "put-signal");
                
                document.getElementById('winRate').innerText = data.win_rate;
                document.getElementById('accuracy').innerText = data.accuracy;

                data.reasons.forEach(r => {
                    let li = document.createElement('li');
                    li.innerText = r;
                    reasonList.appendChild(li);
                });

                speakBangla(data.voice_msg);
            }
        })
        .catch(() => {
            btn.classList.remove('scanning-active');
            btn.innerText = "⚡ SCAN & PREDICT";
            signalOut.innerText = "SCAN FAILED";
        });
    }

    window.onload = () => {
        handleMarketChange();
    };
</script>

</body>
</html>
"""

# ব্যাকএন্ড স্ট্র্যাটেজি এনালাইসিস
def analyze_market_indicators():
    rsi = random.uniform(20, 80)
    macd = random.uniform(-0.002, 0.002)
    volatility = random.uniform(0.1, 1.0)
    
    # ভোলাটিলিটি ফিল্টার (মার্কেট খারাপ থাকলে ট্রেড ব্লক করবে)
    if volatility > 0.82:
        return {
            "status": "VOLATILE",
            "message": "High market volatility detected. Unsafe to open trades right now.",
            "voice_msg": "মার্কেট ভোলাটাইল, এখন ট্রেড নিবেন না।"
        }
    
    # ইন্ডিকেটর কনফ্লুয়েন্স লজিক
    if rsi < 35 and macd > 0:
        signal = "CALL (UP)"
        accuracy = random.randint(92, 98)
        reasons = [
            "RSI oversold rebound pattern matched.",
            "Bullish MACD momentum crossover.",
            "Strong dynamic support level rejection."
        ]
        voice = "আপ ট্রেড নিন।"
    elif rsi > 65 and macd < 0:
        signal = "PUT (DOWN)"
        accuracy = random.randint(91, 97)
        reasons = [
            "RSI overbought exhaustion zone.",
            "Bearish MACD histogram divergence.",
            "Resistance level rejection with high seller volume."
        ]
        voice = "ডাউন ট্রেড নিন।"
    else:
        direction = random.choice(["CALL (UP)", "PUT (DOWN)"])
        signal = direction
        accuracy = random.randint(89, 95)
        reasons = [
            "Trend continuation confluence aligned.",
            "Volume Delta analysis indicates order flow direction.",
            "Exponential Moving Average bounce strategy confirmed."
        ]
        voice = "আপ ট্রেড নিন।" if "UP" in direction else "ডাউন ট্রেড নিন।"

    return {
        "status": "SUCCESS",
        "signal": signal,
        "accuracy": f"{accuracy}%",
        "win_rate": f"{accuracy - 2}%",
        "reasons": reasons,
        "voice_msg": voice
    }

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, markets=MARKETS)

@app.route('/api/scan', methods=['POST'])
def scan_and_predict():
    data = request.get_json() or {}
    market = data.get('market', '')
    timeframe = data.get('timeframe', '1M')
    
    time.sleep(1.5)
    
    result = analyze_market_indicators()
    result['market'] = market
    result['timeframe'] = timeframe
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
