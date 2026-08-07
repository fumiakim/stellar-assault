/* --- ドット絵スプライト定義（art/pixel/ で設計） --- */
const PAL_SHIP = {'3':'#1a2432','2':'#5c7590','1':'#d8e6f2','0':'#ffffff','4':'#2a6fd0','5':'#17427f','6':'#4ff0ff','7':'#ffcf4a'};
const ROWS_SHIP = ['.......11.......','.......11.......','......2112......','......1111......','.....216612.....','.....216612.....','.....211112.....','...2221111222...','..244411114442..','.24444111144442.','.24455111155442.','..22.511115.22..','.....211112.....','.....231132.....','.....273372.....','......7..7......'];
const SP = {};
SP.ship1 = spr(ROWS_SHIP, PAL_SHIP);
SP.ship2 = recolor(ROWS_SHIP, PAL_SHIP, {'4':'#e0741c','5':'#8a3d08','6':'#ffd24a'});
SP.pop = spr(['..........','..caaaac..','.caaaaaac.','caaaddaaac','caabddbaac','.cabbbbac.','..cabbac..','...cbbc...','....cc....','..........'], {'a':'#ff9a5c','b':'#c2551f','c':'#40200f','d':'#ffe6a8','e':'#9fb4c9'});
SP.zig = spr(['............','..ccaaaacc..','.caaaaaaaac.','caaaaddaaaac','caabbddbbaac','caabbddbbaac','c.cabbbbac.c','cc.cabbac.cc','..ccabbacc..','...cabbac...','....cbbc....','.....cc.....'], {'a':'#8affd1','b':'#2c9c76','c':'#0d3328','d':'#eafff6','e':'#9fb4c9'});
SP.dive = spr(['...cc..cc...','..caaaaaac..','.caaaaaaaac.','caaaaddaaaac','caaddddddaac','caaaaddaaaac','caaaabbaaaac','.cabbbbbbac.','..cabbbbac..','...cabbac...','....cbbc....','.....cc.....'], {'a':'#ffd45c','b':'#b8842a','c':'#3d2a08','d':'#fff4c8','e':'#9fb4c9'});
SP.sniper = spr(['.....cc.....','....caac....','...caaaac...','..caaaaaac..','.caaaddaaac.','caaaaddaaaac','caaaabbaaaac','c.caabbaac.c','cc.cabbac.cc','...cabbac...','...ccbbcc...','.....cc.....'], {'a':'#c98aff','b':'#6a3aa8','c':'#251038','d':'#f0dcff','e':'#9fb4c9'});
SP.mine = spr(['..c.cc.c..','..caccac..','.ccaccacc.','ccaaaaaacc','.caaddaac.','.caaddaac.','ccaaaaaacc','.ccaccacc.','..caccac..','..c.cc.c..'], {'a':'#ffe066','b':'#a87f18','c':'#3a2c05','d':'#ff6a3b','e':'#9fb4c9'});
SP.turret = spr(['....cc..cc....','..cceeeeeecc..','.ceeeeeeeeeec.','.ceeaaaaaaeec.','ceeaaaaaaaaeec','ceaaaddddaaaec','ceaaddddddaaec','ceaaddddddaaec','ceaaaaddaaaaec','ceeaaaaaaaaeec','.ceeaaaaaaeec.','.cceeeeeeeecc.','..cceeeeeecc..','....cc..cc....'], {'a':'#9fd8ff','b':'#3f6f96','c':'#10202e','d':'#ffe066','e':'#7f9bb5'});
SP.carrier = spr(['...cccccccccccccc...','..ceeeeeeeeeeeeeec..','.ceeaaaaaaaaaaaaeec.','ceeaaaaaaaaaaaaaaeec','ceaaaddaaaaaaddaaaec','ceaaaddaaaaaaddaaaec','ceaaaaaaaaaaaaaaaaec','ceaabbbbaaaabbbbaaec','ceaabbbbaaaabbbbaaec','ceaaaaaaaaaaaaaaaaec','ceaaddddaaaaddddaaec','ceaaaaaaaaaaaaaaaaec','.ceeaaaaaaaaaaaaeec.','..cceeeeeeeeeeeecc..','...cccccccccccccc...','.....cccccccccc.....'], {'a':'#7fa8ff','b':'#2b4f96','c':'#0c1830','d':'#ffd166','e':'#5c78a8'});
SP.heavy = spr(['.....cccccccc.....','...cceeeeeeeecc...','..ceeaaaaaaaaeec..','.ceaaaaaaaaaaaaec.','ceaaaaddddddaaaaec','ceaaaaddddddaaaaec','ceaaaaaaaaaaaaaaec','ceaabbbbaabbbbaaec','ceaabbbbaabbbbaaec','ceaaaaaaaaaaaaaaec','.ceaaddaaaaddaaec.','.ceaaddaaaaddaaec.','..cceaaaaaaaaecc..','...cceeaaaaeecc...','.....cceeeecc.....','.......cccc.......'], {'a':'#ff8fa8','b':'#a03c58','c':'#340f1c','d':'#fff0a8','e':'#c26a7c'});
// 被弾時に光らせる白抜き版
for (const k in SP) SP[k + 'W'] = whiteOf(SP[k]);
