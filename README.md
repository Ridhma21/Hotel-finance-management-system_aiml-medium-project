# Hotel Finance Management System

## Description

This project is a Python-based hotel management system that focuses on billing, pricing, and basic analytics. It allows users to calculate booking costs based on room type, number of rooms, stay duration, meals, and additional services.

The system also includes dynamic pricing, where room rates change depending on the season and weekends.

## Features

* Dynamic room pricing based on month and demand
* Menu-driven interface for easy navigation
* Detailed bill generation with full cost breakdown
* Multiple room categories (Economy, Premium, Luxury)
* Meal selection and extra bedding options
* Automatic tax (GST) and discount calculation
* Batch booking analysis using NumPy
* Price comparison across room types

## Technologies Used

* Python
* NumPy
* CSV (for storing room pricing data)

## Dataset

The system uses a CSV file named `rooms_min_max.csv` which contains:

* Room Type
* Minimum Price
* Maximum Price
* Category

If the file is not found, the program automatically creates a sample dataset.

## How to Run

1. Make sure Python is installed on your system

2. Run the Python file:
   python your_file_name.py

3. Use the menu options:

   * Calculate individual booking bill
   * Perform batch booking analysis
   * Compare room prices
   * View all room types

4. Enter the required inputs when prompted

## Output

* Generates a detailed invoice with:

  * Room charges
  * Meal costs
  * Extra services
  * Taxes and discounts
* Displays total cost along with per-person and per-room breakdown
* Provides analytics like average booking value and revenue insights

## Logic Used

* Dynamic pricing using seasonal multipliers
* Cost calculations using NumPy arrays
* Conditional logic for taxes, discounts, and categories

## Author

Ridhima Chebolu
