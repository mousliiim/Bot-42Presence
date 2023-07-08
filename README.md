# 42Presence - Bot Discord
![65b47c588e556e6f07aa009f91d8104c](https://github.com/mousliiim/BotDiscord/assets/101677651/b06a3d7a-6a5e-4f3b-910c-ebdbb57678a0)<br>


🤖 <b>42Presence</b> is a Discord bot specifically developed to monitor the attendance of your friend who is a student at 42. It sends you notifications on Discord whenever they are present at the school.

## 🛠️ Configuration

Before you can use the bot, you need to perform the following steps:

1. Clone this repository to your local machine.

2. Install the required dependencies by running the following command:
<b>pip install -r requirements.txt</b>

3. Modify the `students.json` file to add the students you want to track and their photos. You can use the bot's commands to add/remove students and their photos later on.

4. Obtain the necessary API credentials and bot token:

- API_UID: Obtain the UID for your 42 API. (Replace `<API_UID>` in the code)
- API_SECRET: Obtain the secret for your 42 API. (Replace `<API_SECRET>` in the code)
- BOT_ID: Obtain the token for your Discord bot. (Replace `<BOT_ID>` in the code)
- TON_CHANNEL_ID: Replace with the ID of the channel where you want to send messages. (Replace `<TON_CHANNEL_ID>` in the code)
- CTX.AUTHOR.ID: Replace with your Discord ID to grant admin permissions. (Replace `<AUTHOR_ID>` in the code)

## 🚀 Usage

To run the bot, use the following command:
<b>python main.py</b>

Make sure you have correctly set up your Python environment with the required dependencies.

## 📜 Commands

- `/presence` : Displays the list of present humans.
- `/addpresence <login>` : Adds a person to the list of humans to check.
- `/removepresence <login>` : Removes a person from the list of humans to check.
- `/liste` : Displays the list of humans to check.
- `/addpicture <login> <url>` : Adds a photo to a student.
- `/removepicture <login>` : Removes a photo from a student.
- `/setsleeptime <time>` : Changes the wait time between each check (admin only).
- `/restartpresence` : Restarts the bot (admin only).
- `/helppresence` : Displays the list of available commands.
- `/receivejsonpresence` : Receives the JSON file containing student information.
- `/announce <message>` : Sends a message to the specified channel (admin only).

## 🤝 Contributing

Contributions to this project are welcome! If you'd like to make improvements or fix issues, feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
