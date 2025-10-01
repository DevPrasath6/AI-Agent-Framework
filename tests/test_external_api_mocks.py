import asyncio
import pytest
from unittest import mock

# Mock yfinance and requests used by demo scripts
@pytest.mark.asyncio
async def test_yfinance_history_mock(monkeypatch):
    # Create a fake DataFrame-like object
    class FakeHistory:
        def __init__(self):
            from collections import OrderedDict
            self._data = []
        def empty(self):
            return len(self._data) == 0
        def iterrows(self):
            for i, row in enumerate(self._data):
                yield (i, row)
        def __len__(self):
            return len(self._data)
        def tail(self, n):
            return self._data[-n:]

    class FakeTicker:
        def __init__(self, symbol):
            self.symbol = symbol
            self._history = FakeHistory()
            # populate with fake rows similar to yfinance
            for i in range(10):
                self._history._data.append({
                    'Close': 100.0 + i,
                    'Volume': 1000 + i * 10
                })
        def history(self, period, interval):
            return self._history

    # Patch yfinance.Ticker to return our FakeTicker
    import yfinance as yf
    monkeypatch.setattr(yf, 'Ticker', FakeTicker)

    # Import the module under test lazily
    from test_stock_agent import StockMonitorAgent, ExecutionContext

    agent = StockMonitorAgent(change_threshold=0.1)
    # Simulate running the async test function sequence
    # Use the fake ticker inside the test function directly
    ticker = yf.Ticker('AAPL')
    history = ticker.history(period='1d', interval='5m')
    assert len(history) == 10

    # feed last 3 entries to agent to ensure no crash
    for i, row in enumerate(history.tail(3)):
        data = {'symbol': 'AAPL', 'price': float(row['Close']), 'timestamp': '2025-10-02T12:00:00'}
        ctx = ExecutionContext(agent_id=agent.id)
        res = await agent.run(data, ctx)
        assert res['status'] == 'completed'
        assert 'analysis' in res['output']

@pytest.mark.asyncio
async def test_requests_api_mock(monkeypatch):
    import requests

    class FakeResponse:
        def __init__(self, status=200, json_data=None):
            self.status_code = status
            self._json = json_data or {"ok": True}
        def json(self):
            return self._json

    def fake_get(url, *args, **kwargs):
        return FakeResponse(200, {"message": "ok"})

    monkeypatch.setattr(requests, 'get', fake_get)

    # Call a simple request to verify monkeypatch
    resp = requests.get('https://example.com/health')
    assert resp.status_code == 200
    assert resp.json()['message'] == 'ok'
