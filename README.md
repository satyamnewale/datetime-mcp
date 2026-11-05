# Date-Time MCP Server

A Model Context Protocol (MCP) server that provides AI assistants with structured date, time, timezone, and date calculation capabilities.

Built with Python and FastMCP, this project exposes reusable date-time utilities through MCP tools. It is designed to act as a shared date-time service that can be integrated with other MCP servers, AI agents, and applications.

The server follows a modular service-based architecture, separating MCP tool definitions, date-time operations, timezone handling, validation, and configuration.

## ✨ Features

- **Current Date and Time** — Retrieve the current date, time, weekday, timezone, and UTC offset.
- **Timezone Information** — Retrieve timezone details, UTC offset, abbreviation, and daylight saving information.
- **Relative Date Calculation** — Calculate dates in the past or future using days, weeks, months, and years.
- **Relative Date-Time Calculation** — Calculate past or future date-times using seconds, minutes, hours, days, and weeks.
- **Previous and Next Dates** — Retrieve a specified number of previous or upcoming dates.
- **Weekly Date Calculation** — Retrieve all seven dates belonging to a particular week.
- **Date Range Calculation** — Calculate the duration and details of a date range.
- **Natural Language Date Parsing** — Convert expressions such as "tomorrow at 5 PM" into structured date-time values.
- **Monthly Date Retrieval** — Retrieve all dates belonging to a specified month.
- **Date Difference** — Calculate the difference between two dates.
- **Time Difference** — Calculate elapsed time between two date-time values.
- **Timezone-Aware Operations** — Perform date-time operations using IANA timezone identifiers.
- **Input Validation** — Validate dates, times, timezones, units, and calculation ranges.

## 🛠️ Tech Stack

| Technology / Library | Purpose |
|---|---|
| Python 3.13 | Core implementation |
| Model Context Protocol (MCP) | Exposes date-time functionality to AI assistants |
| FastMCP | MCP server and tool registration |
| `datetime` | Date and time manipulation |
| `zoneinfo` | IANA timezone handling |
| `python-dateutil` | Relative date calculations, including months and years |
| `dateparser` | Natural language date-time parsing |
| `tzdata` | Timezone database support, particularly on Windows |
| `pydantic` | Input models and data validation |
| `pydantic-settings` | Environment-based configuration |
| `uv` | Python project and dependency management |
| `pytest` | Automated testing |
| `pytest-mock` | Mocking dependencies during tests |
| `pytest-asyncio` | Asynchronous testing |
| `freezegun` | Controlling system time during tests |
| `pytest-cov` | Test coverage reporting |

### Important Python Modules

The project also uses Python standard-library modules:

| Module | Purpose |
|---|---|
| `datetime` | Date, time, and datetime objects |
| `calendar` | Month and calendar calculations |
| `zoneinfo` | Timezone conversion and timezone-aware datetime objects |
| `time` | Time-related utilities |
| `re` | Input format validation |

## 🧠 Architecture

```text
                 AI Assistant / MCP Client
                            |
                            | MCP Tool Calls
                            v
                    FastMCP Server
                       server.py
                            |
                            v
                     MCP Tool Layer
                            |
       +--------------------+--------------------+
       |                    |                    |
       v                    v                    v
 Current Date          Timezone             Relative Date
   Service              Service                Service
       |                    |                    |
       +--------------------+--------------------+
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
         Date Range      Date Parser     Difference
          Service         Service         Services
             |              |              |
             +--------------+--------------+
                            |
                            v
                     Utility Layer
                            |
       +--------------------+--------------------+
       |                    |                    |
       v                    v                    v
  DateTime Utils      Timezone Utils        Validators
       |                    |                    |
       +--------------------+--------------------+
                            |
                            v
                  Python Date-Time Libraries
                            |
                            v
                    Structured Responses
                            |
                            v
                     AI Assistant / MCP
```

### Architecture Explanation

The server uses a layered architecture.

