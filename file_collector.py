import os
import re
# список для топологической сортировки
blacked=[]
# словарь для хеш таблицы
hash_table={}
# словарь для зависимостей
dependence_dir={}
# словарь для действий
action_dir={}

test={"pottery": [], "irrigation": ["pottery"], "writing": ["pottery"], "animal_husbandry": [], "archery": ["animal_husbandry"], "mining": [], "masonry": ["mining"], "bronze_working": ["mining"], "the_wheel": ["mining"], "apprenticeship": ["mining", "currency", "horseback_riding"], "sailing": [], "celestial_navigation": ["sailing", "astrology"], "shipbuilding": ["sailing"], "astrology": [], "drama_poetry": ["astrology", "irrigation", "masonry", "early_empire", "mysticism"], "theology": ["astrology", "mysticism", "drama_poetry"], "horseback_riding": ["archery"], "machinery": ["archery", "iron_working", "engineering"], "currency": ["writing", "foreign_trade"], "state_workforce": ["writing", "bronze_working", "craftsmanship"], "recorded_history": ["writing", "political_philosophy", "drama_poetry"], "construction": ["masonry", "the_wheel", "horseback_riding"], "engineering": ["masonry", "the_wheel"], "iron_working": ["bronze_working"], "mathematics": ["bronze_working", "celestial_navigation", "currency", "drama_poetry"], "military_training": ["bronze_working", "military_tradition", "games_recreation"], "cartography": ["celestial_navigation", "shipbuilding"], "medieval_faires": ["currency", "feudalism"], "guilds": ["currency", "feudalism", "civil_service"], "mercantilism": ["currency", "humanism"], "stirrups": ["horseback_riding", "feudalism"], "mass_production": ["shipbuilding", "machinery", "education"], "naval_tradition": ["shipbuilding", "defensive_tactics"], "military_tactics": ["mathematics"], "education": ["mathematics", "apprenticeship"], "military_engineering": ["construction", "engineering"], "castles": ["construction", "divine_right", "exploration"], "games_recreation": ["construction", "state_workforce"], "gunpowder": ["apprenticeship", "stirrups", "military_engineering"], "printing": ["machinery", "education"], "metal_casting": ["machinery", "gunpowder"], "banking": ["education", "stirrups", "guilds"], "astronomy": ["education"], "military_science": ["stirrups", "printing", "siege_tactics"], "siege_tactics": ["castles", "metal_casting"], "square_rigging": ["cartography", "gunpowder"], "exploration": ["cartography", "mercenaries", "medieval_faires"], "industrialization": ["mass_production", "square_rigging"], "scientific_theory": ["banking", "astronomy", "the_enlightenment"], "colonialism": ["astronomy", "mercantilism"], "ballistics": ["metal_casting", "siege_tactics"], "economics": ["metal_casting", "scientific_theory"], "scorched_earth": ["metal_casting", "nationalism"], "steam_power": ["industrialization"], "flight": ["industrialization", "scientific_theory", "economics"], "steel": ["industrialization", "rifling"], "class_struggle": ["industrialization", "ideology"], "sanitation": ["scientific_theory", "urbanization"], "rifling": ["ballistics", "military_science"], "totalitarianism": ["military_science", "ideology"], "electricity": ["steam_power", "mercantilism"], "radio": ["steam_power", "flight", "conservation"], "chemistry": ["sanitation"], "suffrage": ["sanitation", "ideology"], "replaceable_parts": ["economics"], "capitalism": ["economics", "mass_media"], "combined_arms": ["flight", "combustion"], "synthetic_materials": ["flight", "plastics"], "rapid_deployment": ["flight", "cold_war"], "advanced_ballistics": ["replaceable_parts", "steel", "electricity"], "combustion": ["steel", "natural_history"], "computers": ["electricity", "radio", "suffrage", "totalitarianism", "class_struggle"], "advanced_flight": ["radio"], "rocketry": ["radio", "chemistry"], "nanotechnology": ["radio", "composites"], "mass_media": ["radio", "urbanization"], "nuclear_program": ["chemistry", "ideology"], "plastics": ["combustion"], "satellites": ["advanced_flight", "rocketry"], "globalization": ["advanced_flight", "rapid_deployment", "space_race"], "guidance_systems": ["rocketry", "advanced_ballistics"], "space_race": ["rocketry", "cold_war"], "nuclear_fission": ["advanced_ballistics", "combined_arms"], "telecommunications": ["computers"], "robotics": ["computers", "globalization"], "lasers": ["nuclear_fission"], "cold_war": ["nuclear_fission", "ideology"], "composites": ["synthetic_materials"], "stealth_technology": ["synthetic_materials"], "social_media": ["telecommunications", "professional_sports", "space_race"], "nuclear_fusion": ["lasers"], "code_of_laws": [], "craftsmanship": ["code_of_laws"], "foreign_trade": ["code_of_laws"], "military_tradition": ["craftsmanship"], "early_empire": ["foreign_trade"], "mysticism": ["foreign_trade"], "political_philosophy": ["state_workforce", "early_empire"], "defensive_tactics": ["games_recreation", "political_philosophy"], "humanism": ["drama_poetry", "medieval_faires"], "mercenaries": ["military_training", "feudalism"], "feudalism": ["defensive_tactics"], "civil_service": ["defensive_tactics", "recorded_history"], "divine_right": ["theology", "civil_service"], "diplomatic_service": ["guilds"], "reformed_church": ["guilds", "divine_right"], "the_enlightenment": ["humanism", "diplomatic_service"], "civil_engineering": ["mercantilism"], "nationalism": ["the_enlightenment"], "opera_ballet": ["the_enlightenment"], "natural_history": ["colonialism"], "urbanization": ["civil_engineering", "nationalism"], "conservation": ["natural_history", "urbanization"], "mobilization": ["urbanization"], "cultural_heritage": ["conservation"], "ideology": ["mass_media", "mobilization"], "professional_sports": ["ideology"]}

