import time
import boardgeneration

board = boardgeneration.DepBoard("underground")

while True:
    pltfrms = board.sanitise_data()
    # print(pltfrms)
    for i in range(len(pltfrms)):
        url = "https://api.tfl.gov.uk/StopPoint/"+pltfrms[i][0]+"/arrivals"
        print("\n\n-------------------------------------------------------\n\n")
        print("Station ID:", pltfrms[i][0])
        print("Station name:", pltfrms[i][1])
        for j in range(len(pltfrms[i][2])):
            board.departure_board_create(pltfrms[i][1], pltfrms[i][2][j][1], pltfrms[i][2][j][0], url)
            print("\n\n\n\n")
            time.sleep(10)