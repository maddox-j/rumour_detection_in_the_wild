import ast
from datetime import datetime

class Node():
    def __init__(self, *args, **kwargs):
        node_string = kwargs.get("node_string", "API_NODE")
        if node_string != "API_NODE":
            node_list = ast.literal_eval(node_string)
            self.uid = node_list[0]
            self.tweet_id = node_list[1]
            self.time_delay = float(node_list[2])
            self.root = False
            self.parent = None
        else:
            self.uid = kwargs.get("uid")
            self.tweet_id = kwargs.get("tweet_id")
            self.time_delay = kwargs.get("time_delay")
            self.text = kwargs.get("text")
            self.root = kwargs.get("root")
            if kwargs.get("created_at"):
                self.created_at = datetime.strptime(kwargs.get("created_at") ,"%Y-%m-%dT%H:%M:%S.%fZ")
            self.parent = kwargs.get("parent")
            self.tokenized_text = kwargs.get("tokenized_text")
            self.dict_repr = kwargs.get("dict_repr")
        self.child = None
        

    def __str__(self) -> str:
        return f"UID: {self.uid} \t Tweet ID: {self.tweet_id} \t Time:{self.time_delay}"
        #

    def __eq__(self, __o: object) -> bool:
        # Check equality based on combination of user id and tweet id.
        return self.tweet_id == __o.tweet_id 
            #and self.uid == __o.uid

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

    def __hash__(self):
        return hash((self.tweet_id))
