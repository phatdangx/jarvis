# Jarvis
<img src="assets/logo.png" alt="Bot Logo" width="200"/>

Jarvis is a Telegram bot equipped with a role management feature. It enables admins to effortlessly manage user groups and determine which commands each user can access. In this scenario, the bot is employed by a small company with departments such as HR, Sales, Marketing, and Tech. Each user group has its own set of commands tailored to support their daily tasks on the go.

## Features

- **Admin commands**: get user lists, add user, remove user
- **HR commands**: get employee info, view upcomming holidays
- **Marketing commands**: fetch statistics for social media channels, get the status of current marketing campaigns
- **Sales commands**: check monthly or quarterly sales quota, fetch client information

## Getting Started

### Prerequisites

- Telegram bot token
- Python
- MongoDB
- Docker

### Installation

1. Clone the repository:
```bash
git clone git@github.com:phatdangx/jarvis.git
```
2. Set up your environment variables. Refer to .env.example for required variables.
3. Run start script.
- Make sure you give permision for the script
```bash
chmod +x start.sh
```
- Simply run
```
./start.sh
```

## Ussage

- **Help commands**:
```
/help - List all of the commands which Jarvis support for that user group
```
- **Admin commands**

```
- Add new user
    /adduser <employee_id> <email> <group>
    /adduser 1507890 user@company.com username hr
- Remove user
    /rmu <employee_id>
    /rmu 1507890
```

- **Other commands related to HR, Marketing, Sales**: Those are just dummy command to demonstrate the usecases. You can custom and add a real feature related to your business later

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

