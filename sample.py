from pybot import robot


@robot.hear(r"^badger$")
def badger(res):
    res.send("thangs")


@robot.respond("say hi")
def say_hi(res):
    res.reply("hello")


@robot.hear(r"open the (.*?) doors")
def open_pod_bay_doors(res):
    door_type = res.match.group(1)
    if door_type == 'pod bay':
        res.reply("I'm afraid I can't let you do that")
    else:
        res.reply("Opening {} doors".format(door_type))


@robot.on('connected')
def on_connected(data):
    robot.send('shell', "I am here world")


if __name__ == '__main__':
    robot.run()
