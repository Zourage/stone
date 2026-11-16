import re,sys
D='<workdir>/lang/'
# gloss|type|tr|noun|adj|def   grouped by field
R={}
R['nature']='''
world|T|0||||the earth and all on it
land|T|0||||ground, dry land, territory
soil|T|0||||earth as material in which plants grow
dust|T|0||dusty||
mud|T|0||muddy||
sand|T|0||sandy||
mountain|T|0||||mountain or hill
valley|T|0||||
island|T|0||||
shore|T|0||||coast, beach, bank: land beside water
cave|T|0||||
water|T|0||||
sea|T|0||marine||sea or ocean
lake|T|0||||lake or pond
river|T|0||||river or stream
wave|T|0||||moving ridge on water
stone|T|0||||stone or rock, piece or material
sky|T|0||||
sun|T|0||solar||
moon|T|0||lunar||
star|T|0||||
lightning|T|0||||
thunder|T|0||||
storm|T|0||stormy||
light|T|0||||illumination, what makes things visible
shadow|T|0||||shadow or shade
air|T|0||||
wind|T|0||windy||
cloud|T|0||cloudy||
fog|T|0||foggy||fog or mist
rain|T|0||rainy||
snow|T|0||snowy||
ice|T|0||icy||
weather|T|0||||
fire|T|0||||
smoke|T|0||smoky||smoke from burning
ash|T|0||||
steam|T|0||||steam or vapour
burn|E|1|burning|burning||be on fire, be consumed by fire
freeze|E|1|freezing|frozen||turn to ice or solid from cold
blow|E|0|blowing|||of air or wind: move as a current
flood|T|0||||overflow of water onto land
desert|T|0||||dry barren region
nature|T|0||natural||the non-human-made world
metal|T|0||metallic||
iron|T|0||||iron or steel
gold|T|0||golden||
silver|T|0||||the metal
glass|T|0||||the material
plastic|T|0||||the material
wood|T|0||wooden||the material of trees
coal|T|0||||coal or charcoal
oil|T|0||oily||oil, for food, fuel or lubrication
fuel|T|0||||what is burned for heat or power
salt|T|0||salty||
'''
R['animal']='''
animal|T|0||||
male|Q|0|||
female|Q|0|||
wild|Q|0|wildness|||not tamed or cultivated
cow|T|0||||bovine of either sex
sheep|T|0||||
pig|T|0||||
goat|T|0||||
horse|T|0||||
chicken|T|0||||
duck|T|0||||the water bird
bird|T|0||||
nest|T|0||||
dog|T|0||||
cat|T|0||||
rabbit|T|0||||rabbit or hare
mouse|T|0||||mouse or rat
fish|T|0||||
shell|T|0||||hard outer covering of animal, egg or nut
whale|T|0||||
wolf|T|0||||
lion|T|0||||
tiger|T|0||||
bear|T|0||||the animal
fox|T|0||||
deer|T|0||||
monkey|T|0||||monkey or ape
elephant|T|0||||
insect|T|0||||insect or similar small crawling creature
ant|T|0||||
spider|T|0||||
bee|T|0||||bee or wasp
housefly|T|0||||fly: the insect
mosquito|T|0||||
worm|T|0||||
snake|T|0||||
butterfly|T|0||||butterfly or moth
frog|T|0||||
turtle|T|0||||turtle or tortoise
'''
R['body']='''
body|T|0||bodily||body of a person or animal
skin|T|0||||skin, hide, or peel-like outer layer
hair|T|0||hairy||hair or fur
beard|T|0||||
blood|T|0||bloody||
bone|T|0||||
muscle|T|0||muscular||
joint|T|0||||place where two bones meet
horn|T|0||||horn of an animal
tail|T|0||||
wing|T|0||||
feather|T|0||||
back|T|0||||rear of the trunk of the body
head|T|0||||the body part
brain|T|0||||
face|T|0||facial||front of the head
cheek|T|0||||
chin|T|0||||chin or jaw
eye|T|0||||
ear|T|0||||
nose|T|0||nasal||
mouth|T|0||oral||
lip|T|0||||
tongue|T|0||||the organ in the mouth
tooth|T|0||dental||
neck|T|0||||
throat|T|0||||
shoulder|T|0||||
arm|T|0||||upper limb
elbow|T|0||||
hand|T|0||manual||
finger|T|0||||
nail|T|0||||fingernail, toenail or claw
leg|T|0||||lower limb
knee|T|0||||
foot|T|0||||the body part
toe|T|0||||
chest|T|0||||front of the upper trunk
breast|T|0||||
heart|T|0||cardiac||the organ
lung|T|0||||
liver|T|0||||
stomach|T|0||||the digestive organ
belly|T|0||||abdomen, front of the lower trunk
gut|T|0||intestinal||intestines
hip|T|0||||hip or waist
buttock|T|0||||
womb|T|0||||
penis|T|0||||
vagina|T|0||||
tear|T|0||||drop of liquid from the eye
fat|T|0||||fat or grease, in bodies or food
breathe|A|0|breathing|||
cough|A|0||||
sneeze|A|0||||
sweat|A|0||sweaty||
spit|A|0|spitting|||
vomit|A|1|vomiting|||
urinate|A|0|urination|||
defecate|A|0|defecation|||
bite|A|1||||
lick|A|1||||
chew|A|1|chewing|||
swallow|A|1|swallowing|||take down the throat
suck|A|1|sucking|||
scratch|A|1||||rub or mark with nails or something sharp
sleep|A|0||sleeping||
dream|A|1||||have a dream while asleep
rest|A|0||||stop activity in order to recover
sex|A|0||sexual||have sexual intercourse
born|E|0|birth|||come out of the womb, begin life
pregnant|Q|0|pregnancy|||
grow|E|1|growth|growing||of living things: develop, get bigger
alive|Q|0|life|living||
die|E|1|death|dying||
bury|A|1|burial|||put a dead body or object under the ground
strong|Q|0|strength|||having bodily or physical power
healthy|Q|0|health|||
disease|T|0||||a particular illness
fever|T|0||||
wound|T|0||||injury to the body
swell|E|0|swelling|swollen||
itch|E|0||itchy||
heal|E|1|healing|||become healthy or whole again
poison|T|0||poisonous||
tired|Q|0|tiredness|||
drunk|Q|0|drunkenness|||affected by alcohol
naked|Q|0|nakedness|||
wash|A|1|washing|||clean with water; bathe
'''
R['food']='''
eat|A|1|eating|||
drink|A|1|drinking|||
hungry|Q|0|hunger|||
thirsty|Q|0|thirst|||
cook|A|1|cooking|cooking||prepare food, especially with heat
raw|Q|0|rawness|||not cooked or processed
ripe|Q|0|ripeness|||
fresh|Q|0|freshness|||of food: recently made or picked, not spoiled
rot|E|0||rotten||decay, spoil
boil|E|1|boiling|boiling||of liquid: bubble from heat; be cooked in it
fry|A|1|frying|||cook in hot oil or fat
bake|A|1|baking|||cook by dry heat: bake, roast, grill
peel|A|1|peeling|||remove the skin or outer layer
mix|A|1|mixing|||combine or stir together
grind|A|1|grinding|||crush to powder or small bits
meal|T|0||||occasion of eating; the food served at it
pot|T|0||||deep vessel for cooking or storing
pan|T|0||||shallow cooking vessel
plate|T|0||||flat dish to eat from
bowl|T|0||||
cup|T|0||||cup, mug or drinking glass
bottle|T|0||||
spoon|T|0||||
fork|T|0||||eating fork, or pronged tool
bread|T|0||||
meat|T|0||||flesh, especially as food
soup|T|0||||
sauce|T|0||||
vegetable|T|0||||
fruit|T|0||||
grain|T|0||||cereal seed; cereals
rice|T|0||||
wheat|T|0||||
corn|T|0||||maize
noodle|T|0||||noodles or pasta
bean|T|0||||bean, pea or lentil
potato|T|0||||
tomato|T|0||||
onion|T|0||||
garlic|T|0||||
apple|T|0||||
banana|T|0||||
citrus|T|0||||orange, lemon and similar fruit
grape|T|0||||
nut|T|0||||edible hard-shelled seed
egg|T|0||||
milk|T|0||||
cheese|T|0||||
butter|T|0||||
honey|T|0||||
sugar|T|0||||
pepper|T|0||||the pungent spice; also chili
spice|T|0||||flavouring from plants, spice or herb
cake|T|0||||sweet baked food
chocolate|T|0||||
juice|T|0||||liquid pressed from fruit or plants
tea|T|0||||
coffee|T|0||||
alcohol|T|0||alcoholic||
wine|T|0||||
beer|T|0||||
tobacco|T|0||||
'''
R['clothing']='''
wear|A|1|wearing|||have or put on the body as clothing
cloth|T|0||||woven material, fabric
wool|T|0||woolen||
cotton|T|0||||
leather|T|0||||
weave|A|1|weaving|||make cloth from threads; also knit
sew|A|1|sewing|||
needle|T|0||||
thread|T|0||||thin strand for sewing; string
coat|T|0||||outer garment: coat or jacket
dress|T|0||||one-piece garment with a skirt
shirt|T|0||||garment for the upper body
skirt|T|0||||
trousers|T|0||||
sock|T|0||||
shoe|T|0||||shoe or boot
hat|T|0||||hat or cap
belt|T|0||||
glove|T|0||||
pocket|T|0||||
button|T|0||||fastener on clothing; also press-button
jewel|T|0||||ornament worn on the body; jewelry
ring|T|0||||band worn on a finger; ring-shaped object
towel|T|0||||
comb|T|0||||
brush|T|0||||
shave|A|1|shaving|||
soap|T|0||||
mirror|T|0||||
clean|Q|0|cleanliness|||free of dirt
'''
R['house']='''
dwell|A|0|residence|residential||live in a place, have one's home there
house|T|0||||
tent|T|0||||
yard|T|0||||enclosed ground beside a house; courtyard
room|T|0||||walled part of a building
door|T|0||||door or gate
lock|A|1|locking|||fasten so that only a key opens it
key|T|0||||thing that opens a lock
window|T|0||||
floor|T|0||||bottom surface of a room; storey
wall|T|0||||
roof|T|0||||
stair|T|0||||step, stairs
ladder|T|0||||
stove|T|0||||device giving heat for cooking or warmth
bed|T|0||||
pillow|T|0||||pillow or cushion
blanket|T|0||||
chair|T|0||||seat: chair, bench, stool
table|T|0||||the piece of furniture
shelf|T|0||||shelf; cupboard
furniture|T|0||||
lamp|T|0||||lamp, torch, light fixture
candle|T|0||||
carpet|T|0||||carpet, rug or mat
curtain|T|0||||
toilet|T|0||||
tube|T|0||tubular||pipe, tube, hose
pole|T|0||||post, pole, pillar, beam
board|T|0||||flat piece of wood: plank, panel
brick|T|0||||
bucket|T|0||||
box|T|0||||
bag|T|0||||bag or sack
basket|T|0||||
sweep|A|1|sweeping|||clean a floor with a broom
garbage|T|0||||rubbish, waste thrown away
'''
R['farming']='''
farm|A|1|farming|agricultural||cultivate land, raise crops or animals
field|T|0||||piece of open farmland
garden|T|0||||
fence|T|0||||
plow|A|1|plowing|||
dig|A|1|digging|||
sow|A|1|sowing|||put seeds or young plants in the ground
harvest|A|1||||gather a crop: reap, mow, pick
plant|T|0||||living vegetable organism
seed|T|0||||
tree|T|0||||
bush|T|0||||shrub
grass|T|0||grassy||
weed|T|0||||unwanted plant
root|T|0||||underground part of a plant
stem|T|0||||stem, stalk or trunk of a plant
branch|T|0||||
stick|T|0||||thin detached piece of wood
leaf|T|0||||
flower|T|0||floral||
thorn|T|0||||
mushroom|T|0||||mushroom or fungus
'''
DER='''
light|opp|dark|absence of light
burn|+agent|ignite|set on fire
burn|opp|extinguish|put out a fire
burn|able|flammable|
burn|made|ember|
freeze|opp|melt|
freeze|tool|freezer|
fire|place|fireplace|
tree|group|forest|woods
mountain|group|mountain range|
island|group|archipelago|
star|group|constellation|
plant|group|vegetation|
leaf|group|foliage|
flower|group|bouquet|
bone|group|skeleton|
stair|group|staircase|
animal|group|herd|
bird|group|flock|
bee|place|beehive|
horse|place|stable|
horse|doer|rider|
sheep|doer|shepherd|
fish|doer|fisherman|
wild|opp|tame|domesticated
sleep|opp|wake|
sleep|place|bedroom|
alive|opp|dead|
alive|ness|life|
die|+agent|kill|
die|able|mortal|
born|+agent|bear|give birth to
born|place|birthplace|
bury|place|grave|
strong|opp|weak|
strong|ness|strength|
healthy|opp|sick|ill
healthy|ness|health|
heal|+agent|cure|
heal|doer|doctor|
heal|tool|medicine|
heal|place|hospital|
heal|able|curable|
drunk|opp|sober|
grow|+agent|raise|grow crops, rear animals or children
grow|opp|shrink|
tooth|doer|dentist|
wash|place|bathroom|
wash|able|washable|
urinate|made|urine|
defecate|made|feces|
spit|made|saliva|
breathe|made|breath|
vomit|made|vomit|
scratch|made|scratch|
swell|made|lump|
eat|made|food|
eat|able|edible|
eat|place|dining room|
drink|made|beverage|a drink
drink|able|drinkable|
hungry|opp|full|having eaten enough
hungry|ness|hunger|
cook|doer|cook|person who cooks
cook|place|kitchen|
cook|made|dish|prepared food
raw|opp|cooked|
ripe|opp|unripe|
fresh|opp|stale|
rot|able|perishable|
boil|+agent|boil|
boil|tool|kettle|
bake|doer|baker|
bake|place|bakery|
bake|tool|oven|
grind|made|flour|
grind|tool|mill|
mix|made|mixture|
mix|tool|mixer|
peel|made|peel|
meat|doer|butcher|
meal|place|restaurant|
coffee|place|cafe|
grape|place|vineyard|
fruit|place|orchard|
wear|made|clothes|clothing, garment
wear|opp|undress|take off
sew|doer|tailor|
weave|tool|loom|
shave|tool|razor|
shave|doer|barber|
shoe|doer|shoemaker|
jewel|doer|jeweler|
clean|opp|dirty|
clean|doer|cleaner|
clean|ness|cleanliness|
sweep|tool|broom|
garbage|place|dump|
dwell|place|home|
dwell|doer|resident|
dwell|able|habitable|
lock|opp|unlock|
lock|tool|lock|the device
brick|doer|mason|
wood|doer|carpenter|
metal|doer|smith|
farm|doer|farmer|
farm|place|farm|
farm|made|crop|
farm|ness|agriculture|
garden|doer|gardener|
dig|tool|shovel|spade
dig|made|hole|pit
plow|tool|plow|
harvest|made|yield|the harvested crop
grass|place|meadow|lawn, pasture
'''
rows=[];seen=set();ok=True
for f,blk in R.items():
    for l in blk.strip().split('\n'):
        p=l.split('|')
        if len(p)==6: p.append('')
        if len(p)!=7: print('BAD',l);ok=False;continue
        g,t,tr,noun,adj,rel,d=p
        rows.append([g,t,tr,noun,adj,rel,f,d])
