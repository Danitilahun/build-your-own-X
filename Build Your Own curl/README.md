# Build Your Own curl (MyCurl)

A lightweight command-line HTTP client built with raw Python sockets.

## 📦 Installation

This project uses `setup.py` to package the tool and link the `mycurl` command to your system.

1. **Activate your virtual environment.**
2. **Install dependencies:**
   pip install -r requirements.txt
   pip install -e .        # Installs mycurl in editable mode

## 🚀 Usage

Once installed, run `mycurl` from any terminal.

**Syntax:**

```
mycurl <URL> [options]
```

**Supported Methods:**
GET, POST, PUT, DELETE

### Options

* `-v` — Enable verbose output (shows headers/protocol)
* `-X <METHOD>` — Custom request method
* `-d <DATA>` — Send JSON string or data
* `-H <HEADER>` — Add custom headers

---

## 🧪 Examples

### Simple GET

```bash
mycurl http://eu.httpbin.org/get -v
```

### DELETE Request

```bash
mycurl http://eu.httpbin.org/delete -X DELETE -v
```

### POST with JSON

```bash
mycurl http://eu.httpbin.org/post -X POST -d '{"name":"test"}' -H "Content-Type: application/json" -v
```