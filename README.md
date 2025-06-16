# Atlas Manager

Atlas Manager is an IoT Device Management Platform based on DDL (Device Description Language). It provides a comprehensive interface for managing IoT devices, entities, services, and applications.

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

#### 4. Application Management
- **Save**: Local storage of applications in .iot format
- **Upload**: Import existing applications for modification
- **Activate**: Start application execution
- **Stop**: End execution and clean up resources
- **Delete**: Remove applications from the system
- Status tracking for running applications

### Key Features
- Real-time updates via WebSocket
- Automatic service discovery
- Relationship visualization
- Application lifecycle management
- Status monitoring
- Error handling and recovery
- Clean and intuitive interface

## Project Structure

```
├── atlas_apps/         # Apps created
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── templates/         # HTML templates
│   ├── apps.html
│   ├── base.html
│   ├── entities.html
│   ├── index.html
│   ├── relationships.html
│   ├── services.html
│   └── things.html
└── venv/              # Virtual environment (not tracked in git)

```

## Usage

1. Ensure Atlas server is running on port 6668
2. Access the web interface at `http://localhost:5000`
3. Navigate through different sections:

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
  - Error handling and recovery

### Dark Mode Interface
- Consistent dark theme across all pages
- High contrast for better readability
- Reduced eye strain for extended use
- Automatic theme persistence

## Development

The application uses:
- Flask for the web framework
- Socket.IO for real-time updates
- Bootstrap for the UI framework
- Custom CSS for dark mode and styling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 