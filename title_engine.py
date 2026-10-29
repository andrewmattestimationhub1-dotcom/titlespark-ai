import json
import urllib.request
import urllib.error


def _template_titles(topic, style, language, count):
    topic = topic.strip().rstrip(".!?")
    if language == "Roman Urdu":
        patterns = [
            f"{topic}: Beginners Ke Liye Asaan Guide",
            f"{topic} Ke Bare Mein 5 Zaroori Baatein",
            f"{topic} Seekhne Ka Sab Se Asaan Tareeqa",
            f"{topic} Karte Waqt Ye Ghaltiyan Na Karein",
            f"{topic}: Woh Tips Jo Kaam Aa Sakti Hain",
            f"Kya {topic} Waqai Itna Useful Hai?",
            f"{topic} Ka Step-by-Step Tutorial",
            f"{topic} Se Behtar Result Kaise Lein",
            f"{topic}: Shuru Karne Se Pehle Ye Dekhein",
            f"{topic} Ke Liye Complete Beginner Guide",
            f"{topic} Ke 7 Practical Ideas",
            f"{topic}: Aam Sawalon Ke Jawabat",
            f"{topic} Ko Samajhna Ab Hua Asaan",
            f"{topic} Try Kiya — Ye Seekha",
            f"{topic} Ke Liye Quick Tips",
        ]
    elif language == "Urdu":
        patterns = [
            f"{topic} کے لیے آسان گائیڈ", f"{topic} کے بارے میں 5 اہم باتیں",
            f"{topic} سیکھنے کا آسان طریقہ", f"{topic} کرتے وقت ان غلطیوں سے بچیں",
            f"{topic} کے لیے مفید ٹپس", f"کیا {topic} واقعی مفید ہے؟",
            f"{topic} کا مرحلہ وار ٹیوٹوریل", f"{topic} میں بہتر نتائج کیسے حاصل کریں",
            f"{topic} شروع کرنے سے پہلے یہ دیکھیں", f"{topic} کی مکمل ابتدائی گائیڈ",
            f"{topic} کے 7 عملی آئیڈیاز", f"{topic} سے متعلق عام سوالات",
            f"{topic} کو آسانی سے سمجھیں", f"{topic} آزمایا — یہ سیکھا",
            f"{topic} کے لیے فوری ٹپس",
        ]
    else:
        patterns = [
            f"The Beginner's Guide to {topic}", f"5 Things You Should Know About {topic}",
            f"How to Get Started With {topic}", f"Common {topic} Mistakes to Avoid",
            f"{topic}: Tips That Actually Help", f"Is {topic} Worth It? Here's What to Know",
            f"{topic} Step by Step: A Simple Tutorial", f"How to Improve at {topic}",
            f"Watch This Before Trying {topic}", f"The Complete {topic} Guide for Beginners",
            f"7 Practical Ideas for {topic}", f"Your Top Questions About {topic}, Answered",
            f"{topic} Explained in Simple Terms", f"I Tried {topic}: Here's What I Learned",
            f"Quick Tips to Make {topic} Easier",
        ]
    if style == "Challenge":
        patterns = [f"I Tried {topic} for 7 Days — Here's What Happened"] + patterns
    elif style == "Funny":
        patterns = [f"My Funny Attempt at {topic}", f"When You Finally Try {topic}"] + patterns
    elif style == "SEO-friendly":
        patterns = [f"{topic} Tutorial for Beginners | Step-by-Step Guide", f"How to Use {topic}: Complete Tutorial"] + patterns
    elif style == "List":
        patterns = [f"7 Practical Ideas for {topic}", f"5 Things You Should Know About {topic}"] + patterns
    elif style == "Curiosity":
        patterns = [f"What Nobody Tells You About {topic}", f"Watch This Before Trying {topic}"] + patterns
    unique = list(dict.fromkeys(patterns))
    return unique[:count]


def generate_titles(topic, style, language, count, api_key=""):
    if not api_key:
        return _template_titles(topic, style, language, count), "template"

    payload = {
        "model": "gpt-4.1-mini",
        "input": (
            "Generate YouTube video titles. Return ONLY a valid JSON array of strings. "
            f"Return exactly {count} distinct titles. Topic: {topic!r}. "
            f"Style: {style}. Language: {language}. "
            "Avoid false promises, spam, and misleading clickbait. Make titles clear and useful."
        ),
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"AI API error ({exc.code}). API key/billing check karo. {detail[:350]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Internet/network issue: {exc.reason}") from exc

    output_text = result.get("output_text", "")
    try:
        titles = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError("AI response expected JSON array mein nahi tha. Dobara try karo.") from exc
    if not isinstance(titles, list):
        raise RuntimeError("AI response ka format valid nahi tha.")
    cleaned = [str(item).strip() for item in titles if str(item).strip()]
    if not cleaned:
        raise RuntimeError("AI ne koi title return nahi kiya.")
    return cleaned[:count], "ai"
