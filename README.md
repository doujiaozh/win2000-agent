# Win2000 Agent

An AI research agent that targets **Windows 2000**.

## The truth

Win2000 caps at **Python 2.7**. Python 2.7 on Win2000 ships with OpenSSL 0.9.8, which only supports **TLS 1.0**.

Modern APIs (Zhipu, Bing, DeepSeek) all require **TLS 1.2**. So:

- Code is Python 2.7 / 3.x compatible
- Code works on Python 3.x (tested on Termux)
- To run on Win2000, you must first solve TLS 1.2

That is the final boss.

## Usage

    set OPENAI_API_KEY=sk-xxx
    set OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4
    set MODEL=glm-4-flash
    python win2000_agent.py "solid state battery"

## Series

- v0.1: Windows 7 (500 lines, pydantic 1.x)
- v0.2: Windows XP (29 lines, stdlib only)
- v0.3: Windows 2000 (this repo, TLS 1.2 is the final boss)

## License

MIT