import math


class Camera:
    def __init__(self, posX, posY, posZ, focalLength):
        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        self.focalLength = focalLength  
            
    @classmethod
    def fromJsonDocument(cls, jsonstr):
        posX = jsonstr["posX"]
        posY = jsonstr["posY"]
        posZ = jsonstr["posZ"]
        focalLength = jsonstr["focalLength"]
        return cls(posX, posY, posZ, focalLength)
    
    def cast_ray(self, pixel_x, pixel_y, sphere):
        # Calculate the direction of the ray from the camera to the pixel
        direction_x = pixel_x - self.posX
        direction_y = pixel_y - self.posY
        direction_z = self.focalLength - self.posZ
        mag = math.sqrt(direction_x**2 + direction_y**2 + direction_z**2)
        direction_x /= mag
        direction_y /= mag
        direction_z /= mag

        # Ray-sphere intersection calculation
        ray_origin = (self.posX, self.posY, self.posZ)
        ray_direction = (direction_x, direction_y, direction_z)
        sphere_center = (sphere.posX, sphere.posY, sphere.posZ)
        radius = sphere.radius

        # Compute the components of the quadratic equation
        a = direction_x**2 + direction_y**2 + direction_z**2
        b = 2 * (direction_x * (ray_origin[0] - sphere_center[0]) +
                 direction_y * (ray_origin[1] - sphere_center[1]) +
                 direction_z * (ray_origin[2] - sphere_center[2]))
        c = (ray_origin[0] - sphere_center[0])**2 + \
            (ray_origin[1] - sphere_center[1])**2 + \
            (ray_origin[2] - sphere_center[2])**2 - \
            radius**2

        discriminant = b**2 - 4 * a * c

        # If the discriminant is negative, there is no intersection
        if discriminant < 0:
            return None

        # Compute the intersection point
        t = (-b - math.sqrt(discriminant)) / (2 * a)
        intersection_point = (ray_origin[0] + t * direction_x,
                              ray_origin[1] + t * direction_y,
                              ray_origin[2] + t * direction_z)

        return intersection_point
    
