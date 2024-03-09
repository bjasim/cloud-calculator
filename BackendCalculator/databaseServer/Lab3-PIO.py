import arcade
import random
import math

# --- Set up the cd constants

# Size of the screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Bouncing Balls Example"


class Ball:
    """
    Class to keep track of a ball's location and vector.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.size = 0
        self.color = None


def make_ball():
    """
    Function to make a new, random ball.
    """
    ball = Ball()

    # Size of the ball
    ball.size = random.randrange(10, 30)

    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.
    ball.x = random.randrange(ball.size, SCREEN_WIDTH - ball.size)
    ball.y = random.randrange(ball.size, SCREEN_HEIGHT - ball.size)

    # Speed and direction of rectangle
    ball.change_x = random.randrange(-2, 3)
    ball.change_y = random.randrange(-2, 3)

    # Color
    ball.color = (random.randrange(256), random.randrange(256), random.randrange(256))

    return ball


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.ball_list = []

        # SENG3090 Note: At lower values, the impact of collision detection isn't as high.
        # Below 150, it has much less effect. Please document your analysis using the
        # value 200 (but you may of course test with lower or higher values)
        for i in range(200):
            ball = make_ball()
            self.ball_list.append(ball)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        for ball in self.ball_list:
            arcade.draw_circle_filled(ball.x, ball.y, ball.size, ball.color)

        # Put the text on the screen.
        output = "Balls: {}".format(len(self.ball_list))
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        """ Movement and game logic """
        for ball in self.ball_list:
            ball.x += ball.change_x
            ball.y += ball.change_y

            if ball.x < ball.size:
                ball.change_x *= -1

            if ball.y < ball.size:
                ball.change_y *= -1

            if ball.x > SCREEN_WIDTH - ball.size:
                ball.change_x *= -1

            if ball.y > SCREEN_HEIGHT - ball.size:
                ball.change_y *= -1

        # SENG3090 - Here is the problem - check for collisions here
        self.check_collisions()

    def check_collisions(self):
        """
        Loop through all the balls and check for collisions.
        TODO: Make the balls change direction on collision.
        """
        for outer, ball1 in enumerate(self.ball_list):
            for inner, ball2 in enumerate(self.ball_list):
                if inner != outer:
                    # Test for contact
                    distx = ball1.x - ball2.x
                    disty = ball1.y - ball2.y
                    distance = math.sqrt((distx * distx) + (disty * disty))
                    if distance <= (ball1.size + ball2.size):
                        # TODO: Make the balls bounce off each other,
                        #       using their angles; keep speed the same
                        print("Ball 1: ", outer, " Ball 2: ", inner)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """
        ball = make_ball()
        self.ball_list.append(ball)


def main():
    MyGame()
    arcade.run()


if __name__ == "__main__":
    main()
