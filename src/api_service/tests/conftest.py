def pytest_configure(config):
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )