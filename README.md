RentalEase — Rental Management System (Hackathon Project)
RentalEase is a Python-based command-line rental management system built during a hackathon to demonstrate a complete rental lifecycle — from item listing to renting and returning — using clean logic and persistent storage.

Problem Statement
Small rental services often rely on manual tracking, which leads to:
Confusion about item availability
No clear rental history
Human errors in record keeping

Our Solution
RentalEase provides a simple, lightweight rental system that:
Separates Admin and User roles
Tracks item availability in real time
Stores rental data persistently
Works fully offline with minimal setup

Key Features

User
View available rental items
Rent items for a selected number of days
Return rented items
Instant availability update

Admin
Secure admin access
Add new rental items
View all items
View complete rental history

Tech Stack
Language: Python

Interface: Command Line (CLI)

Storage: CSV files

Libraries: Python Standard Library only

Project Structure

rental_system/
│
├── main.py
├── data/
│ ├── items.csv
│ └── rentals.csv
└── README.md

How to Run

python main.py

No external dependencies required.

Admin Credentials

Password: 123
(For demo purposes only)

System Workflow
1. User selects Admin or User mode
2. Admin manages inventory and views rentals
3. User rents or returns items
4. Availability updates automatically in storage

Hackathon Highlights
Built within limited time constraints
Beginner-friendly, readable code
Real-world rental workflow
Fully functional demo-ready system

Future Scope

Late return fee calculation

Category-based item filtering

Analytics dashboard for admins

Team / Developer

Strikers 



Note for Judges
This project focuses on clarity, correctness, and completeness rather than scale.
All core rental operations work reliably and are easy to demonstrate live.
