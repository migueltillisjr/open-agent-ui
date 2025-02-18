### UI/UX
![Alt Text](agent/imgs/app_screen2.png)

### Capabilities
- [x] add file pane/upload capability
- [x] render LLM responses properly w/ markup
- [x] authentication, login, logout, signup, track login with cookie
- [x] integrate true llm responses
- [] Add files integration
- [] settings pannel, modify subscription
- [] upgrade view, much like language Gui
- [] pin a chat to save from deletion, must un-pin to delete
- [] stream LLM responses
- [] allow user commands to change the view as well as initiate actions
- [] Use aws bedrock agents
- [] control view using natural language
- [] create view for agent pipelines
- [] add agent steps log view for diagnosis

### To run
```
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requrements.txt
```

```
python -m agent
```

update ~/.assistant/open-agent-ui.yaml

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
gpt_directions: /home/miguel/freedom/open-agent-ui/agent/files/chatgpt.directions.txt
ui_auth: /home/miguel/freedom/open-agent-ui/agent/ui/config.yaml
fine_tuning: /home/miguel/freedom/open-agent-ui/agent/fine_tuning/
log_file: /home/miguel/freedom/open-agent-ui/agent/files/open-agent-ui/agent/Log.md
upload_folder: /home/miguel/freedom/open-agent-ui/agent/ui/uploads
host: '127.0.0.1'
port: '5000'
report_access_port: '8080'
app_files: '/home/miguel/freedom/open-agent-ui/agent/app-files'
google_auth: '/home/miguel/.open-agent-ui/google.credentials.json'
app_workdir: '/home/miguel/freedom/open-agent-ui/agent'
# sqlalchemy_database_uri: 'postgresql://postgres:mysecretpassword@localhost:5432/ldmg'
sqlalchemy_database_uri: 'sqlite:////home/miguel/freedom/open-agent-ui/agent/db/chat.db'
sender_email: 'no-reply@ldmg.org'
html_report_url: 'http://e3.ldmg.org:8080/notify_report'
reply_to_email: 'no-reply@ldmg.org'
```




## Main dev files

### Config
```
/agent/config/__init__.py
```


### Controller - Biz Logic
```
/agent/functions.py
/agent/assistant.py
/agent/routes/chat_mgmt.py
```

### View - Style/Format
```
/agent/templates/*.html
/agent/templates/js/*.js
/agent/templates/css/*.css
```

### Model - DB / Schema
```
/agent/models/__init__.py
```