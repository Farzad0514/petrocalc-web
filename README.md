# PetroCalc Web Application

A modern, comprehensive web application for petroleum engineering calculations built with FastAPI and Bootstrap. This application provides interactive web forms and RESTful APIs for all major petroleum engineering calculations.

## 🚀 Features

### **Complete Petroleum Engineering Suite**
- **Drilling Calculations**: Mud properties, hydraulics, pressure calculations, wellbore analysis
- **Fluid Properties**: PVT properties, formation volume factors, viscosity, compressibility
- **Reservoir Engineering**: Oil/gas properties, PVT correlations, reservoir fluid analysis
- **Production Engineering**: Well performance, IPR curves, nodal analysis, production optimization
- **Economics**: NPV analysis, rate of return, economic evaluation, investment analysis
- **Completion Engineering**: Perforation flow efficiency, gravel pack design, completion optimization
- **Flow Calculations**: Single-phase and multiphase flow, pressure drop calculations
- **Pressure Analysis**: Formation pressures, well control, kick tolerance, pressure gradients
- **Rock Properties**: Porosity, permeability, water saturation, petrophysical analysis
- **Thermodynamics**: Heat transfer, thermal properties, thermodynamic calculations

### **Modern Web Interface**
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Interactive Forms**: Real-time calculations with instant results
- **Professional UI**: Clean, modern interface with Bootstrap 5 and custom styling
- **Organized Navigation**: Dropdown menus grouping related calculations by discipline
- **Search Functionality**: Quick access to specific calculation modules

### **Developer-Friendly APIs**
- **RESTful APIs**: Complete API coverage for all calculation modules
- **Interactive Documentation**: Swagger UI and ReDoc for API exploration
- **JSON Input/Output**: Standardized request/response formats
- **Error Handling**: Comprehensive error messages and validation
- **OpenAPI Specification**: Auto-generated API documentation

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: HTML5, Bootstrap 5, Vanilla JavaScript
- **Templates**: Jinja2 with consistent layout patterns
- **API**: RESTful API with automatic OpenAPI documentation
- **Styling**: Custom CSS with Bootstrap components and subtle shadows
- **Dependencies**: Pure pip/requirements.txt (no Poetry, no local src/)
- **Deployment**: Docker-ready with health checks

## 📦 Installation

### Prerequisites

- **Python 3.11+** - Required for modern async features
- **petrocalc package** - Automatically installed via requirements.txt

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Farzad0514/petrocalc-web.git
cd petrocalc-web

# Create virtual environment (recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

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

### Method 1: Using the run script (Recommended)

```bash
python run.py
```

### Method 2: Using uvicorn directly

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The application will be available at:
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Alternative API Docs**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/api/status

## 📁 Project Structure

```
petrocalc-web/
├── app/                          # FastAPI application
│   ├── main.py                   # Main application file with all routes
│   ├── routers/                  # API route handlers
│   │   ├── drilling.py           # Drilling calculations API
│   │   ├── fluids.py             # Fluid properties API
│   │   ├── reservoir.py          # Reservoir engineering API
│   │   ├── production.py         # Production engineering API
│   │   ├── economics.py          # Economics API
│   │   ├── completion.py         # Completion engineering API
│   │   ├── flow.py               # Flow calculations API
│   │   ├── pressure.py           # Pressure analysis API
│   │   ├── rock_properties.py    # Rock properties API
│   │   └── thermodynamics.py     # Thermodynamics API
│   ├── static/                   # Static files
│   │   ├── css/
│   │   │   └── styles.css        # Custom CSS with consistent styling
│   │   └── js/
│   │       └── main.js           # JavaScript functionality
│   └── templates/                # HTML templates (consistent layout)
│       ├── base.html             # Base template with navigation
│       ├── index.html            # Home page with search
│       ├── drilling.html         # Drilling calculations
│       ├── fluids.html           # Fluid properties
│       ├── reservoir.html        # Reservoir engineering
│       ├── production.html       # Production engineering
│       ├── economics.html        # Economics
│       ├── completion.html       # Completion engineering
│       ├── flow.html             # Flow calculations
│       ├── pressure.html         # Pressure analysis
│       ├── rock_properties.html  # Rock properties
│       └── thermodynamics.html   # Thermodynamics
├── tests/                        # Test files
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
├── run.py                        # Application entry point
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose setup
├── .gitignore                    # Comprehensive Git ignore patterns
└── README.md                     # This file
```

## 🔧 Available Calculations

### Drilling Module
- **Mud Weight Calculations**: Mud weight to pressure gradient conversion
- **Pressure Analysis**: Hydrostatic pressure calculation
- **Flow Analysis**: Annular velocity and pipe velocity calculations
- **Hydraulics**: Reynolds number calculation and flow regime determination
- **Wellbore Calculations**: Advanced drilling hydraulics