# функция для парсинга содержимого файла myMakefile
def parse_func():
    f = open('myMakefile', 'r')
    for line in f:
        if line.find(':')!= -1:
            cur_main=(line[0:line.find(':')])
            cur_dependences=[]
            cur_actions=[]
            for dependence in line[line.find(':'):-1].split(" "):
                cur_dependences.append(dependence)
            cur_dependences.pop(0)
            dependence_dir[cur_main]=cur_dependences
        if line.find('@')!=-1:
            cur_actions.append(line[line.find('@'):])
        else:
            action_dir[cur_main]=cur_actions

# функция создания последовательностей(топологическая сортировка)
def dfs_rec(graph,start,path):
    if start not in graph:
        print("Wrong Key")
        return "Wrong Key"
    for edge in graph[start]:
        if edge not in blacked and edge not in path:
            path = dfs_rec(graph, edge,path)
    path = path + [start]
    blacked.append(start)
    return path
    

# функция реализации действий
def action_maker(action_path):
    for element in action_path:
        if not hash_table_check(element):
            print(element," is up-to-date")
        else:
            for action in action_dir[element]:
                if action.find('@echo')!=-1:
                    print(action[6:-1].replace('"',""))
                if action.find('@dir>')!=-1:
                    f = open(os.getcwd()+'\\myProject\\'+element, 'tw', encoding='utf-8')
                    f.close()

# реализуем  хеш таблицу через словарь для контроля версий, ключи к которому будут генерироваться с помощью hash()
def hash_table_check(element):
    if hash(element) in hash_table.keys():
        return False
    else:
        hash_table[hash(element)]=element
        return True

def hash_table_update():
    hash_table.clear()
    for file in os.listdir(os.getcwd()+'\\myProject'):
        hash_table[hash(file)]=file
        

if __name__ == "__main__":
    parse_func() 
    while True:
        blacked.clear()
        cur_command = input("enter command: ")
        if cur_command == "exit":
            break
        if cur_command =="make":
            if "myProject" not in os.listdir():
                os.mkdir("myProject")
            hash_table_update()
            for element in dependence_dir:
                action_path=dfs_rec(dependence_dir,element,[])
                if action_path != "Wrong Key":
                    action_maker(action_path) 
        if re.match(r'make+[ _a-zA-Z0-9]*', cur_command)!=None:
            if "myProject" not in os.listdir():
                os.mkdir("myProject")
            hash_table_update()
            action_path=dfs_rec(dependence_dir,cur_command[5:],[])
            if action_path != "Wrong Key":
                action_maker(action_path) 