1. **MCP Layer:** Exposes date-time operations as individual MCP tools through FastMCP.
2. **Service Layer:** Handles the actual date-time calculations and operations.
3. **Utility Layer:** Provides reusable functions for date calculations, timezone conversions, formatting, and validation.
4. **Configuration Layer:** Manages default timezone, date formats, time formats, and operation limits.
5. **Model Layer:** Defines structured input schemas using Pydantic.

The MCP server does not maintain email history, calendar events, or user activity. It provides stateless date-time operations that other MCP servers and AI agents can reuse.

## 🔧 Available MCP Tools

The server currently provides 14 MCP tools.

### 1. `get_current_datetime`

Retrieve the current date and time for a specified timezone.

Returns:
- Current date
- Current time
- Weekday
- Timezone
- UTC offset
- ISO-formatted datetime

Example:
```text
Get the current date and time in Asia/Kolkata.
```

### 2. `get_current_date`

Retrieve today's date and weekday for a specified timezone.

Example:
```text
What is today's date in Asia/Kolkata?
```

### 3. `get_current_time`

Retrieve the current time for a specified timezone.

Example:
```text
What time is it currently in UTC?
```

### 4. `get_timezone_info`

Retrieve information about an IANA timezone.

Returns:
- Timezone name
- UTC offset
- Timezone abbreviation
- Daylight saving information
- Current local datetime

Example:
```text
Get timezone information for Europe/Berlin.
```

### 5. `calculate_relative_date`

Calculate a date in the past or future.

Supported units:
- Days
- Weeks
- Months
- Years

Example:
```text
Calculate the date 3 months from today.
```

### 6. `calculate_relative_datetime`

Calculate a past or future datetime using a specified duration.

Supported units:
- Seconds
- Minutes
- Hours
- Days
- Weeks

Example:
```text
What will the date and time be 48 hours from now?
```

### 7. `get_previous_n_days`

Retrieve a specified number of previous dates, excluding today.

Example:
```text
Get the previous 7 dates.
```

### 8. `get_next_n_days`

Retrieve a specified number of upcoming dates, excluding today.

Example:
```text
Get the next 10 dates.
```

### 9. `get_week_dates`

Retrieve the seven dates belonging to a specified week.

Supports:
- Reference date
- Configurable week start
- Monday-based week by default
- Sunday-based week when configured

Example:
```text
Get all dates for the week containing 2026-11-05.
```

### 10. `get_date_range`

Retrieve information about a date range.

Returns:
- Start date
- End date
- Total number of days
- Range details

Example:
```text
Calculate the date range from 2026-11-01 to 2026-11-30.
```

### 11. `parse_natural_datetime`

Convert natural language date-time expressions into structured datetime values.

Examples:
```text
Tomorrow at 5 PM
Next Monday at 10 AM
3 days from now
Next month
```

The parser uses a specified timezone and a relative reference datetime.

**Note:** Natural-language parsing can be ambiguous. Applications performing important operations, such as creating calendar events, should confirm ambiguous date-time interpretations before executing them.

### 12. `get_month_dates`

Retrieve all dates belonging to a specified month and year.

Example:
```text
Get all dates for November 2026.
```

### 13. `calculate_date_difference`

Calculate the difference between two dates.

Returns:
- Absolute difference in days
- Signed difference
- Difference in weeks and remaining days
- Direction of the difference

Example:
```text
Calculate the number of days between 2026-11-05 and 2026-12-05.
```

### 14. `calculate_time_difference`

Calculate elapsed time between two datetime values.

Returns:
- Difference in seconds
- Difference in minutes
- Difference in hours
- Difference in days
- Direction of the difference

Supports timezone-aware datetime values and ISO 8601 datetime strings.

Example:
```text
Calculate the time difference between
2026-11-05T10:00:00+05:30 and
2026-11-05T12:00:00+05:30.
```

## 📁 Project Structure

