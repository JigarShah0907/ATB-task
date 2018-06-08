from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

def longestSubstring(str1, str2):
    str1 = " ".join(i for i in str1) if type(str1)==set else str1
    m = len(str1)
    n = len(str2)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if str1[i] == str2[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(str1[i-c+1:i+1])
                elif c == longest:
                    lcs_set.add(str1[i-c+1:i+1])

    return lcs_set

class Todo(Resource):
    def post(self):
        try:
            if request.data and request.data != "" and request.data != "{}":
                data = eval(request.data)
            else:
                raise Exception
        except :
            return "The format of the request was not acceptable", 400

        if "setOfStrings" not in data or data["setOfStrings"] == '':
            return "SetOfStrings should not be empty.", 400

        values = [i["value"] for i in data["setOfStrings"]]

        if len(values) >len(set(values)):
             return "'SetOfStrings' must be a Set", 400

        res = reduce((lambda x, y: longestSubstring(x, y)), values)
        result = {}
        result["lcs"] = [{"value":i} for i in sorted(list(res))]
        return result, 200

api.add_resource(Todo, '/lcs')
if __name__ == '__main__':
    app.run()
