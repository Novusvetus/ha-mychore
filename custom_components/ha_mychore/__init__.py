"""Init for ha-mychore integration."""

from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.event import async_track_time_change

from .const import DOMAIN
from .data import ChoreData


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ha-mychore from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "button"])

    # Schedule daily job if not already
    if "daily_job_scheduled" not in hass.data.get(DOMAIN, {}):
        if DOMAIN not in hass.data:
            hass.data[DOMAIN] = {}
        hass.data[DOMAIN]["daily_job_scheduled"] = True
        async_track_time_change(hass, daily_chore_update, hour=0, minute=0, second=0)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, ["sensor", "button"])


async def daily_chore_update(hass, now):
    """Update due_today for all chores daily at midnight."""
    if DOMAIN not in hass.data:
        return

    chores = []

    # Collect all chores
    for entry_id, chore_data in hass.data[DOMAIN].items():
        if entry_id == "daily_job_scheduled":
            continue
        if isinstance(chore_data, ChoreData):
            # Get config_entry to access data
            for entry in hass.config_entries.async_entries(DOMAIN):
                if entry.entry_id == entry_id:
                    points = entry.data["points"]
                    interval_hours = entry.data["interval_hours"]
                    # Calculate percentage
                    if chore_data.last_done is None:
                        percentage = 100
                    else:
                        elapsed = now - chore_data.last_done
                        total = timedelta(hours=interval_hours)
                        percentage = max(0, (elapsed / total) * 100)
                    chores.append((chore_data, points, percentage))
                    break

    if not chores:
        return

    # Get target from fixed sensor
    target_sensor = "input_number.daily_chore_target"  # Fixed sensor for global target
    sensor_state = hass.states.get(target_sensor)
    if sensor_state and sensor_state.state not in ["unknown", "unavailable"]:
        try:
            target = float(sensor_state.state)
        except ValueError:
            target = 10  # fallback
    else:
        target = 10  # fallback

    # Sort by percentage descending
    chores.sort(key=lambda x: x[2], reverse=True)

    # Mark due_today
    cumulative = 0
    set_worth = True

    for chore_data, points, _ in chores:
        cumulative += points
        chore_data.set_due_today(set_worth)
        if cumulative < target:
            set_worth = True
        elif cumulative == target:
            set_worth = False
        else:
            set_worth = False
