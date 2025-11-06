# GoFinder

GoFinder is a Django-based web scraping application that allows users to search Google and extract search results (links, titles, and descriptions) in an organized format. The application provides a clean interface for searching and the ability to download results as a CSV file.

## Features

- 🔍 **Google Search Integration** - Automated web scraping of Google search results
- 📊 **Data Organization** - Extracts and displays links, titles, and descriptions
- 📥 **CSV Export** - Download search results in CSV format
- 🎨 **Modern UI** - Clean, user-friendly interface with Bootstrap styling
- 🔄 **Real-time Results** - Instant display of search findings
- 🛡️ **Error Handling** - Robust error handling for failed requests

## Tech Stack

- **Backend**: Django 5.1.2, Python 3.10+
- **Web Scraping**: BeautifulSoup4, Requests
- **Data Processing**: Pandas
- **Static Files**: WhiteNoise
- **Frontend**: HTML, CSS (Bootstrap 5.3.3), JavaScript

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ivantsowlad/GoFinder.git
    cd GoFinder
    ```

2. Create and activate a virtual environment (recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run database migrations:
    ```bash
    python manage.py migrate
    ```

5. Collect static files:
    ```bash
    python manage.py collectstatic --noinput
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

7. Open your browser and navigate to:
    ```
    http://127.0.0.1:8000/
    ```

## Usage

1. Navigate to the **Project** page
2. Enter your search query in the search box
3. Click **Hledat** (Search) to fetch results
4. View the extracted results with links, titles, and descriptions
5. Click **Stáhnout** (Download) to export results as CSV

## Project Structure

```
GoFinder/
├── GoFinder/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── main/              # Main application
│   ├── views.py       # Search logic and web scraping
│   ├── models.py      # Database models
│   ├── forms.py       # Search form
│   ├── templates/     # HTML templates
│   └── static/        # CSS, images
├── manage.py
└── requirements.txt
```

## Requirements

- Python 3.10+
- Django 5.1.2
- BeautifulSoup4 4.12.3
- Pandas 2.2.3
- Requests 2.32.3
- WhiteNoise 6.7.0

## Important Notes

⚠️ **Web Scraping Disclaimer**: This tool scrapes Google search results. Be aware that:
- Google may block automated requests if used excessively
- Google's HTML structure changes frequently, which may require updates to the scraper
- Consider using official Google Search APIs for production use
- Respect Google's Terms of Service and robots.txt

## Configuration

For development, the project is configured with:
- `DEBUG = True`
- CSRF protection enabled
- Static files served via WhiteNoise

For production deployment, update `settings.py`:
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Use environment variables for `SECRET_KEY`
- Set up proper database (PostgreSQL recommended)

## Contributing

Pull requests are welcome! Please open an issue for suggestions or bug reports.

## Author

- [ivantsowlad](https://github.com/ivantsowlad)
