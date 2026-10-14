Public Profile Finder

A Python command-line tool that generates public social profile URLs from a username and checks basic HTTP responses.

Features

- Accepts an optional email and username.
- Checks public profile URLs on GitHub, Reddit, Pinterest, and YouTube.
- Displays HTTP responses and cautious status messages.
- Saves results as JSON and CSV files.
- Uses Python's standard library.

Requirements

- Python 3

Usage

Run:

python finder.py

Enter an email and/or username when prompted.

Output

Results are saved in the "results/" directory as timestamped JSON and CSV files.

Limitations

- An HTTP response does not confirm that a profile exists or belongs to a particular person.
- An email address alone cannot reveal all associated social media accounts.
- Some sites may block automated requests or return inconclusive responses.
- Use this tool only for lawful, authorized research.

Privacy

Avoid sharing reports containing personal email addresses or other private information publicly.

License

MIT
