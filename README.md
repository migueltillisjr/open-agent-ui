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
```
openai:
  api_key: OPEN_AI_API_KEY
instagram:
  access_token: ${INSTAGRAM_ACCESS_TOKEN}
reddit:
  id: Reddit API KEY
  secret: SECRET
  user_agent: firstaccess/0.1 by Low-Jellyfish-8234
alphavantage:
  key: ALPHA_ADVANTAGE_KEY
gpt_directions: /home/miguel/freedom/openllmui-api/agent/files/chatgpt.directions.txt
ui_auth: /home/miguel/freedom/openllmui-api/agent/ui/config.yaml
fine_tuning: /home/miguel/freedom/openllmui-api/agent/fine_tuning/
log_file: /home/miguel/freedom/openllmui-api/agent/files/openllmui-api/agent/Log.md
upload_folder: /home/miguel/freedom/openllmui-api/agent/ui/uploads
host: '127.0.0.1'
port: '5000'
report_access_port: '8080'
app_files: '/home/miguel/freedom/openllmui-api/agent/app-files'
google_auth: '/home/miguel/.openllmui-api/google.credentials.json'
app_workdir: '/home/miguel/freedom/openllmui-api/agent'
# sqlalchemy_database_uri: 'postgresql://postgres:mysecretpassword@localhost:5432/ldmg'
sqlalchemy_database_uri: 'sqlite:////home/miguel/freedom/openllmui-api/agent/db/chat.db'
sender_email: 'no-reply@ldmg.org'
html_report_url: 'http://e3.ldmg.org:8080/notify_report'
reply_to_email: 'no-reply@ldmg.org'
```

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
