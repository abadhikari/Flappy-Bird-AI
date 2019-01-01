import tensorflow as tf
from dqn.dueling_network.dueling_dqn import Qnetwork
from dqn.dueling_network.replay import *
from flappy_bird_game.game import gameEnv

# network variables
y = .99
a_size = 2
num_episodes = 25000
pre_train_steps = 15000
h_size = 512
batch_size = 32
update_freq = 4
learning_rate = 0.0001

# Set the rate of random action decrease.
annealing_steps = 10000
startE = 1
endE = 0.01
e = startE
stepDrop = (startE - endE) / annealing_steps

# rate to update target network toward primary network
tau = 0.001

# initialize the tf graph and variables
tf.reset_default_graph()
init = tf.global_variables_initializer()
trainables = tf.trainable_variables()
targetOps = updateTargetGraph(trainables, tau)

# initialize the main and target network along with the experience buffer and the environment
mainQN = Qnetwork(h_size,a_size,learning_rate)
targetQN = Qnetwork(h_size,a_size,learning_rate)
myBuffer = experience_buffer()
env = gameEnv()

# create lists to contain total rewards and steps per episode
rList = []
total_steps = 0

with tf.Session() as sess:
    sess.run(init)
    for i in range(num_episodes):
        episodeBuffer = experience_buffer()

        # reset environment and also get the first observation
        s = env.reset()
        s = processState(s)
        d = False
        rAll = 0

        # go until game_over
        while True:
            # Choose an action greedily, with an e chance of random action, from the Q-network
            if np.random.rand(1) < e or total_steps < pre_train_steps:
                a = np.random.randint(0, a_size)
            else:
                a = sess.run(mainQN.predict, feed_dict={mainQN.scalarInput: [s]})[0]

            # step the environment
            s1, r, d = env.step(a)
            s1 = processState(s1)
            total_steps += 1

            # save the experience to the episode buffer.
            episodeBuffer.add(np.reshape(np.array([s, a, r, s1, d]), [1, 5]))

            # anneal epsilon
            if total_steps > pre_train_steps:
                if e > endE:
                    e -= stepDrop

                # update the networks
                if total_steps % (update_freq) == 0:
                    # get a random batch of experiences
                    trainBatch = myBuffer.sample(batch_size)

                    # perform the Double-DQN update to the target Q-values
                    Q1 = sess.run(mainQN.predict, feed_dict={mainQN.scalarInput: np.vstack(trainBatch[:, 3])})
                    Q2 = sess.run(targetQN.Qout, feed_dict={targetQN.scalarInput: np.vstack(trainBatch[:, 3])})
                    end_multiplier = -(trainBatch[:, 4] - 1)
                    doubleQ = Q2[range(batch_size), Q1]
                    targetQ = trainBatch[:, 2] + (y * doubleQ * end_multiplier)

                    # update the network with the target values
                    _ = sess.run(mainQN.updateModel, \
                                 feed_dict={mainQN.scalarInput: np.vstack(trainBatch[:, 0]), mainQN.targetQ: targetQ,
                                            mainQN.actions: trainBatch[:, 1]})

                    # update the target network toward the primary network.
                    updateTarget(targetOps, sess)
            rAll += r
            s = s1

            # break the loop if gameover
            if d:
                break

        # add buffers to the experience buffer
        myBuffer.add(episodeBuffer.buffer)
        rList.append(rAll)

        # print the mean rewards for the last 10 experiences
        if len(rList) % 10 == 0:
            print(total_steps, np.mean(rList[-10:]), e)
