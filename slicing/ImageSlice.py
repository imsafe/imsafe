class ImageSlice:
    def __init__(self, image, height, width):
        self.image = image
        self.height = height
        self.width = width

    def slice(self):
        mid_of_height = int(self.height / 2)
        mid_of_width = int(self.width / 2)

        top_left = self.image[:mid_of_height, :mid_of_width]
        top_right = self.image[:mid_of_height, mid_of_width:self.width]
        bottom_left = self.image[mid_of_height:self.height, :mid_of_width]
        bottom_right = self.image[mid_of_height:self.height, mid_of_width:self.width]

        return top_left, top_right, bottom_left, bottom_right
