import tester


def getGameURL():
    game2_file = open("game2.txt", "r")
    game2_url = game2_file.read()
    game2_file.close()
    new_url = tester.getPushURL(game2_url)
    return new_url