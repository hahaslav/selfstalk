# Record what you're doing and summarize it with LLM

This script will screenshot your desktop, send its picture to your local LLM to analyse what you're doing, write down its verdict and repeat.

## Setup

1. Download the [script](main.py).
2. Install dependencies from [requirements.txt](requirements.txt).
3. Open the [script's code](main.py) and check if these variables are correct for your LLM server:
   - LMS_SERVER refers to the address of your LLM server (I was using LM Studio, but I don't see why it would not work with similar servers)
   - LLM refers to your vision-enabled LLM name in your server

## Usage

Just run the script.

To stop the script, press Ctrl+C or just close the terminal window.

## Other thoughts

I explicitly used the Windows method to take screenshots because I don't think users of other OS will want to run this script. But if needed, MSS library should work on any OS.

By looking on how much resources it takes to run LLM, it would be better to just constantly record your screen, but this will instead take a lot of disk space. At least this tool is definitely better than the new feature in Copilot PCs. Yes, this tool does not encrypt collected data. Yes, this tool helps much less than the other solution. But this is just a fun little project I've done in one evening, while the other solution is a flawed unnecessary service which should not be a major part of an operating system.