### Fluids Module
- **Water Properties**: Formation volume factor (McCain correlation), compressibility (Osif correlation)
- **Gas Properties**: Formation volume factor, compressibility calculations
- **Oil Properties**: Viscosity, density, and PVT properties
- **PVT Analysis**: Comprehensive fluid property analysis

### Reservoir Module
- **PVT Correlations**: Oil formation volume factor, solution gas-oil ratio (Standing's correlations)
- **Fluid Properties**: Bubble point pressure, oil compressibility
- **Reservoir Analysis**: Combined PVT analysis and reservoir fluid characterization

### Production Module
- **Well Performance**: IPR curves, productivity index calculations
- **Nodal Analysis**: System optimization and flow performance
- **Production Optimization**: Well performance analysis and optimization

### Economics Module
- **Financial Analysis**: NPV calculation, rate of return analysis
- **Investment Evaluation**: Economic evaluation of petroleum projects
- **Cash Flow Analysis**: Present value and investment decision tools

### Completion Module
- **Perforation Design**: Flow efficiency calculations, perforation optimization
- **Gravel Pack Design**: Sand control and completion optimization
- **Completion Analysis**: Wellbore completion performance

### Flow Module
- **Single-Phase Flow**: Moody friction factor, pressure drop calculations
- **Multiphase Flow**: Gas-liquid flow in pipes and restrictions
- **Pipe Flow**: Flow through various pipe geometries and fittings

### Pressure Module
- **Formation Pressure**: Pressure gradient calculations and formation analysis
- **Well Control**: Kick tolerance and well control calculations
- **Pressure Analysis**: Comprehensive pressure analysis tools

### Rock Properties Module
- **Porosity Analysis**: Porosity from logs and core data
- **Permeability**: Permeability calculations and correlations
- **Water Saturation**: Archie's equation and saturation analysis
- **Petrophysical Analysis**: Comprehensive rock property evaluation

### Thermodynamics Module
- **Heat Transfer**: Heat capacity calculations for oil, gas, and water
- **Thermal Properties**: Thermal conductivity and heat transfer analysis
- **Temperature Effects**: Thermodynamic property calculations

## 📊 API Usage

All calculations are available through RESTful APIs with comprehensive documentation.

### Example API Calls

```python
import requests

# Calculate mud weight to pressure gradient
response = requests.post("http://localhost:8000/api/drilling/mud-weight-to-pressure-gradient", 
                        json={"mud_weight": 10.0, "unit": "ppg"})
result = response.json()
print(f"Pressure gradient: {result['pressure_gradient']} psi/ft")

# Calculate oil formation volume factor
response = requests.post("http://localhost:8000/api/reservoir/oil_formation_volume_factor", 
                        json={
                            "api_gravity": 35.0,
                            "solution_gor": 500.0,
                            "gas_specific_gravity": 0.7,
                            "temperature": 180.0,
                            "pressure": 2000.0
                        })
result = response.json()
print(f"Oil FVF: {result['formation_volume_factor']} bbl/STB")

# Calculate NPV
response = requests.post("http://localhost:8000/api/economics/npv", 
                        json={
                            "cash_flows": [100000, 150000, 200000, 180000, 120000],
                            "discount_rate": 0.1,
                            "initial_investment": 500000
                        })
result = response.json()
print(f"NPV: ${result['npv']:,.2f}")
```

### JavaScript API Usage

```javascript
// Using fetch API for drilling calculations
const calculateMudWeight = async () => {
    const response = await fetch('/api/drilling/mud-weight-to-pressure-gradient', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({mud_weight: 10.0, unit: 'ppg'})
    });
    const result = await response.json();
    console.log(`Pressure gradient: ${result.pressure_gradient} psi/ft`);
};

// Perforation flow efficiency calculation
const calculatePerforation = async () => {
    const response = await fetch('/api/completion/perforation_flow_efficiency', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            perforation_density: 4.0,
            perforation_diameter: 0.5,
            perforation_length: 12.0,
            skin_factor: 2.0
        })
    });
    const result = await response.json();
    console.log(`Flow efficiency: ${result.flow_efficiency}`);
};
```

### API Documentation

- **Interactive Swagger UI**: http://localhost:8000/api/docs
- **ReDoc Documentation**: http://localhost:8000/api/redoc
- **OpenAPI Specification**: http://localhost:8000/openapi.json

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test modules
pytest tests/test_basic.py

# Run with verbose output
pytest -v
```

## 🐳 Docker Deployment

The application is Docker-ready with optimized configuration:

### Using Docker

```bash
# Build the image
docker build -t petrocalc-web .

# Run the container
docker run -p 8000:8000 petrocalc-web
```

### Using Docker Compose

```bash
# Start the application
docker-compose up

# Start in detached mode
docker-compose up -d

# Stop the application
docker-compose down
```

The `docker-compose.yml` includes:
- **Port mapping**: Host port 8000 to container port 8000
- **Volume mounting**: For development with live code reloading
- **Health checks**: Automatic container health monitoring
- **Environment variables**: Configurable runtime settings

### Production Deployment

For production deployment, the Dockerfile includes:
- **Multi-stage build**: Optimized image size
- **Health checks**: Built-in health monitoring
- **Security**: Non-root user execution
- **Performance**: Optimized Python settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Development

### Adding New Calculations

1. **Add the calculation function** to the petrocalc package (external dependency)
2. **Create API endpoints** in the corresponding router file in `app/routers/`
3. **Update the HTML template** to include the new calculation form
4. **Add JavaScript handlers** for the new form submission and result display
5. **Update navigation** in `base.html` if adding a new module
6. **Add tests** for the new endpoints

### Project Architecture

The application follows a clean, modular architecture:

- **Separation of Concerns**: API routes, templates, and static files are organized separately
- **Consistent Patterns**: All modules follow the same structure and naming conventions
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Validation**: Input validation using Pydantic models
- **Documentation**: Auto-generated API documentation with examples

### Layout Consistency

All HTML templates follow a standardized layout pattern:
- **Header Structure**: Consistent icons, titles, and descriptions
- **Card Styling**: Uniform shadows and spacing (`shadow-sm mb-4`)
- **Column Layout**: Two-column layout with forms on left, info/results on right
- **Responsive Design**: Works seamlessly across all device sizes

### Code Style Guidelines

- **Python**: Follow PEP 8, use type hints, include docstrings
- **HTML/CSS**: Use Bootstrap classes, maintain consistent structure
- **JavaScript**: Use modern ES6+ features, handle errors gracefully
- **API Design**: RESTful endpoints with clear request/response models

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

### **Planned Features**
- [ ] **Advanced Visualizations**: Charts and graphs for calculation results
- [ ] **Data Export**: Export calculations to PDF, Excel, and CSV formats
- [ ] **User Accounts**: Save calculations, create projects, and share results
- [ ] **Batch Processing**: Upload data files for bulk calculations
- [ ] **Mobile App**: Native mobile application companion
- [ ] **Field Data Integration**: Connect with real-time field data sources
- [ ] **Advanced Analytics**: Statistical analysis and trend identification
- [ ] **Report Generation**: Automated technical report generation

### **Technical Improvements**
- [ ] **Database Integration**: Store calculation history and user data
- [ ] **Caching**: Redis caching for improved performance
- [ ] **Background Tasks**: Celery for long-running calculations
- [ ] **WebSocket Support**: Real-time calculation updates
- [ ] **API Rate Limiting**: Implement rate limiting for production use
- [ ] **Enhanced Security**: Authentication, authorization, and input sanitization
- [ ] **Microservices**: Split into specialized calculation microservices
- [ ] **Cloud Deployment**: AWS/Azure deployment configurations

### **Domain-Specific Enhancements**
- [ ] **Well Testing Analysis**: Pressure transient analysis and interpretation
- [ ] **Decline Curve Analysis**: Production forecasting and reserves estimation
- [ ] **Geomechanics**: Stress analysis and wellbore stability calculations
- [ ] **Enhanced Oil Recovery**: EOR screening and design calculations
- [ ] **Carbon Capture**: CO2 storage and sequestration calculations
- [ ] **Renewable Energy**: Integration with renewable energy calculations

## 📞 Support & Documentation

### **Getting Help**
1. **API Documentation**: Check http://localhost:8000/api/docs for detailed API usage
2. **PetroCalc Package**: Review the petrocalc package documentation for calculation details
3. **GitHub Issues**: Open an issue for bugs, feature requests, or questions
4. **Examples**: Check the `examples.py` file for usage examples

### **Common Issues**
- **PetroCalc not found**: Ensure `pip install petrocalc` was successful
- **Port already in use**: Change the port in `run.py` or stop conflicting services
- **Import errors**: Verify all dependencies are installed with `pip install -r requirements.txt`

### **Performance Tips**
- Use the API endpoints for programmatic access rather than screen scraping
- Batch multiple calculations when possible to reduce overhead
- The application is designed to handle concurrent requests efficiently

---

## 🎯 Project Status

✅ **Complete**: All major petroleum engineering calculation modules implemented  
✅ **Tested**: API endpoints verified and working  
✅ **Documented**: Comprehensive API documentation available  
✅ **Production Ready**: Docker deployment and health checks configured  
✅ **Consistent**: Standardized UI/UX across all modules  

**Happy Calculating! 🛢️⚡**