open(D+'lex_A.tsv','w').write(''.join('\t'.join(r)+'\n' for r in rows))
open(D+'der_A.tsv','w').write(''.join('\t'.join(l.split('|'))+'\n' for l in DER.strip().split('\n')))
# validate from files
gl=[]
for i,l in enumerate(open(D+'lex_A.tsv')):
    c=l.rstrip('\n').split('\t')
    if len(c)!=8: print('cols',i,l);ok=False;continue
    if not re.match(r'^[a-z]+$',c[0]): print('gloss',c);ok=False
    if c[1] not in 'TQAER' or len(c[1])!=1: print('type',c);ok=False
    if c[2] not in('0','1') or (c[1] in 'TQR' and c[2]!='0'): print('tr',c);ok=False
    if (c[1]=='R')!=(c[5]!=''): print('rel',c);ok=False
    if len(c[7].split())>12: print('def long',c);ok=False
    gl.append(c[0])
import collections
for g,n in collections.Counter(gl).items():
    if n>1: print('dup',g);ok=False
S={'opp','doer','made','tool','place','ness','group','able','+agent'}
nd=0
for l in open(D+'der_A.tsv'):
    c=l.rstrip('\n').split('\t');nd+=1
    if len(c)!=4 or c[0] not in gl or c[1] not in S or not re.match(r'^[a-z]+( [a-z]+)?$',c[2]): print('der',c);ok=False
print(len(gl),nd,ok, collections.Counter(r[6] for r in rows), collections.Counter(r[1] for r in rows))
