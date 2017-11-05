import requests
import json

url = "https://ic-event-service.run.aws-usw02-pr.ice.predix.io/v2/locations/LOC-ATL-0009-3/events"

querystring = {"eventType":"PKIN","startTime":"1509875600000","endTime":"1509875728000"}

headers = {
    'authorization': "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiI5NjliYmRiZDI2ZmM0NWQxYmFhNTBhMjdmNDg3MGM4ZCIsInN1YiI6ImhhY2thdGhvbiIsInNjb3BlIjpbInVhYS5yZXNvdXJjZSIsImllLWN1cnJlbnQuU0RTSU0tSUUtUFVCTElDLVNBRkVUWS5JRS1QVUJMSUMtU0FGRVRZLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtRU5WSVJPTk1FTlRBTC5JRS1FTlZJUk9OTUVOVEFMLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtVFJBRkZJQy5JRS1UUkFGRklDLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtUEFSS0lORy5JRS1QQVJLSU5HLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtUEVERVNUUklBTi5JRS1QRURFU1RSSUFOLkxJTUlURUQuREVWRUxPUCJdLCJjbGllbnRfaWQiOiJoYWNrYXRob24iLCJjaWQiOiJoYWNrYXRob24iLCJhenAiOiJoYWNrYXRob24iLCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwicmV2X3NpZyI6IjlmMWYyYzRkIiwiaWF0IjoxNTA5ODczMDI5LCJleHAiOjE1MTA0Nzc4MjksImlzcyI6Imh0dHBzOi8vODkwNDA3ZDctZTYxNy00ZDcwLTk4NWYtMDE3OTJkNjkzMzg3LnByZWRpeC11YWEucnVuLmF3cy11c3cwMi1wci5pY2UucHJlZGl4LmlvL29hdXRoL3Rva2VuIiwiemlkIjoiODkwNDA3ZDctZTYxNy00ZDcwLTk4NWYtMDE3OTJkNjkzMzg3IiwiYXVkIjpbImllLWN1cnJlbnQuU0RTSU0tSUUtVFJBRkZJQy5JRS1UUkFGRklDLkxJTUlURUQiLCJpZS1jdXJyZW50LlNEU0lNLUlFLVBBUktJTkcuSUUtUEFSS0lORy5MSU1JVEVEIiwiaWUtY3VycmVudC5TRFNJTS1JRS1QVUJMSUMtU0FGRVRZLklFLVBVQkxJQy1TQUZFVFkuTElNSVRFRCIsInVhYSIsImhhY2thdGhvbiIsImllLWN1cnJlbnQuU0RTSU0tSUUtRU5WSVJPTk1FTlRBTC5JRS1FTlZJUk9OTUVOVEFMLkxJTUlURUQiLCJpZS1jdXJyZW50LlNEU0lNLUlFLVBFREVTVFJJQU4uSUUtUEVERVNUUklBTi5MSU1JVEVEIl19.DQihU7hsYoBJyuGLnzdsrUgUhTJmNtGP4yr_MtOUrjOZ6uu2bFVysrKfTVrMIWR3d7cI0jPM4JR1rJcIAsjo2fN3TV0xliSwPGkWL4AzCIX-ZNbbolNZrpOtlVKzhQq80Xbkq2eH1pMC6UN2MNb8zZRtle3B-4M8lhEJ_dg9CG2d15JKp3rBnEB3O-3a1yFmqXeH9mmz1dxl6Or8hHltsvBU6u35yqxNeh3cuIkIGkRfQuJaMinVDrT41AVFKBsyBn83jZ_fjG0JTR87Oo4i2gZAxC4IGgsqTEK8roD0MSh7Dz9m2mJy85Aws_oNgAnAF6i98Vwrli25Yuj-WV515A",
    'predix-zone-id': "SDSIM-IE-PARKING",
    'cache-control': "no-cache",
    'postman-token': "ce79278e-404f-41af-abf2-60082503ae15"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
jsonPKIN = json.loads(response.text)

print(jsonPKIN)

print('\n')
print(jsonPKIN["metaData"])
print('\n')

numin = jsonPKIN["metaData"]["totalRecords"]


print('\n')
print('number of cars that entered in this time period are ' + str(numin) +'\n')


