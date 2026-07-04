import pytest
from app.services.file_generator.firmware_generator import FirmwareGenerator


def test_firmware_generator_platforms():
    gen = FirmwareGenerator()
    assert "esp32" in gen.SUPPORTED_PLATFORMS
    assert "arduino" in gen.SUPPORTED_PLATFORMS
    assert "rp2040" in gen.SUPPORTED_PLATFORMS
    assert "micropython" in gen.SUPPORTED_PLATFORMS
    assert "stm32" in gen.SUPPORTED_PLATFORMS


def test_generate_esp32_firmware():
    gen = FirmwareGenerator()
    spec = {
        "project_name": "Weather Station",
        "platform": "ESP32",
        "interfaces": ["WiFi", "I2C"],
        "sensors": [{"model": "BME280", "type": "temperature"}],
        "displays": [{"model": "SSD1306", "type": "OLED"}],
    }
    components = [{"name": "ESP32", "package": "Module"}]
    connections = [{"net_name": "I2C_SDA", "type": "signal", "pins": []}]

    code = gen.generate(spec, components, connections, platform="esp32")
    assert "#include <Arduino.h>" in code
    assert "Wire.h" in code
    assert "Weather Station" in code
    assert "WiFi.h" in code
    assert "Adafruit_BME280" in code or "bme280" in code.lower()


def test_generate_micropython_firmware():
    gen = FirmwareGenerator()
    spec = {
        "project_name": "IoT Sensor",
        "platform": "MicroPython",
        "sensors": [{"model": "BME280", "type": "temperature"}],
        "interfaces": [],
        "displays": [],
    }
    code = gen.generate(spec, [], [], platform="micropython")
    assert "import time" in code
    assert "machine" in code
    assert "IoT Sensor" in code


def test_generate_stm32_firmware():
    gen = FirmwareGenerator()
    spec = {
        "project_name": "Motor Controller",
        "platform": "STM32",
        "interfaces": [],
        "sensors": [],
        "displays": [],
    }
    code = gen.generate(spec, [], [], platform="stm32")
    assert "stm32f1xx_hal.h" in code
    assert "Motor Controller" in code
    assert "HAL_Init" in code
