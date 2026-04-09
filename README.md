 1. Cyber-Logistics Operational Robots

Welcome to the Cyber-Logistics Operational Robots repository. This project is a reliable warehouse automation simulation built with Python and the Pygame library. It features a complex multi-agent system where specialized autonomous robots handle sorting, shelving, and delivery based on a priority order defined by the user.

 2. Purpose

The primary goal of this program is to illustrate multi-agent processing. It solves multiple task efficiency throughput by:

Task Prioritization: Allows users to define the specific sequence of goods to be processed.

Automated Sorting: Categorizing goods into specific storage zones based on type.

Dynamic Delivery: Users can monitor inventory states and trigger automatic delivery to the shipping gate.

 3. Key Features

Strategic Planning: Arrange goods' priority sequence in the initial "Planning Mode" screen.

Autonomous Multi-Agent System:

 -Sorting Robot (Red): Handles inbound logistics and category-based shelving.

 -Delivering Robot (Yellow): Deals with outbound logistics and revenue collection.

Inventory Integration: Seamlessly collects and processes data from a .csv database.

Real-time Analytics: Track bank revenue and live robot states (Resting, Navigating, Picking up, Depositing).

Visual Excellence: High-contrast Cyberpunk UI with flow effects and intuitive status panels.

 4. System Requirements

Software:
Programming Language: Python 3.8 or higher

Libraries: pygame (v2.0.0+), pandas

OS: Windows, Linux, or MacOS

Hardware:
Processor: Any modern dual-core CPU

Memory: Minimum 4GB RAM (8GB recommended)

Graphics: Integrated graphics supporting OpenGL

 5. Installation

-Clone the Repository:
Bash
git clone https://github.com/your-username/cyber-logistics.git
cd cyber-logistics
-Install Dependencies:
Bash
pip install pygame pandas
Prepare Database:
-Ensure a file with a form of .csv exists in the root directory with the following structure:
ItemID,ItemName,Category,Price
101,Smartphone,Electronics,500
102,Office Chair,Furniture,150
-Run the Application:
Bash
python main.py
 6. Usage Guide

Step 1: Planning Mode
Upon launching, the system starts in Planning Mode.

Select Items: Click buttons in the Available Items panel. Selected items will appear in the Current Plan list on the right.

Review: Verify the sequence to ensure high-priority goods are at the top.

Step 2: Execution Mode
Start: Click the green "START SYSTEM" button.

Simulation: The UI transitions to the warehouse floor. Robots will leave the Docking Station to execute your plan.

Monitor: Watch the top-right corner to see your networth grow as the Deliverer completes shipments.



 7. Authors

Tạ Hiếu Đông - System Design - GitHub Profile: https://github.com/lhtk33

Trần Võ Minh Khang - Robot Logic - GitHub Profile: https://github.com/khangminh1312

Huỳnh Nhật Nam - UI/UX Development - GitHub Profile: https://github.com/huynhnhatnam-guthib

 8. Acknowledgements

Pygame Community: For the robust 2D engine.

Pandas Team: For simplifying inventory management.

Gemini (AI Collaborator): For assisting in state machine logic refinement.

Cyberpunk Aesthetics: Inspiration for the high-contrast color palette.

 9. License

This project is licensed under the MIT License.

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



If you find this project useful, please share it for everyone
<img width="1529" height="816" alt="image" src="https://github.com/user-attachments/assets/b312df5b-2351-43d6-b82c-8bcc4dd2e0f8" />


