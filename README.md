# Date-Time MCP Server

A Model Context Protocol (MCP) server that provides AI assistants with structured date, time, timezone, and date calculation capabilities.

Built with Python 3.13 and FastMCP, this project exposes reusable date-time utilities through MCP tools. It is designed to act as a shared date-time service that can be integrated with other MCP servers, AI agents, and applications.

The server follows a modular, service-based architecture, separating MCP tool definitions, date-time operations, timezone handling, validation, configuration, and error handling.

## ✨ Features

- **Current Date and Time** — Retrieve the current date, time, weekday, timezone, and UTC offset.
- **Timezone Information** — Retrieve timezone details, UTC offset, abbreviation, and daylight-saving information.
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
- **Centralized Error Handling** — Handle expected validation errors and log unexpected tool failures.
- **Automated CI** — Run the test suite automatically through GitHub Actions.

## 🛠️ Tech Stack

| Technology / Library | Purpose |
|---|---|
| Python 3.13 | Core implementation |
| Model Context Protocol (MCP) | Exposes date-time functionality to AI assistants |
| FastMCP | MCP server and tool registration |
| `datetime` | Date and time manipulation |
| `calendar` | Month and calendar calculations |
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

## 🧠 Architecture

```text
                 AI Assistant / MCP Client
                            |
                       MCP Tool Calls
                            |
                            v
                    FastMCP Server
                       server.py
                            |
                            v
                     MCP Tool Layer
                    (14 MCP Tools)
                            |
       +--------------------+--------------------+
       |                    |                    |
       v                    v                    v
  Current Date          Timezone             Relative Date
   Services             Service                Service
       |                    |                    |
       +--------------------+--------------------+
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
         Date Range      Date Parser     Difference
          Service         Service        Services
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
                     Python Libraries
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
2. **Service Layer:** Handles date-time calculations and business logic.
3. **Utility Layer:** Provides reusable functions for date calculations, timezone conversions, formatting, validation, and error handling.
4. **Configuration Layer:** Manages default timezone, date formats, time formats, and operation limits.
5. **Model Layer:** Defines structured input schemas using Pydantic.

The MCP server does not maintain email history, calendar events, or user activity. It provides stateless date-time operations that other MCP servers and AI agents can reuse.

## 🔧 Available MCP Tools

The server currently provides 14 MCP tools.

| # | Tool | Description |
|---|---|---|
| 1 | `get_current_datetime` | Retrieve the current date and time for a specified timezone. |
| 2 | `get_current_date` | Retrieve today's date and weekday for a specified timezone. |
| 3 | `get_current_time` | Retrieve the current local time and UTC offset. |
| 4 | `get_timezone_info` | Retrieve timezone name, UTC offset, abbreviation, and daylight-saving information. |
| 5 | `calculate_relative_date` | Calculate a past or future date using days, weeks, months, and years. |
| 6 | `calculate_relative_datetime` | Calculate a past or future datetime using seconds, minutes, hours, days, and weeks. |
| 7 | `get_previous_n_days` | Retrieve a specified number of previous dates, excluding today. |
| 8 | `get_next_n_days` | Retrieve a specified number of upcoming dates, excluding today. |
| 9 | `get_week_dates` | Retrieve all seven dates belonging to a specified week. |
| 10 | `get_date_range` | Calculate date range details and duration. |
| 11 | `parse_natural_datetime` | Convert natural-language date-time expressions into structured values. |
| 12 | `get_month_dates` | Retrieve all dates belonging to a specified month and year. |
| 13 | `calculate_date_difference` | Calculate the difference between two dates. |
| 14 | `calculate_time_difference` | Calculate elapsed time between two datetime values. |

### Tool Usage Examples

**1. Current date and time**

```text
Get the current date and time in Asia/Kolkata.
```

**2. Relative date calculation**

```text
Calculate the date 3 months from today.
```

**3. Previous dates**

```text
Get the previous 7 dates.
```

**4. Weekly dates**

```text
Get all dates for the week containing 2026-11-05.
```

**5. Natural-language parsing**

```text
Tomorrow at 5 PM
Next Monday at 10 AM
3 days from now
Next month
```

**6. Date difference**

```text
Calculate the number of days between
2026-11-05 and 2026-12-05.
```

**7. Time difference**

```text
Calculate the time difference between
2026-11-05T10:00:00+05:30 and
2026-11-05T12:00:00+05:30.
```

Natural-language parsing can be ambiguous. Applications performing important operations, such as creating calendar events, should confirm ambiguous date-time interpretations before executing them.

## 📁 Project Structure

```text
datetime-mcp/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── config/
│   └── settings.py
│
├── models/
│   └── datetime_model.py
│
├── services/
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
│   ├── datetime_utils.py
│   ├── timezone_utils.py
│   ├── validator.py
│   ├── formatters.py
│   └── error_handler.py
│
├── tests/
│   ├── unit/
│   ├── services/
│   ├── models/
│   ├── integration/
│   └── conftest.py
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
| `settings.py` | Default timezone, date/time formats, and operation limits |
| `models/` | Pydantic input models |
| `datetime_model.py` | Date-time input schemas and validation |
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
| `validator.py` | Input and range validation |
| `formatters.py` | Structured date-time formatting |
| `error_handler.py` | Centralized MCP tool error handling |
| `tests/unit/` | Utility unit tests |
| `tests/services/` | Service-level tests |
| `tests/models/` | Pydantic model tests |
| `tests/integration/` | MCP server integration and schema tests |
| `tests/conftest.py` | Shared pytest fixtures |
| `server.py` | FastMCP server and tool definitions |
| `.github/workflows/ci.yml` | GitHub Actions CI workflow |

