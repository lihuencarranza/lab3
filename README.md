# Atlas IoT DDL Monitor

Atlas IoT DDL Monitor is an IoT Device Management Platform based on DDL (Device Description Language). It provides a comprehensive interface for managing IoT devices, entities, services, and creating applications.

![image](https://github.com/user-attachments/assets/dc022925-b62a-4742-8508-390ba5039ca6)


## Features

- Real-time monitoring of IoT devices
- Service and entities management and discovery
- Application creation and execution
- Device relationship management
- WebSocket-based real-time updates
- Dark mode interface

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)
- Atlas server running on port 6668 (required for app execution)

## Installation

### Linux/macOS

```bash
# Deactivate any active virtual environment
deactivate

# Remove existing virtual environment (if any)
rm -rf venv

# Create a new virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Clear terminal (optional)
clear

# Run the application
python3 app.py
```

### Windows

```bash
# Deactivate any active virtual environment
deactivate

# Remove existing virtual environment (if any)
rmdir /s /q venv

# Create a new virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Clear terminal (optional)
cls

# Run the application
python app.py
```

## Important Note

For the application to work properly, you must have the Atlas server running on port 6668. The Atlas Manager communicates with the Atlas server to execute applications and manage IoT devices. If the Atlas server is not running or is running on a different port, application execution will fail.

## Project Description

Atlas Manager is an IoT Application IDE designed to help developers create and manage Atlas IoT Applications. It provides a comprehensive environment for discovering, managing, and utilizing IoT devices and their services within a Virtual Smart Space (VSS).

### Core Functionalities

#### 1. IoT Device Discovery
- Real-time monitoring of the VSS smart space
- Automatic scanning of connected IoT things
- Processing of various tweet types:
  - Thing identity
  - Service information
  - Thing language
  - Relationships
  - Entity identity
- Continuous background updates of device information

The device discovery system is implemented using Python's asyncio library for asynchronous operations. The core functionality is built around a WebSocket client (`websockets`) that maintains a persistent connection with the Atlas server. Device information is processed through a custom `TweetProcessor` class that handles different tweet types using a factory pattern. The system uses a pub/sub pattern to notify different components about device updates, implemented through Python's `asyncio.Queue` for thread-safe communication.

#### 2. Space Information Display
- Network address information
- Organized tabs for different components:
  - **Things**: Detailed information about each connected device
  - **Services**: Filterable list of available services
    - Filtering by thing ID, service name, or keywords
    - Alphabetical organization by thing
  - **Relationships**: Visual representation of service connections
    - Support for order-based relationships
    - Support for condition-based relationships
    - Ability to bind unbound relationships
  - **Apps**: Application management interface

The space information display is built using Flask for the backend and a combination of HTML5, CSS3, and JavaScript for the frontend. The data is served through RESTful APIs implemented in Flask, with real-time updates handled by Socket.IO. The UI components are built using Bootstrap 5 for responsive design, and custom JavaScript modules handle the dynamic content updates. The filtering system uses a combination of client-side JavaScript for immediate filtering and server-side Python for more complex queries.

#### 3. IoT Application Editor
Supports three types of application structures:
1. **Sequential Services**: Ordered execution of services {S1, S2, S3, ...}
2. **Order-based Relationships**: Service B runs after Service A completes
3. **Condition-based Relationships**: Service B runs based on Service A's return value

Features:
- Interactive GUI-based editor
- Drag-and-drop service arrangement
- Clear and finalize operations
- Real-time validation
- Automatic relationship guidance

The application editor is implemented as a single-page application (SPA) using Vue.js for the frontend. The drag-and-drop functionality is powered by the `vue-draggable` library, while the relationship visualization uses the `vis.js` network graph library. The editor's state management is handled through Vuex, ensuring consistent state across components. The validation system is implemented in Python using a custom validation engine that checks service compatibility and relationship constraints.

#### 4. Application Management
- **Save**: Local storage of applications in .iot format
- **Upload**: Import existing applications for modification
- **Activate**: Start application execution
- **Stop**: End execution and clean up resources
- **Delete**: Remove applications from the system
- Status tracking for running applications

Application management is handled through a combination of Python backend services and JavaScript frontend components. The backend uses a custom `ApplicationManager` class that implements the singleton pattern to ensure consistent application state. File operations are handled using Python's `json` module for serialization, while the execution engine uses `asyncio` for concurrent application execution. The status tracking system uses a combination of WebSocket events and a Redis-based pub/sub system for real-time updates.

### Key Features
- Real-time updates via WebSocket
- Automatic service discovery
- Relationship visualization
- Application lifecycle management
- Status monitoring
- Error handling and recovery
- Clean and intuitive interface

The real-time update system is built on top of Socket.IO, with a custom event system implemented in Python using the `python-socketio` library. The service discovery mechanism uses a combination of UDP multicast for initial device discovery and TCP for persistent connections. The relationship visualization is implemented using the `vis.js` library with custom layout algorithms. Error handling is implemented through a custom exception hierarchy and a centralized logging system using Python's `logging` module.

