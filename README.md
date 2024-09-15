# Operational-Delay-Analysis-Dashboard

## Overview

The **Operational Delay Analysis Dashboard** is a web application built using Streamlit and Plotly. It provides insights into operational delays , allowing users to explore delay patterns, visualize key performance indicators (KPIs), and identify areas for improvement.

## Features

- **Dynamic Filtering**: Users can filter data by year to focus on specific time periods and other criteria
- **KPIs**: The dashboard displays total delay count, total delay hours, and average delay hours.
- **Trends**: Different charts show delays based on various criteria and filters, helping identify patterns.
- **Breakdowns**: A bar chart highlights delays by different filters available like materials, equipments etc.

## Getting Started

1. **Installation**:
   - Clone this repository to your local machine.
   - Install the necessary dependencies using `pip install -r requirements.txt`.

2. **Data Preparation**:
   - Ensure you have the required data.
   - Update the database connection details in the code (`app.py`).

3. **Run the Dashboard**:
   - Navigate to the project directory.
   - Execute `streamlit run app.py` in your terminal.
   - The dashboard will open in your default web browser.

## Usage

1. Open the dashboard in your web browser.
2. Adjust the year slider to explore data for specific years.
3. View KPIs, trends, and various breakdowns.
4. Log out using the sidebar button.

## Security Considerations

- **User Authentication**: Consider adding user authentication to restrict access to authorized personnel.
- **Secure Database Credentials**: Avoid hardcoding database credentials in the code. Use environment variables or other secure methods.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

