# Online Store Project

A responsive e-commerce product catalog application built with **FastAPI**, **SQLAlchemy**, and **Jinja2**. This project provides a complete flow for browsing, filtering, and viewing product details.

## Project Overview
This application serves as a dynamic product catalog. It allows users to browse a collection of products, filter them by price range, search for specific items by name, and sort results. The project follows a clean architecture, separating the database logic from the web presentation.

## Key Features
* **Dynamic Catalog:** Browse products in a responsive, card-based grid layout.
* **Smart Filtering:** Filter products by minimum price and keyword search.
* **Sorting:** Sort products by price (Ascending/Descending).
* **Modern UI:** Responsive design using **Bootstrap 5**, featuring interactive hover animations.
* **Product Details:** Dedicated pages for individual products to display comprehensive descriptions.
* **Stateful Requests:** Maintains filtering states during navigation.

## Tech Stack
* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
* **Database/ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
* **Templating:** [Jinja2](https://jinja.palletsprojects.com/)
* **Frontend:** [Bootstrap 5](https://getbootstrap.com/), Custom CSS animations
* **Server:** [Uvicorn](https://www.uvicorn.org/)

## Project Structure
```text
FinalProject/
├── logic/
│   └── crud.py       # Database queries and filtering logic
├── web/
│   ├── app.py        # FastAPI routes and server initialization
│   └── templates/    # HTML files (base.html, index.html, product_details.html)
├── venv/             # Virtual environment
└── requirements.txt  # Project dependencies

## Installation & Setup
Prerequisites
Python 3.10 or higher installed.

## Setup Steps
1.  the repository:
git clone [YOUR_REPOSITORY_URL]
cd FinalProject

2. Create and activate a virtual environment:
# Windows
python -m venv venv
venv\Scripts\activate

3. Install dependencies:
pip install fastapi uvicorn sqlalchemy jinja2

4. Run the application:
py -m uvicorn web.app:app --reload

5. Access the application:
Open your browser and navigate to: http://127.0.0.1:8000/products-catalog

## Usage Guide
Browsing: The home page displays all available items in a modern grid.

Filtering: Use the inputs at the top of the page (Price, Search) and click "Apply" to refine the view.

Sorting: Use the "Sort By" dropdown to reorder the results by price.

View Details: Click the "View Details" button on any product card to navigate to the product's dedicated information page.

Clear Filters: Use the "Clear" button to reset the view to all available items.

## Contributing
Contributions are welcome! If you want to add new features like a "Shopping Cart," "User Authentication," or "Product Reviews," feel free to fork this repository and submit a Pull Request.

