# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random
import time 


class RunawayGame:
    def __init__(self, canvas, runner, chaser, chaser2, catch_radius=50):
        self.root = root   
        self.start_time = time.time() 
        self.last_update_time = 0 

        self.score1 = 0
        self.score2 = 0

        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.chaser2 = chaser2
        self.catch_radius2 = catch_radius**2

        chaser.target_runner = runner
        
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        self.chaser2.shape('turtle')
        self.chaser2.color('black')
        self.chaser2.penup()

        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

        self.skill_drawer = turtle.RawTurtle(canvas)
        self.skill_drawer.hideturtle()
        self.skill_drawer.penup()
        self.show_skill_info()

        self.obstacles = [] 
        self.spawn_interval = 3000  
        self.canvas.ontimer(self.spawn_obstacle, self.spawn_interval)

        self.restart_button = None  
        
    def spawn_obstacle(self):

        obs = turtle.RawTurtle(self.canvas)
        obs.shape("circle")
        obs.color("gray")
        obs.penup()
        x = random.randint(-300, 300)
        y = random.randint(-300, 300)
        obs.setpos(x, y)
        self.obstacles.append(obs)
        self.canvas.ontimer(self.spawn_obstacle, self.spawn_interval)

    def check_obstacle_collision(self, turtle_obj):
        for obs in self.obstacles:
            dx, dy = turtle_obj.xcor() - obs.xcor(), turtle_obj.ycor() - obs.ycor()
            if dx**2 + dy**2 < 20**2:  
                return True
        return False

    def is_catched(self):
        p = self.runner.pos()


        q1 = self.chaser.pos()
        dx1, dy1 = p[0] - q1[0], p[1] - q1[1]
        if dx1**2 + dy1**2 < self.catch_radius2:
            return "chaser1"

        q2 = self.chaser2.pos()
        dx2, dy2 = p[0] - q2[0], p[1] - q2[1]

        if dx2**2 + dy2**2 < self.catch_radius2:
            return "chaser2"
        
        return None 
    

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)

        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)
        
        self.chaser2.setpos((+init_dist / 2, -100))
        self.chaser2.setheading(180)

        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        if self.score1 >= 10 or self.score2 >= 10:
            self.drawer.clear()
            if self.score1 >= 10:
                self.drawer.setpos(0, 0)
                self.drawer.write("HUMAN WIN!", align="center", font=("Arial", 30, "bold"))
                self.drawer.setpos(0, -40)
                self.drawer.write("AI BLACK LOSE", align="center", font=("Arial", 20))
            else:
                self.drawer.setpos(0, 0)
                self.drawer.write("AI BLACK WIN!", align="center", font=("Arial", 30, "bold"))
                self.drawer.setpos(0, -40)
                self.drawer.write("HUMAN LOSE", align="center", font=("Arial", 20))

            
            if not self.restart_button:
                self.restart_button = tk.Button(
                    self.root, text="Restart", font=("Arial", 14, "bold"),
                    command=self.reset_game
                )
                self.restart_button.pack()
            return


        self.keep_inside(self.runner)
        self.keep_inside(self.chaser)
        self.keep_inside(self.chaser2)
        
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())
        self.chaser2.run_ai(self.runner.pos(), self.runner.heading())

        elapsed= time.time() -self.start_time

        is_catched = self.is_catched()

        if is_catched == "chaser1":
            self.score1 +=1
            self.chaser.step_move +=1
            self.reset_runner()
        elif is_catched == "chaser2":
            self.score2 +=1
            self.reset_runner()


        if self.check_obstacle_collision(self.chaser):
            self.score1 = max(0, self.score1 - 1)
            self.reset_runner()
        if self.check_obstacle_collision(self.chaser2):
            self.score2 = max(0, self.score2 - 1)
            self.reset_runner()
        if self.check_obstacle_collision(self.runner):
            self.reset_runner()
            

        self.drawer.clear()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Score - Red: {self.score1} | Black: {self.score2}', font=("Arial", 14))

        self.drawer.setpos(-300, 270)
        self.drawer.write(f'Time: {elapsed:.1f}', font=("Arial", 14))

        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def reset_runner(self):
        self.runner.setpos((-200+ random.randint(-50,50), random.randint(-200,200)))
        self.runner.setheading(random.randint(0,360))

    def keep_inside(self, turtle_obj, limit=350):
        x, y = turtle_obj.pos()

        if abs(x) > limit or abs(y) > limit:

            new_x = random.randint(-200, 200)
            new_y = random.randint(-200, 200)
            turtle_obj.setpos(new_x, new_y)
            turtle_obj.setheading(random.randint(0, 360))

    def show_skill_info(self):
        self.skill_drawer.clear()
        self.skill_drawer.setpos(-300, 330)
        self.skill_drawer.write(
            "Skills: Q=Teleport | W=Boost | E=Face Runner | R=Dash",
            font=("Arial", 12, "bold")
        )

    def reset_game(self):
        # 점수/시간/장애물 초기화
        self.score1 = 0
        self.score2 = 0
        self.start_time = time.time()
        for obs in self.obstacles:
            obs.hideturtle()
        self.obstacles.clear()

        # 버튼 제거
        if self.restart_button:
            self.restart_button.destroy()
            self.restart_button = None

        # 게임 다시 시작
        self.start()
class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        self.canvas = canvas

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

        canvas.onkeypress(self.skill_q, 'q')
        canvas.onkeypress(self.skill_w, 'w')
        canvas.onkeypress(self.skill_e, 'e')
        canvas.onkeypress(self.skill_r, 'r')
        canvas.listen()
    
    def skill_q(self):
        new_x = random.randint(-50, 50)
        new_y = random.randint(-50, 50)
        self.setpos(new_x, new_y)

    def skill_w(self):
        old_speed = self.step_move
        self.step_move *=2 
        self.canvas.ontimer(lambda: self.reset_speed(old_speed), 1000)

    def skill_e(self):
        if hasattr(self, "target_runner"):
            angle = self.towards(self.target_runner.pos())
            self.setheading(angle)

    def skill_r(self):
        if hasattr(self, "target_runner"):
            angle = self.towards(self.target_runner.pos())
            self.setheading(angle)
            self.forward(100)

    def reset_speed(self, old_speed):
        self.step_move = old_speed

    def run_ai(self, opp_pos, opp_heading):


        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)


class AutoChaser(turtle.RawTurtle):
    def __init__(self, canvas, step_move=50):
        super().__init__(canvas)
        self.step_move = step_move

    def run_ai(self, opp_pos, opp_heading):
        angle = self.towards(*opp_pos)
        self.setheading(angle)
        self.forward(self.step_move)

if __name__ == '__main__':
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("#429FAD")

    runner = RandomMover(screen)   
    chaser = ManualMover(screen)    
    chaser2 = AutoChaser(screen)    

    game = RunawayGame(screen, runner, chaser, chaser2)
    game.start()
    screen.mainloop()