## Project Structure

```
├── atlas/              # Atlas
├── atlas_apps/         # Apps created
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── apps.html
│   ├── base.html
│   ├── entities.html
│   ├── index.html
│   ├── relationships.html
│   ├── services.html
│   └── things.html
└── venv/              # Virtual environment (not tracked in git)

```

The project follows a modular architecture with clear separation of concerns:
- Backend: Python 3.8+ with Flask framework
- Frontend: HTML5, CSS3, JavaScript (ES6+)
- Real-time Communication: WebSocket (Socket.IO)
- Database: SQLite for local storage
- Testing: pytest for unit tests
- Build System: Custom Python scripts for dependency management

## Usage

1. Ensure Atlas server is running on port 6668
2. Access the web interface at `http://localhost:5000`
3. Navigate through different sections:

### Dashboard
- Real-time monitoring of system metrics and device status
- Key features:
  - System overview with active devices count
  - Service utilization statistics
  - Application execution status
  - Network connectivity status
  - Resource usage monitoring
- Interactive charts and graphs:
  - Device connection trends
  - Service call frequency
  - Application performance metrics
  - System resource utilization
- Quick access to:
  - Active applications
  - Connected devices
  - Recent service calls
  - System alerts and notifications
- Customizable widgets and layouts
- Real-time data updates via WebSocket


The dashboard is built using a combination of Chart.js for data visualization and custom JavaScript modules for real-time updates. The data collection system uses Python's `asyncio` for concurrent metric gathering, with a custom metrics collector class. The WebSocket implementation uses Socket.IO for real-time updates, with a custom event system for different metric types. The widget system is implemented using a custom JavaScript framework that supports dynamic loading and layout management.


### Things Page
- Displays a comprehensive list of all connected IoT devices
- Each device entry shows:
  - Device ID and name
  - Available services
  - Current status
  - Connection details
- Real-time updates when devices connect/disconnect
- Search and filter capabilities
- Detailed view for each device with service information

![image](https://github.com/user-attachments/assets/0c2720f2-8212-4e5a-a9b9-5109b0585721)

The Things page is implemented using Flask's template engine (Jinja2) for server-side rendering, with dynamic updates handled by JavaScript. The device list is managed through a custom `DeviceManager` class that implements the observer pattern for real-time updates. The search functionality uses a combination of client-side filtering and server-side search using SQLite's full-text search capabilities.


### Services Page
- Lists all available services across all devices
- Features:
  - Filtering by device ID
  - Search by service name
  - Service type categorization
  - Input/output parameter details
  - Service status indicators
- Interactive service testing interface
- Service documentation and usage examples

The Services page uses a RESTful API architecture with Flask's Blueprint system for route organization. The service testing interface is implemented using Python's `asyncio` for concurrent service calls, with a custom timeout mechanism. The filtering system uses a combination of SQL queries for server-side filtering and JavaScript for client-side sorting and additional filtering.

![image](https://github.com/user-attachments/assets/4ff15cbd-f3b5-496c-a670-0050197440ab)


### Relationships Page
- Visual representation of device and service connections
- Shows:
  - Order-based relationships (sequential execution)
  - Condition-based relationships (conditional execution)
  - Unbound relationships (available connections)
- Interactive relationship management:
  - Create new relationships
  - Modify existing connections
  - Delete relationships
  - Validate relationship configurations
- Real-time relationship status updates

The Relationships page uses the `vis.js` library for graph visualization, with custom layout algorithms implemented in JavaScript. The relationship management system is built on top of a custom `RelationshipManager` class that handles the creation and validation of relationships. The real-time updates are implemented using Socket.IO events, with a custom event system for relationship changes.


### Apps Page
- Application management interface with features:
  - Create new applications
  - Upload existing applications
  - Edit application configurations
  - Monitor running applications
  - View application logs
- Application editor capabilities:
  - Visual relationship mapping
  - Real-time validation
  - Save and export functionality
- Application execution controls:
  - Start/Stop applications
  - View execution status
  - Monitor resource usage
  - Error handling and recover
 
The Apps page is implemented as a single-page application using Vue.js, with a custom state management system using Vuex. The application editor uses a custom DSL (Domain Specific Language) for defining application structures, parsed using Python's `lark` library. The execution engine is built on top of `asyncio`, with a custom scheduler for managing application execution.
 
![image](https://github.com/user-attachments/assets/e2052404-a2d8-4df2-93f3-16ca376ec7f9)

![image](https://github.com/user-attachments/assets/b1368414-9941-4474-b340-7d1a34ed2abc)


### Dark Mode Interface
- Consistent dark theme across all pages
- High contrast for better readability
- Reduced eye strain for extended use
- Automatic theme persistence

The dark mode implementation uses CSS custom properties (variables) for theme management, with a custom JavaScript module handling theme persistence using the browser's localStorage API. The theme system is built using SCSS for better maintainability, with a custom build process using `node-sass`.

![Untitled video - Made with Clipchamp](https://github.com/user-attachments/assets/5d385c13-ae05-402c-ad74-d47dacc9af65)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
