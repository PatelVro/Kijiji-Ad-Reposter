Automating Kijiji Ad Reposting with Python and Selenium
How a repetitive daily task led me to build a full-blown automation bot

🧠 The Problem
At my previous job, one of my daily responsibilities was to manually delete and repost 30 ads on Kijiji — every single day.
It usually took me 30 to 45 minutes and was honestly one of the most repetitive, boring tasks I’ve done.
Naturally, I started wondering:
Can I automate this?

🔍 The Research
At the time, I didn’t know about Selenium or browser automation tools. I had only worked with JavaScript and Python for smaller scripting tasks.
So I started exploring.
With help from ChatGPT (v3.5) and some GitHub issues, I slowly started learning about how Selenium can control a browser, click buttons, fill forms — and yes, even post ads on Kijiji.

🧪 The Breakthrough
Initially, I struggled — my custom scripts didn’t work. Kijiji’s structure was tricky and I wasn’t sure if this idea was even feasible.
Eventually, I came across a legacy code snippet that demonstrated how to post a basic ad using JSON and Selenium. It was incomplete and outdated — but it was the spark I needed to realize:
✅ This is possible.

🛠️ The Build
Once I knew it could work, I built the bot step by step:
Started with Excel for input data (ad titles, descriptions, images, etc.)
Added automatic login and delete-before-repost flow Gradually added:
Category selection
Location handling
Price formatting
Bot delay logic (to avoid detection)
Retry system if blocked or rate-limited
Switched from Excel to MySQL database for flexibility
Built a simple front-end dashboard (displays and manages ad data)

🤖 The Reposter in Action
Here’s how it works today:
A Python + Selenium script reads ad data from a MySQL database Automatically:
Logs into Kijiji
Deletes the existing ad (if it exists)
Reposts it with updated timestamp
Supports multiple accounts, locations, and up to 300+ ads daily
Deployed on a Windows server with:
.bat file to auto-run & fetch updates from GitHub
Scheduled tasks for daily execution

🧵 Lessons Learned
Selenium is powerful, but requires patience — especially with UI changes and bot detection
Automation often starts with scratching your own itch
You don’t need to know everything — you just need to keep digging
Don’t hesitate to build on someone else’s idea if it helps you learn and grow

📎 Tech Stack
Python
Selenium
MySQL
Basic HTML/CSS frontend

📂 Code & Demo
🔗 GitHub Repository (insert link)
🖼️ Screenshots or short demo video (optional)

✍️ Next Steps
If you're doing something repetitive every day — chances are it can be automated.
I didn’t know anything about browser automation when I started this, but curiosity and persistence took care of that.

Feel free to reach out if you’re stuck with a similar challenge — I’d love to help or just nerd out over bots.
