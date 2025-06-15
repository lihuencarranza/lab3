# Atlas Manager

Atlas Manager is an IoT Device Management Platform based on DDL (Device Description Language). It provides a comprehensive interface for managing IoT devices, services, and applications.

## Features

- Real-time monitoring of IoT devices
- Service management and discovery
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
   - Things: View and manage connected IoT devices
   - Services: Explore available device services
   - Relationships: Manage device and service connections
   - Apps: Create and manage IoT applications

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