```text
datetime-mcp/
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── models/
│   ├── __init__.py
│   └── datetime_models.py
│
├── services/
│   ├── __init__.py
│   ├── current_datetime.py
│   ├── timezone_service.py
│   ├── relative_date.py
│   ├── relative_datetime.py
│   ├── date_range.py
│   ├── date_parser.py
│   ├── month_service.py
│   ├── date_difference.py
│   └── time_difference.py
│
├── utils/
│   ├── __init__.py
│   ├── datetime_utils.py
│   ├── timezone_utils.py
│   ├── validators.py
│   └── formatters.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_current_datetime.py
│   ├── test_timezone.py
│   ├── test_relative_date.py
│   ├── test_relative_datetime.py
│   ├── test_date_range.py
│   ├── test_date_parser.py
│   ├── test_month_service.py
│   ├── test_date_difference.py
│   ├── test_time_difference.py
│   ├── test_validators.py
│   └── test_mcp_server.py
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
├── server.py
└── README.md
```

### Folder Responsibilities

| Folder / File | Responsibility |
|---|---|
| `config/` | Application configuration |
| `settings.py` | Default timezone, formats, and operation limits |
| `models/` | Pydantic input models |
| `datetime_models.py` | Date-time input schemas |
| `services/` | Core date-time business logic |
| `current_datetime.py` | Current date and time retrieval |
| `timezone_service.py` | Timezone information |
| `relative_date.py` | Relative date and weekly date calculations |
| `relative_datetime.py` | Relative datetime calculations |
| `date_range.py` | Date range operations |
| `date_parser.py` | Natural-language date parsing |
| `month_service.py` | Monthly date retrieval |
| `date_difference.py` | Date difference calculations |
| `time_difference.py` | Elapsed time calculations |
| `utils/` | Shared date-time helper functions |
| `datetime_utils.py` | Date and datetime calculations |
| `timezone_utils.py` | Timezone handling and conversion |
| `validators.py` | Input and range validation |
| `formatters.py` | Structured date-time formatting |
| `tests/` | Automated test cases |
| `conftest.py` | Shared pytest fixtures |
| `server.py` | FastMCP server and tool definitions |

## 🚀 Getting Started

### Prerequisites

