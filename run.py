"""
Entry point for running the PetroCalc Web application.

This application requires the petrocalc package to be installed via pip.
Install it using: pip install petrocalc
"""

# Import and run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting PetroCalc Web Application...")
    print("📚 API Documentation: http://localhost:8000/api/docs")
    print("🌐 Web Interface: http://localhost:8000")
    
    # Check if petrocalc is available
    try:
        import petrocalc
        print(f"✅ Using petrocalc package from: {petrocalc.__file__}")
        print(f"📦 PetroCalc version: {getattr(petrocalc, '__version__', 'unknown')}")
    except ImportError:
        print("❌ Error: petrocalc package not found!")
        print("💡 Please install it using: pip install petrocalc")
        print("🔗 Or install from source if available")
        exit(1)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
