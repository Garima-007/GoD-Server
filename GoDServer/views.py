from django.http.response import HttpResponse
from django.http import JsonResponse
import uuid

Waiting_Games = {}
Playing_Games = {}

class GameState:
    
    def __init__(self,game_id,game_name,p1_id,p2_id,stack,start_index,end_index,p1_score,p2_score,turn,max_coins,status):
        self.game_id = game_id
        self.game_name = game_name
        self.p1_id = p1_id;
        self.p2_id = p2_id;
        self.stack = stack
        self.coin_stack = generateStackArray(stack)
        self.start_index = start_index
        self.end_index = end_index
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.turn = turn
        self.max_coins = max_coins
        self.status = status	

    def __str__(self):
        return str(self.game_id)+"$$"+str(self.game_name)+"$$"+str(self.p1_id)+"$$"+str(self.p2_id)+"$$"+str(self.coin_stack)+"$$"+\
                    str(self.start_index)+"$$"+str(self.end_index)+"$$"+\
					str(self.p1_score)+"$$"+str(self.p2_score)+"$$"+str(self.turn)+"$$"+str(self.max_coins)+\
					str(self.status)

def generateStackArray(stack):
    string_stack = [x for x in stack.split(',')]
    coin_stack = []
    for coin in string_stack:
        coin_stack.append(int(coin))
    return coin_stack
    
def gameDictionary(game):
    response_data = {}
    response_data['game_id'] = game.game_id
    response_data['game_name'] = game.game_name
    response_data['p1_id'] = game.p1_id
    response_data['p2_id'] = game.p2_id
    response_data['coin_stack'] = game.coin_stack
    response_data['start_index'] = game.start_index
    response_data['end_index'] = game.end_index
    response_data['p1_score'] = game.p1_score
    response_data['p2_score'] = game.p2_score
    response_data['turn'] = game.turn
    response_data['max_coins'] = game.max_coins
    response_data['status'] = game.status
    return response_data

def getGameList(request):
    global Waiting_Games
    response_data = {}
    #test_map(request)                                 #initialisation to be removed later
    for game in Waiting_Games:
        response_data[Waiting_Games[game].game_id] = str(Waiting_Games[game].game_name) + "$" + str(Waiting_Games[game].end_index) 
    return JsonResponse(response_data)

def getGameState(request):
    global Playing_Games
    global Waiting_Games
    #xyz = Waiting_Games
    #test_map(request)                                #initialisation function to be removed later
    game_str = request.GET["game_id"]
    #game = int(game_str)
    if game_str in Playing_Games:
        response_data = gameDictionary(Playing_Games[game_str])
    else:
        #print(str(game))
    #print("#######################################")
    #print("%%%%%%%" + str(xyz[game_str]))
        response_data = gameDictionary(Waiting_Games[game_str])
    return JsonResponse(response_data)
 
def createGame(request):
    global Waiting_Games
    p_id = request.GET["p_id"]
    stack = request.GET["stack"]
    game_name = request.GET["game_name"]
    total_coins = int(request.GET["total_coins"])
    game_id = str(uuid.uuid4().int) #use uuid
    game = GameState(game_id,game_name,p_id,'',stack,1,total_coins,0,0,1,2,1)
    Waiting_Games[game_id] = game
    response_data = gameDictionary(Waiting_Games[game_id])
    return JsonResponse(response_data)

def makeTurn(request):
    #test_map(request)        #initialisation remove later
    global Playing_Games
    game_id = request.GET["game_id"]
    #game_id = int(game)
    p_id = request.GET["p_id"]
    #turn = request.GET["turn"]
    coins_picked = int(request.GET["coins_picked"])
    start = Playing_Games[game_id].start_index
    if p_id == Playing_Games[game_id].p1_id:
        Playing_Games[game_id].turn = 2
        i = 0
        while i < coins_picked:
            Playing_Games[game_id].p1_score += Playing_Games[game_id].coin_stack[start+i-1]
            i += 1
            #print(str(Playing_Games[game_id].p1_score))
    else:
         Playing_Games[game_id].turn = 1
         i = 0
         while i < coins_picked:
            Playing_Games[game_id].p2_score += Playing_Games[game_id].coin_stack[start+i-1]
            i += 1
            #print(str(Playing_Games[game_id].p2_score))
    Playing_Games[game_id].max_coins = 2*coins_picked
    Playing_Games[game_id].start_index += coins_picked
    if Playing_Games[game_id].start_index == Playing_Games[game_id].end_index + 1:
        Playing_Games[game_id].status = 0
    response_data = gameDictionary(Playing_Games[game_id])
    return JsonResponse(response_data)

def joinGame(request):
    global Waiting_Games
    global Playing_Games
    #test_map(request)         #intialisation to be removed later
    game = request.GET["game_id"]
    p2_id = request.GET["p2_id"]
    Waiting_Games[game].p2_id = Waiting_Games[game].p2_id + p2_id
    Waiting_Games[game].status = 2
    Playing_Games[game] = Waiting_Games[game]
    del Waiting_Games[game]
    response_data = gameDictionary(Playing_Games[game])
    return JsonResponse(response_data)

def dropGame(request):
    global Waiting_Games
    game = request.GET["game_id"]
    del Waiting_Games[game]
    return HttpResponse("Deleted!")

def test_map(request):                                #initialisation function to be removed later     
    global Waiting_Games
    global Playing_Games
    Waiting_Games[123] = GameState('123','abc','1','','25,75',1,2,25,50,1,2,1)
    Waiting_Games[234] = GameState('234','defXX','1','','25,75',1,2,25,50,1,2,1)
    Playing_Games[1] = GameState('1','abc','1','2','25,75',1,2,0,0,1,2,2) 
    #return ""
    #return HttpResponse(str(Waiting_Games['123']) + "$$ " + str(Waiting_Games['234']))

def test(request):
    return HttpResponse(request.GET["name"]+str(GameState('123','frw','1','2','25,75',1,2,25,50,1,4,2)))