- Python 3.13
- [uv](https://docs.astral.sh/uv/)
- [Git](https://git-scm.com/)
- Windows, Linux, or macOS

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/datetime-mcp.git
cd datetime-mcp
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

```bash
uv venv
```

Activate it in PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

Install the project dependencies:

```bash
uv sync
```

Alternatively, install the runtime dependencies individually:

```bash
uv add fastmcp pydantic pydantic-settings python-dateutil tzdata dateparser
```

Install testing dependencies:

```bash
uv add --dev pytest pytest-mock pytest-asyncio freezegun pytest-cov
```

### 4. Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a reference.

Example:

```env
DEFAULT_TIMEZONE=Asia/Kolkata
DEFAULT_DATE_FORMAT=%Y-%m-%d
DEFAULT_TIME_FORMAT=%H:%M:%S
WEEK_STARTS_ON=0
MAX_DATE_RANGE_DAYS=366
MAX_LIST_DAYS=366
```

### Configuration Options

| Variable | Description | Default |
|---|---|---|
| `DEFAULT_TIMEZONE` | Default IANA timezone | `Asia/Kolkata` |
| `DEFAULT_DATE_FORMAT` | Date output format | `%Y-%m-%d` |
| `DEFAULT_TIME_FORMAT` | Time output format | `%H:%M:%S` |
| `WEEK_STARTS_ON` | First day of week (0 = Monday, 6 = Sunday) | `0` |
| `MAX_DATE_RANGE_DAYS` | Maximum permitted date range | `366` |
| `MAX_LIST_DAYS` | Maximum permitted date list size | `366` |

## 📚 Date-Time Documentation

The project uses Python's standard date-time functionality alongside specialized libraries.

### 1. Python Datetime

Official documentation:

https://docs.python.org/3/library/datetime.html

Important classes and methods:

| Class / Method | Purpose |
|---|---|
| `date` | Represents a calendar date |
| `time` | Represents a time of day |
| `datetime` | Represents a date and time |
| `timedelta` | Represents a duration |
| `datetime.now()` | Retrieves the current datetime |
| `datetime.fromisoformat()` | Parses ISO-formatted datetime strings |
| `date.fromisoformat()` | Parses ISO-formatted dates |
| `strftime()` | Formats date-time values |
| `strptime()` | Parses formatted date-time strings |
| `astimezone()` | Converts an aware datetime to another timezone |

### 2. ZoneInfo

Official documentation:

https://docs.python.org/3/library/zoneinfo.html

Used for IANA timezone support.

Important concepts:

- `ZoneInfo("Asia/Kolkata")`
- `ZoneInfo("UTC")`
- `datetime.astimezone()`
- UTC offsets
- Daylight saving time
- Timezone-aware datetime objects

### 3. Python Dateutil

Official documentation:

https://dateutil.readthedocs.io/

Used for calendar-aware relative date calculations.

Important functionality:

- `relativedelta`
- Month calculations
- Year calculations
- Relative date arithmetic
- Calendar-aware date adjustments

`relativedelta` is useful because adding one month is not equivalent to adding a fixed number of days.

### 4. Dateparser

Official documentation:

https://dateparser.readthedocs.io/

Used to interpret natural-language date-time expressions.

Examples:

```python
import dateparser

result = dateparser.parse(
    "tomorrow at 5 PM",
    settings={
        "TIMEZONE": "Asia/Kolkata",
        "RETURN_AS_TIMEZONE_AWARE": True
    }
)
```

The parser should receive an explicit timezone and reference datetime when the application needs predictable results.

### 5. Pydantic

Official documentation:

https://docs.pydantic.dev/latest/

Used to define and validate structured input models.

Important concepts:

- `BaseModel`
- Field validation
- Type validation
- Optional fields
- Literal types
- Field constraints

### 6. FastMCP

Official documentation:

https://gofastmcp.com/

Used to create the MCP server and expose Python functions as MCP tools.

Important concepts:

- `FastMCP`
- `@mcp.tool()`
- Tool descriptions
- Input schemas
- STDIO transport
- MCP client-server communication

## 🧪 Testing

The project uses pytest to test individual services, utilities, validation logic, and MCP tool execution.

### Run All Tests

```bash
uv run pytest -v
```

### Run a Specific Test File

```bash
uv run pytest tests/test_current_datetime.py -v
```

### Run Tests with Coverage

```bash
uv run pytest --cov=services --cov=utils --cov-report=term-missing
```

### Testing Time-Dependent Operations

The project uses `freezegun` to freeze the system time during tests.

Example:

```python
import pytest
from freezegun import freeze_time


@pytest.fixture
def frozen_time():
    with freeze_time("2026-11-05 10:00:00", tz_offset=0):
        yield
```

This makes date-time tests predictable and repeatable.

## ▶️ Running the MCP Server

Run the following command from the project root:

```bash
uv run fastmcp run server.py --transport stdio
```

To inspect the server during development:

```bash
uv run fastmcp dev server.py
```

The server uses STDIO transport, allowing an MCP client to launch the local process and communicate with it.

## 🔌 Codex Integration

OpenAI Codex CLI can connect to local MCP servers and use their tools during development.

### 1. Install Codex CLI

Official documentation:

https://developers.openai.com/codex/cli/

On Windows, open PowerShell and execute:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

Alternatively, install through npm:

```bash
npm install -g @openai/codex
```

Verify installation:

```bash
codex --version
```

### 2. Authenticate Codex

Start Codex:

```bash
codex
```

Complete the sign-in process using an available authentication method.

### 3. Register the Date-Time MCP Server

Register the local server using:

```powershell
codex mcp add datetime_mcp -- "PATH_TO_UV_EXE" run --directory "PATH_TO_DATETIME_MCP" fastmcp run server.py --transport stdio
```

Replace:

- `PATH_TO_UV_EXE` with the absolute path to your `uv.exe` executable.
- `PATH_TO_DATETIME_MCP` with the absolute path to the Date-Time MCP project directory.

For example, if your project is stored at:

```text
C:\Users\YourUsername\Projects\datetime-mcp
```

Use the corresponding absolute paths in the registration command.

You can find the `uv.exe` location using:

```powershell
(Get-Command uv).Source
```

### 4. Verify MCP Connection

```bash
codex mcp list
```

The registered `datetime_mcp` server should appear in the list.

To inspect its configuration:

```bash
codex mcp get datetime_mcp
```

### 5. Test the Tools in Codex

Start Codex inside your project or another working directory:

```bash
codex
```

Try prompts such as:

```text
Use the datetime MCP server to get the current date and time in Asia/Kolkata.
```

```text
Calculate the date 45 days from today.
```

```text
Find the date and time 72 hours from now in Europe/Berlin.
```

```text
Parse "next Monday at 10 AM" into a datetime.
```

Codex can discover and invoke the tools exposed by the connected MCP server.

## 💻 ChatGPT for Windows

ChatGPT for Windows can be used alongside Codex during development.

Download:

https://chatgpt.com/download/

ChatGPT can assist with:

- Understanding the project architecture.
- Learning Python datetime and timezone operations.
- Understanding FastMCP implementation.
- Reviewing service and utility classes.
- Debugging date-time calculation errors.
- Writing and improving tests.
- Designing integrations with other MCP servers.

**Note:** Installing the ChatGPT Windows application does not automatically connect it to this local MCP server. The Codex integration described above is configured separately.

## 🔗 Integration with Other MCP Servers

The Date-Time MCP server is designed as a reusable utility service.

It can be integrated with other MCP servers that need date-time calculations.

Potential integrations include:

| MCP Server | Possible Usage |
|---|---|
| Gmail MCP | Date-based email searches, relative date filters, and email summaries |
| Google Calendar MCP | Event date calculations, timezone conversions, and scheduling |
| Reminder MCP | Reminder dates, recurring schedules, and notification timing |
| Task Management MCP | Due dates, deadlines, and task duration calculations |
| Personal Assistant | Current date-time retrieval and natural-language date interpretation |

### Example: Gmail MCP Integration

A user asks:

```text
Find emails received in the previous 7 days.
```

Possible workflow:

```text
                AI Assistant
                     |
                     v
              Date-Time MCP
                     |
                     v
             get_previous_n_days
                     |
                     v
             Date Range Values
                     |
                     v
                 Gmail MCP
                     |
                     v
              Search Emails
                     |
                     v
                AI Response
```

The Date-Time MCP calculates the relevant dates, while the Gmail MCP performs the actual email search.

### Example: Google Calendar MCP Integration

A user asks:

```text
Schedule a meeting 3 days from now at 10 AM.
```

Possible workflow:

```text
                AI Assistant
                     |
                     v
              Date-Time MCP
                     |
                     v
            parse_natural_datetime
                     |
                     v
            Structured Datetime
                     |
                     v
             Google Calendar MCP
                     |
                     v
              Create Event
```

The Date-Time MCP handles date-time interpretation. The Calendar MCP handles event creation and availability checking.

**Important:** The Date-Time MCP calculates and returns date-time values. It does not independently create calendar events, send emails, or schedule notifications.

## 🔐 Security and Reliability

- No Google OAuth credentials or external account tokens are required.
- No API keys are required for the current date-time functionality.
- The server is designed to be stateless.
- Validate date-time inputs before performing calculations.
- Use IANA timezone identifiers instead of relying on machine-local timezone settings.
- Use timezone-aware datetime values for timezone conversions.
- Perform elapsed-time calculations in UTC to avoid daylight saving time arithmetic errors.
- Confirm ambiguous natural-language date-time interpretations before executing important operations.
- Keep environment-specific configuration in `.env`.
- Do not commit local environment files or virtual environments.

## 🤝 Credits

This project and its documentation were developed with AI assistance and reviewed by the repository owner.

**Built with Python, FastMCP, and Model Context Protocol (MCP).**