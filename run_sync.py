import json
import os
from socketsync.core import Core
from datetime import datetime, timedelta, timezone
from socketsync.connectors.slack import Slack


if __name__ == '__main__':
    now = datetime.now(tz=timezone.utc) - timedelta(minutes=300)
    now_str = now.strftime("%Y-%m-%d %H:%M")
    api_key = os.getenv("SOCKET_SECURITY_API_KEY") or exit(1)
    start_date = os.getenv("START_DATE") or now_str
    default_branches = [
        "master",
        "main"
    ]
    core = Core(
        api_key=api_key,
        start_date=start_date,
        default_branch_only=False
    )
    issue_data = core.get_issues()
    slack_url = os.getenv("SLACK_WEBHOOK") or exit(1)
    slack = Slack(slack_url)
    for issue in issue_data:
        issue_json = json.loads(str(issue))
        slack.send(issue_json)
