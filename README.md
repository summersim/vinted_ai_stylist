# Vinted AI Stylist

An AI-powered fashion search assistant that helps users find clothing items through natural conversation. The assistant uses advanced language models to understand user preferences and search through Vinted listings, providing personalized fashion recommendations.

## Features

- Natural language conversation interface for fashion search
- Integration with Vinted marketplace for real-time item search
- Advanced filtering capabilities:
  - Brand filtering
  - Price range filtering
  - Size filtering
  - Condition/status filtering
  - Color matching
- Detailed item information including:
  - Product descriptions
  - Color details
  - Brand information
  - Price and size
  - Product images
- LLM-powered item matching based on user preferences
- Interactive conversation flow with user confirmation

## Tech Stack

- **Language**: Python 3.8+
- **AI/ML**:
  - LangChain for LLM orchestration
  - Groq for high-performance LLM inference
  - Llama3-8b and Gemma models for natural language understanding
- **Web Scraping**:
  - BeautifulSoup4 for HTML parsing
  - Custom Vinted scraper implementation
- **Data Processing**:
  - Pandas for data manipulation
  - NumPy for numerical operations
- **Testing**:
  - unittest for unit testing
  - pytest for test automation
- **Development Tools**:
  - Poetry for dependency management
  - Black for code formatting
  - Flake8 for linting

## Project Structure

```
vinted_ai_stylist/
├── src/
│   └── vinted_ai_stylist/
│       ├── core/
│       │   └── app.py              # Main application logic
│       ├── models/
│       │   └── types.py           # Type definitions
│       ├── services/
│       │   ├── vinted_scraper.py  # Vinted scraping service
│       │   ├── filter_service.py  # Item filtering service
│       │   └── llm_service.py     # LLM integration service
│       └── __main__.py            # Application entry point
├── tests/
│   └── test_vinted_filter.py      # Unit tests
├── pyproject.toml                 # Poetry configuration
└── README.md                      # This file
```

## Prerequisites

- Python 3.8+
- Poetry (Python package manager)
- Environment variables for API keys:
  - `Gemma` (Groq API key)
  - `Llama3_8b` (Groq model identifier)

## Installation

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone the repository:
```bash
git clone [repository-url]
cd vinted_ai_stylist
```

3. Install dependencies using Poetry:
```bash
poetry install
```

4. Set up environment variables in the `env` file:
```bash
# Groq API Key
GROQ_API_KEY=your-groq-api-key

# Groq Models
Llama3_8b=llama3-8b-8192
Gemma=gemma2-9b-it
```

## Usage

Run the application using Poetry:
```bash
poetry run vinted-ai-stylist
```

The assistant will start an interactive session where you can:
1. Describe the clothing item you're looking for (e.g., "I want a sexy Boho dress with the colour sand or white for a cocktail party")
2. Provide additional details when prompted (brand, size, price range, etc.)
3. Review and confirm search results
4. Get personalized recommendations based on your preferences

## Running Tests

Run the test suite using Poetry:
```bash
poetry run pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license information here]

## Acknowledgments

- LangChain team for the excellent framework
- Groq for the high-performance LLM inference
- Vinted for the marketplace integration
- BeautifulSoup for web scraping capabilities 