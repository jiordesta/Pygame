import sys, pygame, random, os
try:
	import gym
	import numpy as np
	from stable_baselines3 import PPO
	from stable_baselines3.common.env_checker import check_env
except ImportError:
	sys.exit(
		'Please make sure you have all dependencies installed. '
		'Run: "pip3 install numpy gym stable_baselines3"'
	)

RIGHT   = 0
LEFT    = 1
UP      = 2
DOWN    = 3

class GameEnvironment(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(low=0, high=3, shape=(50, 50), dtype=np.int8)#0 - empty | 1 - body | 2 - head | 3 - food
        self.state = np.zeros((50, 50), dtype=np.int8)
        self.done = False

        self.step_count           = 0
        self.__total_reward       = 0

        pygame.init()
        self.width = 500
        self.height = 500
        self.snake_size = [10,10]
        self.food_size = [10,10]
        self.font = pygame.font.SysFont(None, 30)
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((self.width, self.height))

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)

        self.snake_position = [0,0]
        self.snake_direction = 'right'
        self.food_position = [0,0]
        self.score = 0
        self.snake_length = 2
        self.snake_body = []
        
        self.moves = 0
    def reset(self):
        self.done = False
        self.state = []
        self.moves = 0
        self.state = np.zeros((50, 50), dtype=np.int8)

        self.window.fill(self.black)
        self.score = 0
        self.snake_length = 3
        self.snake_position = [250,250]
        self.food_position = [random.randint(1, (self.width/10) - 1) * 10,random.randint(1, (self.height/10) - 1) * 10]
        self.snake_direction = 'right'
        self.snake_body = []

        self.state[int(self.snake_position[0]/10)][int(self.snake_position[1]/10)] = 2
        self.state[int(self.food_position[0]/10)][int(self.food_position[1]/10)] = 3

        return np.array(self.state)
    def render(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if self.snake_length > 0:
            pygame.draw.rect(self.window,self.white,[self.snake_position[0], self.snake_position[1], self.snake_size[0], self.snake_size[1]])
            self.snake_length -= 1
            self.snake_body += [list(self.snake_position)]
        else:
            pygame.draw.rect(self.window,self.black,[self.snake_body[0][0], self.snake_body[0][1], self.snake_size[0], self.snake_size[1]])
            self.snake_body.pop(0)  # remove the oldest element from the list
            pygame.draw.rect(self.window,self.white,[self.snake_position[0], self.snake_position[1], self.snake_size[0], self.snake_size[1]])
            self.snake_body += [list(self.snake_position)]

        if self.snake_position == self.food_position:
            self.score += 1
            self.snake_length += 1
            self.food_position = [random.randint(1, (self.width/10) - 1) * 10,random.randint(1, (self.height/10) - 1) * 10]
        pygame.draw.rect(self.window,self.red,[self.food_position[0], self.food_position[1], self.food_size[0], self.food_size[1]])
        pygame.display.update()
    def rewards(self,action):
        food = self.food_position
        snake = self.snake_position
        reward = -0.5

        if snake in self.snake_body:
            self.done = True
        if snake[0] == self.width or snake[1] == self.height:
            self.done = True
        if snake[0] == -10 or snake[1] == -10:
            self.done = True

        if self.done == True:
            reward -= 1

        if snake == food:
            reward += 1
 
        if snake[0] == food[0]:
            reward +=0.25
        if snake[1] == food[1]:
            reward += 0.25

        if action == RIGHT and (snake[0] < food[0]):
            reward += 0.25
        if action == LEFT and (snake[0] > food[0]):
            reward += 0.25
        if action == UP and (snake[1] > food[1]):
            reward += 0.25
        if action == DOWN and (snake[1] < food[1]):
            reward += 0.25

        return reward
    def step(self, action):
        self.clock.tick(25)
        self.reward = 0
        self.step_count += 1

        if action == RIGHT and self.snake_direction != 'left':
            self.snake_direction = 'right'
        if action == LEFT and self.snake_direction != 'right':
            self.snake_direction = 'left'
        if action == UP and self.snake_direction != 'down':
            self.snake_direction = 'up'
        if action == DOWN and self.snake_direction != 'up':
            self.snake_direction = 'down'

        if self.snake_direction == 'right':
            self.snake_position[0] += 10
        if self.snake_direction == 'left':
            self.snake_position[0] -= 10
        if self.snake_direction == 'up':
            self.snake_position[1] -= 10
        if self.snake_direction == 'down':
            self.snake_position[1] += 10

        self.reward += self.rewards(action)

        head = [self.snake_position[0]/10,self.snake_position[1]/10]
        food = [self.food_position[0]/10,self.food_position[1]/10]

        for x in range(50):
            for y in range(50):
                self.state[x][y] = 0

        self.__total_reward += self.reward

        for body in self.snake_body:
            x = int(body[0]/10)
            y = int(body[1]/10)
            self.state[x][y] = 1


        self.state[int(food[0])][int(food[1])] = 3
        self.state[int(head[0]) - 1][int(head[1]) - 1] = 2
        
        if self.done:
            self.step_count = 0
        self.render()
        return self.state, self.reward, self.done, {}
if __name__ == '__main__':
    models_dir = 'models/PPO'
    logdir = 'logs'

    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    env = GameEnvironment()
    try:
    # Check if the environment is compatible with the PPO algorithm
        check_env(env)
        print("The environment is compatible with the PPO algorithm.")
    except ValueError:
        print("The environment is not compatible with the PPO algorithm.")

    model = PPO('MlpPolicy', env, n_steps=2048, verbose=1, tensorboard_log=logdir)
    #modelPath = f'{models_dir}/275.zip'
    #model = PPO.load(modelPath, env)
    TIMESTEP = 40960
    filenumber = len(os.listdir(models_dir))
    #obs = env.reset()
    #done = False
    #while not done:
    #    action, _ = model.predict(obs)
    #    obs, reward, done, info = env.step(action)
    while True:
        model.learn(total_timesteps=TIMESTEP, reset_num_timesteps=False, tb_log_name='PPO')
        model.save(f"{models_dir}/{filenumber}")
        filenumber = len(os.listdir(models_dir))