## 🚀 Getting Started

### Prerequisites

- Python 3.13
- [uv](https://docs.astral.sh/uv/)
- [Git](https://git-scm.com/)
- Windows, Linux, or macOS

### 1. Clone the Repository

```bash
git clone https://github.com/satyamnewale/datetime-mcp.git

cd datetime-mcp
```

### 2. Install Dependencies

The repository includes `uv.lock` for reproducible dependency installation.

Run:

```bash
uv sync --locked --dev
```

This creates the project environment and installs the locked runtime and development dependencies.

### 3. Configure Environment Variables

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

Keep environment-specific configuration in `.env`. Do not commit this file to GitHub.

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

## 🧪 Testing

The project uses pytest to test individual utilities, services, Pydantic models, and MCP tool execution.

### Run All Tests

```bash
uv run pytest -v
```

### Run Tests by Category

**Unit tests**

```bash
uv run pytest tests/unit -v
```

**Service tests**

```bash
uv run pytest tests/services -v
```

**Model tests**

```bash
uv run pytest tests/models -v
```

**Integration tests**

```bash
uv run pytest tests/integration -v
```

### Run a Specific Test File

```bash
uv run pytest tests/unit/test_formatters.py -v
```

### Run Tests with Coverage

```bash
uv run pytest --cov=services --cov=utils --cov-report=term-missing
```

### Testing Time-Dependent Operations

The project uses `freezegun` to freeze system time during tests.

A shared fixture is available in `tests/conftest.py`.

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

## 🔄 Continuous Integration

The project uses **GitHub Actions for Continuous Integration (CI)**.

The workflow is located at:

```text
.github/workflows/ci.yml
```

### Workflow Triggers

The CI workflow runs automatically on:

- Pushes to `main`, `master`, or `develop`.
- Pull requests targeting these branches.
- Manual execution through `workflow_dispatch`.

### CI Pipeline

```text
              GitHub Repository
                       |
                       v
                 Push / PR Event
                       |
                       v
                GitHub Actions
                       |
                       v
                Checkout Code
                       |
                       v
                Setup Python 3.13
                       |
                       v
                    Setup uv
                       |
                       v
              Install Dependencies
                 uv sync --locked
                    --dev
                       |
                       v
                 Run pytest
                       |
               +-------+-------+
               |               |
               v               v
             Passed          Failed
               |               |
               v               v
          CI Success        CI Failure
```

### CI Responsibilities

1. Checkout the repository.
2. Set up Python 3.13.
3. Install and configure uv.
4. Install locked dependencies using `uv sync --locked --dev`.
5. Run the complete test suite using `uv run pytest -v`.
6. Report the execution result in GitHub Actions.

**Note:** This workflow performs testing only. It does not deploy, publish, or host the MCP server.

View workflow executions:

https://github.com/satyamnewale/datetime-mcp/actions

## ⚠️ Error Handling

The project uses centralized error handling for MCP tool execution.

### Error Handling Responsibilities

| Error Type | Handling |
|---|---|
| Invalid input | Pydantic model validation |
| Invalid timezone | Meaningful validation error |
| Invalid date/time | Date-time validation error |
| Unsupported unit or direction | Input validation |
| Invalid calculation range | Range validation |
| Unexpected internal exception | Log details and return a generic error message |

### Error Handling Flow

```text
             MCP Tool Call
                   |
                   v
             Input Validation
                   |
           +-------+-------+
           |               |
           v               v
         Valid           Invalid
           |               |
           v               v
       Service Layer    Validation Error
           |
           v
       Calculation
           |
     +-----+-----+
     |           |
     v           v
  Success     Exception
     |           |
     v           v
 Structured   Error Handler
  Response       |
                 v
          +------+------+
          |             |
          v             v
       Expected     Unexpected
        Error         Error
          |             |
          v             v
      Meaningful    Log Internally
       Message          |
                        v
                 Safe Error Message
```

The error handler is implemented in `utils/error_handler.py` and applied to the MCP tool functions in `server.py`.

Expected validation and value errors are communicated with meaningful messages. Unexpected errors are logged internally and returned to the caller as a generic internal-error message.

FastMCP also performs tool argument validation. Errors rejected by FastMCP before a tool function starts are handled by FastMCP itself.

## 📚 Date-Time Documentation

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
| `strptime()` | Parses formatted date-time values |
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
- Daylight-saving time
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

Example:

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

The parser should receive an explicit timezone and reference datetime when predictable results are required.

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
- Model validators

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

## 🔌 Codex Integration

OpenAI Codex CLI can connect to local MCP servers and use their tools during development.

### 1. Install Codex CLI

Official documentation:

https://developers.openai.com/codex/cli/

Follow the official installation instructions for your operating system.

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

Start Codex:

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
Schedule a meeting 3 days from now at 10