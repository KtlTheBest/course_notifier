# course_notifier
Course registration made a tad bit easier...

I created a simple script which would help me register the courses I wanted to register. THe problem is that some people start to drop their courses just before the add deadline. This is bad, since we can't constantly check for available places and they can open any time.

This is where the script comes in. When you run the script, it checks whether there are available courses from ones you've specified. Just like that

## Any gotcha's?
Well, a bit. First of all, you need to supply four things:
 * Your email address
 * Your email password
 * Your registrar login
 * Your registrar password
All of those things can be added in `config.py`

Are we done? Not quite... You need to allow your script to connect to your email. Google is quite nit-picky about it, so you need to either:
 * Use O2Auth token
 * Lessen security settings (this is bad)
Guess which one I am using :) To change your options, please choose `Allow less secure apps - ON` [here](https://myaccount.google.com/lesssecureapps).

So... are we done yet? Almost there. You also need to specify course codes for the courses you want to register. But this script only checks once. So how to run it constantly? I thought about `schedule` module, but I didn't like the idea. First of all, a lot of code. Second, if your computer shuts down or you kill the program, you won't get any notifications.

So the safest solution I could come up with is crontab. It's a Linux scheduler which runs as soon as OS boots up. So you just need to add a line in your crontab file.

Okay, so here we go.

## Usage
Download from git:
```
git clone https://github.com/KtlTheBest/course_notifier ~/course_notifier
```

After you added your credentials into `config.py`, you need to schedule the script with crontab:
```
crontab -e # opens a text editor
*/5 * * * * python3 ~/course_notifier/smtp.py
```

What this does, is that it runs the script every 5 miuntes. Yes, even at 2:00 am... To me 5 minutes looked like a nice compromiss between the freshness of the information and not spamming my email. But you can set any value you want. Please read how to set cron schedule.
