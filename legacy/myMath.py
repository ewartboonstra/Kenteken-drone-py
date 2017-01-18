import math

class myMath:

    def distance_between_points(self, p1, p2):
        #p[0] = x, p[1] = y
        #c^2 = (xA - xB)^2 + (yA - yB)^2 =
        #c = root((xA - xB)^2 + (yA - yB)^2)
        return abs(math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2)))

    def ratio(self, n1, n2):
        r = n2/n1
        return r
