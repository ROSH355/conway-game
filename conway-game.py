import pygame
import random

pygame.init()                   #initialise module

BLACK=(0,0,0)                   #this value can range from 0 to 255(red,green,blue)
GREY=(128,128,128)
YELLOW=(255,255,0)

#GRID DIMENSION
WIDTH,HEIGHT=600,600
TILE_SIZE=20                    #20 PIXEL BY 20 PIXEL
GRID_WIDTH=WIDTH//TILE_SIZE     #NO OF TILES
GRID_HEIGHT=HEIGHT//TILE_SIZE   #BASED ON PIXELS
FPS=60                          #60 times per second

screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock()

def draw_grid(positions):       #we r going to check only the alive cell and its neighbour,set-updation is easier no need to go thro each grid
    for position in positions:
        col,row=position
        #we r gonna draw rectangle in top left corner of a cell
        top_left=(col*TILE_SIZE,row*TILE_SIZE)                          #just a starting point in a cell
        pygame.draw.rect(screen,YELLOW,(*top_left,TILE_SIZE,TILE_SIZE)) #unpacking tuple ,(length,breadth,height)
    #gonna draw grid line
    for row in range(GRID_HEIGHT):#(horiz line)
        pygame.draw.line(screen,BLACK,(0,row*TILE_SIZE),(WIDTH,row*TILE_SIZE))  #line on the screen,color of th eline,start pos,end pos
    for col in range(GRID_WIDTH):#(vertical line)
        pygame.draw.line(screen,BLACK,(col*TILE_SIZE,0),(col*TILE_SIZE,HEIGHT)) #y coord constant=0

def gen(num):
    return set([(random.randrange(0,GRID_HEIGHT),random.randrange(0,GRID_WIDTH)) for _ in range(num)])     #random genertaion shld not overlap -so set is used

def adjust_grid(positions):
    #loop only thro live cells
    all_neighbors=set()                 #any cell with atleast one live neigh 
    new_positions=set()                 #cells for next round ,ensure update not in same set
    
    #check if we need to keep the exisiting cell
    for position in positions:
        neighbors=get_neighbors(position)
        all_neighbors.update(neighbors)
        #to check neigh live cell or not
        neighbors=list(filter(lambda x: x in positions,neighbors)) #if x in position(live cell) keep it in filter ,#filter gives us iterator so we make it into list 

        if len(neighbors) in [2,3]:
            new_positions.add(position)                            #we vl keep it for nxt round
    
    #to create or come alive
    for position in all_neighbors:
        neighbors=get_neighbors(position)
        neighbors=list(filter(lambda x: x in positions,neighbors))
        if len(neighbors)==3:
            new_positions.add(position)
    return new_positions

def get_neighbors(pos): #we hv 8 neigh for a cell
    x,y=pos
    neighbors=[]
    for dx in [-1,0,1]:
        if x+dx < 0 or x+dx > GRID_WIDTH:
            continue
        for dy in [-1,0,1]:
            if y+dy < 0 or y+dy > GRID_HEIGHT:
                continue
            if dx==0 and dy==0:
                continue #no movement,curr_pos
            neighbors.append((x+dx,y+dy))
    return neighbors

def main():
    running=True
    positions=set()
    playing=False
    count=0
    update_freq=120
    while running:

        clock.tick(FPS)

        if playing:         # im in active or play simulation
            count+=1        #max fps ie for every sec count goes 60 times
        
        if count>=update_freq:
            count=0                             #reset the count
            positions=adjust_grid(positions)    # i want new pos
        
        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get(): #loop thro event to check if player quits the game
            if event.type==pygame.QUIT:
                running =False           #stop the loop

            if event.type==pygame.MOUSEBUTTONDOWN: #to click n add positions
                x,y=pygame.mouse.get_pos()
                col=x//TILE_SIZE
                row=y//TILE_SIZE
                pos=(col,row)
                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)
            
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:   #pause or playing simulation with space bar
                        playing = not playing   #toggle the current playing state
        
                if event.key==pygame.K_c:       #clear screen ,pause simulation
                    positions=set()
                    playing= False
                    count=0

                if event.key==pygame.K_g:
                    positions=gen(random.randrange(4,10)*GRID_WIDTH)      #generate random pos by clicking G
        
        screen.fill(GREY)           #background screen color
        draw_grid(positions)
        pygame.display.update()     #update the display
    pygame.quit()                   #stop the game
             
if __name__=="__main__":
    main()