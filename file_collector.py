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

# функция создания последовательностей
def dfs_rec(graph,start,path):
    path = path + [start]
    for edge in graph[start]: 
        if edge not in path:
            path = dfs_rec(graph, edge,path)
    print (start)
    return path
    

# функция реализации действий
def action_maker(element):
    for action in action_dir[element]:
        if action.find('@echo')!=-1:
            print(action[6:-1].replace('"',""))
        


parse_func()            
print(dependence_dir)
print(action_dir)
print(dfs_rec(dependence_dir,'dress',[]))
