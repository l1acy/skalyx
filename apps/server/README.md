# Installing
You need Python 3.12+

## 1. Clone the repository
```bash
git clone https://github.com/l1acy/skalyx
cd skalyx
```

## 2. Installing dependencies
```bash
cd apps/server
python -m venv .venv
source .venv/bin/activate  # For Windows: .venv\scripts\activate
pip install -r requirements.txt
```

# 3. (Optional) Frontend building
If you need to serve the Skalyx dashboard via the main backend (e.g., if Node.js cannot be installed on the server due to permission restrictions).

```bash
cd ../../apps/client
npm install
npm run build
cd ../../apps/server
```

# 4. Run the server
```bash
python -m skalyx --host 127.0.0.1 --port 1823
```
