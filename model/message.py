import json


# class MonitorMessage:
#     def __init__(self):
#         self.id = None
#         self.server_ip = None
#         self.project = None
#         self.spider = None
#         self.username = None
#         self.followings = None
#         self.expected_execute_at = None
#         self.real_execute_at = None
#         self.status = None
#
#     def to_json(self):
#         return json.dumps(self, default=lambda o: o.__dict__,
#                           sort_keys=True, indent=4)


class UpdateJobMessage:
    def __init__(self):
        self.id = None
        self.real_execute_at = None
        self.status = None
        self.error_code = None
        self.error_detail = None
        self.finished_at = None

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
