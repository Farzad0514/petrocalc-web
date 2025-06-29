"""
Configuration module for PetroCalc Web Application.

This application requires petrocalc to be installed via pip.
Install it using: pip install petrocalc
"""

import os
import sys
from pathlib import Path
from typing import Optional

class PetroCalcConfig:
    """Configuration class for PetroCalc Web Application."""
    
    def __init__(self):
        self.app_root = Path(__file__).parent.parent
        self.petrocalc_location = None
        self.is_development = self._detect_development_mode()
        self._setup_petrocalc_import()
    
    def _detect_development_mode(self) -> bool:
        """Detect if running in development mode."""
        return (
            os.getenv("ENVIRONMENT", "development") == "development" or
            "--reload" in sys.argv
        )
    
    def _setup_petrocalc_import(self):
        """Setup petrocalc import."""
        try:
            import petrocalc
            self.petrocalc_location = "pip_installed"
            print(f"ℹ️  Using pip-installed petrocalc from: {petrocalc.__file__}")
        except ImportError:
            self.petrocalc_location = "not_found"
            print("❌ petrocalc package not found!")
    
    def is_petrocalc_available(self) -> bool:
        """Check if petrocalc is available."""
        return self.petrocalc_location == "pip_installed"
    
    def get_import_instructions(self) -> str:
        """Get instructions for installing petrocalc if not available."""
        if self.petrocalc_location == "not_found":
            return """
petrocalc is not available. Please install it using:

pip install petrocalc

If petrocalc is not yet published to PyPI, you can install from source:
1. Get the petrocalc source code
2. Install it using: pip install -e /path/to/petrocalc-source
"""
        return ""
    
    def get_status_info(self) -> dict:
        """Get configuration status information."""
        try:
            import petrocalc
            petrocalc_version = getattr(petrocalc, '__version__', 'unknown')
            petrocalc_path = getattr(petrocalc, '__file__', 'unknown')
        except ImportError:
            petrocalc_version = 'not_installed'
            petrocalc_path = 'not_found'
        
        return {
            "app_root": str(self.app_root),
            "is_development": self.is_development,
            "petrocalc_location": self.petrocalc_location,
            "petrocalc_version": petrocalc_version,
            "petrocalc_path": petrocalc_path,
        }

# Global configuration instance
config = PetroCalcConfig()

def get_config() -> PetroCalcConfig:
    """Get the global configuration instance."""
    return config
