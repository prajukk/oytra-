from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(r"d:\odee\oytra\oytra-\screenshots")


def font(size=16, bold=False):
    candidates = [
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def box(draw, xy, text, fill, outline="#222222", tw=180, th=54):
    x, y = xy
    draw.rounded_rectangle([x, y, x + tw, y + th], radius=10, fill=fill, outline=outline, width=2)
    f = font(13)
    # crude center
    bbox = draw.textbbox((0, 0), text, font=f)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((x + (tw - w) / 2, y + (th - h) / 2), text, fill="#111111", font=f)


def arrow(draw, x1, y1, x2, y2, label=""):
    draw.line((x1, y1, x2, y2), fill="#444444", width=3)
    # arrow head
    draw.polygon([(x2, y2), (x2 - 10, y2 - 6), (x2 - 10, y2 + 6)], fill="#444444")
    if label:
        draw.text(((x1 + x2) / 2 - 10, y1 - 18), label, fill="#666666", font=font(11))


def make_task2():
    img = Image.new("RGB", (1400, 720), "#F7F8FA")
    d = ImageDraw.Draw(img)
    d.text((40, 24), "Task 2 - Morning Brief Workflow (canvas reference)", fill="#111", font=font(22))

    box(d, (40, 180), "Schedule 1h", "#DCEBFF")
    box(d, (40, 280), "Webhook test", "#DCEBFF")
    box(d, (280, 230), "CoinGecko Markets", "#E8F8E8")
    box(d, (520, 230), "Transform Top 5", "#FFF4D6")
    box(d, (760, 230), "Enrich Leader", "#E8F8E8")
    box(d, (1000, 230), "IF change>2%", "#F3E8FF")
    box(d, (1240, 140), "Bullish Digest", "#FFF4D6", tw=140)
    box(d, (1240, 320), "Soft Digest", "#FFF4D6", tw=140)
    box(d, (760, 430), "Format Failure", "#FFE0E0")
    box(d, (1000, 430), "Discord Alert", "#E0E7FF")
    box(d, (1240, 230), "Discord Digest", "#E0E7FF", tw=140)

    arrow(d, 220, 207, 280, 250)
    arrow(d, 220, 307, 280, 270)
    arrow(d, 460, 257, 520, 257)
    arrow(d, 700, 257, 760, 257)
    arrow(d, 940, 257, 1000, 257)
    arrow(d, 1180, 245, 1240, 167, "yes")
    arrow(d, 1180, 270, 1240, 340, "no")
    # error path from markets/enrich
    d.line((370, 284, 370, 457), fill="#B00020", width=2)
    d.line((370, 457, 760, 457), fill="#B00020", width=2)
    d.line((850, 284, 850, 430), fill="#B00020", width=2)
    arrow(d, 940, 457, 1000, 457, "error")

    d.text((40, 640), "APIs: CoinGecko markets + coin detail | Notify: Discord credential | Errors: continueErrorOutput -> alert", fill="#333", font=font(14))
    path = OUT / "task2-workflow-canvas.png"
    img.save(path)
    print("wrote", path)


def make_bonus():
    img = Image.new("RGB", (1100, 520), "#F7F8FA")
    d = ImageDraw.Draw(img)
    d.text((40, 24), "Bonus - Uptime Monitor (canvas reference)", fill="#111", font=font(22))

    box(d, (40, 200), "Every 5 Minutes", "#DCEBFF")
    box(d, (280, 200), "Ping Conduit", "#E8F8E8")
    box(d, (520, 200), "Evaluate Status", "#FFF4D6")
    box(d, (760, 200), "IF Not Healthy", "#F3E8FF")
    box(d, (980, 120), "Discord Alert", "#E0E7FF", tw=100)
    box(d, (980, 280), "Log Healthy", "#E8F8E8", tw=100)

    arrow(d, 220, 227, 280, 227)
    arrow(d, 460, 227, 520, 227)
    arrow(d, 700, 227, 760, 227)
    arrow(d, 940, 220, 980, 147, "down")
    arrow(d, 940, 245, 980, 300, "ok")

    d.text((40, 420), "Target: https://demo.realworld.show/ | Retry 3x / 5s | Alert on status != 200", fill="#333", font=font(14))
    path = OUT / "bonus-uptime-canvas.png"
    img.save(path)
    print("wrote", path)


def make_execution_sample():
    img = Image.new("RGB", (1000, 560), "#1E1E1E")
    d = ImageDraw.Draw(img)
    d.text((30, 24), "Task 2 - Sample successful execution output (reference)", fill="#EAEAEA", font=font(18))
    sample = """{
  "route": "bullish",
  "content": "MORNING BRIEF — Bullish leader (>2% 24h)\\nLeader: Bitcoin (BTC)\\n...",
  "leader": { "symbol": "BTC", "change24h": 3.41, "price": 97500 },
  "top5": [
    {"rank": 1, "symbol": "BTC"},
    {"rank": 2, "symbol": "ETH"},
    {"rank": 3, "symbol": "USDT"},
    {"rank": 4, "symbol": "BNB"},
    {"rank": 5, "symbol": "SOL"}
  ],
  "enrichment": { "ath": 109000, "athChange": -10.5 }
}"""
    y = 70
    for line in sample.splitlines():
        d.text((40, y), line, fill="#9CDCFE", font=font(13))
        y += 22
    d.text((30, 510), "Replace with a real n8n Executions screenshot after first successful run.", fill="#AAAAAA", font=font(12))
    path = OUT / "task2-successful-execution.png"
    img.save(path)
    print("wrote", path)


if __name__ == "__main__":
    make_task2()
    make_bonus()
    make_execution_sample()
