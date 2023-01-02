import pygame
import time
import fileRead
from pygame.locals import *
# memulai pygame
pygame.init()
pygame.mixer.init()

keybind=[
    pygame.K_s,#set key apa saja yang akan dipanggil nanti untuk bermain
    pygame.K_d,
    pygame.K_k,
    pygame.K_l
]
#set ukuran layar game
height = 1366
width = 768
screen = pygame.display.set_mode((height,width),pygame.FULLSCREEN)

clock=pygame.time.Clock()

light = pygame.image.load(".\\resources\\light.png")
x_lane=(401,502,603,704)#ini adalah posisi x untul lane 1-4
skin_lane=(#ini akan load gambar .png yang nanti akan dipakai, untuk gambar kita ambil dari google
    pygame.image.load(".\\resources\\note1.png"),
    pygame.image.load(".\\resources\\note2.png"),
    pygame.image.load(".\\resources\\note2.png"),
    pygame.image.load(".\\resources\\note1.png")
)
skin_Longlane=(
    pygame.image.load(".\\resources\\LNhead1.png"),
    pygame.image.load(".\\resources\\LNhead2.png"),
    pygame.image.load(".\\resources\\LNhead2.png"),
    pygame.image.load(".\\resources\\LNhead1.png")
)
skin_LongTail=(
    pygame.image.load(".\\resources\\LNtail1.png"),
    pygame.image.load(".\\resources\\LNtail2.png"),
    pygame.image.load(".\\resources\\LNtail2.png"),
    pygame.image.load(".\\resources\\LNtail1.png")
)
#di versi kedua kita convert ln_ms dan note_ms di fileRead ke tuple karena setelah kami uji coba,
#tuple ternyata lebih cepat dioperasikan dibanding list
notes=tuple(
    tuple(note
    ) for note in fileRead.note_ms
)
longNotes=tuple(
    tuple(
        tuple(
            mss
            ) for mss in tuple(lanes)
        ) for lanes in fileRead.ln_ms
)
tuple_notes=(notes,longNotes)
notes=fileRead.note_ms
longNotes=fileRead.ln_ms
judgementValue=(#ini akan digunakan untuk judgement nanti 
    16.5,#maksudnya apabila player mengklik lebih atau kurang 16.5 ms maka akan keluar judge "EXCELLENT"
    43.5,#sama aja tapi untuk "PERFECT"
    76.5,#"GREAT"
    106.6,#dan seterusnya
    130.5
)
# judgement={
#     excellent:  pygame.transform.scale(pygame.image.load(".\\resources\\excellent.png"),(256,72)),
#     perfect:    pygame.transform.scale(pygame.image.load(".\\resources\\perfect.png"),(256,72)),
#     great:      pygame.transform.scale(pygame.image.load(".\\resources\\great.png"),(256,72)),
#     good:       pygame.transform.scale(pygame.image.load(".\\resources\\good.png"),(256,72)),
#     bad:        pygame.transform.scale(pygame.image.load(".\\resources\\bad.png"),(256,72)),
#     miss:       pygame.transform.scale(pygame.image.load(".\\resources\\miss.png"),(256,72))
# }
#variabel ini untuk menghitung FPS dan mengatur kecepatan scroll
# https://osu.ppy.sh/community/forums/topics/976158?n=1
#bisa dilihat dari sini kecepatan scroll adalah misal scroll = 1000 (ms) maka 
#kecepatan note jatuh dari atas ke bawah sama dengan 1 detik
fifty=-50
fps=0
sedetik=1000
scroll=508
ukurany=768
stageHint=635
efpees=int()
t=True
running = True
music="audio.mp3"
ybelum=-50

def background():#ini akan membuat background dari lane 1-4
    stg = pygame.image.load(".\\resources\\stageHint.png")
    scorebar = pygame.transform.rotate(pygame.image.load(".\\resources\\scorebar.png"),-90)
    screen.blit(pygame.transform.scale(stg,(403,128)),(401,stageHint))
    pygame.draw.rect(screen,(255,255,255),pygame.Rect(401,stageHint+64,403,1))

def click():#fungsi click ini dipakai ketika player menekan keyboard, lane1pressed didapat dari operasi pada fungsi pressed dan unpressed
    press = pygame.key.get_pressed()
    light = pygame.image.load(".\\resources\\light.png")
    lighty=365
    if lane1pressed:
        screen.blit(pygame.transform.scale(light,(100,320)),(401,lighty))
    if lane2pressed:
        screen.blit(pygame.transform.scale(light,(100,320)),(502,lighty))
    if lane3pressed:
        screen.blit(pygame.transform.scale(light,(100,320)),(603,lighty))
    if lane4pressed:
        screen.blit(pygame.transform.scale(light,(100,320)),(704,lighty))
