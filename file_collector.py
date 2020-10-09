# список для топологической сортировки
blacked=[]
# словарь для зависимостей
dependence_dir={}
# словарь для действий
action_dir={}
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
        for action in action_dir[element]:
            if action.find('@echo')!=-1:
                print(action[6:-1].replace('"',""))
            if action.find('@dir>')!=-1:
                f = open(element, 'tw', encoding='utf-8')
                f.close()
        

if __name__ == "__main__":
    parse_func() 
    # print(dependence_dir)
    # print(action_dir)
    while True:
        cur_command = input("enter command ")
        if cur_command == "exit":
            break
        blacked.clear()
        if cur_command =="make":
            pass
        else:
        # print(dfs_rec(dependence_dir,'dress',[]))
            action_path=dfs_rec(dependence_dir,cur_command,[])
            if action_path != "Wrong Key":
                action_maker(action_path)
