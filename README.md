# ha-mychore

## Overview

Home Assistant integration for managing chores with points, intervals, and daily targets.

## Features

- **Chore Tracking**: Track when chores were last done and calculate overdue percentage.
- **Points System**: Assign points to each chore for different workloads.
- **Daily Targets**: Automatically mark chores as "due today" based on a daily point target, prioritizing the most overdue chores.
- **Persistent Storage**: Last done times are saved and persist across restarts.
- **Multi-language Support**: English and German translations.

## Installation

...

## Configuration

### Setting up a Chore

1. Add the integration and configure:
   - **Name**: Name of the chore (e.g., "Clean Kitchen").
   - **Points**: Point value for workload (e.g., 5).
   - **Interval Hours**: How often the chore should be done (e.g., 24 for daily).

2. In Options, you can adjust Points and Interval Hours.

### Global Daily Target

Create an Input Number helper in Home Assistant with Entity ID `input_number.daily_chore_target` and set the desired daily point target (e.g., 10). The integration will read this value daily at midnight to determine which chores are due today.

## Entities

For each chore, the integration creates:

- **Sensor**: Shows the overdue percentage (0-100%). Attributes include `last_done`, `points`, `interval_hours`, and `due_today`.
- **Button**: Press to mark the chore as done (sets `last_done` to now).

## How It Works

- The sensor calculates the percentage of time elapsed since `last_done` relative to the interval.
- Daily at 00:00, all chores are sorted by overdue percentage (descending).
- Chores are marked as `due_today = true` until the cumulative points reach or exceed the daily target.
- The most overdue chores get priority.

## License

3-clause BSD license
See [License](LICENSE)

## Bugs and Contributing

See [Contributing](CONTRIBUTING.md)

## Thanks to

- Home Assistant community for inspiration.

## Links

- [ReindeerWeb](https://www.reindeer-web.de)
- [Novusvetus](https://www.novusvetus.de)
- [License](./LICENSE)
- [Contributing](./CONTRIBUTING.md)
