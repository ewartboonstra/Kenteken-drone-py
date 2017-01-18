import cv2
from jsondata import Json
import server

cropped_img = cv2.imread("cropped_img.png", cv2.IMREAD_COLOR)
# send image to server
# test code
# jsonData = base64.b64encode(cropped_img)
# echte code
json = Json()
jsonData = json.convertToJson()

server = server.Server()
server.openConnection()
server.sendJsonData(jsonData)
server.closeConnection()