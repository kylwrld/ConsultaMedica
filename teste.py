# lista = [1, '2', 3, 4, 5]

# dictn = {"a":1, "b":2, "c":3}

# d = {"a": {
#         'teste':2,
#         'teste2':4,
#     }
# }

# d2 = {"b": 2, "c":3}

# def teste(b, c):
#     print(b, c)

# teste(**d2)

# d = dictn.pop("a", "b")
# d = dictn.popitem()

# # t = lista.pop('2')

# print(d)
# print(d)

# a = {1: 2}

# if "1"




def find(nums, target):
    hashmap = {}

    for i in range(len(nums)):
        if target-nums[i] in hashmap:
            return [hashmap[target-nums[i]], i]
        
        hashmap[nums[i]] = i

nums = [1, 9, 8, 2, 4] 
target = 11

print(find(nums, target))

