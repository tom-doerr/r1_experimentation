#!/bin/zsh


for i in {1..1000}
do
        #MODEL=openrouter/deepseek/deepseek-r1
        MODEL=r1
        #MODEL=deepseek
        echo "$i - $(date) ====================================================="
        aider --architect --model $MODEL --subtree-only --read plex.md --read context.txt --yes-always --no-show-model-warnings --weak-model 'openrouter/google/gemini-2.0-flash-001' --message 'if there are errors, work on fixing the errors. if there are no errors, work on cleaning up the code a little bit. Please also read the comments in testing.py and make sure that the code outside of testing.py matches the requirements mentioned in the comments. I am importing from main, so if you see that something is not defined or implemented, please work on implementing until there are no errors. Please fix the code in main.py if we get errors when running testing.py. testing.py needs to work as it is right now. Do not edit testing.py. Do not add testing.py to the chat. Do not edit the linting rules. Do not run any commands. Do not try to install anything. Do not mock any functionality, actually implement it. Is there any functionality that is not yet implemented? Replace all mocking with actual implementations. Only use small search replace blocks, but you can use multiple ones.' **/*py
        sleep 1
done






