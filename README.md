# AI Coding Tutor

An interactive AI-powered coding tutor that helps users learn programming concepts through personalized instruction and real-time feedback.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate
```
```bash
# On Mac
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

The application consists of two main components that need to be run separately:

1. Start the Parlant server:
```bash
parlant-server --module "service"
```

2. In a new terminal window, activate the virtual environment again and run the Streamlit frontend:
```bash
streamlit run Home.py
```

## Support

If you encounter any issues or have questions, please open an issue in the repository.
