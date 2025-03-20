Overview
The WGUPS Routing Program is a Python-based application that optimizes package delivery routes using a Greedy/Nearest Neighbor Algorithm. The goal is to minimize total mileage and ensure on-time deliveries while providing real-time package tracking. The program simulates the delivery process for multiple trucks, calculates delivery times based on distance and order of delivery, and allows the user to track the status of any package at a specified time.

This project demonstrates the use of advanced data structures, efficient routing algorithms, and real-time delivery status tracking to solve complex logistical challenges.

Objectives
✅ Minimize total delivery mileage
✅ Ensure on-time package deliveries
✅ Provide real-time tracking and status updates
✅ Handle package delivery constraints (deadlines, special handling)

Features
🚚 Delivery Optimization
Uses a Greedy/Nearest Neighbor Algorithm to calculate the shortest delivery route.
Handles multiple trucks with independent delivery schedules.
📦 Package Tracking
Tracks delivery status (At Hub, En Route, Delivered).
Provides real-time lookup for package status based on user-specified time.
📅 Deadline Management
Prioritizes packages based on delivery deadlines.
Ensures critical deliveries are handled first.
🌍 Dynamic Distance Calculation
Uses a distance matrix to compute shortest paths.
Adjusts routes dynamically based on package constraints.
