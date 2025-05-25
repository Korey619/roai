def modify_main(new_code_block):
    with open("main.py", "r") as f:
        code = f.read()

    if "```python" in new_code_block:
        start = new_code_block.find("```python") + 9
        end = new_code_block.find("```", start)
        new_code = new_code_block[start:end]
    else:
        new_code = new_code_block

    # Naive overwrite logic – can be smarter with regex sectioning
    with open("main.py", "w") as f:
        f.write(new_code)
