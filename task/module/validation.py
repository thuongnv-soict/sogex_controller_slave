from datetime import datetime
import constant


def checkValidExecuteAt(execute_at):
    execute_at = datetime.strptime(execute_at, constant.FORMAT_DATETIME)
    now = datetime.now()
    diff = now - execute_at
    if diff.seconds > constant.MAX_DELAY:
        return False
    return True