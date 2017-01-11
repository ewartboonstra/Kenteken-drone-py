from myMath import myMath

class contour:

    points = []
    next_contour = -1
    previous_contour = -1
    first_child = -1
    parent = -1


    def __init__(self, points, next_contour, previous_contour, first_child, parent):
        self.points = points
        self.next_contour = next_contour
        self.previous_contour = previous_contour
        self.first_child = first_child
        self.parent = parent

# a rectangle is a contour with four points
class rectangle(contour):

    def __init__(self, contour):
        if len(contour.points) == 4:
            contour.__init__(contour.points, contour.next_contour, contour.previous_contour, contour.first_child, contour.parent)
        else:
            #TODO: trow exception
            print 'son you disapoint me, rectangle have no more and no less then 4 points'
            asdf

    #points[0][0][0] x of point 1
    #points[0][0][1] y of point 1
    #points[1][0][0] x of point 2
    #points[1][0][1] y of point 2
    #points[2][0][0] x of point 3
    #points[2][0][1] y of point 3
    #points[3][0][0] x of point 4
    #points[3][0][1] y of point 4
    #points go counterclockwise starting with the top left one
    #1 is left
    #2 is bottom
    #3 is right
    #4 is top

    def get_side_1(self):
        return myMath.distance_between_points(points[0][0],points[1][0])

    def get_side_2(self):
        return myMath.distance_between_points(points[1][0],points[2][0])

    def get_side_3(self):
        return myMath.distance_between_points(points[2][0],points[3][0])

    def get_side_4(self):
        return myMath.distance_between_points(points[3][0],points[1][0])


    '''
    len1 = mm.distance_between_points(cnt[0][0],cnt[1][0])
    len2 = mm.distance_between_points(cnt[1][0],cnt[2][0])
    len3 = mm.distance_between_points(cnt[2][0],cnt[3][0])
    len4 = mm.distance_between_points(cnt[3][0],cnt[1][0])
    '''
