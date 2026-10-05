# Running win2000_agent.py on real Windows 2000 with TLS 1.2

## The problem

Windows 2000's Python 2.7.8 ships OpenSSL 0.9.8, which only supports TLS 1.0.

Every modern LLM API requires TLS 1.2. So the agent can't talk to Zhipu / DeepSeek / OpenAI directly.

## The solution: stunnel

We put a small TLS 1.2 proxy in front of Python.

    Python 2.7 (HTTP only)
        |
        v
    127.0.0.1:8443
        |
        v
    stunnel.exe (OpenSSL 1.0.2, TLS 1.2)
        |
        v
    open.bigmodel.cn:443

Python talks plain HTTP to localhost. stunnel upgrades the connection to TLS 1.2 on the way out.

### Why this works

- stunnel ships its own OpenSSL 1.0.2 build, which supports TLS 1.2
- OpenSSL 1.0.2 is the last branch that loads on Windows 2000
- Python 2.7 never sees TLS at all - it just talks to localhost

## Step 1: Download stunnel for Windows 2000

The last stunnel version that works on Windows 2000 is **stunnel 4.56**.

Direct link (stunnel.org mirror):

    https://www.stunnel.org/downloads/archive/4.x/stunnel-4.56-installer.exe

If the link is dead, search for "stunnel 4.56 win32 installer".

## Step 2: Install stunnel

Run `stunnel-4.56-installer.exe` on the Windows 2000 machine.

Default install path: `C:\Program Files\stunnel\`

## Step 3: Place the config file

Copy `stunnel.conf` (in this folder) to:

    C:\Program Files\stunnel\stunnel.conf

Overwrite the default one.

## Step 4: Start stunnel

    cd "C:\Program Files\stunnel"
    stunnel.exe

You should see:

    stunnel 4.56 on Win32/Win32
    Clients: 1
    Listening on 127.0.0.1:8443

## Step 5: Point the agent at localhost

In `run.bat` on the Windows 2000 machine:

    set BACKEND=zhipu
    set OPENAI_API_KEY=sk-xxx
    set OPENAI_BASE_URL=http://127.0.0.1:8443/api/paas/v4
    set MODEL=glm-4-flash
    C:\Python27\python.exe win2000_agent.py "solid state battery"

The only change is the `OPENAI_BASE_URL` - now HTTP on localhost.

## Step 6: Verify

    C:\Python27\python.exe -c "import urllib2; r=urllib2.urlopen('http://127.0.0.1:8443/api/paas/v4/models', timeout=30); print(r.getcode())"

Expected: `401` (TLS handshake succeeded through stunnel; auth rejected because no key sent).

If you see `401`, TLS 1.2 is working end-to-end on Windows 2000.

## Fallback: replace Python DLLs instead

If stunnel is unavailable, an alternative is to install Python 2.7.8 on Windows 2000, then replace:

- `DLLs\_ssl.pyd`
- `DLLs\_hashlib.pyd`
- `libeay32.dll`
- `ssleay32.dll`

with the same files from a Python 2.7.14 install (which ships OpenSSL 1.0.2).

This is not yet verified. PRs welcome.

## Status

- [x] Verified on Win7: Python 2.7.18 + OpenSSL 1.0.2t connects to Zhipu with TLS 1.2
- [ ] Verified on real Windows 2000 with stunnel (needs a tester with a real Win2000 machine)
- [ ] Verified on real Windows 2000 with DLL replacement (needs a tester)

If you have a Windows 2000 machine, please open an issue with your results.