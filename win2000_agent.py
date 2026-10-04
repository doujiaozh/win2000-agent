# -*- coding: gbk -*-
import os, sys, json, re
PY3 = sys.version_info[0] >= 3
if PY3:
    from urllib.request import Request, urlopen
    from urllib.parse import quote
else:
    from urllib2 import Request, urlopen
    from urllib import quote

BACKENDS = {
    "zhipu":       ("https://open.bigmodel.cn/api/paas/v4", "glm-4-flash"),
    "deepseek":    ("https://api.deepseek.com/v1",          "deepseek-chat"),
    "siliconflow": ("https://api.siliconflow.cn/v1",        "Qwen/Qwen2.5-7B-Instruct"),
    "moonshot":    ("https://api.moonshot.cn/v1",           "moonshot-v1-8k"),
    "openai":      ("https://api.openai.com/v1",            "gpt-4o-mini"),
}

BACKEND = os.environ.get("BACKEND", "zhipu")
KEY = os.environ.get("OPENAI_API_KEY", "")

if BACKEND in BACKENDS:
    default_url, default_model = BACKENDS[BACKEND]
else:
    default_url, default_model = "", ""

URL = os.environ.get("OPENAI_BASE_URL", default_url).rstrip("/")
MODEL = os.environ.get("MODEL", default_model)

UA = "Mozilla/5.0 (Windows NT 5.1) Chrome/120.0"

def post(path, body):
    data = json.dumps(body).encode("utf-8")
    req = Request(URL + path, data=data)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", "Bearer " + KEY)
    raw = urlopen(req, timeout=180).read()
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    return json.loads(raw)

def get(url):
    req = Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Accept-Language", "zh-CN,zh;q=0.9")
    raw = urlopen(req, timeout=30).read()
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", "ignore")
    return raw

def search(q):
    try:
        url = "https://cn.bing.com/search?q=" + quote(q) + "&mkt=zh-CN"
        html = get(url)
        print("[2000] html length: " + str(len(html)))
        out = []
        for c in re.split(r'<li class="b_algo"', html)[1:6]:
            m = re.search(r'<h2[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', c, re.S)
            if m:
                title = re.sub(r"<[^>]+>", "", m.group(2)).strip()
                out.append(title + "\n" + m.group(1))
        return "\n".join(out)
    except Exception as e:
        print("[2000] search error: " + str(e))
        return ""

def main(g):
    print("[2000] backend: " + BACKEND)
    print("[2000] model:   " + MODEL)
    print("[2000] url:     " + URL)
    print("[2000] goal:    " + g)
    print("[2000] searching...")
    s = search(g)
    print("[2000] got " + str(len(s)) + " chars")
    if s:
        print(s[:300])
    print("[2000] generating report...")
    if s:
        prompt = ("用中文写一份关于《" + g + "》的 Markdown 研究报告。\n"
                  "严格要求：\n"
                  "1. 只基于下面提供的资料，不要编造资料以外的任何事实、数据、文献。\n"
                  "2. 不要编造参考文献、作者、期刊名。\n"
                  "3. 末尾列出资料中出现的 URL。\n"
                  "4. 用中文输出。\n\n资料：\n" + s)
    else:
        prompt = ("用中文写一份关于《" + g + "》的 Markdown 研究报告。\n"
                  "严格要求：\n"
                  "1. 只写你确定知道的事实。不确定的，直接说\"我不确定\"。\n"
                  "2. 绝对不要编造参考文献、作者、期刊名。\n"
                  "3. 报告末尾不要列 References，除非你确定文献真实存在。\n"
                  "4. 用中文输出。")
    r = post("/chat/completions", {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2048
    })
    print("=" * 50)
    print(r["choices"][0]["message"].get("content", ""))

main(sys.argv[1] if len(sys.argv) > 1 else "solid state battery")