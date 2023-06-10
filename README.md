# HexaPA - Productivity Accelerator
HexaPA is an open source AI chat (much like ChatGPT) using the OpenAI API, allowing more control over GPT-3.5 language model. It allows tweaking the model as well as sending rules, and customized context to the API rather then just the last few promt-response pairs in order to get improved responses.

**Please note that it's currently not a fully functional release yet. (Still a work in progress...)**



## Why should you care?!
Max 2048 tokens in - max 2048 tokens out... But how much of that 2048 input tokens is actually useful data to you, and how much is "wasted"?
I found that the token counter only gives somewhat accurate estimates, if you not only include the content but also include the roles, so this is what you actually pay for in tokens:

```
role: system, content: "List of rules come here if any, else it's left empty, but this line is obligatory and also included into the token count either way you pay for it..."
role: user, content: "Long text that you've sent earlier... This line is optional, hence in HexaPA you can select what context to send, but if it's not included, the AI doesn't \"remember\" it..."
role: assistant, content: "Long text that the AI sent you as a response. Same here, it's optional but if not included it is forgotten..."
role: user, content: "More of your prompts... Optional."
role: assistant, content: "More AI answer... Optional."
role: user, content: "Your current prompt you want to send... Obviously this line is also obligatory."
```

Nothing is stored on their server that you could later reference as far as I know! You must send at the very least the first and last lines of the above example to get a response from the AI. If you want the AI to "remember" more of the conversation you have to also send more of the conversation every time you make a prompt! That means if the AI farts(and it is usually verbose), other more simple applications would include the bad prompt-response pair, so you would pay for it several times, and you have that much less tokens to include other more useful context, therefore the chances of the AI chainfarting is also way higher. The main point of my entire HexaPA application is to eliminate what you don't need (long useless content) in favor of more useful content, OR decreased token usage(aka pay for less), in order to get the answers you want with less frustration, and potentially cheaper.

The other point of HexaPA is user definalbe rules! I found that once the conversation gets longer then what fits in the token limit, ChatGPT "forgets" that I said I want code in C++, and it gives me useless answers in other programming languages, so I have to repeat myself several times during a long conversation. Rules in HexaPA do just that! Anything you define as a Rule, is sent to the AI with every prompt, whether or not you choose to include any other context form the conversation, thus the AI stays focused, and actually does what you ask! (Hopefully! :D)

The 3rd point of HexaPA is alternatives! I plan to support other AI chat APIs in the future, such as Google's Bard, and Open Assistent, once they make a public API available. (Currently neither of those are avialable.) A healthy competition of large companies is obviously good for the user.

To be clear: I'm not against payed services, the OpenAI dev's job is to make money from it's users, mine is to maximize the value you get for your money spent on their services! Either way you use their payed service, I'm not trying to find a loophole around that. (I'm using OpenAI's payed service, because it's a good service, and I don't mind paying for it!) With the official ChatGPT you get simplicity, with HexaPA you get full control. (The exact same reason why I love linux is full control! :D)



## Support options
- [SubscribeStar](https://www.subscribestar.com/OSRC)
- [Patreon](https://www.patreon.com/OSRC)
- [PayPal](https://www.paypal.com/paypalme/OSRC)

By the way you can also see images of the project on SubscribeStar and Patreon.



## Installation

### On Ubuntu linux:
```
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install -y git pip python3-tk python3-imaging
pip install openai
pip install tiktoken
pip install cairosvg
```

Get an Open AI API key. (Relatively cheap for text models but not free, follow the instructions in HexaPA on how to get an API key.)
Run the HexaPA executable.

```
cd /path/to/HexaPA
./HexaPA
```
You may also want to use --verbose option to see what it does in the terminal, or --help to list options...

Optionally on Linux you can also use my Systemd-Service-Generator script to launch it automatically at start.

### On other platforms:
If you have no experience asking the AI is probably the fastest way to do it... (Although I wrote it with cross platform compatibility in mind, I'm a Linux only user since 2011, so sorry can't help with that.)
- Log in to [ChatGPT](https://chat.openai.com/) (Create an OpenAI account if you don't have one, you'll need it anyway to get an API key!)
- Copy paste this into the ChatGPT prompt(Copy it from the downloaded README.md file, not directly from github!), replacing the {placeholder} with your specific requirements, and send it:

I need some help installing a python application on {your operating system} with the following dependencies:
`io, os, re, sys, glob, time, argparse, pickle, platform, webbrowser, cryptography, hashlib, base64, gzip, tkinter, cairosvg, pillow, openai, tiktoken`
I know nothing about python programming, please help. I may not even have python istalled.

- When you're done installing dependencies, ask the AI to help you start it:

The main script is called "HexaPA". How can I start it?

- If you have any issues, tell it to the AI, copy-pasting any errors, and it should be able to help you pretty fast, even though the current public model (GPT 3.5) does not know about HexaPA since I wrote it way after it has been trained.
- Once HexaPA is running follow the instructions to get your API key. Good luck!



## Dependencies
These should be included with your python3 installation:
- io (for rendering SVG to image data)
- os (for file handling)
- re (for input sanitization)
- sys (mostly for exitting)
- glob (for importing .py files recursively)
- time (reqired for logging and timestamps)
- argparse (for CLI options handling)
- pickle (for saving objects into binary files)
- platform (for clross platform compatibility)
- webbrowser (for opening links in browser)
- cryptography (for encryption)
- hashlib (for hashing)
- base64 (for encoding encryption key)
- gzip (for text compression)

Installed separately:
- tkinter (for GUI)
- cairosvg (for using SVG images)
- from pillow -> Image, ImageTk (for images and use of images in tkinter GUI)
- openai (for accessing OpenAI API)
- tiktoken (for OpenAI token counting)