def noteColumn(scroll,ukurany,pengurang):
    for i in range(0,4):
        for note in notes[i]:
            ye=(ukurany/scroll)*note #fungsi ini adalah kunci dari permainan. ini akan membaca tuple tadi yang dari milidetik
                                     #yang kita convert ke satuan koordinat pixel agar bisa terbaca oleh pygame
                                     #caranya dalam 1 loop kita dapatkan posisi lagu yang dimainkan dan kita ambil variable note dan ln
                                     #lalu variabel tersebut kita hitung dengan variabel scroll. karena diketahui lebar posisi y adalah 700
                                     #dan scroll adalah 508, maka setiap loop akan mencari posisi lagu dan menghitung (misal panjang lagu adalah 2032 ms)
                                     #maka diketahui akan ada 4x scroll dalam 1 lagu tersebut. nah setiap loop nanti menghitung posisi lagu sudah sampai mana
                                     #dan mengconvert posisi y dari note dengan dibandingkan ke variabel scroll
                                     #sehingga di setiap loop karena waktu terus berjalan maka posisi y note pun akan bertambah ke bawah
                                     #yang menciptakan ilusi note tersebut "jatuh" di mata kita, padahal hanya berkurang posisi y nya saja
            yekeatas=50-ye
            #print(yekeatas)
            yeberjalan=yekeatas+pengurang
            if yeberjalan >= -50 and yeberjalan < ukurany:
                screen.blit(pygame.transform.scale(skin_lane[i],(100,50)),(x_lane[i],yeberjalan))
        for longNote in longNotes[i]:
            longNote_y=(ukurany/scroll)*longNote[0]
            longTail_y=(ukurany/scroll)*longNote[1]

            longNote_ykeatas=50-longNote_y
            longTail_ykeatas=50-longTail_y

            longNote_yBerjalan=longNote_ykeatas+pengurang
            longTail_yBerjalan=longTail_ykeatas+pengurang

            tail_y=longTail_yBerjalan+25
            panjangTail=longNote_yBerjalan - tail_y

            # if longNote_yBerjalan >=-50 and longNote_yBerjalan <ukurany+panjangTail:
            #     screen.blit(pygame.transform.scale(skin_LongTail[i],(100,panjangTail)),(x_lane[i],longNote_yBerjalan-panjangTail))
            if longNote_yBerjalan >=-50 and longNote_yBerjalan <ukurany+panjangTail:
                screen.blit(pygame.transform.scale(skin_Longlane[i],(100,50)),(x_lane[i],longNote_yBerjalan))
            if longTail_yBerjalan >=-50-panjangTail and longTail_yBerjalan < ukurany:
                screen.blit(pygame.transform.scale(skin_LongTail[i],(100,panjangTail)),(x_lane[i],tail_y))
def pressed():#ini akan mendapatkan setiap kali player menekan keyboard maka akan mengubah variabel menjadi true
    global lane1pressed,lane2pressed,lane3pressed,lane4pressed
    if event.key == pygame.K_s:
        lane1pressed=True
        time_s=pygame.mixer.music.get_pos()
        
    if event.key == pygame.K_d:
        lane2pressed=True
    if event.key == pygame.K_k:
        lane3pressed=True
    if event.key == pygame.K_l:
        lane4pressed=True
def unpressed():#dan ini kebalikan dari fungsi pressed
    global lane1pressed,lane2pressed,lane3pressed,lane4pressed
    if event.key == pygame.K_s:
        lane1pressed=False
    if event.key == pygame.K_d:
        lane2pressed=False
    if event.key == pygame.K_k:
        lane3pressed=False
    if event.key == pygame.K_l:
        lane4pressed=False

lane1pressed=False
lane2pressed=False
lane3pressed=False
lane4pressed=False
pygame.mixer.music.load(music)
pygame.mixer.music.play()
press = pygame.key.get_pressed()
timeawal=pygame.mixer.music.get_pos()
length=pygame.mixer.Sound(music).get_length()*1000
length_y=(length/scroll)*ukurany
print(length_y)
timstart=pygame.mixer.music.get_pos()
while running:
    #loop
    screen.fill((0, 0, 0))
    tim=time.time()*1000-timstart

    for event in pygame.event.get():
        #click()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running=False
            pressed()
        if event.type == pygame.KEYUP:
            unpressed()
    click()
    timstart=pygame.mixer.music.get_pos()

    efpees=pygame.mixer.music.get_pos()-timeawal
    if efpees>=sedetik:#ini akan menghitung fps dengan menggunakan posisi waktu lagu
                       #jadi sambil while loop berjalan apabila waktu belum 1 detik 
                       #akan menghitung berapa kali while yang sudah dijalankan
                       #dan apabila sudah 1 detik akan print berapa banyak fps dan akan mereset variabel fps dan variabel waktu
        efpees-=efpees
        timeawal=pygame.mixer.music.get_pos()
        print(fps)
        fps=0

    fps+=1
    
    ypos=(ukurany/scroll)*timstart
    yselisih=(ypos-50)-ybelum
    ybelum=ypos+(ukurany-50)
    background()

    noteColumn(scroll,ukurany,ybelum)
    fifty+=yselisih
    pygame.display.update()







pygame.quit()