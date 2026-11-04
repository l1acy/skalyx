# OpenWeatherMap Integration Guide

This guide explains how to add **OpenWeatherMap** as a data source in Skalyx. By using the HTTP adapter, Skalyx will periodically poll the OpenWeatherMap API and ingest current weather data for your chosen location

# Prerequisites
- **OpenWeatherMap**: You need a free account to obtain an API key
- **Coordinates**: You will need the latitude and longitude of the location you want to monitor

# 1. Obtain an OpenWeatherMap API key
1. Go to the [OpenWeatherMap sign-up page](https://home.openweathermap.org/users/sign_up) and create a free account
2. After verifying your email, log in and navigate to the [API key section](https://home.openweathermap.org/api_keys) of your account dashboard
3. Generate a new API key (or use the default one provided) and copy it:
  - *Note*: A newly created API key may take a few hours to become active

# 2. Configure Skalyx
Open your skalyx.toml configuration file (located in the server directory) and add the following [[devices]] block:

```toml
[[devices]]
device_id = "openweathermap"
address = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={appid}&units=metric"
parser = "openweathermap"
ask_interval = 900.0

[devices.parser_params]
lat = YOUR_LAT
lon = YOUR_LON
appid = "YOUR_API_KEY"
```

**Important**: Leave the `address` and `parser` fields exactly as they are. Edit **only** `devices.parser_params` section
