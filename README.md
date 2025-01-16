### Capabilities
[x] add file pane/upload capability
[x] render LLM responses properly w/ markup
[x] authentication, login, logout, signup, track login with cookie
[x] integrate true llm responses
- settings pannel, modify subscription

- upgrade view, much like language Gui
- pin a chat to save from deletion, must un-pin to delete
- stream LLM responses
- allow user commands to change the view as well as initiate actions

### To run
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requrements.txt
update ~/.assistant/openllmui.yaml
python -m agent

## Main dev files

### Biz Logic
/functions.py
/assistant.py
/routes/chat_mgmt.py

### Style/Format
/templates/index.html
/js/index.js
/css/index.css

### Model
/models/__init__.py
