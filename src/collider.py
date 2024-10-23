import pygame as pg
vec = pg.Vector2

'''
    Collider Class
    The original C++ Code belongs to David Barr, aka javidx9, OneLoneCoder 
    Adapted to Python: Christian Krauss

    Resources for this code:
    https://www.gamedev.net/tutorials/programming/general-and-gameplay-programming/swept-aabb-collision-detection-and-response-r3084/
    https://github.com/OneLoneCoder/olcPixelGameEngine/blob/master/Videos/OneLoneCoder_PGE_Rectangles.cpp
    '''


class Collider:

    def __init__(self):
        self.contact_normal = vec(0, 0)
        self.contact_point = vec(0, 0)
        self.contact_time = 0
        self.t_hit_near = 0
        self.t_hit_far = 0

    '''
        Collision Point and Rect vs Rect
    '''

    def PointVsRect(self, point, rect):
        # Test if a point is colliding with a rect
        # returns True or False
        return point.x >= rect.x and point.y >= rect.y and point.x < rect.x + rect.width and point.y < rect.y + rect.height

    def RectVsRect(self, rect1, rect2):
        # Test if rect1 is colliding with rect2
        # returns True or False
        return rect1.x < rect2.x + rect2.width and rect1.x + rect1.width > rect2.x and rect1.y < rect2.y + rect2.height and rect1.y + rect1.height > rect2.y

    '''
        Collision Detection Swept AABB method
    '''

    def RayVsRect(self, ray_origin, ray_dir, rect):
        self.contact_normal = vec(0, 0)
        self.contact_point = vec(0, 0)
        self.contact_time = 0
        self.t_hit_near = 0
        self.t_hit_far = 0

        # Calculate Ray Distances
        if ray_dir.x == 0:
            if ray_origin.x <= rect.left:
                t_near_x = float('-inf')
                t_far_x = float('-inf')
            elif ray_origin.x >= rect.right:
                t_near_x = float('inf')
                t_far_x = float('inf')
            else:
                t_near_x = float('-inf')
                t_far_x = float('+inf')
        else:
            t_near_x = (rect.left - ray_origin.x) / ray_dir.x
            t_far_x = (rect.right - ray_origin.x) / ray_dir.x

        # Calculate Ray Distances
        if ray_dir.y == 0:
            if ray_origin.y <= rect.top:
                t_near_y = float('-inf')
                t_far_y = float('-inf')
            elif ray_origin.y >= rect.bottom:
                t_near_y = float('inf')
                t_far_y = float('inf')
            else:
                t_near_y = float('-inf')
                t_far_y = float('inf')
        else:
            t_near_y = (rect.top - ray_origin.y) / ray_dir.y
            t_far_y = (rect.bottom - ray_origin.y) / ray_dir.y

        # Sort distances
        if t_near_x > t_far_x:
            t_near_x, t_far_x = t_far_x, t_near_x
        if t_near_y > t_far_y:
            t_near_y, t_far_y = t_far_y, t_near_y

        # Early rejection
        if t_near_x > t_far_y or t_near_y > t_far_x:
            return False

        # Closest 'time' will be the first contact
        self.t_hit_near = max(t_near_x, t_near_y)

        # Furthest 'time' is contact on opposite side of target
        self.t_hit_far = min(t_far_x, t_far_y)

        # Some things that should not happen
        if self.t_hit_near > self.t_hit_far:
            return False

        if t_near_x < 0 and t_near_y < 0:
            return False

        # Reject if ray direction is pointing away from object
        if self.t_hit_far < 0 or self.t_hit_near > self.t_hit_far or self.t_hit_near > 1:
            return False

        # Contact point of collision from parametric line equation
        self.contact_point = ray_origin + self.t_hit_near * ray_dir

        if t_near_x > t_near_y:
            if ray_dir.x < 0:
                self.contact_normal = vec(1, 0)
            else:
                self.contact_normal = vec(-1, 0)
        elif t_near_x < t_near_y:
            if ray_dir.y < 0:
                self.contact_normal = vec(0, 1)
            else:
                self.contact_normal = vec(0, -1)

        # The is only collision in time t < 1
        if self.t_hit_near < 1:
            self.contact_time = self.t_hit_near
            return True
        else:
            return False

    def DynamicRectVsRect(self, r_dynamic, vel, r_static):

        if (vel.x == 0 and vel.y == 0):
            return False

        expanded_target = pg.Rect(r_static.left-r_dynamic.width/2, r_static.top-r_dynamic.height/2,
                                  r_static.width+r_dynamic.width, r_static.height+r_dynamic.height)

        if self.RayVsRect(vec(r_dynamic.center), vel, expanded_target):
            return True
        else:
            return False

    def ResolveDynamicRectVsRect(self, vel, time, normal):
        vel_x = vel.x + normal.x * abs(vel.x) * (1 - time)
        vel_y = vel.y + normal.y * abs(vel.y) * (1 - time)

        return vec(vel_x, vel_y)

    def __takeFirstElement(self, elem):
        return elem["contact_time"]

    def collideSweptAABB(self, sprite, obstacles):
        # Collision detection
        collisions = []
        for rect in obstacles:
            if self.DynamicRectVsRect(sprite.rect, sprite.vel, rect.rect):
                contact_time = self.contact_time
                contact_normal = self.contact_normal
                collisions.append({"contact_time": contact_time,
                                   "contact_normal": contact_normal, "object": rect})
        # Sort from nearest collision to far
        if len(collisions) > 0:
            collisions.sort(key=self.__takeFirstElement)
        return collisions

    '''
        Collision Detection AABB method
    '''

    def getAABBHits(self, sprite, obstacles):
        hits = []
        for obstacle in obstacles:
            if self.RectVsRect(sprite.rect, obstacle.rect):
                hits.append(obstacle)
        return hits

    def checkAABBx(self, sprite, obstacles):
        sprite.pos.x += sprite.vel.x
        sprite.rect.topleft = sprite.pos
        hits = self.getAABBHits(sprite, obstacles)
        collisions = []
        for hit in hits:
            if sprite.vel.x > 0:  # Hit moving right
                collisions.append({"contact_time": 0,
                                   "contact_normal": vec(-1, 0), "object": hit})
            elif sprite.vel.x < 0:  # Hit moving left
                collisions.append({"contact_time": 0,
                                   "contact_normal": vec(1, 0), "object": hit})
        sprite.pos.x -= sprite.vel.x
        sprite.rect.topleft = sprite.pos
        return collisions

    def checkAABBy(self, sprite, obstacles):
        sprite.pos.y += sprite.vel.y
        sprite.rect.topleft = sprite.pos
        hits = self.getAABBHits(sprite, obstacles)
        collisions = []
        for hit in hits:
            if sprite.vel.y > 0:  # Hit moving bottom
                collisions.append({"contact_time": 0,
                                   "contact_normal": vec(0, -1), "object": hit})
            elif sprite.vel.y < 0:  # Hit moving top
                collisions.append({"contact_time": 0,
                                   "contact_normal": vec(0, 1), "object": hit})
        sprite.pos.y -= sprite.vel.y
        sprite.rect.topleft = sprite.pos
        return collisions

    def collideAABB(self, sprite, obstacles):
        collisions = []
        collisions.extend(self.checkAABBx(sprite, obstacles))
        collisions.extend(self.checkAABBy(sprite, obstacles))
        return collisions

    def resolveAABB(self, sprite, collisions):
        sprite.pos += sprite.vel
        for hit in collisions:
            if hit["contact_normal"] == vec(-1, 0):  # Hit moving right
                sprite.pos.x = hit["object"].rect.left - sprite.rect.width
                sprite.vel.x = 0
            elif hit["contact_normal"] == vec(1, 0):  # Hit moving left
                sprite.pos.x = hit["object"].rect.right
                sprite.vel.x = 0
            elif hit["contact_normal"] == vec(0, -1):  # Hit moving bottom
                sprite.pos.y = hit["object"].rect.top - sprite.rect.height
                sprite.vel.y = 0
            elif hit["contact_normal"] == vec(0, 1):  # Hit moving top
                sprite.pos.y = hit["object"].rect.bottom
                sprite.vel.y = 0
            else:
                return False
        sprite.rect.topleft = sprite.pos
        return True
