from utils import ProfileSourceEnum

from gui_agents.get_references import get_nl_profile

import argparse

dumb_generic_prompt = """
# Reference Information
This is the reference information to fill out the form.

```
{user_reference}
```

# Instructions
Complete the form. Ignore fields that have already been filled, you can identify added text as it would be in red font color. """

smart_generic_prompt = """
These are instructions for how to operate the interface.

# Interface Instructions
## Add Text
Follow these instructions literally to add text to the page

1. Click the answer area to create a new textbox (note that the text box is inserted top right of the cursor location) and type the the answer to the field (if no value, still proceed to step 2)
2. Click the checkmark on the top-right right of the X icon which indicates cancel. It is the check NOT the cross. Location is 'coordinate': [804, 53]
3. Proceed to step 1 as you will remain in text edit mode

## Notes
For checkboxes, as the interface does not have interactive checkboxes, “check” it by adding text “X” on it. 
If you click too close to an existing text box, it will enter editing mode for that textbox.
Remember that the textbox is created on top right of the cursor location (e.g. click location is bottom left corner)
You can identify previously added text as it would be in red font color. 
Do not redo the same field, continue onwards
If no text is added to a textbox, still remember to press the checkmark (step 2) to escape that textbox so a new one could be made later.

## Navigational
Make sure when doing navigational actions that the focus is in the canvas not the area around it

### Pan : 
Scrolling

{dumb_prompt}"""

def get_prompt(smart=True, file_id=None, user_idx=0, profile_source=ProfileSourceEnum.TEXT.value):
    dumb_prompt = dumb_generic_prompt.format(user_reference=get_nl_profile(file_id, user_idx, profile_source))
    if not smart:
        return dumb_prompt
    else:
        return smart_generic_prompt.format(dumb_prompt=dumb_prompt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # New argument to take a list of PNG file paths
    parser.add_argument(
        "-s", "--smart", action="store_true", help="Use smart prompt"
    )
    parser.add_argument(
        "-d", "--dumb", action="store_true", help="Use dumb prompt"
    )
    parser.add_argument(
        "--file_id", type=str, help="File ids, e.g. al_0_0"
    )
    # parser.add_argument("--source_doc_id", type=str, default=None)
    parser.add_argument("--user_idx", type=int, default=0)
    parser.add_argument(
        "--profile_source",
        type=str,
        help=f"Whether to use a baseline action set or our model [{', '.join([c.value for c in ProfileSourceEnum])}]",
        default=ProfileSourceEnum.TEXT.value,
    )
    args = parser.parse_args()
    
    if args.smart and args.dumb:
        raise ValueError("Cannot use both smart and dumb prompts at the same time.")
    
    if not args.smart and not args.dumb:
        raise ValueError("Must use either smart or dumb prompts.")
    
    prompt = get_prompt(args.smart, args.file_id, args.user_idx, args.profile_source)
    print("=" * 50)
    print(prompt)
    print("=" * 50)