from collections import deque

f = open("recipes.txt", "r", encoding='utf-8')
cook_book = {}
lines = deque(f.readlines())
curr_recipe = ''
while lines:
    line = lines.popleft().strip().split('|')
    if len(line) != 1:
        line[1] = int(line[1])
        line = dict(zip(['ingredient_name', 'quantity', 'measure'], line))
        if curr_recipe in cook_book:
            cook_book[curr_recipe].append(line)
        else:
            cook_book[curr_recipe] = [line]
    else:
        if not line[0].isdigit() and line[0]:
            curr_recipe = line[0]
f.close()


def get_shop_list_by_dishes(dishes, person_count):
    shop_list = {}
    for d in dishes:
        if d not in cook_book:
            continue
        dish = cook_book[d]
        for ing in dish:
            if ing['ingredient_name'] in shop_list:
                shop_list[ing['ingredient_name']]['quantity'] += ing['quantity'] * person_count
            else:
                shop_list[ing['ingredient_name']] = {'measure': ing['measure'],
                                                     'quantity': ing['quantity'] * person_count}
    return dict(sorted(shop_list.items(), key=lambda x: x[0]))


def merge_files(input_files, output_file):
    file_lines = []
    for path in input_files:
        curr_file = [path]
        with open(path, 'r+', encoding='utf-8') as f:
            lines = f.readlines()
            curr_file.append(len(lines))
            lines = '\n'.join([l.strip() for l in lines])
            curr_file.append(lines)
            file_lines.append(curr_file)
    file_lines = sorted(file_lines, key=lambda x: x[1])
    with open(output_file, 'w+', encoding='utf-8') as f:
        for file in file_lines:
            for l in file:
                print(l, file=f, end='\n')


if __name__ == "__main__":
    print(get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2))

    merge_files(['1.txt', '2.txt', '3.txt'], 'out.txt')
