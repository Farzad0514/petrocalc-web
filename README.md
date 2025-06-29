# PetroCalc Web Application

A modern, responsive web application for petroleum engineering calculations built with FastAPI and Bootstrap.

## 🚀 Features

- **Drilling Calculations**: Mud properties, hydraulics, pressure calculations
- **Fluid Properties**: PVT properties, formation volume factors, viscosity
- **Reservoir Engineering**: Oil/gas properties using Standing's correlations
- **Modern UI**: Responsive design with Bootstrap and custom styling
- **API Documentation**: Interactive Swagger UI for developers
- **Real-time Calculations**: AJAX-powered forms with instant results

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, Bootstrap 5, Vanilla JavaScript
- **Templates**: Jinja2
- **API**: RESTful API with automatic documentation
- **Styling**: Custom CSS with Bootstrap components

## 📦 Installation

### Prerequisites

- **Python 3.10+** - Required for modern async features
- **petrocalc package** - Install using `pip install petrocalc`

### Installation

```bash
# Clone the repository
git clone https://github.com/Farzad0514/petrocalc-web.git
cd petrocalc-web

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

### Development Setup

```bash
# Install with development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black .

# Type checking
mypy app/
```

## 🚀 Running the Application

### Method 1: Using the run script

```bash
python run.py
```

### Method 2: Using uvicorn directly

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Method 3: Using Poetry

```bash
poetry run python run.py
```

The application will be available at:
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Alternative API Docs**: http://localhost:8000/api/redoc

## 📁 Project Structure

```
petrocalc-web/
├── app/                          # FastAPI application
│   ├── main.py                   # Main application file
│   ├── routers/                  # API route handlers
│   │   ├── drilling.py           # Drilling calculations API
│   │   ├── fluids.py             # Fluid properties API
│   │   ├── reservoir.py          # Reservoir engineering API
│   │   ├── production.py         # Production engineering API (placeholder)
│   │   └── economics.py          # Economics API (placeholder)
│   ├── static/                   # Static files
│   │   ├── css/
│   │   │   └── styles.css        # Custom CSS
│   │   └── js/
│   │       └── main.js           # JavaScript functionality
│   └── templates/                # HTML templates
│       ├── base.html             # Base template
│       ├── index.html            # Home page
│       ├── drilling.html         # Drilling calculations
│       ├── fluids.html           # Fluid properties
│       ├── reservoir.html        # Reservoir engineering
│       ├── production.html       # Production engineering
│       └── economics.html        # Economics

├── tests/                        # Test files
├── run.py                        # Application entry point
├── pyproject.toml                # Project configuration
└── README.md                     # This file
```

## 🔧 Available Calculations

### Drilling Module
- Mud weight to pressure gradient conversion
- Hydrostatic pressure calculation
- Annular velocity calculation
- Pipe velocity calculation
- Reynolds number calculation

### Fluids Module
- Water formation volume factor (McCain correlation)
- Water compressibility (Osif correlation)
- Gas formation volume factor
- Water viscosity

### Reservoir Module
- Oil formation volume factor (Standing's correlation)
- Solution gas-oil ratio (Standing's correlation)
- Combined PVT analysis

## 📊 API Usage

### Example API Call

```python
import requests

# Calculate mud weight to pressure gradient
response = requests.post("http://localhost:8000/api/drilling/mud-weight-to-pressure-gradient", 
                        json={"mud_weight": 10.0, "unit": "ppg"})
result = response.json()
print(f"Pressure gradient: {result['pressure_gradient']} psi/ft")
```

### JavaScript Example

```javascript
// Using the built-in API helper
const result = await PetroCalc.makeAPICall('/drilling/mud-weight-to-pressure-gradient', {
    mud_weight: 10.0,
    unit: 'ppg'
});
console.log(result);
```

## 🧪 Testing

```bash
# Run tests
poetry run pytest

# With coverage
poetry run pytest --cov=src --cov-report=html
```

## 🐳 Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

COPY . .

EXPOSE 8000

CMD ["python", "run.py"]
```

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  petrocalc-web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - PYTHONPATH=/app/src
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Development

### Adding New Calculations

1. Add the calculation function to the installed petrocalc package
2. Create API endpoints in the corresponding router file in `app/routers/`
3. Update the HTML template to include the new calculation form
4. Add JavaScript handlers for the new form

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to all functions
- Include input validation and error handling

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Muhammad Farzad Ali**
- Email: muhammad.farzad.ali@gmail.com
- GitHub: [@Farzad0514](https://github.com/Farzad0514)

## 🙏 Acknowledgments

- Standing correlations for oil and gas properties
- McCain correlation for water properties
- Bootstrap team for the excellent CSS framework
- FastAPI team for the amazing web framework

## 🔮 Future Enhancements

- [ ] Production engineering calculations
- [ ] Economics and NPV analysis
- [ ] Well testing analysis
- [ ] Decline curve analysis
- [ ] Data visualization with charts
- [ ] Export calculations to PDF/Excel
- [ ] User authentication and saved calculations
- [ ] Mobile app companion
- [ ] Integration with field data sources

## 📞 Support

If you encounter any issues or have questions:

1. Check the [API documentation](http://localhost:8000/api/docs) for API usage
2. Review the petrocalc package documentation for available functions
3. Open an issue on GitHub for bugs or feature requests

---

**Happy Calculating! 🛢️**
