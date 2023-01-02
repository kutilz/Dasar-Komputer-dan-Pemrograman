import time
import pygame
import re
import os
from pygame.locals import *


#pertama kita baca file .osu, di dalam file pada bagian [HitObjects] terdapat informasi
#yang bisa kita gunakan untuk membuat note. kita bisa lihat formatnya dari sini:
# https://osu.ppy.sh/wiki/en/Client/File_formats/Osu_%28file_format%29



file1=open("wo.osu","r",)
reg = re.compile("\[(.*)\]")
Lines = file1.readlines()
hit = False
ln_ms = [[], [], [], []]   #ini akan berisi long note, long note adalah note yang panjang yang harus kita klik sampai kotak note nya habis
note_ms = [[], [], [], []] #ini akan berisi note biasa yang cukup kita klik 1x
                           #dalam format file ini terdapat satuan milidetik yang akan kita append ke 2 variabel list tadi
                           #misal di note_me terdapat angka 200, maka akan muncul sebuah note di 200 milidetik setelah lagu dimulai
                           #dan misal ada [200,300] di ln_ms maka kita harus menekan tombol dari 200 sampai 300 milidetik semenjak lagu dimulai
                           #note_ms dan ln_ms berisi 4 list yang berarti list pertama untuk lane 1, kedua untuk lane 2, dan seterusnya.
score = 0
a = 0
length = 0
dis = 0

for line in Lines:

    if hit:#disini karena hit masih false maka tidak akan berjalan dulu(lanjut di line 55)
        line = line.split(",")[:-1] + [line.split(",")[5].split(":")[0]]
        if int(line[3]) == 128:
            length = int(line[5])
            if int(line[0]) == 64:
                ln_ms[0].append([int(line[2]), int(line[5])])
            elif int(line[0]) == 192:
                ln_ms[1].append([int(line[2]), int(line[5])])
            elif int(line[0]) == 320:
                ln_ms[2].append([int(line[2]), int(line[5])])
            elif int(line[0]) == 448:
                ln_ms[3].append([int(line[2]), int(line[5])])

        else:
            length = int(line[2])
        if int(line[0]) == 64:
            note_ms[0].append(int(line[2]))
        elif int(line[0]) == 192:
            note_ms[1].append(int(line[2]))
        elif int(line[0]) == 320:
            note_ms[2].append(int(line[2]))
        elif int(line[0]) == 448:
            note_ms[3].append(int(line[2]))
    else:#sampai line yang terbaca adalah ["HitObjects"], lalu kita olah data srting tersebut dan masukkan nilai yang ada sesuai format
        if reg.findall(line) == ["HitObjects"]:
            hit = True
#print(note_ms[2])
yes=False
for line in Lines:
        if "AudioFilename" in line: #AudioFilename akan digunakan untuk mendapatkan nama lagu yang akan di play
            nameSong = line.split(":")[1].strip()
        if "[Events]" in line:
            yes = True
        elif yes and line[:2] != "//":
            try:
                temp = int(line.split(",")[0])
                bg = line.split(",")[2][1:-1]
            except:
                pass
            try:
                if bg:
                    pass
            except:
                break
        if "TimingPoints" in line:
            yes = False
